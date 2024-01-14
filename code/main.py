from random_alg import run_random_amount_of_trajects
from random_alg_opt import run_random_amount_of_trajects_opt
from rail_NL import Rail_NL
import sys
from greedy_random_start import run_greedy_random
from greedy_best_comb import run_greedy_combinations

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
        if sys.argv[2] == "random":
            Min, T, p = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations)
            K = p*10000 - (T*100 + Min)
            print(f"score,{K}")
        elif sys.argv[2] == "random_opt":
            Min, T, p = run_random_amount_of_trajects_opt(area, amount_trajects, max_time, amount_stations)
            K = p*10000 - (T*100 + Min)
            print(f"score,{K}")
        elif sys.argv[2] == "greedy_random":
            Min, T, p = run_greedy_random(area, amount_trajects, max_time, amount_stations)
            K = p*10000 - (T*100 + Min)
            print(f"score,{K}")
        elif sys.argv[2] == "greedy_optim":
            run_greedy_combinations(map, amount_trajects, max_time, amount_stations)
        else:
            print("usage python3 main.py size algorithm")
    else:
        Min, T, p = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations)
        K = p*10000 - (T*100 + Min)
        print(f"score,{K}")





