from beat_craft_sdk.config import Config


class BeatCraft:
    def __init__(self, config=None):
        self.config = config if config else Config()


    def generate_music(self):
        tempo = self.config.tempo
        vibe = self.config.vibe

        return f"Generating {tempo}, {vibe} music"

    def greet(self,name):
        return f"Hi,{name}"

    def get_tempo(self):
        return self.config.tempo
    def get_vibe(self):
        return self.config.vibe