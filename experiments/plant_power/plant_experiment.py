from code.algorithms.plant_propagation.plant_propagation import plant

import time
import pickle

def timed_plant(area, amount_trajects, max_time, amount_stations, time_to_run):
    list_power = [0.5, 1, 1.5]
    for i in list_power:
        start = time.time()
        results = []
        best = 0
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            area.reset()
            test = plant(area, amount_trajects, max_time, amount_stations, 1000, i)
            test.run_program()
            info = test.get_data()
            results.append(info)
            if info[-1] > best:
                best = info[-1]
        print(best)
        file_name = f'plant_power{i}.pickle'
        with open(file_name, 'wb') as f:
            pickle.dump(results, f)
