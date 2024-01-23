from code.algorithms.random_alg import run_random_amount_of_trajects
from code.algorithms.hill_climbing_alg import evaluate_solution
from code.algorithms.hill_climbing_alg import generate_random_solution
from code.algorithms.hill_climbing_alg import run_random_traject

from code.classes.rail_NL import Rail_NL

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import copy

def simulated_annealing(area, amount_trajects, amount_stations, max_time, initial_temperature):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area, False)[0]
    print(evaluate_solution(current_solution, area, False)[1])
    print(evaluate_solution(current_solution, area, False)[2])
    print(evaluate_solution(current_solution, area, False)[3])

    temperature = initial_temperature

    total_iteraties = 50
    iteraties = 0
    while iteraties < total_iteraties:
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        neighbor = random.choice(neighbors)

        neighbor_score = evaluate_solution(neighbor, area, False)[0]
        print(evaluate_solution(neighbor, area, False)[1])
        print(evaluate_solution(neighbor, area, False)[2])
        print(evaluate_solution(neighbor, area, False)[3])

        delta_score = current_score - neighbor_score

        if delta_score/temperature > 100:
            p_accept = 0
        elif delta_score < 0:
            p_accept = 1
        else:
            p_accept = math.exp(1)**(-delta_score/temperature)

        if delta_score < 0 or p_accept > random.random():
            current_solution = neighbor
            current_score = neighbor_score
            area.reset()

        temperature = initial_temperature - (initial_temperature/total_iteraties) * iteraties
        iteraties += 1

    for i in range(0, amount_trajects):
        stations_str = ', '.join(current_solution[i].traject_connections)
        print(f"train_{i + 1},\"[{stations_str}]\"")
    # print(evaluate_solution(current_solution, area, False)[1])
    return current_solution, current_score

def get_neighbors(solution, area, amount_trajects, amount_stations, max_time):
    neighbors = []
    for i in range(amount_trajects):
        neighbor = copy.deepcopy(solution)
        neighbor[i] = run_random_traject(area, amount_stations, max_time)[2]
        neighbors.append(neighbor)
    return neighbors