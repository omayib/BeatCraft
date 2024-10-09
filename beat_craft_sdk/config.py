import os
from enum import Enum

from beat_craft_sdk.utils.beat_craft_utils import get_current_time

class GameGenre(Enum):
    ACTION="Energetic"
    RPG = "Epic"
    Horror = "Dissonant"
    Puzzle = "Ambient"

class GameMood(Enum):
    JOYFUL="Upbeat And Lively"
    SERENE="Calm and Ambient"
    EPIC="Grand and orchestral"
    RELAXING="Relaxing"
    TENSE="Dark and suspenseful"

class GameEmotional(Enum):#mapping into music scale
    EXCITEMENT = "Major"
    FEAR = "Minor"
    PEACEFUL = "Pentatonic"
    CHALLENGE = "Dorian"


class BeatCraftConfig:

    DEFAULT_OUTPUT_DIR = './../.outputx'
    C_major = [60, 62, 64, 65, 67, 69, 71]
    C_minor = [60, 62, 63, 65, 67, 68, 70]
    C_pentatonic = [60, 62, 64, 67, 69]
    C_dorian = [60, 62, 63, 65, 67, 69, 70]
    emotional_to_midi = {
        GameEmotional.EXCITEMENT.value: C_major,
        GameEmotional.FEAR.value: C_minor,
        GameEmotional.PEACEFUL.value: C_pentatonic,
        GameEmotional.CHALLENGE.value: C_dorian
    }

    def __init__(self,output_dir=None, file_name=None):
        self.output_dir = output_dir
        self.file_name = file_name
        self.path_midi_file = ''
        self.path_wav_file = ''
        self.genre = GameGenre.ACTION.value
        self.mood = GameMood.JOYFUL.value
        self.emotional = GameEmotional.EXCITEMENT.value
        self.validate_config()
        print(f" input default emot:{self.emotional}, genre:{self.genre}, mood:{self.mood}")

    def validate_config(self):
        # If output_dir is None or doesn't exist, create it
        if self.output_dir is None:
            os.makedirs(self.DEFAULT_OUTPUT_DIR, exist_ok=True)
            self.output_dir = self.DEFAULT_OUTPUT_DIR
            # self.output_dir = os.path.abspath('./../.outputx')  # Using absolute path for consistency
        elif not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)  # Create the directory if it doesn't exist

        if self.file_name is None:
            self.file_name = get_current_time()

        print(f"validating config output_dir {self.output_dir}")
        print(f"validating config default_file_name {self.file_name}")

    def get_output_dir(self):
        return self.output_dir

    def get_file_name(self):
        return self.file_name

    def set_game_genre(self,game_genre:GameGenre):
        self.genre = game_genre.value

    def get_game_genre(self):
        return self.genre

    def set_game_mood(self,game_mood:GameMood):
        self.mood=game_mood.value

    def get_game_mood(self):
        return self.mood

    def set_game_emotional(self,game_emotional:GameEmotional):
        self.emotional = game_emotional.value

    def get_game_emotional(self):
        return self.emotional

    def get_midi_notes(self, game_emotional):
        return self.emotional_to_midi.get(game_emotional, "Unknown Emotion")