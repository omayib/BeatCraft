import matplotlib.pyplot as plt
import os
from beat_craft_sdk.utils.beat_craft_utils import get_current_time
import numpy as np
import librosa
import json

def fitness_smoothness(sequence):
    total_jump = sum(abs(sequence[i] - sequence[i + 1]) for i in range(len(sequence) - 1))
    return 1 / (1 + total_jump)

consonant_intervals = {0, 7, 12}
def fitness_consonance(sequence):
    consonant_pairs = sum(1 for i in range(len(sequence) - 1) if abs(sequence[i] - sequence[i + 1]) in consonant_intervals)
    return consonant_pairs / (len(sequence) - 1)

def fitness_rhythmic_variety(sequence):
    variety = len(set(sequence)) / len(sequence)
    return variety

def combined_fitness(sequence):
    smoothness_score = fitness_smoothness(sequence)
    consonance_score = fitness_consonance(sequence)
    variety_score = fitness_rhythmic_variety(sequence)
    return 0.4 * smoothness_score + 0.4 * consonance_score + 0.2 * variety_score

# Hamming distance to measure genotypic diversity
def hamming_distance(seq1, seq2):
    return sum(el1 != el2 for el1, el2 in zip(seq1, seq2))

def population_diversity(population):
    total_distance = 0
    count = 0
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            total_distance += hamming_distance(population[i], population[j])
            count += 1
    if count == 0:
        return 0
    return total_distance / count  # Return average Hamming distance

# Fitness diversity (standard deviation of fitness scores)
def fitness_diversity(fitness_scores):
    return np.std(fitness_scores)

# Count the number of unique individuals in the population
def unique_individuals(population):
    unique_sequences = set(tuple(seq) for seq in population)
    return len(unique_sequences) / len(population)  # Fraction of unique sequences

def plot_fitness_over_generations(num_generation,fitness_per_generations,output_dir,file_name):
    filename = f"fitness_score_evaluation_{get_current_time()}_{file_name}.png"
    output_path = os.path.join(output_dir, filename)
    plt.figure()
    plt.plot(range(1,num_generation+1),fitness_per_generations,marker='o')
    plt.title('Scale-Fitness Score Evaluation Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Best Fitness Score')
    plt.grid(True)
    plt.savefig(output_path)

def plot_pitch_diversity_over_generation(num_generation,diversity_per_generation,output_dir,file_name):
    filename = f"pitch_diversity_evaluation_{get_current_time()}_{file_name}.png"
    output_path = os.path.join(output_dir, filename)
    plt.figure()
    plt.plot(range(1, num_generation + 1), diversity_per_generation, marker='o', color='orange')
    plt.title('Pitch Diversity Evolution Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Pitch Population Diversity (Hamming Distance)')
    plt.grid(True)
    plt.savefig(output_path)

def plot_waveform(audio_data,sample_rate, output_dir,file_name):
    validate_audio_data(audio_data)
    filename = f"waveform_generated_music_{get_current_time()}_{file_name}.png"
    output_path = os.path.join(output_dir, filename)
    # Create time axis
    time = np.linspace(0, len(audio_data) / sample_rate, num=len(audio_data))
    # Plot the waveform
    plt.figure(figsize=(10, 4))
    plt.plot(time, audio_data)
    plt.title("Waveform of Generated Music")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.savefig(output_path)

    plot_audio_analyze_into_json('Time',
                                 time,
                                 'Amplitude',
                                 audio_data,
                                 output_dir,
                                 file_name)

def plot_spectrogram(audio_data,sample_rate, output_dir,file_name):
    validate_audio_data(audio_data)
    filename = f"spectrogram_generated_music_{get_current_time()}_{file_name}.png"
    output_path = os.path.join(output_dir, filename)
    plt.figure(figsize=(10, 6))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data)), ref=np.max)
    librosa.display.specshow(D, sr=sample_rate, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram of Generated Music')
    plt.savefig(output_path)

    # Extract X data (time) from the frames
    time = librosa.frames_to_time(np.arange(D.shape[1]), sr=sample_rate)

    # Extract Y data (frequency in Hz)
    frequencies = librosa.fft_frequencies(sr=sample_rate)

    plot_audio_analyze_into_json('Time',
                                 time,
                                 'Spectrogram (log)',
                                 frequencies,
                                 output_dir,
                                 filename)

def plot_mel_spectrogram(audio_data,sample_rate, output_dir,file_name):
    validate_audio_data(audio_data)
    filename = f"mel_spectrogram_generated_music_{get_current_time()}_{file_name}.png"
    output_path = os.path.join(output_dir, filename)
    mel_spect = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate, n_mels=128)
    mel_spect_db = librosa.power_to_db(mel_spect, ref=np.max)
    # Check the shape of mel_spectrogram_db to ensure it's in the correct format
    print("Mel Spectrogram shape1:", mel_spect_db.shape)  # Should be (128, n_time_frames)
    mel_spect_db = np.squeeze(mel_spect_db)
    print("Mel Spectrogram shape2:", mel_spect_db.shape)

    # Compute the Short-Time Fourier Transform (STFT)
    stft_result = librosa.stft(audio_data)
    D = librosa.amplitude_to_db(np.abs(stft_result), ref=np.max)

    # Extract X data (time) from the frames
    time = librosa.frames_to_time(np.arange(D.shape[1]), sr=sample_rate)

    # Extract Y data (frequency in Hz)
    frequencies = librosa.fft_frequencies(sr=sample_rate)  # For linear frequency scale

    # Plot the mel spectrogram
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(D, sr=sample_rate, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram of Generated Music')
    plt.savefig(output_path)
    plot_audio_analyze_into_json('Time',
                                 time,
                                 'Mel',
                                 frequencies,
                                 output_dir,
                                 filename)

def plot_pitch_contour(audio_data,sample_rate, output_dir,file_name):
    validate_audio_data(audio_data)
    filename = f"pitch_contour_generated_music_{get_current_time()}_{file_name}.png"
    output_path = os.path.join(output_dir, filename)
    # Pitch and harmonic analysis
    harmonic, _ = librosa.effects.hpss(audio_data)
    pitch = librosa.yin(harmonic, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

    time = librosa.frames_to_time(np.arange(len(pitch)), sr=sample_rate)
    # Plot pitch contour
    plt.figure(figsize=(10, 4))
    plt.plot(pitch, label='Pitch Contour')
    plt.title('Pitch Contour of Generated Music')
    plt.xlabel('Time (frames)')
    plt.ylabel('Pitch (Hz)')
    plt.legend()
    plt.savefig(output_path)
    plot_audio_analyze_into_json('Time (frames)',
                                 time,
                                 'Pitch (Hz)',
                                 pitch,
                                 output_dir,
                                 filename)
def validate_audio_data(audio_data):
    if len(audio_data) == 0 or np.all(audio_data == 0):
        print("Error: Audio data is empty or consists of only zeros.")
    else:
        print("Audio data is valid.")

def load_audio_file(file_path):
    # Load the audio file with librosa
    try:
        audio_data, sample_rate = librosa.load(file_path, sr=None)  # sr=None to preserve the original sample rate
        print(f"Loaded audio file: {file_path}")
        print(f"Sample rate: {sample_rate}")
        print(f"Audio data shape: {audio_data.shape}")
        return audio_data, sample_rate
    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None, None

def plot_ga_evaluation_into_json(diversity_per_generation, best_fitness_per_generation,output_dir,file_name):
    filename = f"ga_evaluation_{get_current_time()}_{file_name}.json"
    output_path = os.path.join(output_dir, filename)
    data = {
        "diversity_per_generation": diversity_per_generation,
        "best_fitness_per_generation": best_fitness_per_generation
    }
    # Save to a JSON file
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def plot_audio_analyze_into_json(x_label,x_data,y_label,y_data,output_dir,file_name):
    filename = f"audio_analyze_{get_current_time()}_{file_name}.json"
    output_path = os.path.join(output_dir, filename)
    data = {
        f"{x_label}": json.dumps(x_data.tolist()),
        f"{y_label}": json.dumps(y_data.tolist())
    }
    # Save to a JSON file
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)