import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import os

output_dir = ".output"
model = MusicGen.get_pretrained('melody')
model.set_generation_params(duration=8)  # generate 8 seconds.

descriptions = ['happy rock', 'energetic EDM', 'sad jazz']

melody, sr = torchaudio.load('./.output/output.wav')
# generates using the melody from the given audio and the provided descriptions.
wav = model.generate_with_chroma(descriptions, melody[None].expand(3, -1, -1), sr)


# Create the directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

for idx, one_wav in enumerate(wav):
    output_filename = f'{idx}'
    # Full path where the audio will be saved
    output_path = os.path.join(output_dir, output_filename)
    # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
    audio_write(stem_name=output_path, wav=one_wav.cpu(), sample_rate=model.sample_rate, strategy="loudness")
