from code.algorithms.random_alg import run_random_amount_of_trajects
from code.algorithms.hill_climbing_alg import evaluate_solution
from code.algorithms.hill_climbing_alg import generate_random_solution
from code.algorithms.hill_climbing_alg import get_neighbors
from code.algorithms.hill_climbing_alg import run_random_traject

from code.classes.rail_NL import Rail_NL

import random
import math
import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 2000, 0, 8000])

def simulated_annealing(area, amount_trajects, amount_stations, max_time, initial_temperature):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area, True)

    temperature = initial_temperature

    iteraties = 0
    while iteraties < 2000:
        iteraties += 1
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        neighbor = random.choice(neighbors)

        neighbor_score = evaluate_solution(neighbor, area, True)
        delta_score = current_score - neighbor_score
        print(current_score)
        print(delta_score)
        print(math.exp(1)**(-delta_score/temperature))
        print(temperature)
        if delta_score < 0 or math.exp(1)**(-delta_score/temperature) < random.random():
            current_solution = neighbor
            current_score = neighbor_score

        print(current_score)
        temperature = initial_temperature - (initial_temperature/2000) * iteraties

        plt.scatter(iteraties, current_score)
        plt.pause(0.05)
        
    plt.show()

    for i in range(0, amount_trajects):
        stations_str = ', '.join(current_solution[i].traject_connections)
        print(f"train_{i + 1},\"[{stations_str}]\"")

    return current_solution, current_score