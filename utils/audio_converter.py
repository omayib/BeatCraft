from midi2audio import FluidSynth

class AudioConverter:
    def __init__(self,input_path,output_path):
        self._input_path = input_path
        self._output_path = output_path
        self.sound_font = '/usr/share/sounds/sf2/FluidR3_GM.sf2'

    def midi_to_wav(self):
        fs = FluidSynth(self.sound_font)
        fs.midi_to_audio(self._input_path,self._output_path)