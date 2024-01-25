from code.algorithms.random_alg import run_random_amount_of_trajects
from code.algorithms.hill_climbing_alg import evaluate_solution
from code.algorithms.hill_climbing_alg import generate_random_solution
from code.algorithms.hill_climbing_alg import run_random_traject
from code.algorithms.greedy_best_comb import run_trajects
from code.algorithms.remove_unnecessary import removing_lines

from code.classes.rail_NL import Rail_NL

import math
import random

def simulated_annealing(area, amount_trajects, amount_stations, max_time, initial_temperature):
    """
    Perform simulated annealing to optimize the railway schedule.
    Simulated annealing is an iterative algorithm that explores neighboring solutions
    to find an optimal solution based on an acceptance probability of worse neihgbors.

    Preconditions:
        - area is an instance of the Rail_NL class.
        - amount_trajects is a positive integer representing the maximum number of train trajects we can choose.
        - amount_stations is a positive integer representing the number of stations present in the current map.
        - max_time is a positive integer representing the maximum time duration for a train route.
        - initial_temperature is a positive float representing the initial temperature for the temperature function.

    Postconditions:
        - Returns a tuple containing:
            - trajects: List of optimized train routes.
            - current_score (int): Score of the optimized solution.
            - scores: List of scores during the optimization process.
            - temperature_list: List of temperatures during the optimization process.
            - p_acceptlist: List of acceptance probabilities during the optimization process.
        - Prints optimized train routes and their corresponding stations.
    """
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area)[0]
    area.reset()
    temperature = initial_temperature

    total_iteraties = 20000
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

        if delta_score/temperature > 500:
            p_accept = 0
        elif delta_score < 0:
            p_accept = 1
        else:
            p_accept = math.exp(1)**(-delta_score/temperature)
            p_acceptlist.append(p_accept)

        if delta_score < 0 or p_accept > random.random():
            current_solution = neighbor
            current_score = neighbor_score

        temperature = initial_temperature / ((iteraties + 1) ** 0.48)
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
    """
    This function generates neighboring solutions by randomly selecting a train route and replacing it
    with a new random train route.

    Preconditions:
        - solution is a list representing the current solution of trajects.
        - area is an instance of the Rail_NL class.
        - amount_trajects is a positive integer representing the number of train routes.
        - amount_stations is a positive integer representing the number of stations.
        - max_time is a positive integer representing the maximum time duration for a train route.

    Postconditions:
        - Returns a list of neighboring solutions.
    """
    neighbors = []
    for i in range(amount_trajects):
        neighbor = solution[:]
        neighbor[i] = run_random_traject(area, amount_stations, max_time)[2]
        neighbors.append(neighbor)
    return neighbors