import unittest

from beat_craft_sdk import Config

class TestConfig(unittest.TestCase):
    def test_default_config(self):
        config = Config()
        self.assertEqual(config.tempo,"medium")
        self.assertEqual(config.vibe,"neutral")

    def test_custom_config(self):
        config = Config(tempo="fast", vibe="calm")
        self.assertEqual(config.tempo,"fast")
        self.assertEqual(config.vibe,"calm")
    def test_invalid_config(self):
        with self.assertRaises(ValueError):
            Config(tempo="extreme",vibe="neutral")

if __name__ == '__main__':
    unittest.main()