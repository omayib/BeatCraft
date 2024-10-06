

class BackTracking:
    def __init__(self, max_sum=4, max_items=16):
        self.valid_combinations = []
        # Define the note durations
        self.note_durations = {
            "whole": 4,
            "half": 2,
            "quarter": 1,
            "eighth": 0.5,
            "sixteenth": 0.25
        }

        # Maximum sum and maximum number of items
        self.max_sum = max_sum
        self.max_items = max_items

    # Backtracking function to generate all valid combinations
    def find_combinations(self, current_combo, current_sum, note_count):
        # If the current sum exceeds the maximum or note count exceeds the limit, return
        if current_sum > self.max_sum  or note_count > self.max_items:
            return

        # If the current sum is exactly equal to max_sum, store the combination
        if current_sum == self.max_sum:
            # print(f"current sum {current_sum} - note count {note_count}")
            self.valid_combinations.append(current_combo)
            return

        # Recursively add more notes and explore further combinations
        for note, duration in self.note_durations.items():
            self.find_combinations(current_combo + [duration], current_sum + duration, note_count + 1)

    def generate_combinations(self):
        self.find_combinations(current_combo=[], current_sum=0, note_count=0)
        return self.valid_combinations

# Usage example
# generator = BackTracking()
# generator.generate_combinations()
