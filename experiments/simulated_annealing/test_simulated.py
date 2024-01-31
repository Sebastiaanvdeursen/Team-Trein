from code.algorithms.simulated_annealing.sim_annealing_alg import simulated_annealing

import pickle

def Test_simulated(area, amount_trajects, max_time_train, amount_stations, time_to_run):
    list_temperaturevalues = [600, 700, 800, 900]
    list_valuesexponent = [0.4125, 0.425, 0.4375]
    for j in range(len(list_temperaturevalues)):
        for i in range(len(list_valuesexponent)):
            start = time.time()
            results = []
            best = []
            current_max = 0
            while True:
                if (time.time() - start) / 60 > time_to_run:
                    break
                result = simulated_annealing(area, amount_trajects, amount_stations, max_time_train, list_temperaturevalues[j], list_valuesexponent[i])
                current_traject = result[0]
                score = result[1]
                area.reset()
                if score > current_max:
                    current_max = score
                    best = current_traject
                results.append(score)
            count = 1
            for a in best:
                print(f"train_{count},{a}")
                count += 1
            print(f"score,{max(results)}")

            file_name = f'results_{list_temperaturevalues[j]}_{list_valuesexponent[i]}.pickle'
            with open(file_name, 'wb') as f:
                pickle.dump(results, f)