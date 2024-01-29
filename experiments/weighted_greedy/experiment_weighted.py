from code.algorithms.weighted_greedy import run_weighted

import pickle

def timed_weighted(area, amount_trajects, max_time_train, amount_stations, time_to_run):
    list_powers = [1, 1.25, 1.5, 2, 3, 4, 5, 6, 7]
    for i in range(len(list_powers)):
        results = []
        start = time.time()
        max_value = 0
        while True:
                if (time.time() - start) / 60 > time_to_run:
                    break
                area.reset()
                min, T, fraction_done = run_weighted(area, amount_trajects, max_time_train, amount_stations, False, power = list_powers[i])
                score = fraction_done * 10000 - (T * 100 + min)
                results.append(score)
                if score > max_value:
                    max_value = score
        print(max_value)
        file_name = f'results_weighted{list_powers[i]}.pickle'
        with open(file_name, 'wb') as f:
                pickle.dump(results, f)
