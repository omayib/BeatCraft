from beat_craft_sdk.config import BeatCraftConfig
from beat_craft_sdk.crafting_with_genetic import CraftingGenetic
import mido
from mido import MidiFile, MidiTrack, Message
import pygame
import os
import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

from beat_craft_sdk.evaluation.beat_craft_evaluation import plot_mel_spectrogram, plot_waveform, plot_spectrogram, plot_pitch_contour, \
    load_audio_file
from beat_craft_sdk.utils.beat_craft_utils import get_current_time


class BeatCraft:
    def __init__(self, config=None, melody_engine=None):
        self.config = config if config else BeatCraftConfig()
        self.melody_engine = melody_engine if melody_engine else CraftingGenetic()

    def set_melody_engine(self, melody_engine):
        self.melody_engine = melody_engine

    def compose_melody(self):
        notes = self.melody_engine.generate(self.config.get_output_dir(),self.config.get_file_name(), self.config.get_midi_notes(self.config.get_game_emotional()))
        self.melody_engine.evaluate(self.config.get_output_dir(),self.config.get_file_name())
        print(f"notes in core generate music {notes}")
        return notes

    def melody_to_midi(self, generated_notes=None):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        # Set a tempo (BPM)
        tempo = mido.bpm2tempo(120)  # Convert BPM to MIDI tempo
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))

        # Define a base time unit for quarter notes (in MIDI ticks, typically 480 ticks per beat)
        ticks_per_beat = 480

        for duration, pitch in generated_notes:
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
        output_path = f"{self.config.get_output_dir()}/{self.config.get_file_name()}.mid"
        print(f"output_path {output_path} ")
        mid.save(output_path)

    def play_generated_music(self, path):
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pass
    def generate_rythm(self,melody_file_name):

        audio_melody_path = f"{self.config.get_output_dir()}/{melody_file_name}.wav"
        model = MusicGen.get_pretrained('melody')
        model.set_generation_params(duration=8)  # generate 8 seconds.
        desc = f"{self.config.get_game_emotional()} {self.config.get_game_mood()}"
        descriptions = [desc]

        melody, sr = torchaudio.load(audio_melody_path)
        # generates using the melody from the given audio and the provided descriptions.
        wav = model.generate_with_chroma(descriptions, melody[None].expand(1, -1, -1), sr)

        for idx, one_wav in enumerate(wav):
            output_filename = f'{idx}_{get_current_time()}_{self.config.get_file_name()}'
            # Full path where the audio will be saved
            output_path = os.path.join(self.config.get_output_dir(), output_filename)
            # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
            audio_write(stem_name=output_path, wav=one_wav.cpu(), sample_rate=model.sample_rate, strategy="loudness")

            audio_data, sample_rate = load_audio_file(f"{output_path}.wav")

            plot_pitch_contour(audio_data,sample_rate, self.config.get_output_dir(), self.config.get_file_name())
            plot_mel_spectrogram(audio_data,sample_rate,self.config.get_output_dir(), self.config.get_file_name())
            plot_waveform(audio_data, sample_rate, self.config.get_output_dir(), self.config.get_file_name())
            plot_spectrogram(audio_data, sample_rate, self.config.get_output_dir(), self.config.get_file_name())

    def get_config(self):
        return self.config