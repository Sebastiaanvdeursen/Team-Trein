from code.algorithms.random_alg import run_random_amount_of_trajects
from code.classes.rail_NL import Rail_NL
from code.algorithms.greedy_random_start import run_greedy_track_random
from code.algorithms.greedy_best_comb import run_greedy_combinations
import random
import itertools as iter
from math import comb
import copy


def hill_climbing_greedy_optim(area, amount_trajects, amount_stations, max_time):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area)
    area.reset()

    while True:
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        
        # Selecteer het beste buur
        best_neighbor = max(neighbors, key=lambda neighbor: evaluate_solution(neighbor, area))

        # Als het beste buur beter is dan de huidige oplossing, update de oplossing en score
        eval_sol = evaluate_solution(best_neighbor, area)

        if eval_sol > current_score:
            current_solution = best_neighbor
            current_score = eval_sol
            area.reset()
        
        else:
            # Stop als er geen verbetering is
            break

    for i in range(0, amount_trajects):
        stations_str = ', '.join(current_solution[i].traject_connections)
        print(f"train_{i + 1},\"[{stations_str}]\"")
    
    return current_solution, current_score

def generate_random_solution(area, amount_trajects, amount_stations, max_time):
    solution = run_greedy_combinations(area, amount_trajects, max_time, amount_stations, True)
    return solution

def evaluate_solution(solution, area):
    # Hier implementeer je de evaluatie van de doelfunctie K voor de gegeven oplossing
    # Je kunt de p-waarde, T-waarde en Min-waarde berekenen zoals beschreven in je doelfunctie.
    total_time = 0
    for i in range(0, len(solution)):
        total_time += solution[i].total_time

    n_done = 0
    for station in area.stations.values():
        for connection in station.connections.values():
            if connection.done:
                n_done += 1

    fraction_done = (n_done / 2) / area.total_connections

    return fraction_done * 10000 - (len(solution) * 100 + total_time)


def get_neighbors(solution, area, amount_trajects, amount_stations, max_time):
    neighbors = []
    for i in range(amount_trajects):
        neighbor = copy.deepcopy(solution)
        neighbor[i] = run_greedy_track_random(area, amount_stations, max_time, True)[2]
        neighbors.append(neighbor)
        area.reset()
    return neighbors