from beat_craft_sdk.config import Config
from beat_craft_sdk.crafting_with_genetic import CraftingGenetic


class BeatCraft:
    def __init__(self, config=None, strategy=CraftingGenetic):
        self.config = config if config else Config()
        self.tempo = self.config.tempo
        self.vibe = self.config.vibe
        self.strategy = strategy

    def set_strategy(self, strategy=CraftingGenetic):
        self.strategy = strategy

    def generate_music(self):
        notes = self.strategy.generate(self)
        print(f"notes in core generate music {notes}")
        return f"Generating notes {notes}"

    def greet(self,name):
        return f"Hi,{name}"

    def get_tempo(self):
        return self.config.tempo
    def get_vibe(self):
        return self.config.vibe