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
    if sys.argv[3] == "weighted":
        list_powers = [1, 1.25, 1.5, 2, 3, 4, 5, 6, 7]
        max_values = []
        for i in list_powers:
            file = open(f'results_weighted{i}.pickle', 'rb')
            results = pickle.load(file)
            max_values.append(max(results))
            print(f"power: {i}")
            print(f"amount of results, {count}")
            print(f"max, {max(results)}")
            print(f"average, {sum(results) / len(results)}")
            print(f"std, {np.std(results)}")
        plt.plot(max_values, range(len(max_values)))
        plt.show()

    if sys.argv[3] == "plant":
        list_power = [0.5, 1, 1.5, 2, 3, 5]
        for i in list_power:
            file = open(f'plant_power{i}.pickle', 'rb')
            results = pickle.load(file)
            print(max(results))
            if len(results) > 0:
                print(f"average, {sum(results) / len(results)}")

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

    if sys.argv[3] == "hill_climbing" or sys.argv[3] == "hill_climbing_greedy":
        # make list containing the different colors of the lines in the plot
        colors = ["red", "green", "purple", "blue", "orange"]
        index = 0

        list_amount_trajects = [14, 16, 18, 20]
        list_amount_neighbors = [1, 5, 10]
        for q in range(len(list_amount_trajects)):
            list_averages = []
            for r in range(len(list_amount_neighbors)):
                # open the file, corresponding to this loops amount of trajects and neighbors
                file = open(f'experiments/hill_climbing/pickle/results_{list_amount_trajects[q]}_{list_amount_neighbors[r]}.pickle', 'rb')
                # extract the results from this file
                results = pickle.load(file)
                print(results)
                file.close()
                count = 0
                for i in results:
                    count += 1

                # print some interesting measurements of this data
                print(f"amount trajects: {list_amount_trajects[q]}")
                print(f"amount neighbors: {list_amount_neighbors[r]}")
                print(f"amount of results, {count}")
                print(f"max, {max(results)}")
                list_averages.append(max(results))
                print(f"average, {sum(results) / len(results)}")
                print(f"std, {np.std(results)}")
                print()

            # plot the found line
            plt.plot(list_amount_neighbors, list_averages, color=colors[index], label=f"{list_amount_trajects[q]} trajects")
            index += 1

        # complete the plot
        plt.xlabel("Amount of neighbors")
        plt.ylabel("Mean score (K)")
        plt.title("Graph of average score, using the hill climbing algorithm, against amount of neighbors, for different amount of stations (run for 1 minute per starting combination)")
        plt.legend()

        # show the plot
        plt.show()
