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

from code.classes.rail_NL import Rail_NL

import random
import matplotlib.pyplot as plt
import sys
import time
import pickle

def timed(area, amount_trajects, max_time_train, amount_stations, time_to_run):
    start = time.time()
    results = []
    best = []
    current_max = 0
    if sys.argv[2] == "random_opt":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = run_random_amount_of_trajects_opt(area, amount_trajects, max_time_train, amount_stations, printed = False, info = True)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(p*10000 - (T*100 + Min))

    if sys.argv[2] == "greedy" or sys.argv[2] == "greedy_random":
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            Min, T, p, current = run_greedy_random(area, amount_trajects, max_time_train, amount_stations, printed = False, info = True)
            area.reset()
            k = p*10000 - (T*100 + Min)
            if k > current_max:
                current_max = k
                best = current
            results.append(p*10000 - (T*100 + Min))

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
            results.append(p * 10000 - (T * 100 + Min))

    count = 1
    for a in best:
        print(f"train_{count},{a}")
        count += 1
    print(f"score,{max(results)}")

    with open('results.pickle', 'wb') as f:
        pickle.dump(results, f)


def iterate(area, amount_trajects, max_time, amount_stations,
             fitter: bool = False, histogram: bool = False, group_info: bool = False ):
    results = []
    best = []
    if sys.argv[2] == "random_optim":
        for i in range(0, int(sys.argv[3])):
            Min, T, p, current = run_random_amount_of_trajects_opt(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
            area.reset()
            results.append(p*10000 - (T*100 + Min))
            if results[i] == max(results):
                best = current

    elif sys.argv[2] == "greedy_random" or sys.argv[2] == "greedy":
        for i in range(0, int(sys.argv[3])):
            Min, T, p, current = run_greedy_random(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
            area.reset()
            results.append( p * 10000 - (T * 100 + Min))
            if results[i] == max(results):
                best = current
    
    if sys.argv[2] == "hill_climbing":
        for i in range(0, int(sys.argv[3])):
            current, K = hill_climbing(area, amount_trajects, amount_stations, max_time)
            area.reset()
            results.append(K)
            if results[i] == max(results):
                best = current
    
    if sys.argv[2] == "hill_climbing/greedy":
        for i in range(0, int(sys.argv[3])):
            current, K = hill_climbing_greedy(area, amount_trajects, amount_stations, max_time)
            area.reset()
            results.append(K)
            if results[i] == max(results):
                best = current
    
    if sys.argv[2] == "hill_climbing_opt":
        for i in range(0, int(sys.argv[3])):
            current, K = hill_climbing_opt(area, amount_trajects, amount_stations, max_time)
            area.reset()
            results.append(K)
            if results[i] == max(results):
                best = current

    elif sys.argv[2] == "double" or sys.argv[2] == "double_greedy":
        for i in range(0, int(sys.argv[3])):
            Min, T, p, current = double_greedy_random(area, amount_trajects, max_time, amount_stations, printed = False)
            area.reset()
            results.append(p * 10000 - (T * 100 + Min))
            if results[i] == max(results):
                best = current

    else:
        for i in range(0, int(sys.argv[3])):
            Min, T, p, current = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
            area.reset()
            results.append(p*10000 - (T*100 + Min))
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

def find_p(area, amount_trajects, max_time, amount_stations):
    while True:
        Min, T, p, trajects = run_greedy_random(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
        if p == 1:
            count = 1
            for a in trajects:
                stations_str = ', '.join(a)
                print(f"train_{count},\"[{stations_str}]\"")
                count += 1
            print(f"score,{p * 10000 - (T * 100 + Min)}")
            break
        area.reset()

# Main script
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "large":
            map = "NL"
            amount_trajects = 20
            amount_stations = 61
            max_time = 180
        else:
            map = "Holland"
            amount_trajects = 7
            amount_stations = 22
            max_time = 120
    else:
        map = "Holland"
        amount_trajects = 7
        amount_stations = 22
        max_time = 120

    area = Rail_NL(map, amount_trajects, amount_stations, max_time)
    print("train,stations")

    if len(sys.argv) > 2:
        if sys.argv[2] == "find_p":
            find_p(area, amount_trajects, max_time, amount_stations)

        elif len(sys.argv) > 3:
            if sys.argv[3] == "time":
                if len(sys.argv) > 4:
                    timed(area, amount_trajects, max_time, amount_stations, float(sys.argv[4]))
            else:
                if len(sys.argv) > 4:
                    if sys.argv[4] == "hist" or sys.argv[4] == "histogram":
                        iterate(area, amount_trajects, max_time, amount_stations, histogram = True)
                    elif sys.argv[4] == "all":
                        iterate(area, amount_trajects, max_time, amount_stations, histogram = True, group_info = True)
                    else:
                        iterate(area, amount_trajects, max_time, amount_stations)
                else:
                    iterate(area, amount_trajects, max_time, amount_stations)

        else:
            if sys.argv[2] == "simulated" or sys.argv[2] == "annealing":
                K = simulated_annealing(area, amount_trajects, amount_stations, max_time, 1000)[1]
                print(f"score, {K}")
            
            elif sys.argv[2] == "simulatedplot":
                plt.plot(range(simulated_annealing(area, amount_trajects, amount_stations, max_time, 1000)[2]), simulated_annealing(area, amount_trajects, amount_stations, max_time, 1000)[3])
                plt.xlabel('Iterations')
                plt.ylabel('Current Score')
                plt.title('Simulated Annealing Convergence')
                plt.show()

            elif sys.argv[2] == "plant":
                plantprop = plant(area, amount_trajects, max_time, amount_stations, 70)
                plantprop.run_program()
            elif sys.argv[2] == "random":
                Min, T, p = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations)
                K = p*10000 - (T*100 + Min)
                print(f"score,{K}")

            elif sys.argv[2] == "random_max":
                K_list = []
                for i in range(10000):
                    Min, T, p = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations)
                    K = p*10000 - (T*100 + Min)
                    K_list.append(K)
                    area.reset()
                print(max(K_list))

            elif sys.argv[2] == "random_optim":
                Min, T, p = run_random_amount_of_trajects_opt(area, amount_trajects, max_time, amount_stations)
                K = p*10000 - (T*100 + Min)
                print(f"score,{K}")
            elif sys.argv[2] == "greedy_random" or sys.argv[2] == "greedy":
                Min, T, p, trajects = run_greedy_random(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
                count = 0
                for a in trajects:
                    stations_str = ', '.join(a)
                    print(f"train_{count},\"[{stations_str}]\"")
                    count += 1
                K = p * 10000 - (T * 100 + Min)
                print(f"score,{K}")
            elif sys.argv[2] == "greedy_random_max":
                K_list = []
                for i in range(10000):
                    Min, T, p = run_greedy_random(area, amount_trajects, max_time, amount_stations)
                    K = p*10000 - (T*100 + Min)
                    K_list.append(K)
                    area.reset()
                print(max(K_list))
            elif sys.argv[2] == "greedy_optim":
                run_greedy_combinations(area, amount_trajects, max_time, amount_stations)
            elif sys.argv[2] == "hill_climbing":
                K = hill_climbing(area, amount_trajects, amount_stations, max_time)[1]
                print(f"score,{K}")
            elif sys.argv[2] == "hill_climbing_max":
                K_list = []
                solution_list = []
                for i in range(10000):
                    sol, K, solution = hill_climbing(area, amount_trajects, amount_stations, max_time)
                    K_list.append(K)
                    solution_list.append(solution)
                    area.reset()
                max_K = max(K_list)
                print(max_K)
                for i in range(len(K_list)):
                    if K_list[i] == max_K:
                        index = i
                
                for i in range(len(solution_list[index])):
                    stations_str = ', '.join(solution_list[index][i])
                    print(f"train_{i + 1},\"[{stations_str}]\"")
            elif sys.argv[2] == "hill_climbing_opt":
                K = hill_climbing_opt(area, amount_trajects, amount_stations, max_time)[1]
                print(f"score,{K}")
            elif sys.argv[2] == "hill_climbing_opt_max":
                K_max = 0
                for i in range(1000):
                    current_solution, K = hill_climbing_opt(area, amount_trajects, amount_stations, max_time)
                    if K >= K_max:
                        K_max = K
                        max_solution = current_solution
                    area.reset()
                for i in range(len(max_solution)):
                    stations_str = ', '.join(max_solution[i].traject_connections)
                    print(f"train_{max_solution[i].train_count},\"[{stations_str}]\"")
                print(K_max)
                K_max = 0

            elif sys.argv[2] == "hill_climbing/greedy":
                K = hill_climbing_greedy(area, amount_trajects, amount_stations, max_time)[1]
                print(f"score,{K}")
            elif sys.argv[2] == "hill_climbing/greedy_max":
                K_list = []
                solution_list = []
                for i in range(10000):
                    sol, K, solution = hill_climbing_greedy(area, amount_trajects, amount_stations, max_time)
                    K_list.append(K)
                    solution_list.append(solution)
                    area.reset()
                max_K = max(K_list)
                print(max_K)
                for i in range(len(K_list)):
                    if K_list[i] == max_K:
                        index = i
                
                for i in range(len(solution_list[index])):
                    stations_str = ', '.join(solution_list[index][i])
                    print(f"train_{i + 1},\"[{stations_str}]\"")

            elif sys.argv[2] == "hill_climbing/greedy_optim":
                K = hill_climbing_greedy_optim(area, amount_trajects, amount_stations, max_time)[1]
                print(f"score,{K}")
            elif sys.argv[2] == "hill_climbing/greedy_optim_max":
                K_list = []
                for i in range(10):
                    K = hill_climbing_greedy_optim(area, amount_trajects, amount_stations, max_time)[1]
                    K_list.append(K)
                    area.reset()
                print(max(K_list))
            elif sys.argv[2] == "double_greedy":
                Min, T, p = double_greedy_random(area, amount_trajects, max_time, amount_stations)
                K = p*10000 - (T*100 + Min)
                print(f"score,{K}")
            else:
                print("usage python3 main.py size algorithm")
    else:
        Min, T, p = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations)
        K = p*10000 - (T*100 + Min)
        print(f"score,{K}")

