import os.path
import unittest

from numpy.distutils.command.config import config

from beat_craft_sdk.core import BeatCraft, Config
from utils.audio_converter import AudioConverter


class TestBeatCraftSdk(unittest.TestCase):

    def test_greet(self):
        sdk = BeatCraft()
        greeting = sdk.greet("Arul")

        self.assertEqual(greeting,"Hi,Arul")
    def test_generate_melody_with_config(self):
        config = Config(tempo="fast",vibe="calm")
        sdk = BeatCraft(config)
        notes = sdk.generate_melody()
        self.assertGreater(len(notes),0,"list of notes are empty")

        sdk.melody_to_midi(notes)
        self.assertTrue(os.path.exists('../.output/output.mid'))

    def test_sdk_play_midi_generated(self):
        config = Config(tempo="fast",vibe="calm")
        sdk = BeatCraft(config)
        sdk.play_generated_music('../.output/output.mid')

    def test_convert_midi_to_wav(self):
        conv = AudioConverter('../.output/output.mid','../.output/output.wav')
        conv.midi_to_wav()

    def test_generate_rythm(self):
        config = Config(tempo="fast",vibe="calm")
        sdk = BeatCraft(config)
        sdk.generate_rythm('../.output/output.wav','../.output')

    def test_genetic_fitness_over_generation(self):
        pass
if __name__ == '__main__':
    unittest.main()