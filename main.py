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

from code.classes.rail_NL import Rail_NL

import random
import matplotlib.pyplot as plt
import sys


def iterate(area, amount_trajects, max_time, amount_stations):
    if sys.argv[2] == "random_optim":
        results = []
        p_scores = []
        for i in range(0, int(sys.argv[3])):
            print(i)
            Min, T, p = run_random_amount_of_trajects_opt(area, amount_trajects, max_time, amount_stations - 1)
            area.reset()
            p_scores.append(p)
            results.append(p*10000 - (T*100 + Min))
        print(max(p_scores))
        print(max(results))
        f = Fitter(results, distributions = ["norm"])
        f.fit()
        f.summary()
        ##plt.hist(results, int(20))
        ##plt.show()
    if sys.argv[2] == "greedy_random" or sys.argv[2] == "greedy":
        results = []
        p_scores = []
        for i in range(0, int(sys.argv[3])):
            Min, T, p = run_greedy_random(area, amount_trajects, max_time, amount_stations)
            area.reset()
            p_scores.append(p)
            results.append( p * 10000 - (T * 100 + Min))
        print(f"highest = {max(results)}")
    else:
        results = []
        p_scores = []
        for i in range(0, int(sys.argv[3])):
            print(i)
            Min, T, p = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations - 1)
            area.reset()
            p_scores.append(p)
            results.append(p*10000 - (T*100 + Min))
        print(max(p_scores))
        ##f = Fitter(results)
        ##f.fit()
        ##f.summary()
        print(sum(results) / int(sys.argv[3]))
        plt.hist(results, int(100))
        plt.show()

def find_p(area, amount_trajects, max_time, amount_stations):
    while True:
        print("new random attempt")
        Min, T, p = run_greedy_random(area, amount_trajects, max_time, amount_stations)
        if p == 1:
            print(p * 10000 - (T * 100 + Min))
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
            iterate(area, amount_trajects, max_time, amount_stations)
        else:
            if sys.argv[2] == "simulated" or sys.argv[2] == "annealing":
                K = simulated_annealing(area, amount_trajects, amount_stations, max_time, 1000)[1]
                print(f"score, {K}")
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
                Min, T, p = run_greedy_random(area, amount_trajects, max_time, amount_stations)
                K = p*10000 - (T*100 + Min)
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
                run_greedy_combinations(map, amount_trajects, max_time, amount_stations)
            elif sys.argv[2] == "hill_climbing":
                K = hill_climbing(area, amount_trajects, amount_stations, max_time)[1]
                print(f"score,{K}")
            elif sys.argv[2] == "hill_climbing_max":
                K_list = []
                for i in range(10000):
                    K = hill_climbing(area, amount_trajects, amount_stations, max_time)[1]
                    K_list.append(K)
                    area.reset()
                print(max(K_list))
            elif sys.argv[2] == "hill_climbing_opt":
                K = hill_climbing_opt(area, amount_trajects, amount_stations, max_time)[1]
                print(f"score,{K}")
            elif sys.argv[2] == "hill_climbing_opt_max":
                K_max = 0
                for i in range(10000):
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
                for i in range(10000):
                    K = hill_climbing_greedy(area, amount_trajects, amount_stations, max_time)[1]
                    K_list.append(K)
                    area.reset()
                print(max(K_list))
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

