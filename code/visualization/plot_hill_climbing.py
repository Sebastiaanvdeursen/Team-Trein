"""
Algorithms & Heuristics

Group: Team-Trein

The Plot_hill_climbing function is used to visualize the improvement through the
iterations of the hill climbing algorithm

By: Sebastiaan van Deursen
"""


from code.algorithms.hill_climbing.hill_climbing_alg import hill_climbing
from code.classes.rail_NL import Rail_NL
import matplotlib.pyplot as plt


def Plot_hill_climbing(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int, number_iterations,
                       amount_neighbors: int, greedy: bool, random_optim: bool):
    """
    Perform hill climbing optimization and plot the improvement of the score through iterations.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.
    - amount_neighbors is a positive integer.
    - greedy is a bool indicating whether to use the greedy algorithm.
    - random_optim is a bool indicating whether to use random optimization.

    post:
    - Performs hill climbing optimization on the given parameters.
    - Plots the improvement of the score through iterations.
    """
    result = hill_climbing(area, amount_trajects, amount_stations, max_time, number_iterations, amount_neighbors,
                           greedy, random_optim, plot=True)
    score_list = result[3]
    x_list = range(1, len(score_list) + 1)
    plt.plot(x_list, score_list, color="blue")
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    if not greedy and not random_optim:
        plt.title('Hill Climbing Random Netherlands')
    if greedy:
        plt.title('Hill Climbing Greedy Netherlands')
    plt.show()
