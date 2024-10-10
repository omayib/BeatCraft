# BEAT CRAFT
While you focus on your game's logic, BeatCraft assists you in creating authentic music for your game!
IIf you're curious about how it works, check out the [Wiki](https://github.com/omayib/BeatCraft/wiki) for more information.

Listen to a sample of the results [here](https://soundcloud.com/omayib/generated-game-sound-with-emational-fear-action-and-tense?si=0ff0d27087d648e28f40edaccd010188&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)

## Installation
BeatCraft is available on PyPI. To install it, run:
```bash
pip install beatcraft
```

If you encounter conflicts, refer to the dependencies we utilize here.

It's advisable to run your pip command with constraints to avoid potential dependency conflicts:
```bash
pip install beatcraft -c constraints.txt
```

here is the `constrains.txt` file:
```
pandas==2.2.3
numpy>=1.26.0
matplotlib==3.9.2
gradio==4.44.0
torchmetrics==1.4.2
encodec==0.1.1
```

## Usage
To use BeatCraft in your Python code, start by importing it:

```python
from beat_craft_sdk.core import BeatCraft

sdk = BeatCraft()
```

### Define the parameter
You can define parameters using `BeatCraftConfig`:
```python
bcconfig = BeatCraftConfig(file_name='output_bt')
```

Initialize `BeatCraft` with your configuration

```python
sdk = BeatCraft(bcconfig)
melodies = sdk.compose_melody()
print(f"{melodies}")
```

The result will be a list of paired notes and their durations (note values):
```python
[(1, 65), (1, 67), (0.5, 64), (0.25, 67), (0.25, 62), (2, 62), (0.25, 65), (1, 62), (2, 59), (0.5, 65), (4, 67), (1, 62), (0.25, 0), (0.25, 67), (1, 60), (0.5, 0), (0.25, 67)]
```
By default, the algorithm uses a Genetic Algorithm. However, you can change the melody generation algorithm:

```python
sdk = BeatCraft()
sdk.set_melody_engine(CraftingBackingTrack())
melodies = sdk.compose_melody()
```
### Play the Generated MIDI Melody
Would you like to listen to the generated MIDI melody? Here’s how:
```python
sdk.play_generated_music('../.outputx/output_bt.mid')
```

Now that you have a beautiful melody. It's time to generate the full music
```python
# Convert the midi file into wav
conv = AudioConverter('../.outputx/output_bt.mid','../.outputx/output_bt.wav')
conv.midi_to_wav()

# lets make the music
sdk = BeatCraft()
sdk.generate_rythm('../.outputx/output_bt.wav','../.outputx')
```
# Contact
For inquiries, please reach out to Arif Akbarul Huda at [omayib@gmail.com](mailto:omayib@gmail.com)
