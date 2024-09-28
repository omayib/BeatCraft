import random

# Define the A minor scale using MIDI numbers
A_minor_scale_midi = [0, 57, 59, 60, 62, 64, 65, 67]  # A, B, C, D, E, F, G

# User input for series length and population size
series_length = 0
population_size = 100
num_generations = 500


# Fitness function (placeholder for now)
def fitness_function(sequence):
    # Add logic for evaluating the fitness of a sequence
    return random.random()  # For now, use random fitness


# Initialize population
def initialize_population(population_size, series_length):
    population = []
    for _ in range(population_size):
        sequence = [random.choice(A_minor_scale_midi) for _ in range(series_length)]
        population.append(sequence)
    return population


# Selection function: Selects the top sequences based on fitness
def selection(population, fitness_scores, num_parents):
    selected = [population[i] for i in
                sorted(range(len(fitness_scores)), key=lambda k: fitness_scores[k], reverse=True)[:num_parents]]
    return selected


# Crossover function: Combines two parent sequences
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 2)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2


# Mutation function: Mutates a sequence
def mutate(sequence, mutation_rate=0.1):
    for i in range(len(sequence)):
        if random.random() < mutation_rate:
            sequence[i] = random.choice(A_minor_scale_midi)
    return sequence


# Main genetic algorithm
def scale_genetic_algorithm(num_item=4):
    population = initialize_population(population_size, num_item)

    for generation in range(num_generations):
        # Evaluate fitness of each sequence
        fitness_scores = [fitness_function(sequence) for sequence in population]

        # Select parents based on fitness
        parents = selection(population, fitness_scores, population_size // 2)

        # Generate the next generation
        next_generation = []
        while len(next_generation) < population_size:
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = crossover(parent1, parent2)
            next_generation.append(mutate(child1))
            next_generation.append(mutate(child2))

        # Replace old population with new generation
        population = next_generation[:population_size]

        # Print progress
        print(f"Generation {generation + 1}: Best fitness: {max(fitness_scores)}")

    # Return the best sequence
    best_sequence = max(population, key=lambda seq: fitness_function(seq))
    return best_sequence


# Run the genetic algorithm and print the best sequence
# best_sequence = scale_genetic_algorithm()
# print("Best sequence found (MIDI numbers):", best_sequence)
