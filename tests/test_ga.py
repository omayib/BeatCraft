import unittest

from beat_craft_sdk.algorithms.phrase_generator_backtracking import BackTracking
from beat_craft_sdk.algorithms.phrase_generator_genetic import generate_phrase_with_genetic_algorithm
from beat_craft_sdk.algorithms.scale_generator import generate_scale_with_genetic_algorithm


class TestBeatCraftSdk(unittest.TestCase):
    def test_generate_population(self):
        phrase = generate_phrase_with_genetic_algorithm()
        flattened_phrase = [item for sublist in phrase for item in
                            (sublist if isinstance(sublist, list) else [sublist])]
        series_scale, self.pitch_fitness_per_generations, self.pitch_diversity_per_generation = generate_scale_with_genetic_algorithm(
            len(flattened_phrase), [60, 62, 63, 65, 67, 68, 70])
        paired_notes = list(zip(flattened_phrase, series_scale))
        pass

    def test_backingtrack(self):
        backingtrack = BackTracking()
        combs = backingtrack.generate_combinations()
        for co in combs:
            print(f" sum {sum(co)} in {co}")