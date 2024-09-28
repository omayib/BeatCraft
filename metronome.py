import sounddevice as sd
import numpy as np
import time

# Metronome parameters
bpm = 120  # Beats per minute
interval = 60.0 / bpm  # Seconds per beat

# "Cradle Song" melody in C major with note lengths
cradle_melody = [
    (392.00, 0.5), (440.00, 0.5), (392.00, 0.5),  # G A G
    (349.23, 0.5), (261.63, 0.5), (293.66, 0.5),  # F C D
    (261.63, 1.0),                               # C (whole note)

    (392.00, 0.5), (440.00, 0.5), (392.00, 0.5),  # G A G
    (349.23, 0.5), (261.63, 0.5), (293.66, 0.5),  # F C D
    (261.63, 1.0),                               # C (whole note)

    (293.66, 0.5), (349.23, 0.5), (392.00, 0.5),  # D F G
    (349.23, 0.5), (293.66, 0.5), (261.63, 0.5),  # F D C
    (392.00, 0.5), (440.00, 0.5), (392.00, 0.5),  # G A G

    (349.23, 0.5), (261.63, 0.5), (293.66, 0.5),  # F C D
    (261.63, 1.0)                                # C (whole note)
]

# Generate a sound wave for melody notes
def sound_wave(duration=0.05, frequency=440, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    return wave

# Play a sound (either click or melody note)
def play_sound(frequency, duration=0.05):
    sound = sound_wave(frequency=frequency, duration=duration)
    sd.play(sound, samplerate=44100)
    sd.wait()  # Wait until the sound finishes playing

# Function to play just the melody
def play_melody():
    print(f"Playing 'Cradle Song' melody at {bpm} BPM (Press Ctrl+C to stop)")
    melody_index = 0  # Track which note in the melody is playing
    melody_time = 0  # Track the time for note length

    try:
        while True:
            # Play melody if it's time for a new note
            note, length = cradle_melody[melody_index]  # Get the current melody note and its length
            if melody_time <= 0:  # If the note's time is up, play the next one
                print(f"Playing note: {note} Hz, Length: {length * 4}/4")
                play_sound(frequency=note, duration=length * interval)  # Play the note
                melody_time = length  # Reset the time for the new note
                melody_index = (melody_index + 1) % len(cradle_melody)  # Move to the next note

            # Decrease melody time by 1 beat interval (to account for note duration)
            melody_time -= 1
            time.sleep(interval - 0.05)  # Adjust for the note duration

    except KeyboardInterrupt:
        print("\nMelody stopped.")

# Start the melody playback
if __name__ == "__main__":
    play_melody()
