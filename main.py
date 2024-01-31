from code.algorithms.random.random_alg import run_random_amount_of_trajects
from code.algorithms.random.random_alg_opt import run_random_amount_of_trajects_opt
from code.algorithms.greedy.greedy_random_start import run_greedy_random
from code.algorithms.greedy.greedy_best_comb import run_greedy_combinations
from code.algorithms.hill_climbing.hill_climbing_greedy_alg import hill_climbing_greedy
from code.algorithms.hill_climbing.hill_climbing_alg import hill_climbing
from code.algorithms.hill_climbing.hill_climbing_opt_alg import hill_climbing_opt
from code.algorithms.greedy.double_greedy import double_greedy_random
from code.algorithms.simulated_annealing.sim_annealing_alg import simulated_annealing
from code.algorithms.plant_propagation.plant_propagation import plant
from code.algorithms.greedy.weighted_greedy import run_weighted
from code.other.part1 import find_p
from code.other.part5 import Part5
from code.other.use_pickle import run_pickle
from code.other.timed import Timed
from experiments.plant_power.plant_experiment import timed_plant
from experiments.weighted_greedy.experiment_weighted import timed_weighted
from experiments.hill_climbing.test_hill_climbing import test_hill_climbing
from experiments.hill_climbing_greedy.test_hill_climbing_greedy import test_hill_climbing_greedy
from experiments.simulated_annealing.test_simulated import timed_multiple
from fitter import Fitter

from code.classes.rail_NL import Rail_NL

import matplotlib.pyplot as plt
import sys
import pickle


def iterate(area, amount_trajects, max_time, amount_stations,
            fitter: bool = False, histogram: bool = False, group_info: bool = False):
    results = []
    best = []
    for i in range(0, int(sys.argv[3])):
        if sys.argv[2] == "random":
            Min, T, p, current = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations, 
                                                               printed = False, info = True)
        elif sys.argv[2] == "random_optim":
            Min, T, p, current = run_random_amount_of_trajects_opt(area, amount_trajects, max_time, amount_stations, 
                                                                   printed = False, info = True)
        elif sys.argv[2] == "greedy_random" or sys.argv[2] == "greedy":
            Min, T, p, current = run_greedy_random(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
        elif sys.argv[2] == "greedy_optim":
            Min, T, p, current = run_greedy_combinations(area, amount_trajects, max_time, amount_stations,
                                                        used_for_hill_climbing = False, longer = True)
        elif sys.argv[2] == "double_greedy" or sys.argv[2] == "double":
            Min, T, p, current = double_greedy_random(area, amount_trajects, max_time, amount_stations, False)
        elif sys.argv[2] == "weighted":
            Min, T, p, current = run_weighted(area, amount_trajects, max_time, amount_stations, False, info = True)
        elif sys.argv[2] == "hill_climbing":
            p, Min, current = hill_climbing(area, amount_trajects, amount_stations, max_time, amount_neighbors = 100)
            T = len(current)
        elif sys.argv[2] == "hill_climbing/greedy":
            p, Min, current = hill_climbing_greedy(area, amount_trajects, amount_stations, max_time, amount_neighbors = 10)
            T = len(current)
        elif sys.argv[2] == "hill_climbing_opt":
            p, Min, current = hill_climbing_opt(area, amount_trajects, amount_stations, max_time, amount_neighbors = 100)
            T = len(current)
        elif sys.argv[2] == "simulated" or sys.argv[2] == "annealing":
            result = simulated_annealing(area, amount_trajects, amount_stations, max_time, 500, 0.4)
            p = result[0]
            Min = result[1]
            T = len(result[2])
        area.reset()
        K = p*10000 - (T*100 + Min)
        results.append(K)
        if results[i] == max(results):
            best = current

    if fitter:
        f = Fitter(results, distributions = ["norm"])
        f.fit()
        f.summary()

    if histogram:
        plt.hist(results, int(20))
        plt.show()

    count = 1
    for a in best:
        stations_str = ', '.join(a)
        print(f"train_{count},\"[{stations_str}]\"")
        count += 1
    print(f"score,{max(results)}")

    if group_info:
        print(f"average = {sum(results) / int(sys.argv[3])}")

    with open('results.pickle', 'wb') as f:
        pickle.dump(results, f)


# Main script
if __name__ == "__main__":
    made_area = False
    if len(sys.argv) > 1:
        if sys.argv[1] == "large":
            map = "NL"
            amount_trajects = 20
            amount_stations = 61
            max_time = 180
        elif sys.argv[1] == "small":
            map = "Holland"
            amount_trajects = 7
            amount_stations = 22
            max_time = 120
        elif sys.argv[1] == "small_random":
            map = "Holland"
            amount_trajects = 7
            amount_stations = 22
            max_time = 120
            area = Rail_NL(map, amount_trajects, amount_stations, max_time, randomizer = True)
            amount_stations = area.get_amount_stations()
            made_area = True
        elif sys.argv[1] == "large_random":
            map = "NL"
            amount_trajects = 20
            amount_stations = 61
            max_time = 180
            area = Rail_NL(map, amount_trajects, amount_stations, max_time, randomizer = True)
            amount_stations = area.get_amount_stations()
            made_area = True
        else:
            map = "NL"
            amount_trajects = 20
            amount_stations = 61
            max_time = 180
            area = Rail_NL(map, amount_trajects, amount_stations, max_time, removing = sys.argv[1])
            amount_stations = area.get_amount_stations()
            made_area = True


    if not made_area:
        area = Rail_NL(map, amount_trajects, amount_stations, max_time)
    print("train,stations")

    if len(sys.argv) > 2:
        if sys.argv[2] == "find_p" or sys.argv[2] == "part1":
            find_p(area, amount_trajects, max_time, amount_stations)
        elif sys.argv[2] == "part5":
            Part5()
        elif sys.argv[2] == "test_weighted":
            timed_weighted(area, amount_trajects, max_time, amount_stations, float(sys.argv[3]))
        elif sys.argv[2] == "test_plant":
            timed_plant(area, amount_trajects, max_time, amount_stations, float(sys.argv[3]))
        elif sys.argv[2] == "test_hill_climbing":
            test_hill_climbing(area, amount_trajects, max_time, amount_stations, float(sys.argv[3]))
        elif sys.argv[2] == "test_hill_climbing_greedy":
            test_hill_climbing_greedy(area, amount_trajects, max_time, amount_stations, float(sys.argv[3]))
        elif sys.argv[2] == "pickle":
            run_pickle()

        elif len(sys.argv) > 3:
            if sys.argv[3] == "time":
                if len(sys.argv) > 4:
                    Timed(area, amount_trajects, max_time, amount_stations, float(sys.argv[4]))
            elif sys.argv[3] == "timemultiple":
                if len(sys.argv) > 4:
                    timed_multiple(area, amount_trajects, max_time, amount_stations, float(sys.argv[4]))

            elif len(sys.argv) > 4:
                if sys.argv[4] == "hist" or sys.argv[4] == "histogram":
                    iterate(area, amount_trajects, max_time, amount_stations, histogram = True)
                elif sys.argv[4] == "all":
                    iterate(area, amount_trajects, max_time, amount_stations, histogram = True, group_info = True)
                else:
                    iterate(area, amount_trajects, max_time, amount_stations)
            else:
                iterate(area, amount_trajects, max_time, amount_stations)

        else:
            if sys.argv[2] == "simulatedplot":
                result = simulated_annealing(area, amount_trajects, amount_stations, max_time, 500, 0.40)
                trajects = result[0]
                count = 1
                for a in trajects:
                    stations_str = ', '.join(a)
                    print(f"train_{count},\"[{stations_str}]\"")
                    count += 1
                print(f"score, {result[1]}")
                scoresplot = result[2]
                temperatureplot = result[3]
                iterationstemperatureplot = range(len(temperatureplot))
                iterationsplot = range(len(scoresplot))
                plt.plot(iterationstemperatureplot, temperatureplot)
                plt.plot(iterationsplot, scoresplot)
                plt.xlabel('Iterations')
                plt.ylabel('Score')
                plt.title('Simulated Annealing for the Netherlands')
                plt.show()

            elif sys.argv[2] == "simulatedprobplot":
                result = simulated_annealing(area, amount_trajects, amount_stations, max_time, 2000, 0.50)
                print(f"score, {result[1]}")
                pacceptplot = result[4]
                iterationsprobplot = range(len(pacceptplot))
                plt.plot(iterationsprobplot, pacceptplot)
                plt.show()

            elif sys.argv[2] == "plant":
                plantprop = plant(area, amount_trajects, max_time, amount_stations, 100)
                plantprop.run_program()
                results = plantprop.get_data()
                with open('plant.pickle', 'wb') as f:
                    pickle.dump(results, f)

            else:
                print("usage python3 main.py size algorithm")
    else:
        Min, T, p = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations)
        K = p*10000 - (T*100 + Min)
        print(f"score,{K}")