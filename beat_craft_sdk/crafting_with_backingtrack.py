import random

from beat_craft_sdk.algorithms.phrase_generator_backtracking import BackTracking
from beat_craft_sdk.algorithms.scale_generator import generate_scale_with_genetic_algorithm, num_generations
from beat_craft_sdk.craft_strategy import CraftStrategy
from beat_craft_sdk.evaluation.beat_craft_evaluation import plot_fitness_over_generations, plot_pitch_diversity_over_generation, \
    plot_ga_evaluation_into_json


class CraftingBackingTrack(CraftStrategy):

    def __init__(self):
        self.pitch_fitness_per_generations = []
        self.pitch_diversity_per_generation = []

    def generate(self,output_dir,file_name, scale):
        bt = BackTracking()
        combs = bt.generate_combinations()
        flattened_phrase= random.choice(combs)
        series_scale, self.pitch_fitness_per_generations, self.pitch_diversity_per_generation = generate_scale_with_genetic_algorithm(len(flattened_phrase),scale)
        paired_notes = list(zip(flattened_phrase, series_scale))
        return paired_notes

    def evaluate(self,output_dir,file_name):
        plot_fitness_over_generations(num_generations, self.pitch_fitness_per_generations,output_dir,file_name)
        plot_pitch_diversity_over_generation(num_generations, self.pitch_diversity_per_generation,output_dir,file_name)
        plot_ga_evaluation_into_json(self.pitch_diversity_per_generation,self.pitch_fitness_per_generations,output_dir,file_name)