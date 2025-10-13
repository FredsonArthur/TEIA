'''
Unit tests for the TSP Genetic Algorithm components.
'''

import unittest
import numpy as np
import codigo # Import the script we want to test

class TestGeneticAlgorithmComponents(unittest.TestCase):

    def setUp(self):
        """Set up a fixed environment for each test."""
        # Mock the global DISTANCE_MATRIX with a predictable 3x3 matrix for testing
        # This avoids network calls and provides a stable test environment.
        self.test_matrix = np.array([
            [0, 10, 20],
            [10, 0, 30],
            [20, 30, 0]
        ])
        codigo.DISTANCE_MATRIX = self.test_matrix
        codigo.NUM_CITIES = 3

    def test_calculate_fitness(self):
        """Test that fitness (distance) is calculated correctly."""
        # For a 3-city problem, the individual is a permutation of [1, 2]
        individual = [1, 2] # Represents route 0 -> 1 -> 2 -> 0
        
        # Expected distance: (0->1) + (1->2) + (2->0)
        expected_distance = self.test_matrix[0, 1] + self.test_matrix[1, 2] + self.test_matrix[2, 0]
        # 10 + 30 + 20 = 60
        self.assertEqual(codigo.calculate_fitness(individual), expected_distance)

        individual_2 = [2, 1] # Represents route 0 -> 2 -> 1 -> 0
        # Expected distance: (0->2) + (2->1) + (1->0)
        expected_distance_2 = self.test_matrix[0, 2] + self.test_matrix[2, 1] + self.test_matrix[1, 0]
        # 20 + 30 + 10 = 60
        self.assertEqual(codigo.calculate_fitness(individual_2), expected_distance_2)

    def test_ordered_crossover(self):
        """Test the Ordered Crossover (OX) implementation."""
        # For a 5-city problem, individuals have length 4
        codigo.NUM_CITIES = 5
        parent1 = [1, 2, 3, 4]
        parent2 = [4, 3, 2, 1]

        # To make the test deterministic, we monkey-patch random.sample
        original_sample = codigo.random.sample
        codigo.random.sample = lambda population, k: [1, 3] # Force crossover points to be 1 and 3

        child1, child2 = codigo.ordered_crossover(parent1, parent2)

        # Restore the original random.sample function
        codigo.random.sample = original_sample

        # --- Manual verification of expected result ---
        # Parent 1: [1, 2, 3, 4]
        # Parent 2: [4, 3, 2, 1]
        # Crossover segment from index 1 to 3 (exclusive of 3): [2, 3]
        # Child 1 starts with [_, 2, 3, _]
        # Genes from parent2 in order: [4, 3, 2, 1]. 
        # Genes not in child1: [4, 1].
        # Fill child1: [4, 2, 3, 1]
        expected_child1 = [4, 2, 3, 1]
        self.assertEqual(child1, expected_child1)
        
        # Check if the child is a valid permutation
        self.assertEqual(sorted(child1), [1, 2, 3, 4])

    def test_swap_mutation(self):
        """Test the swap mutation."""
        individual = [1, 2, 3, 4]
        
        # With a 0% mutation rate, the individual should not change
        mutated = codigo.swap_mutation(individual[:], mutation_rate=0.0)
        self.assertEqual(individual, mutated)

        # With a 100% mutation rate, it's not guaranteed to change but very likely.
        # A better test is to ensure it remains a valid permutation.
        mutated = codigo.swap_mutation(individual[:], mutation_rate=1.0)
        self.assertEqual(sorted(individual), sorted(mutated))
        self.assertEqual(len(set(mutated)), len(individual)) # No duplicates

    def test_create_individual(self):
        """Smoke test to ensure create_individual returns a valid permutation."""
        codigo.NUM_CITIES = 10
        individual = codigo.create_individual()
        # Should have 9 cities (1 to 9)
        self.assertEqual(len(individual), 9)
        self.assertEqual(len(set(individual)), 9) # No duplicates
        self.assertEqual(sorted(individual), list(range(1, 10)))

    def test_load_matrix_fallback(self):
        """Test that the fallback matrix is loaded when the URL is invalid."""
        # Use a clearly invalid URL that will trigger an exception
        invalid_url = "http://127.0.0.1:1/invalid"
        matrix = codigo.load_distance_matrix(invalid_url)
        # The fallback matrix has 5 cities
        self.assertEqual(matrix.shape, (5, 5))
        # Check that it's actually the fallback matrix by checking a known value
        self.assertEqual(matrix[0, 1], 20)

if __name__ == '__main__':
    unittest.main()
