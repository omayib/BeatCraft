import os
import  platform

from midi2audio import FluidSynth


def get_default_sound_font():
    current_os = platform.system()
    if current_os=='Linux':
        return '/usr/share/sounds/sf2/FluidR3_GM.sf2'
    elif current_os=='Darwin':
        return '/Library/Audio/Sounds/Banks/FluidR3_GM.sf2'
    else:
        raise Exception(f"Unsupported OS:{current_os}. Please provide a valid sound font path.")


class AudioConverter:
    def __init__(self,input_path,output_path, sound_font=None):
        self._input_path = input_path
        self._output_path = output_path
        self.sound_font = sound_font or os.getenv('SOUND_FONT_PATH') or get_default_sound_font()

    def midi_to_wav(self):
        try:
            if not os.path.exists(self._input_path):
                raise FileNotFoundError(f"Input MIDI file not found : {self._input_path}")
            if not os.path.exists(self.sound_font):
                raise FileNotFoundError(f"SoundFont file not found : {self.sound_font}")

            fs = FluidSynth(self.sound_font)
            fs.midi_to_audio(self._input_path,self._output_path)
        except Exception as e:
            print(f"An error occurred during conversion: {e}")