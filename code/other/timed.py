"""
Algorithms & Heuristics

Group: Team-Trein

This script run all the algorithms that we made, but now for a certain time.
Then after that it prints the best solution it found in that time.

By: Ties Veltman
"""


from code.algorithms.greedy.double_greedy import double_greedy_random
from code.algorithms.greedy.greedy_best_comb import run_greedy_combinations
from code.algorithms.greedy.greedy_random_start import run_greedy_random
from code.algorithms.greedy.weighted_greedy import run_weighted
from code.algorithms.hill_climbing.hill_climbing_alg import hill_climbing
from code.algorithms.random.random_alg import run_random_amount_of_trajects
from code.algorithms.random.random_alg_opt import run_random_amount_of_trajects_opt
from code.algorithms.simulated_annealing.sim_annealing_alg import simulated_annealing

import sys
import time
import pickle


def Timed(area: object, amount_trajects: int, max_time: int, 
          amount_stations: int, time_to_run: float) -> None:
    """
    Runs an algorithm for a specific amount of time in minutes.

    Preconditions:
        - area is an instance of the Rail_NL class.
        - amount_trajects is a positive integer representing the maximum number of train trajects we can choose.
        - amount_stations is a positive integer representing the number of stations present in the current map.
        - max_time_train is a positive integer representing the maximum time duration for a train route.
        - time_to_run represents how long the algorithm should run.

    Postconditions:
        - Has a side effect of printing the entire output.
        - Has a side effect of dumping the results into a pickle file.
    """
    start = time.time()
    results = []
    best = []
    current_max = 0
    if sys.argv[2] == "random_opt":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = run_random_amount_of_trajects_opt(area, amount_trajects, max_time,
                                                                    amount_stations, printed = False, info = True)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)
    
    elif sys.argv[2] == "random":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = run_random_amount_of_trajects(area, amount_trajects, max_time,
                                                               amount_stations, printed=False, info=True)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)

    elif sys.argv[2] == "greedy" or sys.argv[2] == "greedy_random":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = run_greedy_random(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)
    
    elif sys.argv[2] == "greedy_optim":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = run_greedy_combinations(area, amount_trajects, max_time, amount_stations, longer=True)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)
    
    elif sys.argv[2] == "double_greedy" or sys.argv[2] == "double":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = double_greedy_random(area, amount_trajects, max_time, amount_stations, False)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)
    
    elif sys.argv[2] == "hill_climbing":
        amount_trajects = 14
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            p, Min, current = hill_climbing(area, amount_trajects, amount_stations, max_time,
                                            amount_neighbors=10)
            T = len(current)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)
    
    elif sys.argv[2] == "hill_climbing_greedy":
        amount_trajects = 18
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            p, Min, current = hill_climbing(area, amount_trajects, amount_stations, max_time,
                                            amount_neighbors=5, greedy=True)
            T = len(current)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)
    
    elif sys.argv[2] == "hill_climbing_optim":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            p, Min, current = hill_climbing(area, amount_trajects, amount_stations, max_time,
                                            amount_neighbors=10, random_optim=True)
            T = len(current)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)

    elif sys.argv[2] == "weighted":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = run_weighted(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
            area.reset()
            k = p * 10000 - (T * 100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)
    
    elif sys.argv[2] == "simulated" or sys.argv[2] == "annealing":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            result = simulated_annealing(area, amount_trajects, amount_stations, max_time, 500, 0.4)
            p = result[0]
            Min = result[1]
            current = result[2]
            T = len(current)
            area.reset()
            k = p * 10000 - (T * 100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)
    else:
        print("Please enter a valid algorithm to time")

    count = 1
    for a in best:
        stations_str = ', '.join(a)
        print(f"train_{count},\"[{stations_str}]\"")
        count += 1
    print(f"score,{max(results)}")

    with open('results.pickle', 'wb') as f:
        pickle.dump(results, f)
