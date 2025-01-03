from pyemd import emd
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.metrics import mean_squared_error
from scipy.spatial.distance import euclidean

####### EMD Evaluation #########
# Fungsi untuk merekonstruksi pitch pattern dari data validasi
def reconstruct_pitch_patterns(valDf):
    # Gabungkan pitch_pattern berdasarkan judul lagu dengan mempertimbangkan urutan bar
    return (
        valDf
        .sort_values(by=['judul_lagu', 'bar_number'])  # Pastikan bar diurutkan
        .groupby('judul_lagu')['bar']  # Gunakan kolom 'bar' untuk pitch pattern
        .apply(lambda x: ' '.join(x))  # Gabungkan pitch pattern dari setiap bar
        .reset_index()
    )

def normalize_distribution(distribution):
    total = sum(distribution)
    return [x / total if total > 0 else 0 for x in distribution]

# Fungsi untuk mengonversi urutan pitch menjadi distribusi pitch
def convert_to_pitch_distribution(sequence):
    # Jika sequence adalah list, gabungkan menjadi string
    if isinstance(sequence, list):
        # Konversi setiap elemen menjadi string jika elemen berupa tuple
        sequence = ' '.join(map(str, sequence))
    
    # Ekstrak nada (A-G) menggunakan regex
    pitch_set = 'ABCDEFG'
    pitches = re.findall(f"[{pitch_set}]", sequence)
    
    # Hitung distribusi pitch
    return [pitches.count(p) for p in pitch_set]

# Fungsi untuk menghitung jarak EMD
def calculate_emd(validasi_distribution, generated_distribution):
    # Konversi semua distribusi menjadi np.float64
    validasi_distribution = np.array(validasi_distribution, dtype=np.float64)
    generated_distribution = np.array(generated_distribution, dtype=np.float64)

    # Pastikan kedua distribusi memiliki panjang yang sama
    if len(validasi_distribution) != len(generated_distribution):
        raise ValueError(f"Distribusi tidak sama panjang: validasi={len(validasi_distribution)}, generated={len(generated_distribution)}")

    # Matriks jarak (harus berupa float64)
    distance_matrix = np.abs(np.subtract.outer(range(len(validasi_distribution)), range(len(generated_distribution)))).astype(np.float64)
    
    # Hitung EMD
    return emd(validasi_distribution, generated_distribution, distance_matrix)

# Function to calculate the average pitch distribution
def calculate_average_pitch_distribution(df, column_name):
    """
    Menghitung distribusi pitch rata-rata dari data yang diberikan.
    """
    pitch_counts = {label: 0 for label in 'ABCDEFG'}  # Misal label pitch A-G
    total_entries = len(df)
    
    # Menghitung jumlah pitch untuk setiap label
    for pitch in df[column_name]:
        if pitch in pitch_counts:
            pitch_counts[pitch] += 1
    
    # Menghitung rata-rata distribusi
    average_distribution = {label: count / total_entries for label, count in pitch_counts.items()}
    return list(average_distribution.values())

# Function to plot pitch distributions
def plot_pitch_distribution(validasi_distribution, generated_distribution, title="Pitch Distribution Comparison"):
    labels = 'A', 'B', 'C', 'D', 'E', 'F', 'G'
    x = np.arange(len(labels))  # positions for each label
    width = 0.35  # width of the bars

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, validasi_distribution, width, label='Validasi', color='blue')
    rects2 = ax.bar(x + width/2, generated_distribution, width, label='Generated', color='orange')

    ax.set_ylabel('Average Count')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    plt.tight_layout()
    plt.show()

# Fungsi evaluasi utama dengan EMD
def evaluate_with_EMD(valDf, generatedSeq):
    reconstructed_data = reconstruct_pitch_patterns(valDf=valDf)
    
    # Konversi distribusi pitch hasil generate
    generated_distribution = convert_to_pitch_distribution(generatedSeq)
    if sum(generated_distribution) == 0:
        raise ValueError("Distribusi pitch hasil generate kosong.")
    
    # Menghitung distribusi rata-rata pitch untuk validasi
    all_validasi_distributions = []
    for idx, row in reconstructed_data.iterrows():
        validasi_sequence = row['bar']  # Ambil kolom 'bar' untuk evaluasi pitch
        
        # Konversi distribusi pitch data validasi
        validasi_distribution = convert_to_pitch_distribution(validasi_sequence)
        if sum(validasi_distribution) > 0:
            all_validasi_distributions.append(validasi_distribution)
    
    # Hitung rata-rata distribusi pitch dari validasi
    if all_validasi_distributions:
        validasi_avg_distribution = np.mean(all_validasi_distributions, axis=0)
    else:
        validasi_avg_distribution = np.zeros_like(generated_distribution)  # Jika tidak ada data validasi
    
    # Normalisasi distribusi
    validasi_avg_distribution = normalize_distribution(validasi_avg_distribution)
    generated_distribution = normalize_distribution(generated_distribution)
    
    # Hitung EMD untuk distribusi rata-rata
    emd_distance = calculate_emd(validasi_avg_distribution, generated_distribution)
    
    # Plot distribusi pitch rata-rata
    plot_pitch_distribution(validasi_avg_distribution, generated_distribution, title="Rata-rata Pitch Distribution Comparison")
    
    # Menyusun hasil untuk setiap lagu
    results = []
    invalid_data = []  # Simpan baris dengan distribusi kosong
    for idx, row in reconstructed_data.iterrows():
        judul = row['judul_lagu']
        validasi_sequence = row['bar']  # Ambil kolom 'bar' untuk evaluasi pitch

        # Konversi distribusi pitch data validasi
        validasi_distribution = normalize_distribution(convert_to_pitch_distribution(validasi_sequence))
        generated_distribution = normalize_distribution(generated_distribution)

        if sum(validasi_distribution) == 0:
            invalid_data.append({'judul_lagu': judul, 'validasi_sequence': validasi_sequence})
            continue  # Lewati baris ini tanpa error

        # Hitung EMD
        emd_distance_per_row = calculate_emd(validasi_distribution, generated_distribution)
        
        results.append({
            'judul_lagu': judul,
            'emd_distance': emd_distance_per_row,
            'validasi_sequence': validasi_sequence
        })
    
    # Mengubah results menjadi DataFrame
    results = pd.DataFrame(results)
    
    # Log data tidak valid untuk analisis lebih lanjut
    if invalid_data:
        invalid_df = pd.DataFrame(invalid_data)
        invalid_df.to_csv("assets/invalid_pitch_data.csv", index=False)
        print(f"Data dengan distribusi pitch kosong disimpan di 'invalid_pitch_data.csv'.")
    
    return results


# Function to calculate descriptive statistics
def calculate_statistics(data):
    mean_emd = data['emd_distance'].mean()
    median_emd = data['emd_distance'].median()
    max_emd = data['emd_distance'].max()
    min_emd = data['emd_distance'].min()

    stats = {
        "mean": mean_emd,
        "median": median_emd,
        "max": max_emd,
        "min": min_emd
    }

    print(f"Mean EMD Distance: {mean_emd:.2f}")
    print(f"Median EMD Distance: {median_emd:.2f}")
    print(f"Max EMD Distance: {max_emd:.2f}")
    print(f"Min EMD Distance: {min_emd:.2f}")
    return stats

# Function to identify outliers
def identify_outliers(data):
    outlier_song = data.loc[data['emd_distance'].idxmax()]
    print(f"Lagu dengan EMD tertinggi:\n{outlier_song}")
    return outlier_song

# Function to plot histogram
def plot_histogram(data, column='emd_distance', bins=10):
    plt.figure(figsize=(10, 6))
    plt.hist(data[column], bins=bins, color='skyblue', edgecolor='black')
    plt.title('Distribusi EMD Distance')
    plt.xlabel('EMD Distance')
    plt.ylabel('Frequency')
    plt.show()

# Function to plot boxplot
def plot_boxplot(data, column='emd_distance'):
    plt.figure(figsize=(10, 6))
    plt.boxplot(data[column], vert=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
    plt.title('Boxplot EMD Distance')
    plt.xlabel('EMD Distance')
    plt.show()

# Function to plot scatter plot
def plot_scatter(data, column='emd_distance', mean_value=None):
    plt.figure(figsize=(10, 6))
    plt.scatter(data.index, data[column], color='blue', alpha=0.7)
    if mean_value is not None:
        plt.axhline(mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')
    plt.title('Scatter Plot EMD Distance per Song')
    plt.xlabel('Song Index')
    plt.ylabel('EMD Distance')
    if mean_value is not None:
        plt.legend()
    plt.show()
    
#### F1 Score, Accuracy, etc. Evaluation ###
# Fungsi untuk menghitung metrik berbasis token
def evaluate_classification_metrics(valDf, generated_sequence):
    """
    Menghitung akurasi, precision, recall, dan F1-score berbasis token.
    valDf: DataFrame validasi yang mengandung ground truth.
    generated_sequence: Output yang dihasilkan oleh model.
    """
    # Konversi data validasi dan keluaran model ke token
    val_tokens = [normalize_distribution(seq) for seq in valDf['bar']]
    generated_tokens = normalize_distribution(generated_sequence)
    
    # Pastikan panjang token sama untuk perbandingan
    min_length = min(len(val_tokens), len(generated_tokens))
    val_tokens = val_tokens[:min_length]
    generated_tokens = generated_tokens[:min_length]
    
    # Hitung metrik
    accuracy = accuracy_score(val_tokens, generated_tokens)
    precision = precision_score(val_tokens, generated_tokens, average='macro', zero_division=0)
    recall = recall_score(val_tokens, generated_tokens, average='macro', zero_division=0)
    f1 = f1_score(val_tokens, generated_tokens, average='macro', zero_division=0)
    
    # Print hasil
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    
    # Laporan klasifikasi
    report = classification_report(val_tokens, generated_tokens, zero_division=0)
    print("\nClassification Report:")
    print(report)
    
    return {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}


### Fitness Evalutation ###
# Fitness Evaluation
def fitness_smoothness(sequence):
    """Mengukur kelancaran transisi pitch."""
    if len(sequence) < 2:
        return 0
    total_jump = sum(abs(sequence[i] - sequence[i + 1]) for i in range(len(sequence) - 1))
    return 1 / (1 + total_jump)

consonant_intervals = {0, 7, 12}  # Unison, perfect fifth, octave

def fitness_consonance(sequence):
    """Mengukur keselarasan transisi pitch berdasarkan interval harmonik."""
    if len(sequence) < 2:
        return 0
    consonant_pairs = sum(1 for i in range(len(sequence) - 1) if abs(sequence[i] - sequence[i + 1]) in consonant_intervals)
    return consonant_pairs / (len(sequence) - 1)

def fitness_rhythmic_variety(durations):
    """Mengukur keberagaman ritme berdasarkan durasi not."""
    if len(durations) == 0:
        return 0
    variety = len(set(durations)) / len(durations)
    return variety

def fitness_range(sequence):
    """Mengukur rentang pitch dalam sequence."""
    return max(sequence) - min(sequence) if sequence else 0

def repetition_rate(sequence):
    """Mengukur tingkat pengulangan pola pitch dalam sequence."""
    if len(sequence) < 2:
        return 0
    repeated_patterns = sum(1 for i in range(len(sequence) - 1) if sequence[i] == sequence[i + 1])
    return repeated_patterns / len(sequence)

def tonality_score(sequence, key_signature):
    """Mengukur kesesuaian tonalitas dengan key signature tertentu."""
    if not sequence:
        return 0
    tonal_notes = sum(1 for pitch in sequence if pitch % 12 in key_signature)
    return tonal_notes / len(sequence)

# Key signature untuk tonalitas mayor (C Major)
key_signature_major = {0, 2, 4, 5, 7, 9, 11}  # C, D, E, F, G, A, B

def combined_fitness(sequence, durations, key_signature=key_signature_major):
    """Gabungkan semua metrik fitness menjadi satu nilai."""
    smoothness_score = fitness_smoothness(sequence)
    consonance_score = fitness_consonance(sequence)
    variety_score = fitness_rhythmic_variety(durations)
    range_score = fitness_range(sequence) / 12  # Normalisasi terhadap 1 oktaf
    repetition_score = repetition_rate(sequence)
    tonality_score_val = tonality_score(sequence, key_signature)

    return (
        0.3 * smoothness_score +
        0.2 * consonance_score +
        0.2 * variety_score +
        0.1 * range_score +
        0.1 * repetition_score +
        0.1 * tonality_score_val
    )

# Ekstrak MIDI dari string
def extract_midi_pitches_from_bar(bar):
    """Ekstraksi pitch dari string bar ke angka MIDI."""
    pitch_map = {'A': 69, 'B': 71, 'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67}
    return [pitch_map[ch] for ch in bar if ch in pitch_map]

# Evaluasi MIDI
def evaluate_midi_output(valDf, generated_midi):
    """
    Mengevaluasi pitch dan durasi setiap bar di valDf terhadap generated MIDI, lalu memberikan summary hasil rata-rata.
    """
    generated_pitches = [note[1] for note in generated_midi if note[1] > 0]
    generated_durations = [note[0] for note in generated_midi]

    evaluation_results = []
    for index, row in valDf.iterrows():
        val_pitches = extract_midi_pitches_from_bar(row['bar'])
        if not val_pitches:  # Jika pitch ground truth kosong, skip bar ini
            continue

        min_length = min(len(val_pitches), len(generated_pitches))
        val_pitches = val_pitches[:min_length]
        gen_pitches = generated_pitches[:min_length]

        # Evaluasi musikal
        smoothness = fitness_smoothness(gen_pitches)
        consonance = fitness_consonance(gen_pitches)
        rhythmic_variety = fitness_rhythmic_variety(generated_durations[:min_length])
        range_score = fitness_range(gen_pitches)
        repetition_score = repetition_rate(gen_pitches)
        tonality = tonality_score(gen_pitches, key_signature_major)
        combined_score = combined_fitness(gen_pitches, generated_durations[:min_length])

        mse_pitch = mean_squared_error(val_pitches, gen_pitches)
        euclidean_dist = euclidean(val_pitches, gen_pitches)

        evaluation_results.append({
            "bar_index": index,
            "smoothness": smoothness,
            "consonance": consonance,
            "rhythmic_variety": rhythmic_variety,
            "range": range_score,
            "repetition_rate": repetition_score,
            "tonality": tonality,
            "combined_fitness": combined_score,
            "mse_pitch": mse_pitch,
            "euclidean_distance": euclidean_dist
        })

    results_df = pd.DataFrame(evaluation_results)

    summary = {
        "avg_smoothness": results_df["smoothness"].mean(),
        "avg_consonance": results_df["consonance"].mean(),
        "avg_rhythmic_variety": results_df["rhythmic_variety"].mean(),
        "avg_range": results_df["range"].mean(),
        "avg_repetition_rate": results_df["repetition_rate"].mean(),
        "avg_tonality": results_df["tonality"].mean(),
        "avg_combined_fitness": results_df["combined_fitness"].mean(),
        "avg_mse_pitch": results_df["mse_pitch"].mean(),
        "avg_euclidean_distance": results_df["euclidean_distance"].mean()
    }

    return results_df, summary

# Plotting
def plot_fitness_components(summary, output_path):
    metrics = list(summary.keys())
    values = list(summary.values())

    plt.figure(figsize=(12, 6))
    plt.bar(metrics, values, alpha=0.7, color='skyblue')
    plt.title("Fitness Metrics Evaluation")
    plt.xlabel("Metrics")
    plt.ylabel("Scores")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path)
