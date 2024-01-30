import sys
from code.classes.rail_NL import Rail_NL
from code.algorithms.hill_climbing.hill_climbing_alg import hill_climbing
import time
import pickle
import numpy as np
import matplotlib.pyplot as plt
from typing import Any, List

def test_hill_climbing(area: Rail_NL, amount_trajects: int, max_time: int, amount_stations: int, time_to_run: float) -> None:
    """
    Test the hill climbing algorithm with different parameters and generate a plot.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - max_time is a positive integer.
    - amount_stations is a positive integer.
    - time_to_run is a positive float.
    """
    # make lists containing the values to test for amount_trajects and amount_neighbors
    list_amount_trajects = [14, 16, 18, 20]
    list_amount_neighbors = [1, 5, 10]

    # loop through all of these values
    for i in range(len(list_amount_trajects)):
        for j in range(len(list_amount_neighbors)):
            # store the starting time in "start"
            start = time.time()
            results = []
            best = []
            current_max = 0

            # loop until time is over time_to_run
            while True:
                if (time.time() - start) / 60 > time_to_run:
                    break
                result = hill_climbing(area, list_amount_trajects[i], amount_stations, max_time, amount_neighbors=list_amount_neighbors[j])
                current_traject = result[2]

                # calculate the score (K)
                score = result[0] * 10000 - (len(current_traject) * 100 + result[1])

                # set all connections to "not done"
                area.reset()

                # if score is better than the current best score, replace current best solution by solution
                if score > current_max:
                    current_max = score
                    best = current_traject
                results.append(score)

                # write results to pickle file
                file_name = f'experiments/hill_climbing/pickle/results_{list_amount_trajects[i]}_{list_amount_neighbors[j]}.pickle'
                with open(file_name, 'wb') as f:
                    pickle.dump(results, f)

    # make list containing the different colors of the lines in the plot
    colors = ["red", "green", "purple", "blue", "orange"]
    index = 0

    for q in range(len(list_amount_trajects)):
        list_averages = []
        for r in range(len(list_amount_neighbors)):
            # open the file, corresponding to this loops amount of trajects and neighbors
            file = open(f'experiments/hill_climbing/pickle/results_{list_amount_trajects[q]}_{list_amount_neighbors[r]}.pickle', 'rb')

            # extract the results from this file
            results = pickle.load(file)
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
