from code.algorithms.hill_climbing.hill_climbing_alg import hill_climbing
from code.classes.rail_NL import Rail_NL
import matplotlib.pyplot as plt

def Plot_hill_climbing(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int,
                       amount_neighbors: int, greedy: bool, random_optim: bool):
    result = hill_climbing(area, amount_trajects, amount_stations, max_time, amount_neighbors,
                           plot=True)
    score_list = result[3]
    x_list = range(1, len(score_list) + 1)
    plt.plot(x_list, score_list)
    plt.plot(iterationsplot, scoresplot)
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    plt.title('Simulated Annealing for the Netherlands')
    plt.show()