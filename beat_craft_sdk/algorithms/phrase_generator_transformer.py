import random
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json

def get_data_source():
    # Get Dataset
    filtered_df = pd.read_csv('assets/cleaned.csv')

    # Get Json Key Maps Ritme
    with open('assets/key_maps.json', 'r') as json_file:
        key_maps = json.load(json_file)
        
    train_data = pd.DataFrame()
    validation_data = pd.DataFrame()

    for value in filtered_df['kunci'].unique():
        subset = filtered_df[filtered_df['kunci'] == value]
        validation_size = max(1, int(len(subset) * 0.1))  # Minimal 1 untuk validasi
        validation_subset = subset.sample(validation_size, random_state=42)
        training_subset = subset.drop(validation_subset.index)
        
        train_data = pd.concat([train_data, training_subset])
        validation_data = pd.concat([validation_data, validation_subset])
    
    validation_data.to_csv('assets/val_data.csv')
    return train_data, key_maps

# Fungsi untuk memproses kolom 'bar'
def process_abc(abc_notation, tokenizer):
    tokens = tokenize_abc(abc_notation)
    processed = [tokenizer.get(token, tokenizer['[UNK]']) for token in tokens]
    original_length = len(processed)
    return processed, original_length

# Fungsi untuk membuat tokenizer berdasarkan kolom 'bar'
def create_tokenizer(df):
    tokenizer = {'[PAD]': 0, '[UNK]': 1}  # Menambahkan token PAD dan UNK
    token_id = 2
    for notation in df['bar']:
        if pd.notnull(notation):
            tokens = tokenize_abc(notation)
            for token in tokens:
                if token not in tokenizer:
                    tokenizer[token] = token_id
                    token_id += 1
    return tokenizer

# Fungsi untuk mengubah notasi ABC menjadi token
def tokenize_abc(abc_notation):
    return list(abc_notation)

# Fungsi untuk mencetak hasil mapping dari LabelEncoder
def print_encoding_mapping(encoder, col_name):
    print(f"Mapping for '{col_name}':")
    for index, label in enumerate(encoder.classes_):
        print(f"{label}: {index}")

# Fungsi untuk menambahkan konteks ke teks input
def add_context(row):
    context = f"Pitch pattern: {row['pitch_pattern']}, Ritme: {row['ritme']}, Kunci: {row['kunci']}."
    return f"{context} Sequence: {row['bar_encoded_str']}"

def preprocess_data():
    # Label encoder untuk kolom lainnya
    encoder = LabelEncoder()
    pickedCol = ['bar', 'pitch_pattern', 'birama', 'panjang_note', 'ritme', 'kunci']
    
    df, key_maps = get_data_source()
    tokenizer = create_tokenizer(df)
    encodedDf = pd.DataFrame({})
    
    # Make a reversed tokenizer
    reverse_tokenizer = {v: k for k, v in tokenizer.items()}
    
    # Processing column bar into encoded bar
    encodedDf['bar_encoded'] = df['bar'].apply(lambda x: process_abc(x, tokenizer)[0] if pd.notnull(x) else [0])
    encodedDf['bar_length'] = df['bar'].apply(lambda x: process_abc(x, tokenizer)[1] if pd.notnull(x) else 0)

    for col in pickedCol:
        if col != 'bar':
            encodedDf[col] = encoder.fit_transform(df[col])
            # Menyimpan key map untuk kolom ini
            key_maps[col] = {index: label for index, label in enumerate(encoder.classes_)}

    # Simpan DataFrame yang sudah diproses
    df = encodedDf.copy()
    # Konversi list of integers menjadi string agar kompatibel dengan GPT-2
    df['bar_encoded_str'] = df['bar_encoded'].apply(lambda x: ' '.join(map(str, x)))
    df['input_text'] = df.apply(add_context, axis=1)
    
    return df, tokenizer, reverse_tokenizer, key_maps

# Fungsi untuk mengonversi durasi dalam notasi ABC ke ketukan
def convert_duration(duration_str):
    # Contoh sederhana: tanpa angka = ketukan penuh (1), angka = pecahan
    if duration_str == "":
        return 1  # durasi default adalah 1 ketukan
    elif duration_str.isdigit():
        return 1 / int(duration_str)  # misalnya '2' menjadi 0.5 ketukan
    else:
        return 1  # fallback

# Fungsi utama untuk parsing notasi ABC
def abc_to_midi_notes(abc_notation):
    abc_to_midi = {
        'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71,
        'c': 72, 'd': 74, 'e': 76, 'f': 77, 'g': 79, 'a': 81, 'b': 83,
        'z': 0
    }
    
    output = []
    i = 0
    while i < len(abc_notation):
        note = abc_notation[i]
        
        # Cek jika ada durasi yang mengikuti nada
        duration_str = ""
        i += 1
        while i < len(abc_notation) and abc_notation[i].isdigit():
            duration_str += abc_notation[i]
            i += 1
        
        # Konversi nada dan durasi ke MIDI dan ketukan
        midi_note = abc_to_midi.get(note, 0)  # 0 digunakan untuk 'z' atau istirahat
        duration = convert_duration(duration_str)
        output.append((duration, midi_note))
    
    return output
# Fungsi untuk memfilter data berdasarkan pitch_pattern, birama, dan kunci
def filter_data(df, ritme, key_maps):
    # 1. Filter berdasarkan kolom 'ritme' dengan ketentuan dari for loop matching_rhythm
    matching_rhythm = []
    for item in ritme:
        for key, val in key_maps.items():
            if val == item:
                matching_rhythm.append(key)

    # Casting menjadi int untuk memastikan konsistensi tipe data
    matching_rhythm = list(map(int, matching_rhythm))

    # Ambil subset DataFrame berdasarkan matching_rhythm menggunakan .isin()
    df_filtered = df[df['ritme'].isin(matching_rhythm)]

    if df_filtered.empty:
        print("Tidak ditemukan data dengan ritme yang cocok.")
        return df_filtered, [None, None, None]

    # 2. Ambil pitch pattern dan kunci unique dari hasil filter
    pitchPatternUnq = df_filtered['pitch_pattern'].unique()
    kunciUnq = df_filtered['kunci'].unique()

    # 3. Lakukan randomisasi pitch_pattern dan kunci
    pitch_pattern = random.choice(pitchPatternUnq)
    kunci = random.choice(kunciUnq)

    # Gunakan seluruh matching_rhythm untuk variasi lebih luas
    rhythm_variation = df_filtered['ritme'].unique().tolist()

    # Simpan atribut musik ke dalam list
    musicAtr = [pitch_pattern, kunci, rhythm_variation]

    # 4. Return hasil filter dan atribut musik
    return df_filtered[
        (df_filtered['pitch_pattern'] == pitch_pattern) &
        (df_filtered['kunci'] == kunci)
    ], musicAtr
    # return df[df['ritme'].isin(matching_rhythm)], musicAtr

# Fungsi untuk menggabungkan bar dari data yang difilter
def combine_bars(filtered_df):
    all_bars = filtered_df['bar_encoded'].tolist()
    random.shuffle(all_bars)
    
    combined_bar = []
    for bar in all_bars:
        combined_bar.extend(bar)
    
    return combined_bar

# Fungsi untuk menambahkan padding jika diperlukan
def pad_sequence(sequence, max_length, tokenizer):
    pad_value = tokenizer.pad_token_id
    
    if len(sequence) < max_length:
        sequence.extend([pad_value] * (max_length - len(sequence)))
    return sequence


# Fungsi untuk membersihkan hasil yang dihasilkan
def clean_generated_sequence(sequence):
    # Filter out non-numeric tokens or invalid sequences
    filtered_sequence = [token for token in sequence.split() if token.isdigit() and 0 <= int(token) <= 100]
    return ' '.join(filtered_sequence)

# Fungsi untuk mengembalikan angka-angka menjadi notasi ABC
def decode_to_abc(sequence, reverse_tokenizer):
    tokens = sequence.split()  # Memisahkan urutan angka ke dalam daftar
    abc_notation = []
    
    for token in tokens:
        decoded_token = reverse_tokenizer[int(token)]
        if abc_notation and (decoded_token.isdigit() or decoded_token in ['/', '^', '=', '-', '<', '>']):
            # Jika token adalah angka atau simbol yang berkaitan dengan not sebelumnya, gabungkan tanpa spasi
            abc_notation[-1] += decoded_token
        else:
            # Jika token adalah not atau karakter baru, tambahkan sebagai elemen baru
            abc_notation.append(decoded_token)
    return ''.join(abc_notation)  # Gabungkan semua tanpa spasi tambahan

def generate_phrase_with_transformer_algorithm(model, tokenizer, logits_processor, pitch_pattern, ritme, kunci, filtered_df, max_length=1024, deviceType=None):
    # Gunakan ritme_list untuk menghasilkan konteks
    ritme_str = ', '.join(map(str, ritme))
    context = f"Pitch pattern: {pitch_pattern}, Ritme: {ritme_str}, Kunci: {kunci}. Sequence: "
    print(context)
    combined_bar = combine_bars(filtered_df)
    min_sequence_length = 10

    if len(combined_bar) < min_sequence_length:
        raise ValueError(f"Sequence terlalu pendek setelah filterisasi, panjang minimal adalah {min_sequence_length} tokens.")

    combined_bar_str = ' '.join(map(str, combined_bar))
    combined_bar_tokens = combined_bar_str.split()

    if len(combined_bar_tokens) > max_length:
        combined_bar_tokens = combined_bar_tokens[:max_length]

    input_text = context + ' '.join(combined_bar_tokens)
    inputs = tokenizer(input_text, return_tensors='pt', padding=True, truncation=True, max_length=1024)
    inputs = {key: value.to(deviceType) for key, value in inputs.items()}

    print(f"Input IDs size: {inputs['input_ids'].size(1)}")

    remaining_tokens = 1024 - inputs['input_ids'].size(1)
    max_new_tokens = min(remaining_tokens, 50)

    if max_new_tokens > 0:
        outputs = model.generate(
            inputs['input_ids'], 
            max_new_tokens=max_new_tokens,
            num_return_sequences=1,
            pad_token_id=tokenizer.pad_token_id,
            bad_words_ids=[[tokenizer.pad_token_id]],
            repetition_penalty=1.5,
            no_repeat_ngram_size=2,
            do_sample=True,
            logits_processor=[logits_processor] if logits_processor else None,
            top_k=30,
            temperature=0.6
        )

        generated_sequence = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return generated_sequence
    else:
        print("Sequence input terlalu panjang, tidak ada token baru yang dihasilkan.")
        return combined_bar_str