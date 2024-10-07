import os.path
import unittest

from beat_craft_sdk.config import BeatCraftConfig
from beat_craft_sdk.core import BeatCraft
from beat_craft_sdk.crafting_with_backingtrack import CraftingBackingTrack
from beat_craft_sdk.utils.audio_converter import AudioConverter


class TestBeatCraftSdk(unittest.TestCase):

    def test_greet(self):
        sdk = BeatCraft()
        greeting = sdk.greet("Arul")

        self.assertEqual(greeting,"Hi,Arul")

    def test_config_all_params_none(self):
        conf = BeatCraftConfig()
        self.assertEqual(conf.get_output_dir(),"./../.outputx")
        self.assertTrue(conf.get_file_name())

    def test_config_filled_all_params(self):
        conf = BeatCraftConfig("./../.outputz","malam")
        self.assertEqual(conf.get_output_dir(), "./../.outputz")
        self.assertEqual(conf.get_file_name(),"malam")

    def test_generate_melody_with_genetic(self):
        config = BeatCraftConfig()
        sdk = BeatCraft(config)
        notes = sdk.compose_melody()
        self.assertGreater(len(notes),0,"list of notes are empty")

        sdk.melody_to_midi(notes)
        self.assertTrue(os.path.exists('../.output/output.mid'))

    def test_generate_melody_with_backingtrack(self):
        btconfig = BeatCraftConfig(file_name='output_bt')
        sdk = BeatCraft(btconfig)
        sdk.set_melody_engine(CraftingBackingTrack())
        notes = sdk.compose_melody()
        self.assertGreater(len(notes),0,"list of notes are empty")

        sdk.melody_to_midi(notes)
        self.assertTrue(os.path.exists('../.outputx/output_bt.mid'))
    def test_sdk_play_midi_generated(self):
        config = BeatCraftConfig()
        sdk = BeatCraft(config)
        sdk.play_generated_music('../.outputx/output_bt.mid')

    def test_convert_midi_to_wav(self):
        conv = AudioConverter('../.outputx/output_bt.mid','../.outputx/output_bt.wav')
        conv.midi_to_wav()

    def test_generate_rythm(self):
        sdk = BeatCraft()
        sdk.generate_rythm('../.outputx/output_bt.wav','../.outputx')

    def test_genetic_fitness_over_generation(self):
        pass
if __name__ == '__main__':
    unittest.main()