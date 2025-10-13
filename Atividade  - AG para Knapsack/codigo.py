
'''
Genetic Algorithm implementation for the 0/1 Knapsack Problem.
'''
import random
from typing import List, Tuple

# --- Problem Data (PLACEHOLDERS) ---
# TODO: Replace with data from Atividade 1
WEIGHTS: List[int] = [random.randint(1, 20) for _ in range(20)]
VALUES: List[int] = [random.randint(10, 100) for _ in range(20)]
KNAPSACK_CAPACITY: int = int(sum(WEIGHTS) * 0.5)

# --- GA Parameters ---
POPULATION_SIZE: int = 50
GENERATIONS: int = 500
CROSSOVER_RATE: float = 0.8
MUTATION_RATE: float = 0.02
TOURNAMENT_SIZE: int = 3
ELITE_SIZE: int = 2

Individual = List[int]
Population = List[Individual]

# --- Genetic Algorithm Functions ---
def create_individual() -> Individual:
    """Creates a random individual solution."""
    return [random.randint(0, 1) for _ in range(len(WEIGHTS))]

def create_initial_population(size: int) -> Population:
    """Creates an initial population of random individuals."""
    return [create_individual() for _ in range(size)]

def calculate_fitness(individual: Individual) -> int:
    """Calculates the fitness of an individual."""
    total_weight = sum(w * gene for w, gene in zip(WEIGHTS, individual))
    total_value = sum(v * gene for v, gene in zip(VALUES, individual))

    # Penalize solutions that exceed capacity
    if total_weight > KNAPSACK_CAPACITY:
        return 0
    return total_value

def tournament_selection(population: Population, fitnesses: List[int]) -> Individual:
    """Selects an individual from the population using tournament selection."""
    tournament_contenders_indices = random.sample(range(len(population)), TOURNAMENT_SIZE)
    
    winner_index = max(tournament_contenders_indices, key=lambda i: fitnesses[i])
    
    return population[winner_index]

# --- Crossover Functions ---
def crossover_one_point(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1[:], parent2[:]

def crossover_two_points(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    if random.random() < CROSSOVER_RATE:
        p1, p2 = sorted(random.sample(range(1, len(parent1)), 2))
        child1 = parent1[:p1] + parent2[p1:p2] + parent1[p2:]
        child2 = parent2[:p1] + parent1[p1:p2] + parent2[p2:]
        return child1, child2
    return parent1[:], parent2[:]

def crossover_uniform(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    if random.random() < CROSSOVER_RATE:
        child1, child2 = [], []
        for i in range(len(parent1)):
            if random.random() < 0.5:
                child1.append(parent1[i])
                child2.append(parent2[i])
            else:
                child1.append(parent2[i])
                child2.append(parent1[i])
        return child1, child2
    return parent1[:], parent2[:]

# --- Mutation Function ---
def bit_flip_mutation(individual: Individual) -> Individual:
    """Applies bit-flip mutation to an individual."""
    for i in range(len(individual)):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]  # Flip the bit
    return individual

# --- Main GA Loop ---
def run_ga(crossover_type: str):
    """Runs the complete Genetic Algorithm for a given crossover type."""
    population = create_initial_population(POPULATION_SIZE)
    best_fitness_per_generation = []

    crossover_functions = {
        "one_point": crossover_one_point,
        "two_points": crossover_two_points,
        "uniform": crossover_uniform
    }
    crossover_func = crossover_functions[crossover_type]

    for _ in range(GENERATIONS):
        fitnesses = [calculate_fitness(ind) for ind in population]

        # Elitism: preserve the best individuals
        elite_indices = sorted(range(len(fitnesses)), key=lambda i: fitnesses[i], reverse=True)[:ELITE_SIZE]
        new_population = [population[i] for i in elite_indices]
        
        best_fitness_per_generation.append(max(fitnesses))

        # Generate the new population
        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            
            child1, child2 = crossover_func(parent1, parent2)
            
            new_population.append(bit_flip_mutation(child1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(bit_flip_mutation(child2))
        
        population = new_population

    final_fitnesses = [calculate_fitness(ind) for ind in population]
    best_solution_index = max(range(len(final_fitnesses)), key=lambda i: final_fitnesses[i])
    
    best_solution = population[best_solution_index]
    best_fitness = final_fitnesses[best_solution_index]
    
    return best_solution, best_fitness, best_fitness_per_generation

# --- Execution and Analysis ---
if __name__ == "__main__":
    # This section will be implemented to run the 30 trials,
    # calculate statistics, and generate the plots.
    
    print("Running GA for the Knapsack Problem...")
    
    # Example of how to run a single instance
    crossover_type = "one_point"  # or "two_points", "uniform"
    solution, fitness, convergence = run_ga(crossover_type)
    
    print(f"\nResults for Crossover: {crossover_type}")
    print(f"Best solution found: {solution}")
    print(f"Best fitness: {fitness}")

    # TODO:
    # 1. Loop for 30 executions for each crossover type.
    # 2. Store the results (final fitness of each run).
    # 3. Calculate mean and standard deviation.
    # 4. Generate convergence plot (average of 30 runs).
    # 5. Generate comparative boxplot.
    pass
