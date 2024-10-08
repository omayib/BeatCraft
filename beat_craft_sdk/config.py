import os

from beat_craft_sdk.utils.beat_craft_utils import get_current_time

class BeatCraftConfig:

    DEFAULT_OUTPUT_DIR = './../.outputx'

    def __init__(self,output_dir=None, file_name=None):
        self.output_dir = output_dir
        self.file_name = file_name
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

        print(f"validating config output_dir {self.output_dir}")
        print(f"validating config default_file_name {self.file_name}")

    def get_output_dir(self):
        return self.output_dir

    def get_file_name(self):
        return self.file_name
