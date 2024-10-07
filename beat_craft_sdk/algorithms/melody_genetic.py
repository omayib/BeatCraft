from phrase_generator_genetic import generate_phrase_with_genetic_algorithm
from scale_generator import generate_scale_with_genetic_algorithm
import mido
from mido import MidiFile, MidiTrack, Message

solution = generate_phrase_with_genetic_algorithm()
flattened_list = [item for sublist in solution for item in (sublist if isinstance(sublist, list) else [sublist])]
print(f"flattened list {flattened_list}")

numberitem = len(flattened_list)
best_sequence = generate_scale_with_genetic_algorithm(numberitem)
print(f"best_sequence list {best_sequence}")

paired_notes = list(zip(flattened_list,best_sequence))

print(paired_notes)

# Create a new MIDI file and track
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Set a tempo (BPM)
tempo = mido.bpm2tempo(120)  # Convert BPM to MIDI tempo
track.append(mido.MetaMessage('set_tempo', tempo=tempo))

# Define a base time unit for quarter notes (in MIDI ticks, typically 480 ticks per beat)
ticks_per_beat = 480

# Add notes to the MIDI track
for duration, pitch in paired_notes:
    # Convert the duration (in beats) to MIDI ticks
    ticks = int(duration * ticks_per_beat)

    if pitch != 0:  # 0 means rest, so skip note_on/note_off
        # Add a note on event (velocity 64 for normal sound)
        track.append(Message('note_on', note=pitch, velocity=64, time=0))

        # Add a note off event after the note duration
        track.append(Message('note_off', note=pitch, velocity=64, time=ticks))
    else:
        # If it's a rest, just wait (no note_on or note_off)
        track.append(Message('note_off', note=0, velocity=0, time=ticks))

# Save the MIDI file
mid.save('output.mid')

print("MIDI file 'output.mid' has been created!")