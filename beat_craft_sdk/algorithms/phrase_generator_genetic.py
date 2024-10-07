import random

# Define the possible note durations (in beats) in a 4/4 time signature
note_durations = {
    "whole": 4,
    "half": 2,
    "quarter": 1,
    "eighth": 0.5,
    "sixteenth": 0.25
}

# Total number of beats for 8 bars in 4/4 time signature
total_beats = 16
beats_per_bar = 4

# List of possible note durations
duration_values = list(note_durations.values())

# Function to create an initial population (randomly generate sequences of notes)
def create_individual():
    sequence = []
    total = 0
    while total < total_beats:
        note = random.choice(duration_values)
        if total + note <= total_beats:
            sequence.append(note)
            total += note
    return sequence


# Grouping function to ensure notes are grouped by bars of exactly 4 beats
def group_by_bar(note_sequence, bar_length=4):
    grouped_bars = []
    current_bar = []
    total_in_bar = 0

    for note in note_sequence:
        if total_in_bar + note <= bar_length:
            current_bar.append(note)
            total_in_bar += note
        else:
            # If adding the note exceeds 4 beats, start a new bar
            grouped_bars.append(current_bar)
            current_bar = [note]
            total_in_bar = note

        # If the bar sums exactly to 4, finalize the bar
        if total_in_bar == bar_length:
            grouped_bars.append(current_bar)
            current_bar = []
            total_in_bar = 0

    # If there are remaining notes, add them as the last bar
    if current_bar:
        grouped_bars.append(current_bar)

    return grouped_bars


# Fitness function: Penalize individuals that don't fit perfectly into 8 bars of 4 beats each
def fitness(individual):
    grouped_bars = group_by_bar(individual)

    # Check if the total number of bars is 8 and each bar sums exactly to 4 beats
    if len(grouped_bars) == 8 and all(sum(bar) == beats_per_bar for bar in grouped_bars):
        return 0  # Perfect fit
    else:
        # Penalize based on the deviation from the ideal
        return abs(total_beats - sum([sum(bar) for bar in grouped_bars])) + len(grouped_bars) - 8


# Selection function (select individuals based on fitness)
def selection(population):
    population.sort(key=lambda x: fitness(x))
    return population[:len(population) // 2]


# Crossover function (combine two individuals to create offspring)
def crossover(parent1, parent2):
    point = random.randint(1, min(len(parent1), len(parent2)) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2


# Mutation function (randomly change one note duration in the individual)
def mutation(individual):
    if random.random() < 0.1:  # 10% chance of mutation
        idx = random.randint(0, len(individual) - 1)
        individual[idx] = random.choice(duration_values)
    return individual


# Genetic Algorithm function
def generate_phrase_with_genetic_algorithm(generations=1000, population_size=50):
    population = [create_individual() for _ in range(population_size)]
    for generation in range(generations):
        # Selection
        population = selection(population)

        # Crossover
        offspring = []
        for i in range(0, len(population), 2):
            if i + 1 < len(population):
                child1, child2 = crossover(population[i], population[i + 1])
                offspring.append(child1)
                offspring.append(child2)

        # Mutation
        population = [mutation(ind) for ind in offspring]

        # Add new random individuals to maintain diversity
        while len(population) < population_size:
            population.append(create_individual())

        # Check if we found a perfect solution
        best_individual = min(population, key=lambda x: fitness(x))
        # print(f"fitness {best_individual} found in generation {generation + 1}")
        # print(f"fitness {fitness(best_individual)} found in generation {generation + 1}")
        if fitness(best_individual) == 0:
            print(f"Solution found in generation {generation + 1}")
            return best_individual

    # Return the best individual after all generations
    return min(population, key=lambda x: fitness(x))


# Running the genetic algorithm
# solution = genetic_algorithm()
# grouped_solution = group_by_bar(solution)
#
# # Output the generated solution
# print(f"Generated Note Durations for 8 Bars:{grouped_solution}")
# for bar in grouped_solution:
#     print(bar)
# print("Total Duration in each bar (should be exactly 4):", [sum(bar) for bar in grouped_solution])
