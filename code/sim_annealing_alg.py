from copy import deepcopy
from random_alg import run_random_amount_of_trajects
from rail_NL import Rail_NL
from hill_climbing_alg import evaluate_solution
from hill_climbing_alg import generate_random_solution
from hill_climbing_alg import get_neighbors
from hill_climbing_alg import run_random_traject
import random
import math

def simulated_annealing(area, amount_trajects, amount_stations, max_time, initial_temperature, cooling_rate):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area)
    area.reset()

    temperature = initial_temperature

    while temperature > 1:
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        neighbor = random.choice(neighbors)

        neighbor_score = evaluate_solution(neighbor, area)
        delta_score = neighbor_score - current_score

        if delta_score > 0 or random.uniform(0, 1) < math.exp(delta_score / temperature):
            current_solution = neighbor
            current_score = neighbor_score

        temperature *= 1 - cooling_rate
        area.reset()

    for i in range(0, amount_trajects):
        stations_str = ', '.join(current_solution[i].traject_connections)
        print(f"train_{i + 1},\"[{stations_str}]\"")

    return current_solution, current_score

