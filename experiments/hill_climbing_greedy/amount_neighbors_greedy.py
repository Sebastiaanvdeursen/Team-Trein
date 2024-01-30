import sys
from code.classes.rail_NL import Rail_NL
from code.algorithms.hill_climbing_greedy_alg import hill_climbing_greedy
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt

def timed_hill_climbing_greedy_neighbors(area, amount_trajects, max_time, amount_stations, time_to_run):
        list_amount_trajects = list(range(1, amount_trajects + 1))
        start = time.time()
        counts = [0] * 20
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            counter = 0
            for i in range(1, 21):
                results = []
                best = []
                current_max = 0
                result = hill_climbing_greedy(area, amount_trajects, amount_stations, max_time, amount_neighbors = i)
                current_traject = result[2]
                score = result[0]*10000 - (len(current_traject)*100 + result[1])
                area.reset()
                if score > current_max:
                    current_max = score
                    best = current_traject
                results.append(score)
                counts[i - 1] += 1

                file_name = f'/experiments/hill_climbing_greedy/pickle/results_{list_amount_trajects[i - 1]}.pickle'
                with open(file_name, 'wb') as f:
                    pickle.dump(results, f)

        average_list = []
        i_list = []
        for i in range(amount_trajects):
            i_list.append(i)
            file = open(f'/experiments/hill_climbing_greedy/pickle/results_{i + 1}.pickle', 'rb')
            results = pickle.load(file)
            file.close()
            print(i + 1)
            print(f"amount of results, {counts[i]}")
            print(f"max, {max(results)}")
            average = sum(results) / len(results)
            average_list.append(average)
            print(f"average, {sum(results) / len(results)}")
            print(f"std, {np.std(results)}")
        plt.plot(i_list, average_list)
        plt.show()