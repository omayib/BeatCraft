import os
from enum import Enum

from beat_craft_sdk.utils.beat_craft_utils import get_current_time

class GameGenre(Enum):
    ACTION="Energetic"
    RPG = "Epic"
    Horror = "Dissonant"
    Puzzle = "Ambient"
    @staticmethod
    def from_transformer_data(ritme):
        # Defined genre mapping from transformer data
        genre_map = {
            'Cheerfully': GameGenre.ACTION,'Playfully': GameGenre.ACTION,
            'With spirit': GameGenre.ACTION,'Brilliant': GameGenre.ACTION,
            'Slow with expression': GameGenre.RPG,'Slow and mournful': GameGenre.Horror,
            'Mournful': GameGenre.Horror,'Plaintive': GameGenre.Horror,
            'Tenderly': GameGenre.Puzzle,'Gracefully': GameGenre.Puzzle,
            'Animated': GameGenre.Puzzle, 'Boldly': GameGenre.Horror,
            'Cheerful': GameGenre.RPG, 'Distincly': GameGenre.Horror,
            'Gaily': GameGenre.ACTION, 'Gheerfuly': GameGenre.ACTION,
            'Graceful': GameGenre.ACTION, 'Lively': GameGenre.RPG,
            'Moderate': GameGenre.ACTION, 'Plaintively': GameGenre.Horror,
            'Playful': GameGenre.Puzzle, 'Playfully': GameGenre.Puzzle,
            'Quick and spirit': GameGenre.ACTION, 'Rather slow': GameGenre.Puzzle,
            'Slow': GameGenre.Horror, 'Slow and distinctly': GameGenre.Puzzle,
            'Slow and plaintive': GameGenre.Horror, 'Slow and tenderly': GameGenre.Puzzle,
            'Slow and with feeling': GameGenre.Horror, 'Slow with expression': GameGenre.RPG,
            'Slow with feeling': GameGenre.Horror, 'Slow, with expression': GameGenre.RPG,
            'Spirited': GameGenre.ACTION, 'Unknown': GameGenre.Horror,
            'Very Slow': GameGenre.Puzzle, 'Very slow and plaintive': GameGenre.Horror,
            'With Animation': GameGenre.RPG, 'With expression': GameGenre.RPG,
            'With feeling': GameGenre.Horror, 'With Force': GameGenre.ACTION,
            'With spirit and feeling': GameGenre.ACTION
        }
        # Return default genre into ACTION
        return genre_map.get(ritme, GameGenre.ACTION)
    
    @staticmethod
    def to_transformer_ritme(emotional_enum):
        transformer_map = {
            GameGenre.RPG: ['Slow with expression', 'Cheerful', 'Lively', 'Slow with expression',
                            'Slow, with expression', 'With Animation', 'With expression'],
            GameGenre.Horror: ['Mournful', 'Slow and mournful','Plaintive', 'Boldly',
                               'Distincly', 'Plaintively', 'Slow', 'Slow and with feeling',
                               'Slow and with feeling', 'Slow with feeling', 'Unknown',
                               'With feeling', 'Very slow and plaintive'],
            GameGenre.Puzzle: ['Tenderly', 'Slow', 'Gracefully', 'Animated',
                               'Playful', 'Playfully', 'Rather slow', 'Slow and distinctly',
                               'Slow and tenderly', 'Very Slow'],
            GameGenre.ACTION: ['Cheerfully', 'Playfully', 'Brilliant', 'With spirit',
                               'Gaily', 'Gheerfuly', 'Graceful', 'Moderate',
                               'Quick and spirit', 'Spirited', 'With Force', 'With spirit and feeling'
                               ]
        }
        # Mengembalikan list ritme yang terkait dengan enum atau default list
        return transformer_map.get(emotional_enum, ['Tenderly'])

class GameMood(Enum):
    JOYFUL="Upbeat And Lively"
    SERENE="Calm and Ambient"
    EPIC="Grand and orchestral"
    RELAXING="Relaxing"
    TENSE="Dark and suspenseful"
    
    @staticmethod
    def from_transformer_data(ritme):
        mood_map = {
            'Cheerfully': GameMood.JOYFUL, 'Playfully': GameMood.JOYFUL,
            'Gaily': GameMood.JOYFUL, 'Gracefully': GameMood.SERENE,
            'Tenderly': GameMood.RELAXING, 'Slow and with feeling': GameMood.RELAXING,
            'With spirit': GameMood.EPIC, 'Brilliant': GameMood.EPIC,
            'Mournful': GameMood.TENSE, 'Slow and mournful': GameMood.TENSE,
            'With force': GameMood.TENSE, 'Animated': GameMood.JOYFUL,
            'Boldly': GameMood.EPIC, 'Cheerful': GameMood.JOYFUL,
            'Gheerfully': GameMood.JOYFUL, 'Graceful': GameMood.SERENE,
            'Lively': GameMood.JOYFUL, 'Distinctly': GameMood.RELAXING,  
            'Moderate': GameMood.TENSE, 'Plaintive': GameMood.TENSE,
            'Plaintively': GameMood.TENSE, 'Quick and spirit': GameMood.EPIC,
            'Rather slow': GameMood.RELAXING,'Slow': GameMood.RELAXING,
            'Slow and distinctly': GameMood.RELAXING,'Slow and plaintive': GameMood.TENSE,
            'Slow and tenderly': GameMood.RELAXING,'Slow with expression': GameMood.RELAXING,
            'Slow with feeling': GameMood.RELAXING,'Slow, with expression': GameMood.RELAXING,
            'Spirited': GameMood.EPIC,'Unknown': GameMood.SERENE,
            'Very slow': GameMood.RELAXING, 'Very slow and plaintive': GameMood.TENSE, 
            'With Animation': GameMood.JOYFUL,'With expression': GameMood.RELAXING,
            'With feeling': GameMood.RELAXING, 'With spirit and feeling': GameMood.EPIC
        }

        return mood_map.get(ritme, GameMood.SERENE)  # Default ke SERENE jika ritme tidak dikenali
    
    @staticmethod
    def to_transformer_ritme(mood_enum):
        transformer_map = {
            GameMood.JOYFUL: [
                'Cheerfully', 'Playfully', 'Gaily', 'Lively', 'With Animation', 'Happy', 
                'Animated', 'Cheerful', 'Gheerfully', 'Quick and spirit'
            ],
            GameMood.SERENE: [
                'Gracefully', 'Tenderly', 'Calmly', 'Peaceful', 'Gently', 'Softly',
                'Graceful', 'Unknown'
            ],
            GameMood.EPIC: [
                'With spirit', 'Brilliant', 'Majestic', 'Grandly', 'Heroic', 'Triumphant', 
                'Boldly', 'Spirited', 'Quick and spirit', 'With spirit and feeling'
            ],
            GameMood.RELAXING: [
                'Slow and with feeling', 'Tenderly', 'Calm', 'Smoothly', 'Warmly', 'Slow',
                'Rather slow', 'Slow and distinctly', 'Slow with expression', 'Slow with feeling', 
                'Slow, with expression', 'Very slow', 'Distinctly', 'Moderate'
            ],
            GameMood.TENSE: [
                'Mournful', 'Slow and mournful', 'With force', 'Intensely', 'Dramatic', 'Darkly',
                'Plaintive', 'Plaintively', 'Slow and plaintive', 'Very slow and plaintive'
            ],
        }
        # Mengembalikan list ritme yang terkait dengan enum atau default list
        return transformer_map.get(mood_enum, ['Tenderly'])  # Default ke 'Tenderly' jika enum tidak dikenali

class GameEmotional(Enum):  # Mapping into music scale
    EXCITEMENT = "Major"
    FEAR = "Minor"
    PEACEFUL = "Pentatonic"
    CHALLENGE = "Dorian"
    
    # Updated dictionary with enum member names as keys
    emotional_to_midi = {
        "EXCITEMENT": [60, 62, 64, 65, 67, 69, 71],   # Major scale for EXCITEMENT
        "PEACEFUL": [60, 62, 64, 67, 69],             # Pentatonic scale for PEACEFUL
        "FEAR": [60, 61, 63, 65, 67, 68, 70],         # Minor scale for FEAR
        "CHALLENGE": [60, 62, 63, 65, 67, 69, 70]     # Dorian scale for CHALLENGE
    }

    @staticmethod
    def from_transformer_data(ritme):
        emotional_map = {
            'Cheerfully': GameEmotional.EXCITEMENT, 'Playfully': GameEmotional.EXCITEMENT,
            'Gaily': GameEmotional.EXCITEMENT, 'Lively': GameEmotional.EXCITEMENT,
            'With Animation': GameEmotional.EXCITEMENT,'Happy': GameEmotional.EXCITEMENT,
            'Animated': GameEmotional.EXCITEMENT,'Cheerful': GameEmotional.EXCITEMENT,
            'Gheerfully': GameEmotional.EXCITEMENT,'Quick and spirit': GameEmotional.CHALLENGE,
            'Gracefully': GameEmotional.PEACEFUL,'Graceful': GameEmotional.PEACEFUL,
            'Tenderly': GameEmotional.PEACEFUL,'Slow': GameEmotional.PEACEFUL,
            'Rather slow': GameEmotional.PEACEFUL,'Slow and with feeling': GameEmotional.PEACEFUL,
            'Slow with expression': GameEmotional.PEACEFUL,'Slow with feeling': GameEmotional.PEACEFUL,
            'Slow, with expression': GameEmotional.PEACEFUL,'Very slow': GameEmotional.PEACEFUL,
            'Brilliant': GameEmotional.EXCITEMENT,'Boldly': GameEmotional.CHALLENGE,
            'With spirit': GameEmotional.CHALLENGE,'Spirited': GameEmotional.CHALLENGE,
            'With spirit and feeling': GameEmotional.CHALLENGE,'Majestic': GameEmotional.CHALLENGE,
            'Grandly': GameEmotional.CHALLENGE,'Heroic': GameEmotional.CHALLENGE,
            'Triumphant': GameEmotional.CHALLENGE,'Mournful': GameEmotional.FEAR,
            'Slow and mournful': GameEmotional.FEAR,'Plaintive': GameEmotional.FEAR,
            'Plaintively': GameEmotional.FEAR,'Slow and plaintive': GameEmotional.FEAR,
            'Very slow and plaintive': GameEmotional.FEAR,'With force': GameEmotional.CHALLENGE,
            'Distinctly': GameEmotional.CHALLENGE,'Moderate': GameEmotional.CHALLENGE,
            'Unknown': GameEmotional.CHALLENGE
        }

        return emotional_map.get(ritme, GameEmotional.PEACEFUL)  # Default ke PEACEFUL jika ritme tidak dikenali

    @staticmethod
    def to_transformer_ritme(emotional_enum):
        transformer_map = {
            GameEmotional.EXCITEMENT: [
                'Cheerfully', 'Playfully', 'Gaily', 'Lively', 'With Animation', 'Happy', 
                'Animated', 'Cheerful', 'Gheerfully', 'Brilliant'
            ],
            GameEmotional.PEACEFUL: [
                'Gracefully', 'Tenderly', 'Graceful', 'Slow', 'Rather slow', 
                'Slow and with feeling', 'Slow with expression', 'Slow with feeling', 
                'Slow, with expression', 'Very slow'
            ],
            GameEmotional.CHALLENGE: [
                'Quick and spirit', 'Boldly', 'With spirit', 'Spirited', 'With spirit and feeling', 
                'Majestic', 'Grandly', 'Heroic', 'Triumphant', 'With force', 
                'Distinctly', 'Moderate', 'Unknown'
            ],
            GameEmotional.FEAR: [
                'Mournful', 'Slow and mournful', 'Plaintive', 'Plaintively', 
                'Slow and plaintive', 'Very slow and plaintive'
            ]
        }
        
        return transformer_map.get(emotional_enum, ['Cheerfully'])


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

        # print(f"validating config output_dir {self.output_dir}")
        # print(f"validating config default_file_name {self.file_name}")

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


# Separate class for Transformer Config
class TransformerConfig:
    DEFAULT_OUTPUT_DIR = './../.outputx'
    
    emotional_to_midi = {
        GameEmotional.EXCITEMENT: [60, 62, 64, 65, 67, 69, 71],  # Major scale
        GameEmotional.FEAR: [60, 62, 63, 65, 67, 68, 70],         # Minor scale
        GameEmotional.PEACEFUL: [60, 62, 64, 67, 69],             # Pentatonic scale
        GameEmotional.CHALLENGE: [60, 62, 63, 65, 67, 69, 70]     # Dorian scale
    }
    
    def __init__(self, file_name=None, output_dir=None):
        self.file_name= file_name
        self.output_dir = "./transformer_output"
        self.genre = GameGenre.ACTION
        self.mood = GameMood.JOYFUL
        self.emotional = GameEmotional.EXCITEMENT
        self.path_midi_file = ''
        self.path_wav_file = ''
        self.validate_config()

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
    
    def get_output_dir(self):
        return self.output_dir

    def get_file_name(self):
        return self.file_name
    
    def set_game_genre(self, game_genre: GameGenre):
        self.genre = GameGenre.to_transformer_ritme(game_genre)
    
    def get_game_genre(self):
        return self.genre

    def set_game_mood(self, game_mood: GameMood):
        self.mood = GameMood.to_transformer_ritme(game_mood)
    
    def get_game_mood(self):
        return self.mood
    
    def set_game_emotional(self, game_emotional: GameEmotional):
        self.emotional = GameEmotional.to_transformer_ritme(game_emotional)

    def get_game_emotional(self):
        return self.emotional
    
    def get_midi_notes(self, game_emotional: GameEmotional):
    # Ensure that the game_emotional is an instance of the GameEmotional enum
        if isinstance(game_emotional, GameEmotional):
            emotional_name = game_emotional.name  # Get the name of the emotional state (e.g., 'EXCITEMENT')
            
            # Fetch the corresponding MIDI notes from the emotional_to_midi dictionary
            notes = self.emotional_to_midi.get(game_emotional, [])
            
            # If notes are found, return them; otherwise, handle the "Unknown Genre"
            if notes:
                return notes
            else:
                return "Unknown Emotion"  # Return a proper response for an unknown emotion
        else:
            return "Invalid Emotion"  # Return error message if input is not a valid GameEmotional