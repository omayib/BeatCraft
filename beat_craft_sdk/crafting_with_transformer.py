from beat_craft_sdk.algorithms.phrase_generator_transformer import (
    generate_phrase_with_transformer_algorithm, 
    preprocess_data, 
    filter_data,
    clean_generated_sequence,
    decode_to_abc,
    abc_to_midi_notes
    )
from beat_craft_sdk.craft_strategy import CraftStrategy
from transformers import (
    GPT2Tokenizer, 
    GPT2LMHeadModel, 
    LogitsProcessor,
    AdamW,
    get_linear_schedule_with_warmup
    )

from beat_craft_sdk.evaluation.transformer_evaluation import (
    evaluate_with_EMD,
    evaluate_midi_output,
    calculate_statistics,
    identify_outliers,
    plot_histogram,
    plot_boxplot,
    plot_scatter
    )

from torch.utils.data import DataLoader
from torch.cuda.amp import autocast, GradScaler
import torch
import os
import pandas as pd
from tqdm import tqdm

# Create a simple custom dataset without padding
class MusicDataset(torch.utils.data.Dataset):
    def __init__(self, input_ids, attention_masks):
        self.input_ids = input_ids
        self.attention_masks = attention_masks

    def __len__(self):
        return len(self.input_ids)

    def __getitem__(self, idx):
        return self.input_ids[idx], self.attention_masks[idx], self.input_ids[idx]
    
class CustomLogitsProcessor(LogitsProcessor):
    def __init__(self, valid_tokens=None):
        self.valid_tokens = valid_tokens

    def __call__(self, input_ids, scores):
        mask = torch.ones(scores.shape[-1], dtype=torch.bool, device=scores.device)
        mask[self.valid_tokens] = False
        scores[..., mask] = -float("inf")
        return scores
    
class CraftingTransformer(CraftStrategy):
    def __init__(self, ritme=None):
        self.model = None
        self.tokenizer = None
        self.logits_processor = CustomLogitsProcessor()
        self.device = self.get_device()  # Set device secara otomatis
        self.scaler = GradScaler()
        self.ritme = ritme
        self.default_directories = {
            'TRANSFORMER_DIRS': os.path.join('beat_craft_sdk', 'algorithms', 'transformers_config'),
            'MODEL_DIR': os.path.join('beat_craft_sdk', 'algorithms', 'transformers_config', 'fine_tuned_gpt2'),
        }
        self.pitch_fitness_per_generations = []
        self.pitch_diversity_per_generation = []
    
    def set_transformers_directories(self):
        LIST_DIR = self.default_directories
        # Check if model dirs is existed
        if not os.path.exists(LIST_DIR['TRANSFORMER_DIRS']):
            os.makedirs(LIST_DIR['TRANSFORMER_DIRS'], exist_ok=True)
            os.makedirs(LIST_DIR['MODEL_DIR'], exist_ok=True)
        else:
            print('Main Directories with All Sub Directories is Existed')
        
    def set_default_tokenizer(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        return self.tokenizer

    def set_default_model(self):
        self.model = GPT2LMHeadModel.from_pretrained('gpt2').to(self.device)  # Pindahkan model ke device
        return self.model
        
    def set_model_configuration(self):
        tokenizer_gpt2 = self.set_default_tokenizer()
        tokenizer_gpt2.add_special_tokens({'pad_token': '[PAD]', 'unk_token': '[UNK]'})
        model = self.set_default_model()
        model.resize_token_embeddings(len(tokenizer_gpt2))
        self.set_transformers_directories()
        
        return tokenizer_gpt2, model
    
    def get_device(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        return device
        
    def retrain_model(self, df):
        # Tokenize the input sequences individually (tanpa padding)
        tokenizer_gpt2, model_gpt2 = self.set_model_configuration()
        
        input_ids = [tokenizer_gpt2(text, return_tensors='pt')['input_ids'].squeeze(0) for text in df['input_text'].tolist()]
        attention_masks = [torch.ones_like(ids) for ids in input_ids]  # Semua tokens dianggap penting, jadi masking 1
        dataset = MusicDataset(input_ids, attention_masks)
        dataloader = DataLoader(dataset, batch_size=1, shuffle=True)  # batch_size=1 untuk menghindari padding
        print(f"Total batches in dataloader: {len(dataloader)}")
        
        checkpoint_dir = './gpt2_checkpoints'
        os.makedirs(checkpoint_dir, exist_ok=True)
        # Training configuration
        optimizer = AdamW(model_gpt2.parameters(), lr=5e-5)
        epochs = 1
        total_steps = len(dataloader) * epochs
        scheduler = get_linear_schedule_with_warmup(optimizer, num_warmup_steps=0, num_training_steps=total_steps)
        
        device = self.get_device()
        model_gpt2.to(device)
        
        model_gpt2.train()
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            epoch_iterator = tqdm(dataloader, desc=f"Epoch {epoch+1}/{epochs}", leave=False, dynamic_ncols=True)

            for step, batch in enumerate(dataloader):
                input_ids_batch, attention_mask_batch, labels_batch = [x.to(device) for x in batch]
                
                optimizer.zero_grad()

                with autocast():
                    outputs = model_gpt2(input_ids=input_ids_batch, attention_mask=attention_mask_batch, labels=labels_batch)
                    loss = outputs.loss

                self.scaler.scale(loss).backward()
                self.scaler.step(optimizer)
                self.scaler.update()
                scheduler.step()

                epoch_loss += loss.item()

                # Update tqdm manually
                epoch_iterator.update(1)
                epoch_iterator.set_postfix(loss=loss.item())

            print(f'Epoch {epoch+1}/{epochs}, Loss: {epoch_loss/len(dataloader):.4f}')

            torch.save({
                'epoch': epoch,
                'model_state_dict': model_gpt2.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'scheduler_state_dict': scheduler.state_dict(),
            }, os.path.join(checkpoint_dir, f'checkpoint_epoch_{epoch+1}.pth'))
        
        # Save the fine-tuned model
        model_gpt2.save_pretrained(self.default_directories['MODEL_DIR'])
        tokenizer_gpt2.save_pretrained(self.default_directories['MODEL_DIR'])
        
    def generate(self, output_dir, file_name, ritme):
        df, tokenizer, reverse_tokenizer, key_maps = preprocess_data()
        try:
            # Memuat model dan tokenizer, jika tidak ada, unduh dari awal
            model_gpt2 = GPT2LMHeadModel.from_pretrained(self.default_directories['MODEL_DIR']).to(self.device)
            tokenizer_gpt2 = GPT2Tokenizer.from_pretrained(self.default_directories['MODEL_DIR'])
        except OSError as e:
            print(f"Model not found: {e}. Retraining model...")
            self.retrain_model(df=df)  # Ambil data dan retrain
            model_gpt2 = GPT2LMHeadModel.from_pretrained(self.default_directories['MODEL_DIR']).to(self.device)
            tokenizer_gpt2 = GPT2Tokenizer.from_pretrained(self.default_directories['MODEL_DIR'])

        # Validasi filter data
        filtered_df, musicAtr = filter_data(preprocess_data()[0], ritme, key_maps)
        if filtered_df.empty:
            print('Filtered data is empty. Returning empty melody.')
            return 'Melodi kosong, tidak ada data yang dihasilkan.'

        # Membuat Logits Processor
        valid_token_ids = [token_id for token, token_id in tokenizer_gpt2.get_vocab().items() if token.isdigit()]
        logits_processor = CustomLogitsProcessor(valid_token_ids)

        # Menghasilkan musik
        generated_music = generate_phrase_with_transformer_algorithm(
            model=model_gpt2, 
            tokenizer=tokenizer_gpt2, 
            logits_processor=logits_processor,
            pitch_pattern=musicAtr[0],
            kunci=musicAtr[1],
            filtered_df=filtered_df,
            deviceType=self.device,
            ritme=musicAtr[2]
        )

        cleaned_music = clean_generated_sequence(generated_music)

        try:
            decoded_music = decode_to_abc(cleaned_music, reverse_tokenizer)
            midi_notes = abc_to_midi_notes(decoded_music)
        except Exception as e:
            print(f"Decoding Error: {e}")
            decoded_music = None
            
        return midi_notes, decoded_music or 'Melodi kosong, tidak ada data yang dihasilkan.'


    def evaluate(self, generated_sequence, midiNotes, output_dir, file_name, 
                 game_mood=None, game_genre=None, game_emotional=None, 
                 val_dir='assets/val_data.csv'):
        
        if generated_sequence == 'Melodi kosong, tidak ada data yang dihasilkan.':
            print("Sequence kosong, evaluasi tidak dapat dilanjutkan.")
            return
        
        if game_mood != None and game_genre != None and game_emotional != None:
            listGenre = set(game_mood + game_genre + game_emotional)
            if listGenre:
                valDf = pd.read_csv(val_dir)
                valDf = valDf[valDf['ritme'].isin(listGenre)]
                evalRes = evaluate_with_EMD(valDf=valDf, generatedSeq=generated_sequence)
                
                evalRes.to_csv(f'{output_dir}/{file_name}_emd_evaluation.csv', index=False)
                print(f"Hasil evaluasi EMD disimpan di {output_dir}/{file_name}_emd_evaluation.csv")
                
                # plot and conclusion
                stats = calculate_statistics(evalRes)
                
                print(stats)
                # Identify outliers
                outlier = identify_outliers(evalRes)
                print(outlier)
                
                # Plot histogram
                plot_histogram(evalRes)

                # Plot boxplot
                plot_boxplot(evalRes)

                # Plot scatter plot with mean line
                plot_scatter(evalRes, mean_value=stats['mean'])
                
                # metrics = evaluate_classification_metrics(valDf=valDf, 
                #                                           generated_sequence=generated_sequence)
                
                results, summary = evaluate_midi_output(valDf=valDf, generated_midi=midiNotes)
                # Cetak summary
                print("\nSummary of Evaluation Results:")
                for metric, value in summary.items():
                    print(f"{metric}: {value:.4f}")
            else: 
                print('Data genre tidak lengkap.')
        
        return results, summary