from algorithms.note_duration_generator import generate_note_duration_with_genetic_algorithm
from algorithms.scale_generator import generate_scale_with_genetic_algorithm, num_generations
from beat_craft_sdk.craft_strategy import CraftStrategy
from evaluation.beat_craft_evaluation import plot_fitness_over_generations, plot_pitch_diversity_over_generation, \
    plot_ga_evaluation_into_json


class CraftingGenetic(CraftStrategy):

    def __init__(self):
        self.pitch_fitness_per_generations = []
        self.pitch_diversity_per_generation = []

    def generate(self):
        series_duration = generate_note_duration_with_genetic_algorithm()
        flattened_series_duration= [item for sublist in series_duration for item in
                          (sublist if isinstance(sublist, list) else [sublist])]
        series_scale, self.pitch_fitness_per_generations, self.pitch_diversity_per_generation = generate_scale_with_genetic_algorithm(len(flattened_series_duration))
        paired_notes = list(zip(flattened_series_duration, series_scale))
        print(f"paired notes in crafting genetic {paired_notes}")
        return paired_notes

    def evaluate(self):
        print(f"best_fitness_per_generations {self.pitch_fitness_per_generations}")
        plot_fitness_over_generations(num_generations, self.pitch_fitness_per_generations, "../.output")
        plot_pitch_diversity_over_generation(num_generations, self.pitch_diversity_per_generation, "../.output")
        plot_ga_evaluation_into_json(self.pitch_diversity_per_generation,self.pitch_fitness_per_generations,"../.output")