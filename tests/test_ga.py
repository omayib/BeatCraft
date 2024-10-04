import unittest

from algorithms.backtracking import BackTracking
from algorithms.note_duration_generator import generate_note_duration_with_genetic_algorithm


class TestBeatCraftSdk(unittest.TestCase):
    def test_generate_population(self):
        series_duration=generate_note_duration_with_genetic_algorithm()
        print(series_duration)

    def test_backingtrack(self):
        backingtrack = BackTracking()
        combs = backingtrack.generate_combinations()
        for co in combs:
            print(f" sum {sum(co)} in {co}")