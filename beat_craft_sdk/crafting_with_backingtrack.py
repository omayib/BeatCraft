import random

from algorithms.phrase_generator_backtracking import BackTracking
from algorithms.phrase_generator_genetic import generate_phrase_with_genetic_algorithm
from algorithms.scale_generator import generate_scale_with_genetic_algorithm, num_generations
from beat_craft_sdk.craft_strategy import CraftStrategy
from evaluation.beat_craft_evaluation import plot_fitness_over_generations, plot_pitch_diversity_over_generation, \
    plot_ga_evaluation_into_json


class CraftingBackingTrack(CraftStrategy):

    def __init__(self):
        print(f"init generate in crafing_with_backingtrack.py")
        self.pitch_fitness_per_generations = []
        self.pitch_diversity_per_generation = []

    def generate(self):
        print(f"inside generate in crafing_with_backingtrack.py")
        bt = BackTracking()
        combs = bt.generate_combinations()
        flattened_phrase= random.choice(combs)
        series_scale, self.pitch_fitness_per_generations, self.pitch_diversity_per_generation = generate_scale_with_genetic_algorithm(len(flattened_phrase))
        paired_notes = list(zip(flattened_phrase, series_scale))
        print(f"paired notes in crafting genetic {paired_notes}")
        return paired_notes

    def evaluate(self):
        print(f"best_fitness_per_generations {self.pitch_fitness_per_generations}")
        plot_fitness_over_generations(num_generations, self.pitch_fitness_per_generations, "../.output")
        plot_pitch_diversity_over_generation(num_generations, self.pitch_diversity_per_generation, "../.output")
        plot_ga_evaluation_into_json(self.pitch_diversity_per_generation,self.pitch_fitness_per_generations,"../.output")