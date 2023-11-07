import random
import math

# Define the distance matrix between cities. This example assumes a complete graph.
# You can replace this with your own data.
distance_matrix = [
    [0, 29, 20, 21],
    [29, 0, 15, 17],
    [20, 15, 0, 28],
    [21, 17, 28, 0]
]

# Parameters for simulated annealing
initial_temperature = 1000
cooling_rate = 0.995
iterations_per_temperature = 1000

# Function to calculate the total tour distance
def tour_distance(tour):
    total_distance = 0
    for i in range(len(tour)):
        total_distance += distance_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return total_distance

# Simulated annealing function
def simulated_annealing(tour, temperature, cooling_rate, iterations_per_temp):
    current_tour = tour
    best_tour = tour
    current_distance = tour_distance(current_tour)
    best_distance = current_distance

    while temperature > 1e-3:
        for _ in range(iterations_per_temp):
            # Generate a neighboring solution by swapping two random cities
            i, j = random.sample(range(len(tour)), 2)
            neighbor_tour = current_tour[:]
            neighbor_tour[i], neighbor_tour[j] = neighbor_tour[j], neighbor_tour[i]
            neighbor_distance = tour_distance(neighbor_tour)

            # Decide whether to accept the neighbor solution
            delta = neighbor_distance - current_distance
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_tour = neighbor_tour
                current_distance = neighbor_distance

                # Update the best solution if necessary
                if current_distance < best_distance:
                    best_tour = current_tour
                    best_distance = current_distance

        # Cool the temperature
        temperature *= cooling_rate

    return best_tour, best_distance

# Initialize a random tour as a starting point
num_cities = len(distance_matrix)
initial_tour = list(range(num_cities))
random.shuffle(initial_tour)

# Call the simulated annealing function
best_tour, best_distance = simulated_annealing(initial_tour, initial_temperature, cooling_rate, iterations_per_temperature)

# Print the results
print("Best Tour:", best_tour)
print("Best Distance:", best_distance)
