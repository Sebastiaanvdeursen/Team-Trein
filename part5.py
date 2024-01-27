from code.algorithms.random_alg import run_random_amount_of_trajects
from code.algorithms.random_alg_opt import run_random_amount_of_trajects_opt
from code.algorithms.greedy_random_start import run_greedy_random
from code.algorithms.greedy_best_comb import run_greedy_combinations
from code.algorithms.hill_climbing_greedy_alg import hill_climbing_greedy
from code.algorithms.hill_climbing_greedy_optim_alg import hill_climbing_greedy_optim
from code.algorithms.hill_climbing_alg import hill_climbing
from code.algorithms.hill_climbing_opt_alg import hill_climbing_opt
from code.algorithms.double_greedy import double_greedy_random
from code.algorithms.sim_annealing_alg import simulated_annealing
from code.algorithms.PlantPropagation import plant
from code.algorithms.weighted_greedy import run_weighted

from code.classes.rail_NL import Rail_NL

import random
import matplotlib.pyplot as plt
import sys
import time
import pickle


if __name__ == "__main__":
    made_area = False

    map = "NL"
    amount_trajects = 20
    amount_stations = 61
    max_time = 180
    area2 = Rail_NL(map, amount_trajects, amount_stations, max_time, removing = sys.argv[1])
    amount_stations_2 = area2.get_amount_stations()
    results1 = []
    for i in range(0, int(sys.argv[2])):
        Min, T, p, current = run_greedy_random(area2, amount_trajects, max_time, amount_stations, printed = False, info = True)
        area2.reset()
        results1.append( p * 10000 - (T * 100 + Min))
    maximum = max(results1)



    list = [0] * 89
    count = [0] * 89
    for i in range(int(sys.argv[1])):
        results = []
        area1 = Rail_NL(map, amount_trajects, amount_stations, max_time, randomizer = True)
        numbers = area1.get_ids()
        amount_stations_1 = area1.get_amount_stations()
        for j in range(0, int(sys.argv[2])):
            Min, T, p, current = run_greedy_random(area1, amount_trajects, max_time, amount_stations, printed = False, info = True)
            area1.reset()
            results.append( p * 10000 - (T * 100 + Min))
        max_random = max(results)
        difference = max_random - maximum
        print(difference)
        for i in numbers:
            list[i - 1] += difference
            count[i - 1] += 1
    for i in range(1, 89):
        print(list[i] / count[i])










