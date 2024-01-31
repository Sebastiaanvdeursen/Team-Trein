"""
Algorithms & Heuristics

Group: Team-Trein

This script acts as the central hub for our Rail_NL project. Here, you'll find a large range
of algorithms to try and tackle the Rail_NL problem. Additionally, the script provides tools for
visualization, testing, and ways to evaluate the quality of the algorithms.
"""

from code.algorithms.random.random_alg import run_random_amount_of_trajects
from code.algorithms.random.random_alg_opt import run_random_amount_of_trajects_opt
from code.algorithms.greedy.greedy_random_start import run_greedy_random
from code.algorithms.greedy.greedy_best_comb import run_greedy_combinations
from code.algorithms.hill_climbing.hill_climbing_alg import hill_climbing
from code.algorithms.greedy.double_greedy import double_greedy_random
from code.algorithms.simulated_annealing.sim_annealing_alg import simulated_annealing
from code.algorithms.plant_propagation.plant_propagation import plant
from code.algorithms.greedy.weighted_greedy import run_weighted
from code.visualization.plot_simulated import Plot_simulated
from code.visualization.plot_hill_climbing import Plot_hill_climbing
from code.visualization.visualization import visualization
from code.other.part1 import find_p
from code.other.part5 import Part5
from code.other.use_pickle import run_pickle
from code.other.timed import Timed
from experiments.plant_power.plant_experiment import timed_plant
from experiments.weighted_greedy.experiment_weighted import timed_weighted
from experiments.hill_climbing.test_hill_climbing import test_hill_climbing
from experiments.hill_climbing_greedy.test_hill_climbing_greedy import test_hill_climbing_greedy
from experiments.simulated_annealing.test_simulated import Test_simulated
from fitter import Fitter

from code.classes.rail_NL import Rail_NL

import matplotlib.pyplot as plt
import sys
import pickle


def iterate(area: Rail_NL, amount_trajects: int, max_time: int, amount_stations: int,
            fitter: bool = False, histogram: bool = False, group_info: bool = False, plot: bool = False):
    """
    Perform multiple iterations of a specified algorithm and analyze the results.

    pre:
        - area: Instance of Rail_NL object.
        - amount_trajects: Number of tracks.
        - max_time: Maximum time allowed for one track.
        - amount_stations: Number of stations in the railway network.
        - fitter: Bool indicating whether to use Fitter function.
        - histogram: Boolean indicating whether to generate and display a histogram of results.
        - group_info: Boolean indicating whether to print group information.

    post:
        - results of each iteration are stored in 'results' list.
        - the best-performing iteration's details are stored in 'best'.
        - if 'fitter' is True, ouput of Fitter function is printed.
        - If 'histogram' is True, a histogram of results is displayed.
        - If 'group_info' is True, average score information is printed.
        - Results are saved in 'results.pickle' file.
    """
    first = True
    results = []
    best = []
    for i in range(0, int(sys.argv[3])):
        if sys.argv[2] == "random":
            Min, T, p, current = run_random_amount_of_trajects(area, amount_trajects, max_time,
                                                               amount_stations, printed=False, info=True)
        elif sys.argv[2] == "random_optim":
            Min, T, p, current = run_random_amount_of_trajects_opt(area, amount_trajects, max_time,
                                                                   amount_stations, printed=False,
                                                                   info=True)
        elif sys.argv[2] == "greedy_random" or sys.argv[2] == "greedy":
            Min, T, p, current = run_greedy_random(area, amount_trajects, max_time, amount_stations,
                                                   printed=False, info=True)
        elif sys.argv[2] == "greedy_optim":
            Min, T, p, current = run_greedy_combinations(area, amount_trajects, max_time, amount_stations,
                                                         used_for_hill_climbing=False, longer=True)
        elif sys.argv[2] == "double_greedy" or sys.argv[2] == "double":
            Min, T, p, current = double_greedy_random(area, amount_trajects, max_time, amount_stations,
                                                      False)
        elif sys.argv[2] == "weighted":
            Min, T, p, current = run_weighted(area, amount_trajects, max_time, amount_stations, False,
                                              info=True)
        elif sys.argv[2] == "hill_climbing":
            # use the best values according to experiment
            amount_trajects = 14
            p, Min, current = hill_climbing(area, amount_trajects, amount_stations, max_time,
                                            amount_neighbors=10)
            T = len(current)
        elif sys.argv[2] == "hill_climbing_greedy":
            # use the best values according to experiment
            amount_trajects = 18
            p, Min, current = hill_climbing(area, amount_trajects, amount_stations, max_time,
                                            amount_neighbors=5, greedy=True)
            T = len(current)
        elif sys.argv[2] == "hill_climbing_optim":
            p, Min, current = hill_climbing(area, amount_trajects, amount_stations, max_time,
                                            amount_neighbors=10, random_optim=True)
            T = len(current)
        elif sys.argv[2] == "simulated" or sys.argv[2] == "annealing":
            result = simulated_annealing(area, amount_trajects, amount_stations, max_time, 500, 0.4)
            p = result[0]
            Min = result[1]
            current = result[2]
            T = len(current)
        else:
            Min, T, p, current = run_random_amount_of_trajects(area, amount_trajects, max_time,
                                                               amount_stations, printed=False, info=True)
            if first:
                print("ran random since wrong algorithm was given")
                first = False
        area.reset()
        K = p * 10000 - (T * 100 + Min)
        results.append(K)
        if results[i] == max(results):
            best = current

    if fitter:
        f = Fitter(results, distributions=["norm", "gamma", "lognorm", "beta"])
        f.fit()
        f.summary()
        plt.show()

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
            area = Rail_NL(map, amount_trajects, amount_stations, max_time, randomizer=True)
            amount_stations = area.get_amount_stations()
            made_area = True
        elif sys.argv[1] == "large_random":
            map = "NL"
            amount_trajects = 20
            amount_stations = 61
            max_time = 180
            area = Rail_NL(map, amount_trajects, amount_stations, max_time, randomizer=True)
            amount_stations = area.get_amount_stations()
            made_area = True
        else:
            map = "NL"
            amount_trajects = 20
            amount_stations = 61
            max_time = 180
            area = Rail_NL(map, amount_trajects, amount_stations, max_time, removing=sys.argv[1])
            amount_stations = area.get_amount_stations()
            made_area = True

    if not made_area:
        area = Rail_NL(map, amount_trajects, amount_stations, max_time)
    print("train,stations")

    if len(sys.argv) > 2:
        if sys.argv[2] == "find_p" or sys.argv[2] == "part1":
            find_p(area, amount_trajects, max_time, amount_stations)
        elif sys.argv[2] == "visualization" or sys.argv[2] == "vis":
            visualization(sys.argv[1], "output.csv")
        elif sys.argv[2] == "part5":
            Part5()
        elif sys.argv[2] == "test_weighted":
            timed_weighted(area, amount_trajects, max_time, amount_stations, float(sys.argv[3]))
        elif sys.argv[2] == "test_plant":
            timed_plant(area, amount_trajects, max_time, amount_stations, float(sys.argv[3]))
        elif sys.argv[2] == "test_hill_climbing":
            test_hill_climbing(area, amount_trajects, max_time, amount_stations, float(sys.argv[3]))
        elif sys.argv[2] == "test_hill_climbing_greedy":
            test_hill_climbing_greedy(area, amount_trajects, max_time, amount_stations,
                                      float(sys.argv[3]))
        elif sys.argv[2] == "test_simulated" or sys.argv[2] == "test_annealing":
            Test_simulated(area, amount_trajects, max_time, amount_stations, float(sys.argv[3]))
        elif sys.argv[2] == "pickle":
            run_pickle()

        elif len(sys.argv) > 3:
            if sys.argv[3] == "time":
                if len(sys.argv) > 4:
                    Timed(area, amount_trajects, max_time, amount_stations, float(sys.argv[4]))
            elif len(sys.argv) > 4:
                if sys.argv[4] == "hist" or sys.argv[4] == "histogram":
                    iterate(area, amount_trajects, max_time, amount_stations, histogram=True)
                elif sys.argv[4] == "all":
                    iterate(area, amount_trajects, max_time, amount_stations, fitter = True, group_info=True)
                else:
                    iterate(area, amount_trajects, max_time, amount_stations)
            else:
                iterate(area, amount_trajects, max_time, amount_stations)

        else:
            if sys.argv[2] == "simulatedplot":
                Plot_simulated(area, amount_trajects, amount_stations, max_time, 500, 0.4)
            
            elif sys.argv[2] == "hill_climbing_plot":
                Plot_hill_climbing(area, amount_trajects, amount_stations, max_time, amount_neighbors=10,
                                   greedy=False, random_optim=False)

            elif sys.argv[2] == "plant":
                plantprop = plant(area, amount_trajects, max_time, amount_stations, 400)
                plantprop.run_program()
                results = plantprop.get_data()
                with open('plant.pickle', 'wb') as f:
                    pickle.dump(results, f)

            else:
                print("usage python3 main.py size algorithm")
