import os

from utils.beat_craft_utils import get_current_time

default_output_dir = './../.outputx'

class BeatCraftConfig:
    def __init__(self,output_dir=None, file_name=None):
        self.output_dir = output_dir
        self.file_name = file_name
        self.validate_config()

    def validate_config(self):
        print(f"validating config output_dir {self.output_dir}")
        # If output_dir is None or doesn't exist, create it
        if self.output_dir is None:
            os.makedirs(default_output_dir, exist_ok=True)
            self.output_dir = default_output_dir
            # self.output_dir = os.path.abspath('./../.outputx')  # Using absolute path for consistency
        elif not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)  # Create the directory if it doesn't exist
        if not self.file_name:
            self.file_name = get_current_time()

    def get_output_dir(self):
        return self.output_dir

    def get_file_name(self):
        return self.file_name

    def __repr__(self):
        return f"Config(output_dir='{self.output_dir}', file_name='{self.file_name}')"

    def to_dict(self):
        return {"output_dir":self.output_dir, "file_name":self.file_name}