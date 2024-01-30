import pickle
import math
import matplotlib.pyplot as plt
import numpy as np
import sys

if __name__ == "__main__":
    if sys.argv[3] == "annealing":
        file = open('../../results_900_0.4375.pickle', 'rb')
        results = pickle.load(file)
        file.close()
        count = 0
        for i in results:
            count += 1
        print(f"amount of results, {count}")
        print(f"max, {max(results)}")
        print(f"average, {sum(results) / len(results)}")
        print(f"std, {np.std(results)}")


    # file = open('results.pickle', 'rb')
    # results = pickle.load(file)
    # file.close()

    # plt.plot(range(len(results)), results)
    # plt.show()
    if sys.argv[3] == "greedy":
        file = open('experiments.greedy.results.pickle', 'rb')
        results = pickle.load(file)
        count = 0
        amount = 0
        for i in results:
            count += 1
        print(i)
        if i == 9210.0:
            amount += 1
        prob = amount/count
        print(count)
        confidence_int = prob - (1.96 * math.sqrt(((prob * (1 - prob)) / count)))
        print(confidence_int)
        print("using p")
        print(f" 90% = {math.log(0.1, 1- prob)}")
        print(f" 99% = {math.log(0.01, 1- prob)}")
        print(f" 99.9% = {math.log(0.001, 1- prob)}")
        print(f" 99.99% = {math.log(0.0001, 1- prob)}")
        print(f" 99.999% = {math.log(0.00001, 1- prob)}")
        print(f" 99.9999% = {math.log(0.000001, 1- prob)}")
        print(f" 99.99999% = {math.log(0.0000001, 1- prob)}")
        print(f" 99.999999% = {math.log(0.00000001, 1- prob)}")
        print(f"using 97.5% confidence interval")
        print(f" 90% = {math.log(0.1, 1- confidence_int)}")
        print(f" 99% = {math.log(0.01, 1- confidence_int)}")
        print(f" 99.9% = {math.log(0.001, 1- confidence_int)}")
        print(f" 99.99% = {math.log(0.0001, 1- confidence_int)}")
        print(f" 99.999% = {math.log(0.00001, 1- confidence_int)}")
        print(f" 99.9999% = {math.log(0.000001, 1- confidence_int)}")
        print(f" 99.99999% = {math.log(0.0000001, 1- confidence_int)}")
        print(f" 99.999999% = {math.log(0.00000001, 1- confidence_int)}")
