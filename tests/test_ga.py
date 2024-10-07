import unittest

from beat_craft_sdk.algorithms.phrase_generator_backtracking import BackTracking
from beat_craft_sdk.algorithms.phrase_generator_genetic import generate_phrase_with_genetic_algorithm


class TestBeatCraftSdk(unittest.TestCase):
    def test_generate_population(self):
        series_duration=generate_phrase_with_genetic_algorithm()
        print(series_duration)

    def test_backingtrack(self):
        backingtrack = BackTracking()
        combs = backingtrack.generate_combinations()
        for co in combs:
            print(f" sum {sum(co)} in {co}")