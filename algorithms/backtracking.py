# Define the note durations
note_durations = {
    "whole": 4,
    "half": 2,
    "quarter": 1,
    "eighth": 0.5,
    "sixteenth": 0.25
}

# Maximum sum and maximum number of items
max_sum = 4
max_items = 16


# Backtracking function to generate all valid combinations
def find_combinations(current_combo, current_sum, note_count):
    # If the current sum exceeds the maximum or note count exceeds the limit, return
    if current_sum > max_sum or note_count > max_items:
        return

    # If the current sum is exactly equal to max_sum, store the combination
    if current_sum == max_sum:
        valid_combinations.append(current_combo)
        return

    # Recursively add more notes and explore further combinations
    for note, duration in note_durations.items():
        find_combinations(current_combo + [duration], current_sum + duration, note_count + 1)


# Initialize a list to store valid combinations
valid_combinations = []

# Start backtracking with an empty combination, 0 current sum, and 0 note count
find_combinations([], 0, 0)

# Display the valid combinations
for combination in valid_combinations:
    print(combination)

# Optional: Print the total number of valid combinations found
print(f"Total valid combinations: {len(valid_combinations)}")
