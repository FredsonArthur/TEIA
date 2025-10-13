'''
Script to analyze the impact of different parameters on a Genetic Algorithm for TSP.

Atividade 7 - Análise de Parâmetros do AG
'''

import numpy as np
import requests
import warnings
import random
import time
from typing import List, Dict, Any, Tuple

# --- 1. TSP Problem Definition (Reused from previous activity) ---

URL_TSP_DATA = "https://gist.github.com/rodrigoclira/1cc3dfc603740decb4269096aa7ac122/raw/"

def load_distance_matrix(url: str) -> np.ndarray:
    """Loads the distance matrix from a JSON endpoint."""
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        matrix_list = response.json()
        print(f"TSP data loaded successfully: {len(matrix_list)} cities.")
        return np.array(matrix_list)
    except Exception as e:
        print(f"Error loading TSP data: {e}. Using fallback 5-city matrix.")
        fallback_matrix = np.array([
            [0, 20, 42, 35, 10],
            [20, 0, 30, 34, 25],
            [42, 30, 0, 12, 42],
            [35, 34, 12, 0, 24],
            [10, 25, 42, 24, 0]
        ])
        print(f"Fallback matrix shape: {fallback_matrix.shape}")
        return fallback_matrix

DISTANCE_MATRIX = load_distance_matrix(URL_TSP_DATA)
NUM_CITIES = DISTANCE_MATRIX.shape[0]

# --- 2. Genetic Algorithm for TSP ---

Individual = List[int]
Population = List[Individual]

def create_individual() -> Individual:
    """Creates a random individual (a permutation of cities)."""
    cities = list(range(1, NUM_CITIES))
    random.shuffle(cities)
    return cities

def calculate_fitness(individual: Individual) -> float:
    """Calculates the total distance of the route. Lower is better."""
    route = [0] + individual + [0]
    total_distance = sum(DISTANCE_MATRIX[route[i], route[i+1]] for i in range(len(route) - 1))
    return total_distance

def tournament_selection(population: Population, fitnesses: List[float], k: int) -> Individual:
    """Selects an individual using tournament selection of size k."""
    tournament_indices = random.sample(range(len(population)), k)
    winner_index = min(tournament_indices, key=lambda i: fitnesses[i]) # Minimize distance
    return population[winner_index]

def ordered_crossover(parent1: Individual, parent2: Individual) -> Tuple[Individual, Individual]:
    """Performs Ordered Crossover (OX)."""
    size = len(parent1)
    child1, child2 = [-1]*size, [-1]*size

    start, end = sorted(random.sample(range(size), 2))

    # Copy the segment from parents to children
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # Fill the rest
    def fill_child(child, parent):
        # Get the genes from the parent that are not already in the child
        parent_genes = [gene for gene in parent if gene not in child[start:end]]
        
        # Fill the child with remaining genes in order
        child_idx = 0
        for gene in parent_genes:
            # Find next empty position
            while child_idx < size and child[child_idx] != -1:
                child_idx += 1
            if child_idx < size:
                child[child_idx] = gene
        
        return child

    child1 = fill_child(child1, parent2)
    child2 = fill_child(child2, parent1)
    
    return child1, child2

def swap_mutation(individual: Individual, mutation_rate: float) -> Individual:
    """Performs swap mutation."""
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual

def run_ga(params: Dict[str, Any]):
    """Runs the GA with a given set of parameters."""
    pop_size = params['pop_size']
    generations = params.get('generations', 100) # Default generations
    mutation_rate = params['mutation_rate']
    tournament_size = params['tournament_size']
    elite_perc = params['elite_perc']

    population = [create_individual() for _ in range(pop_size)]
    elite_size = int(pop_size * elite_perc)

    convergence = []
    diversity = []

    for _ in range(generations):
        fitnesses = [calculate_fitness(ind) for ind in population]

        # Data for analysis
        convergence.append(min(fitnesses))
        diversity.append(len(set(tuple(ind) for ind in population)))

        new_population = []
        if elite_size > 0:
            elite_indices = np.argsort(fitnesses)[:elite_size]
            new_population.extend([population[i] for i in elite_indices])

        while len(new_population) < pop_size:
            parent1 = tournament_selection(population, fitnesses, tournament_size)
            parent2 = tournament_selection(population, fitnesses, tournament_size)
            
            child1, child2 = ordered_crossover(parent1, parent2)
            
            new_population.append(swap_mutation(child1, mutation_rate))
            if len(new_population) < pop_size:
                new_population.append(swap_mutation(child2, mutation_rate))
        
        population = new_population

    final_fitnesses = [calculate_fitness(ind) for ind in population]
    best_fitness = min(final_fitnesses)
    
    return best_fitness, convergence, diversity

# --- 3. Experiment Execution ---

def run_experiments():
    """Main function to run all experiments."""
    
    num_runs = 30
    results = {}

    # --- Experiment 1: Population Size ---
    print("Running Experiment 1: Population Size")
    exp1_params = [20, 50, 100]
    results['pop_size'] = {}
    for size in exp1_params:
        print(f"  Testing size: {size}...")
        key = f"pop_{size}"
        results['pop_size'][key] = []
        for i in range(num_runs):
            print(f"    Run {i+1}/{num_runs}")
            params = {
                'pop_size': size,
                'mutation_rate': 0.05, # Fixed
                'tournament_size': 3,    # Fixed
                'elite_perc': 0.05,      # Fixed
                'generations': 200
            }
            start_time = time.time()
            fitness, convergence, diversity = run_ga(params)
            exec_time = time.time() - start_time
            results['pop_size'][key].append({
                'fitness': fitness,
                'convergence': convergence,
                'diversity': diversity,
                'time': exec_time
            })

    # --- Experiment 2: Mutation Rate ---
    print("\nRunning Experiment 2: Mutation Rate")
    exp2_params = [0.01, 0.05, 0.10, 0.20]  # 1%, 5%, 10%, 20%
    results['mutation_rate'] = {}
    for rate in exp2_params:
        print(f"  Testing rate: {rate*100:.0f}%...")
        key = f"mut_{int(rate*100)}"
        results['mutation_rate'][key] = []
        for i in range(num_runs):
            print(f"    Run {i+1}/{num_runs}")
            params = {
                'pop_size': 50,          # Fixed
                'mutation_rate': rate,
                'tournament_size': 3,    # Fixed
                'elite_perc': 0.05,      # Fixed
                'generations': 200
            }
            start_time = time.time()
            fitness, convergence, diversity = run_ga(params)
            exec_time = time.time() - start_time
            results['mutation_rate'][key].append({
                'fitness': fitness,
                'convergence': convergence,
                'diversity': diversity,
                'time': exec_time
            })

    # --- Experiment 3: Tournament Size ---
    print("\nRunning Experiment 3: Tournament Size")
    exp3_params = [2, 3, 5, 7]
    results['tournament_size'] = {}
    for size in exp3_params:
        print(f"  Testing size: {size}...")
        key = f"tour_{size}"
        results['tournament_size'][key] = []
        for i in range(num_runs):
            print(f"    Run {i+1}/{num_runs}")
            params = {
                'pop_size': 50,          # Fixed
                'mutation_rate': 0.05,   # Fixed
                'tournament_size': size,
                'elite_perc': 0.05,      # Fixed
                'generations': 200
            }
            start_time = time.time()
            fitness, convergence, diversity = run_ga(params)
            exec_time = time.time() - start_time
            results['tournament_size'][key].append({
                'fitness': fitness,
                'convergence': convergence,
                'diversity': diversity,
                'time': exec_time
            })

    # --- Experiment 4: Elitism ---
    print("\nRunning Experiment 4: Elitism")
    exp4_params = [0.0, 0.01, 0.05, 0.10]  # 0%, 1%, 5%, 10%
    results['elitism'] = {}
    for perc in exp4_params:
        print(f"  Testing percentage: {perc*100:.0f}%...")
        key = f"elit_{int(perc*100)}"
        results['elitism'][key] = []
        for i in range(num_runs):
            print(f"    Run {i+1}/{num_runs}")
            params = {
                'pop_size': 50,          # Fixed
                'mutation_rate': 0.05,   # Fixed
                'tournament_size': 3,    # Fixed
                'elite_perc': perc,
                'generations': 200
            }
            start_time = time.time()
            fitness, convergence, diversity = run_ga(params)
            exec_time = time.time() - start_time
            results['elitism'][key].append({
                'fitness': fitness,
                'convergence': convergence,
                'diversity': diversity,
                'time': exec_time
            })

    # --- 4. Analysis and Visualization ---
    print("\n--- Analysis ---")
    
    # Calculate mean/std dev for final fitness and time for each experiment
    analyze_results(results)
    
    # Generate plots
    generate_plots(results)
    
    # Save results to file
    save_results_to_file(results)
    
    # Example of accessing results for one configuration
    pop_20_results = results['pop_size']['pop_20']
    avg_fitness_pop_20 = np.mean([r['fitness'] for r in pop_20_results])
    print(f"\nExample: Avg fitness for Pop Size 20: {avg_fitness_pop_20:.2f}")

def analyze_results(results):
    """Analyze and print summary statistics for all experiments."""
    # Experiment 1: Population Size
    print("\nExperiment 1: Population Size")
    for key, data in results['pop_size'].items():
        fitnesses = [r['fitness'] for r in data]
        times = [r['time'] for r in data]
        print(f"  {key}: Fitness Mean={np.mean(fitnesses):.2f}, Std={np.std(fitnesses):.2f}, Time Mean={np.mean(times):.4f}s")
    
    # Experiment 2: Mutation Rate
    print("\nExperiment 2: Mutation Rate")
    for key, data in results['mutation_rate'].items():
        fitnesses = [r['fitness'] for r in data]
        times = [r['time'] for r in data]
        print(f"  {key}%: Fitness Mean={np.mean(fitnesses):.2f}, Std={np.std(fitnesses):.2f}, Time Mean={np.mean(times):.4f}s")
    
    # Experiment 3: Tournament Size
    print("\nExperiment 3: Tournament Size")
    for key, data in results['tournament_size'].items():
        fitnesses = [r['fitness'] for r in data]
        times = [r['time'] for r in data]
        print(f"  {key}: Fitness Mean={np.mean(fitnesses):.2f}, Std={np.std(fitnesses):.2f}, Time Mean={np.mean(times):.4f}s")
    
    # Experiment 4: Elitism
    print("\nExperiment 4: Elitism")
    for key, data in results['elitism'].items():
        fitnesses = [r['fitness'] for r in data]
        times = [r['time'] for r in data]
        print(f"  {key}%: Fitness Mean={np.mean(fitnesses):.2f}, Std={np.std(fitnesses):.2f}, Time Mean={np.mean(times):.4f}s")

def generate_plots(results):
    """Generate convergence plots and boxplots for all experiments."""
    try:
        import matplotlib.pyplot as plt
        
        # Create figures
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        
        # Experiment 1: Population Size - Convergence
        ax = axes[0, 0]
        for key, data in results['pop_size'].items():
            # Average convergence across runs
            avg_convergence = np.mean([r['convergence'] for r in data], axis=0)
            ax.plot(avg_convergence, label=key)
        ax.set_title('Experiment 1: Population Size - Convergence')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Best Fitness')
        ax.legend()
        
        # Experiment 1: Population Size - Boxplot
        ax = axes[1, 0]
        fitness_data = []
        labels = []
        for key, data in results['pop_size'].items():
            fitness_data.append([r['fitness'] for r in data])
            labels.append(key)
        ax.boxplot(fitness_data, labels=labels)
        ax.set_title('Experiment 1: Population Size - Fitness Boxplot')
        ax.set_ylabel('Fitness')
        
        # Experiment 2: Mutation Rate - Convergence
        ax = axes[0, 1]
        for key, data in results['mutation_rate'].items():
            # Average convergence across runs
            avg_convergence = np.mean([r['convergence'] for r in data], axis=0)
            ax.plot(avg_convergence, label=key)
        ax.set_title('Experiment 2: Mutation Rate - Convergence')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Best Fitness')
        ax.legend()
        
        # Experiment 2: Mutation Rate - Boxplot
        ax = axes[1, 1]
        fitness_data = []
        labels = []
        for key, data in results['mutation_rate'].items():
            fitness_data.append([r['fitness'] for r in data])
            labels.append(key)
        ax.boxplot(fitness_data, labels=labels)
        ax.set_title('Experiment 2: Mutation Rate - Fitness Boxplot')
        ax.set_ylabel('Fitness')
        
        # Experiment 3: Tournament Size - Convergence
        ax = axes[0, 2]
        for key, data in results['tournament_size'].items():
            # Average convergence across runs
            avg_convergence = np.mean([r['convergence'] for r in data], axis=0)
            ax.plot(avg_convergence, label=key)
        ax.set_title('Experiment 3: Tournament Size - Convergence')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Best Fitness')
        ax.legend()
        
        # Experiment 3: Tournament Size - Boxplot
        ax = axes[1, 2]
        fitness_data = []
        labels = []
        for key, data in results['tournament_size'].items():
            fitness_data.append([r['fitness'] for r in data])
            labels.append(key)
        ax.boxplot(fitness_data, labels=labels)
        ax.set_title('Experiment 3: Tournament Size - Fitness Boxplot')
        ax.set_ylabel('Fitness')
        
        # Experiment 4: Elitism - Convergence
        ax = axes[0, 3]
        for key, data in results['elitism'].items():
            # Average convergence across runs
            avg_convergence = np.mean([r['convergence'] for r in data], axis=0)
            ax.plot(avg_convergence, label=key)
        ax.set_title('Experiment 4: Elitism - Convergence')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Best Fitness')
        ax.legend()
        
        # Experiment 4: Elitism - Boxplot
        ax = axes[1, 3]
        fitness_data = []
        labels = []
        for key, data in results['elitism'].items():
            fitness_data.append([r['fitness'] for r in data])
            labels.append(key)
        ax.boxplot(fitness_data, labels=labels)
        ax.set_title('Experiment 4: Elitism - Fitness Boxplot')
        ax.set_ylabel('Fitness')
        
        plt.tight_layout()
        plt.savefig('experiment_results.png')
        plt.show()
        
        # Additional plot for diversity in Experiment 3
        plt.figure(figsize=(10, 6))
        for key, data in results['tournament_size'].items():
            # Average diversity across runs
            avg_diversity = np.mean([r['diversity'] for r in data], axis=0)
            plt.plot(avg_diversity, label=key)
        plt.title('Experiment 3: Tournament Size - Diversity')
        plt.xlabel('Generation')
        plt.ylabel('Unique Individuals')
        plt.legend()
        plt.savefig('diversity_plot.png')
        plt.show()
        
        print("\nPlots saved as 'experiment_results.png' and 'diversity_plot.png'")
        
    except ImportError:
        print("\nMatplotlib not available. Skipping plot generation.")

def save_results_to_file(results):
    """Save results to a text file for further analysis."""
    with open('experiment_results.txt', 'w') as f:
        f.write("TSP Genetic Algorithm - Parameter Analysis Results\n")
        f.write("=" * 50 + "\n\n")
        
        # Experiment 1: Population Size
        f.write("Experiment 1: Population Size\n")
        f.write("-" * 30 + "\n")
        for key, data in results['pop_size'].items():
            fitnesses = [r['fitness'] for r in data]
            times = [r['time'] for r in data]
            f.write(f"{key}: Fitness Mean={np.mean(fitnesses):.2f}, Std={np.std(fitnesses):.2f}, Time Mean={np.mean(times):.4f}s\n")
        f.write("\n")
        
        # Experiment 2: Mutation Rate
        f.write("Experiment 2: Mutation Rate\n")
        f.write("-" * 30 + "\n")
        for key, data in results['mutation_rate'].items():
            fitnesses = [r['fitness'] for r in data]
            times = [r['time'] for r in data]
            f.write(f"{key}%: Fitness Mean={np.mean(fitnesses):.2f}, Std={np.std(fitnesses):.2f}, Time Mean={np.mean(times):.4f}s\n")
        f.write("\n")
        
        # Experiment 3: Tournament Size
        f.write("Experiment 3: Tournament Size\n")
        f.write("-" * 30 + "\n")
        for key, data in results['tournament_size'].items():
            fitnesses = [r['fitness'] for r in data]
            times = [r['time'] for r in data]
            f.write(f"{key}: Fitness Mean={np.mean(fitnesses):.2f}, Std={np.std(fitnesses):.2f}, Time Mean={np.mean(times):.4f}s\n")
        f.write("\n")
        
        # Experiment 4: Elitism
        f.write("Experiment 4: Elitism\n")
        f.write("-" * 30 + "\n")
        for key, data in results['elitism'].items():
            fitnesses = [r['fitness'] for r in data]
            times = [r['time'] for r in data]
            f.write(f"{key}%: Fitness Mean={np.mean(fitnesses):.2f}, Std={np.std(fitnesses):.2f}, Time Mean={np.mean(times):.4f}s\n")
        f.write("\n")

if __name__ == "__main__":
    run_experiments()