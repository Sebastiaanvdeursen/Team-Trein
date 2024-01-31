"""
By: Ties Veltman
"""
from code.algorithms.greedy.greedy_random_start import run_greedy_random
from code.algorithms.greedy.weighted_greedy import run_weighted
from code.algorithms.random.random_alg import run_random_amount_of_trajects
from code.algorithms.random.random_alg_opt import run_random_amount_of_trajects_opt

import sys
import time
import pickle


def Timed(area: object, amount_trajects: int, max_time_train: int, 
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
            Min, T, p, current = run_random_amount_of_trajects_opt(area, amount_trajects, max_time_train,
                                                                    amount_stations, printed = False, info = True)
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
            Min, T, p, current = run_greedy_random(area, amount_trajects, max_time_train, amount_stations, printed = False, info = True)
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
            Min, T, p, current = run_weighted(area, amount_trajects, max_time_train, amount_stations, printed = False, info = True)
            area.reset()
            k = p * 10000 - (T * 100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)

    else:
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = run_random_amount_of_trajects(area, amount_trajects, max_time_train,
                                                                amount_stations, printed = False, info = True)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(k)

    count = 1
    for a in best:
        print(f"train_{count},{a}")
        count += 1
    print(f"score,{max(results)}")

    with open('results.pickle', 'wb') as f:
        pickle.dump(results, f)
