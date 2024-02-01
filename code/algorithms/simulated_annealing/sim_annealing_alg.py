"""
Simulated annealing is an iterative algorithm which is very comparable to hill climbing,
the only difference is that we can accept worse solutions with a certain probability.
This probability is based on how much worse the solution is and on the value of a temperature function that
decreases based on how much iterations are already done.

By: Ties Veltman
"""
from code.algorithms.hill_climbing.hill_climbing_alg import evaluate_solution
from code.algorithms.hill_climbing.hill_climbing_alg import generate_solution
from code.algorithms.hill_climbing.hill_climbing_alg import get_neighbors
from code.other.run import run_trajects
from code.other.remove_unnecessary import removing_lines
from code.other.remove_unnecessary import remove_end

import math
import random


def simulated_annealing(area: object, amount_trajects: int,
                        amount_stations: int, max_time: int, initial_temperature: float,
                        exponent_temp: float) -> tuple[float, float, list[list[str]], float, list[float], list[float], list[float]]:
    """
    Perform simulated annealing to optimize the railway schedule.
    Simulated annealing is an iterative algorithm that explores neighboring solutions
    to find an optimal solution based on an acceptance probability of worse neighbors.

    Preconditions:
        - area is an instance of the Rail_NL class.
        - amount_trajects is a positive integer representing the maximum number of train trajects we can choose.
        - amount_stations is a positive integer representing the number of stations present in the current map.
        - max_time is a positive integer representing the maximum time duration for a train route.
        - initial_temperature is a positive float representing the initial temperature for the temperature function.

    Postconditions:
        - Returns a tuple containing:
            - trajects: List of optimized train routes.
            - current_score (int): Score of the optimized solution.
            - scores: List of scores during the optimization process.
            - temperature_list: List of temperatures during the optimization process.
            - p_acceptlist: List of acceptance probabilities during the optimization process.
    """

    # Evaluate a starting position by generating a random solution and calculating what its score is
    current_solution = generate_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area, amount_stations, max_time)
    area.reset()
    temperature = initial_temperature

    total_iterations = 10000
    iterations = 0
    scores = []
    temperature_list = []
    p_acceptlist = []

    # Loop through the total amount of iterations
    while iterations < total_iterations:
        scores.append(current_score)
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time, 1, random_optim = True)
        neighbor = random.choice(neighbors)

        tracks = []
        for track in neighbor:
            tracks.append(track)

        area.reset()
        trajects_result = run_trajects(area, len(tracks), amount_stations, max_time, tracks)
        neighbor_score = trajects_result[0] * 10000 - (len(tracks) * 100 + trajects_result[1])
        area.reset()
        delta_score = current_score - neighbor_score

        # Calculate p_accept, set it to 1 if the neighbor score is higher, set it to 0 if it is negligible (almost 0)
        if delta_score/temperature > 500:
            p_accept = 0
        elif delta_score < 0:
            p_accept = 1
        else:
            p_accept = math.exp(1)**(-delta_score/temperature)
            p_acceptlist.append(p_accept)

        if delta_score < 0 or p_accept > random.random():
            current_solution = neighbor
            current_score = neighbor_score

        # Calculate the temperature value
        temperature = initial_temperature / ((iterations + 1) ** exponent_temp)
        temperature_list.append(temperature)
        iterations += 1

    finaltracks = []
    for track in current_solution:
        finaltracks.append(track)
    area.reset()

    # Remove tracks that decrease the score if we keep them,
    # also remove end stations if they do not contribute to a higher score
    trajects = removing_lines(area, len(finaltracks), amount_stations, max_time, finaltracks)
    fraction_done, time, trajects = remove_end(area, amount_stations, max_time, trajects)

    area.reset()
    final_score = fraction_done * 10000 - (len(trajects) * 100 + time)
    return fraction_done, time, trajects, final_score, scores, temperature_list, p_acceptlist
