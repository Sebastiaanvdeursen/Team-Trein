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


def simulated_annealing(area, amount_trajects, amount_stations, max_time, initial_temperature):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area, True)
    temperature = initial_temperature

    iteraties = 0
    while iteraties < 2000:
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        neighbor = random.choice(neighbors)

        neighbor_score = evaluate_solution(neighbor, area, False)

        delta_score = current_score - neighbor_score

        if delta_score/temperature > 100:
            p_accept = 0
        elif delta_score/temperature < 0:
            p_accept = 1
        else:
            p_accept = math.exp(1)**(-delta_score/temperature)

        if delta_score < 0 or p_accept < random.random():
            current_solution = neighbor
            current_score = neighbor_score
            area.reset()

        temperature = initial_temperature - (initial_temperature/2000) * iteraties
        iteraties += 1

    for i in range(0, amount_trajects):
        stations_str = ', '.join(current_solution[i].traject_connections)
        print(f"train_{i + 1},\"[{stations_str}]\"")

    return current_solution, current_score