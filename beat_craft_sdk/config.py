import os

from beat_craft_sdk.utils.beat_craft_utils import get_current_time

BEATCRAFT_OUTPUT_DIR = './../.output'
BEATCRAFT_FILE_NAME = ''

class BeatCraftConfig:
    def __init__(self,output_dir=None, file_name=None):
        self.output_dir = output_dir
        self.file_name = file_name
        self.validate_config()

    def validate_config(self):
        # If output_dir is None or doesn't exist, create it
        if self.output_dir is None:
            os.makedirs(BEATCRAFT_OUTPUT_DIR, exist_ok=True)
            self.output_dir = BEATCRAFT_OUTPUT_DIR
            # self.output_dir = os.path.abspath('./../.outputx')  # Using absolute path for consistency
        elif not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)  # Create the directory if it doesn't exist

        if self.file_name is None:
            self.file_name = get_current_time()

        self.update_globals()

        print(f"validating config output_dir {self.output_dir}")
        print(f"validating config default_file_name {self.file_name}")

    def update_globals(self):
        """Explicitly update global variables with current instance values."""
        global BEATCRAFT_OUTPUT_DIR, BEATCRAFT_FILE_NAME  # Access global variables
        BEATCRAFT_OUTPUT_DIR = self.output_dir
        BEATCRAFT_FILE_NAME = self.file_name
        print(f"Updated global BEATCRAFT_OUTPUT_DIR to: {BEATCRAFT_OUTPUT_DIR}")
        print(f"Updated global BEATCRAFT_FILE_NAME to: {BEATCRAFT_FILE_NAME}")
