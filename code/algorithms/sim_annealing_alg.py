from code.algorithms.random_alg import run_random_amount_of_trajects
from code.algorithms.hill_climbing_alg import evaluate_solution
from code.algorithms.hill_climbing_alg import generate_random_solution
from code.algorithms.hill_climbing_alg import get_neighbors
from code.algorithms.hill_climbing_alg import run_random_traject

from code.classes.rail_NL import Rail_NL

import random
import math

def simulated_annealing(area, amount_trajects, amount_stations, max_time, initial_temperature):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area)
    area.reset()

    temperature = initial_temperature

    iteraties = 0
    while iteraties < 2000:
        iteraties += 1
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        neighbor = random.choice(neighbors)

        neighbor_score = evaluate_solution(neighbor, area)
        delta_score = neighbor_score - current_score
        if delta_score > 0 or (2**(delta_score/1000))/temperature < random.random():
            current_solution = neighbor
            current_score = neighbor_score

        temperature = initial_temperature - (initial_temperature/2000) * iteraties
        area.reset()

    for i in range(0, amount_trajects):
        stations_str = ', '.join(current_solution[i].traject_connections)
        print(f"train_{i + 1},\"[{stations_str}]\"")

    return current_solution, current_score