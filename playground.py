import random

import mido
# Define the note durations
note_durations = {
    "whole": 4,
    "half": 2,
    "quarter": 1,
    "eighth": 0.5,
    "sixteenth": 0.25
}

# Maximum sum and maximum number of items
max_sum = 4
max_items = 16


# Backtracking function to generate all valid combinations
def find_combinations(current_combo, current_sum, note_count):
    # If the current sum exceeds the maximum or note count exceeds the limit, return
    if current_sum > max_sum or note_count > max_items:
        return

    # If the current sum is exactly equal to max_sum, store the combination
    if current_sum == max_sum:
        valid_combinations.append(current_combo)
        return

    # Recursively add more notes and explore further combinations
    for note, duration in note_durations.items():
        find_combinations(current_combo + [duration], current_sum + duration, note_count + 1)


# Initialize a list to store valid combinations
valid_combinations = []

# Start backtracking with an empty combination, 0 current sum, and 0 note count
find_combinations([], 0, 0)

# Display the valid combinations
for combination in valid_combinations:
    print(combination)

# Optional: Print the total number of valid combinations found
print(f"Total valid combinations: {len(valid_combinations)}")

strong_beats = [0, 1, 2, 3]  # Downbeats
weak_beats = [0.5, 1.5, 2.5, 3.5]  # Off-beats
def generate_beat_duration_pairs(note_group):
    beat_duration_pairs = []
    current_time = 0

    for duration in note_group:
        beat_duration_pairs.append((current_time, duration))
        current_time += duration

        # Ensure current_time stays within 4 beats (1 measure)
        if current_time >= 4:
            current_time = current_time % 4

    return beat_duration_pairs

# Define constants
ticks_per_beat = 480  # Standard ticks per beat for MIDI timing
midi_note = 60  # Middle C

# Function to convert beat-duration pairs to MIDI
def write_midi(beat_duration_pairs, filename='output.mid', tempo_bpm=120):
    # Create a new MIDI file and track
    mid = mido.MidiFile(ticks_per_beat=ticks_per_beat)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Set tempo (MIDI uses microseconds per beat)
    microseconds_per_beat = mido.bpm2tempo(tempo_bpm)
    track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat))

    # Initialize timing variables
    ticks_per_second = ticks_per_beat * (tempo_bpm / 60)  # Calculate ticks per second
    current_time_in_ticks = 0

    # Loop through each beat-duration pair
    for beat, duration in beat_duration_pairs:
        # Convert beat to ticks
        start_time_in_ticks = int(beat * ticks_per_beat)
        duration_in_ticks = int(duration * ticks_per_beat)

        # Add the note-on event (note start)
        track.append(mido.Message('note_on', note=midi_note, velocity=64, time=start_time_in_ticks - current_time_in_ticks))
        current_time_in_ticks = start_time_in_ticks

        # Add the note-off event (note end)
        track.append(mido.Message('note_off', note=midi_note, velocity=64, time=duration_in_ticks))
        current_time_in_ticks += duration_in_ticks

    # Save the MIDI file
    mid.save(filename)
    print(f"MIDI file saved as {filename}")

# Define the metric weights for a 4/4 measure
metric_weights = {
    0: 4,  # Strongest beat
    1: 1,  # Weak beat
    2: 3,  # Strong beat
    3: 1,  # Weak beat
    0.5: 0,  # Off-beat
    1.5: 0,  # Off-beat
    2.5: 0,  # Off-beat
    3.5: 0   # Off-beat
}

# Define the strong beats in a 4/4 measure
strong_beats = [0, 2]  # Downbeats in 4/4 time
# Function to calculate syncopation score
def calculate_syncopation_gomez_naveda(rhythm):
    syncopation_score = 0

    for beat, duration in rhythm:
        # Find the metric weight for the current beat
        current_weight = metric_weights.get(beat, 0)
        # Find the next strong beat dynamically
        next_strong_beat = find_next_strong_beat(beat % 4)  # Use modulo to keep within the measure
        next_strong_beat_weight = metric_weights.get(next_strong_beat % 4, 0)

        # Calculate syncopation contribution
        syncopation_score += abs(next_strong_beat_weight - current_weight)

    return syncopation_score

def calculate_density(rhythmic_sequence):
    """
    measured by the number of rhythmic sequence in the group (more item = higher density). The item of rhythmic represent note values.

    :param
        note_group: group of note value, example [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 2]
    :return
        int: number of note value in the group
    """
    return len(rhythmic_sequence)
# Function to find the next strong beat
def find_next_strong_beat(current_beat):
    # Cycle through the strong beats and find the first one after the current beat
    for strong_beat in strong_beats:
        if strong_beat > current_beat:
            return strong_beat
    # If no strong beat is found ahead, assume the measure wraps around (next measure)
    return strong_beats[0] + 4

selected_duration = random.choice(valid_combinations)
# selected_duration = [0.25, 0.25, 0.25, 0.25, 0.25, 0.5, 0.25, 2]
print(f"selected {selected_duration}")
beat_duration_pairs = generate_beat_duration_pairs(selected_duration)
print(f"beat_duration_pairs {beat_duration_pairs}")
syncopation_score = calculate_syncopation_gomez_naveda(beat_duration_pairs)
print(f"syncopation_score {syncopation_score}")
write_midi(beat_duration_pairs, filename='rhythm_pattern.mid', tempo_bpm=120)

for beat, duration in beat_duration_pairs:
    next_strong_beat = find_next_strong_beat(beat % 4)
    print(f"beat {beat}, duration {duration}, next_strong_beat {next_strong_beat}")