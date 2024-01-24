from code.algorithms.random_alg import run_random_amount_of_trajects
from code.algorithms.hill_climbing_alg import evaluate_solution
from code.algorithms.hill_climbing_alg import generate_random_solution
from code.algorithms.hill_climbing_alg import run_random_traject

from code.classes.rail_NL import Rail_NL
from code.algorithms.greedy_best_comb import run_trajects
from code.algorithms.remove_unnecessary import removing_lines

import random
import math
import numpy as np
import matplotlib.pyplot as plt
import copy

def simulated_annealing(area, amount_trajects, amount_stations, max_time, initial_temperature):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area)[0]
    area.reset()
    temperature = initial_temperature

    total_iteraties = 2000
    iteraties = 0
    scores = []
    temperature_list = []
    p_acceptlist = []
    while iteraties < total_iteraties:
        scores.append(current_score)
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        neighbor = random.choice(neighbors)

        tracks = []
        for track in neighbor:
            tracks.append(track.traject_connections)

        area.reset()
        neighbor_score = run_trajects(area, amount_trajects, amount_stations, max_time, tracks, False)
        area.reset()
        delta_score = current_score - neighbor_score

        if delta_score/temperature > 100:
            p_accept = 0
        elif delta_score < 0:
            p_accept = 1
        else:
            p_accept = math.exp(1)**(-delta_score/temperature)
            p_acceptlist.append(p_accept)

        if delta_score < 0 or p_accept > random.random():
            current_solution = neighbor
            current_score = neighbor_score

        temperature = initial_temperature - (initial_temperature/total_iteraties) * iteraties
        temperature_list.append(temperature)
        iteraties += 1

    finaltracks = []
    for track in current_solution:
        finaltracks.append(track.traject_connections)
    area.reset()
    trajects = removing_lines(area, amount_trajects, amount_stations, max_time, finaltracks)
    area.reset()
    current_score = run_trajects(area, len(trajects), amount_stations, max_time, trajects, False)
    count = 1
    for a in trajects:
        stations_str = ', '.join(a)
        print(f"train_{count},\"[{stations_str}]\"")
        count += 1
    return trajects, current_score, scores, temperature_list, p_acceptlist

def get_neighbors(solution, area, amount_trajects, amount_stations, max_time):
    neighbors = []
    for i in range(amount_trajects):
        neighbor = solution[:]
        neighbor[i] = run_random_traject(area, amount_stations, max_time)[2]
        neighbors.append(neighbor)
    return neighbors