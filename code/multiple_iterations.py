from random_alg import run_random_amount_of_trajects
from random_alg_opt import run_random_amount_of_trajects_opt
from greedy_random_start import run_greedy_random
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