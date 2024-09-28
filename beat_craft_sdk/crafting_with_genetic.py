from algorithms.note_duration_generator import generate_note_duration_with_genetic_algorithm
from algorithms.scale_generator import generate_scale_with_genetic_algorithm
from beat_craft_sdk.craft_strategy import CraftStrategy


class CraftingGenetic(CraftStrategy):
    def generate(self):
        series_duration = generate_note_duration_with_genetic_algorithm()
        flattened_series_duration= [item for sublist in series_duration for item in
                          (sublist if isinstance(sublist, list) else [sublist])]
        series_scale = generate_scale_with_genetic_algorithm(len(flattened_series_duration))
        paired_notes = list(zip(flattened_series_duration, series_scale))
        print(f"paired notes in crafting genetic {paired_notes}")
        return paired_notes