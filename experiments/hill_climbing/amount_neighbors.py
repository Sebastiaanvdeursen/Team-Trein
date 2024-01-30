import sys
from code.classes.rail_NL import Rail_NL
from code.algorithms.hill_climbing.hill_climbing_alg import hill_climbing
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt

def test_hill_climbing(area, amount_trajects, max_time, amount_stations, time_to_run):
    start = time.time()
    results = [[0] * 5] * 3
    print(results[0][0])
    while True:
        i_count = 0
        j_count = 0
        if (time.time() - start) / 60 > time_to_run:
            break
        for i in range(10, 15):
            for j in range(1, 11, 5):
                best = []
                current_max = 0
                result = hill_climbing(area, i, amount_stations, max_time, amount_neighbors = j)
                current_traject = result[2]
                score = result[0]*10000 - (len(current_traject)*100 + result[1])
                area.reset()
                if score > current_max:
                    current_max = score
                    best = current_traject
                results[i_count][j_count].append(score)

                file_name = f'experiments/hill_climbing/pickle/results_{i}_{j}.pickle'
                with open(file_name, 'wb') as f:
                    pickle.dump(results[i_count][j_count], f)
                j_count += 1
            i_count += 1

    average_list = []
    for q in range(10, 15):
        for r in range(1, 11, 5):
            file = open(f'experiments/hill_climbing/pickle/results_{q}_{r}.pickle', 'rb')
            results = pickle.load(file)
            file.close()
            count = 0 
            for i in results:
                count += 1
            print(f"amount trajects: {q}")
            print(f"amount neighbors: {r}")
            print(f"amount of results, {count}")
            print(f"max, {max(results)}")
            average = sum(results) / len(results)
            average_list.append(average)
            print(f"average, {sum(results) / len(results)}")
            print(f"std, {np.std(results)}")