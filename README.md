# BEAT CRAFT
While you are focus on the game logic, BeatCraft help you to make an authentic music for your game!


## Usage

```python
from beat_craft_sdk.core import BeatCraft

sdk = BeatCraft()
```

### Define the parameter

```python
bcconfig = BeatCraftConfig(file_name='output_bt')
```

put the `bconfig` for initialize the `BeatCraft` 
```python
sdk = BeatCraft(bcconfig)
melodies = sdk.compose_melody()
```

The result are paired note and its duration ( note value )
```python
[(1, 65), (1, 67), (0.5, 64), (0.25, 67), (0.25, 62), (2, 62), (0.25, 65), (1, 62), (2, 59), (0.5, 65), (4, 67), (1, 62), (0.25, 0), (0.25, 67), (1, 60), (0.5, 0), (0.25, 67)]
```

By default the algorithm are using Genetic Algorithm. But you can change the algorithm here especially for generate the melodies
```python
sdk = BeatCraft()
sdk.set_melody_engine(CraftingBackingTrack())
melodies = sdk.compose_melody()
```

Wait a minutes. Do you want listen ghe generated midi melody? here the way
```python
sdk.play_generated_music('../.outputx/output_bt.mid')
```

Now, you have a beautiful melody. Its time to generate the full music
```python
# Convert the midi file into wav
conv = AudioConverter('../.outputx/output_bt.mid','../.outputx/output_bt.wav')
conv.midi_to_wav()

# lets make the music
sdk = BeatCraft()
sdk.generate_rythm('../.outputx/output_bt.wav','../.outputx')
```
## Instalation
If you on edge cased by conflict, check the dipendencies we are used [here ](https://gist.github.com/omayib/193a608f4f84323f74c3e91a6c5ab813)
