# BEAT CRAFT
While you are focus on the game logic, BeatCraft help you to make an authentic music for your game


## Usage

```python
from beat_craft_sdk.core import BeatCraft

sdk = BeatCraft()
print(sdk.greet('World'))  # Output: Hello, World!
```

### Define the parameter
```python
config = Config(tempo="fast",vibe="calm")
sdk = BeatCraft(config)
notes = sdk.generate_music()
```
The result are paired note and its duration
```python
[(1, 65), (1, 67), (0.5, 64), (0.25, 67), (0.25, 62), (2, 62), (0.25, 65), (1, 62), (2, 59), (0.5, 65), (4, 67), (1, 62), (0.25, 0), (0.25, 67), (1, 60), (0.5, 0), (0.25, 67)]
```
By default the algorithm are using Genetic Algorithm