import unittest

from numpy.distutils.command.config import config

from beat_craft_sdk.core import BeatCraft, Config

class TestBeatCraftSdk(unittest.TestCase):

    def test_greet(self):
        sdk = BeatCraft()
        greeting = sdk.greet("Arul")

        self.assertEqual(greeting,"Hi,Arul")
    def test_sdk_with_config(self):
        config = Config(tempo="fast",vibe="calm")
        sdk = BeatCraft(config)
        sdk.generate_music()
        self.assertEqual(sdk.get_vibe(),"calm")
        self.assertEqual(sdk.get_tempo(),"fast")
if __name__ == '__main__':
    unittest.main()