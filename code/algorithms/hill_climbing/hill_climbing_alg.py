"""
Algorithms & Heuristics

Group: Team-Trein

Hill Climbing starts with a solution and then tries to improve on this solution by replacing
parts of the solution. If option greedy is chosen, the algorithm starts with a greedy track
and replaces tracks by greedy tracks. If option random_optim is chosen, the algorithm starts with a random
optimized track and replaces tracks by random optimized tracks. If both are not chosen, the algorithm starts
with a random track and replaces tracks by random tracks.

By: Sebastiaan van Deursen
"""


from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL

from code.algorithms.greedy.greedy_random_start import run_greedy_random
from code.algorithms.random.random_alg import run_random_amount_of_trajects
from code.algorithms.random.random_alg_opt import run_random_amount_of_trajects_opt

from code.algorithms.greedy.greedy_random_start import run_greedy_track_random
from code.algorithms.random.random_alg import run_random_traject
from code.algorithms.random.random_alg_opt import run_random_traject_opt

from code.other.remove_unnecessary import removing_lines
from code.other.run import run_trajects


def hill_climbing(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int, amount_neighbors: int = 1,
                  greedy: bool = False, random_optim: bool = False, 
                  plot: bool = False) -> tuple[float, int, list[list[str]]] | tuple[float, int, list[list[str]], list[float]]:
    """
    Perform hill climbing optimization to improve a random solution.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.

    post:
    - returns a tuple containing the optimized solution, the objective function value K, and the list of trajects.
    """
    # make list of stations in area, to use for run_greedy_track_random
    list_stations = []
    for station_name in area.stations:
        list_stations.append(station_name)


    # generate a random solution
    current_solution = generate_solution(area, amount_trajects, amount_stations, max_time,
                                         greedy, random_optim)

    # calculate the score of this solution
    current_score = evaluate_solution(current_solution, area, amount_stations, max_time)

    if plot:
        score_list = []
        score_list.append(current_score)

    # set all the connections to "not done"
    area.reset()

    # run algorithm until no improvements are found
    while True:
        # make neighbours
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time, amount_neighbors,
                                  list_stations, greedy, random_optim)

        # select the best neighbor (highest K)
        best_neighbor = max(neighbors, key=lambda neighbor: evaluate_solution(neighbor, area, amount_stations, max_time))

        eval_sol = evaluate_solution(best_neighbor, area, amount_stations, max_time)

        if plot:
            score_list.append(eval_sol)

        # if best neighbor is better than current solution, replace current_solution
        # by best neighbor and start again
        if eval_sol > current_score:
            current_solution = best_neighbor
            current_score = eval_sol
            area.reset()

        # if not, stop algorithm
        else:
            break

    # remove the trajects that make K lower
    current_solution = removing_lines(area, len(current_solution), amount_stations, max_time, current_solution)

    area.reset()

    # find p, Min  for the solution
    p, Min = run_trajects(area, len(current_solution), amount_stations, max_time, current_solution, False)

    if plot:
        return p, Min, current_solution, score_list
    return p, Min, current_solution


def generate_solution(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int,
                      greedy: bool = False, random_optim: bool = False) -> list[Traject]:
    """
    Generate a solution for the hill climbing optimization.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.
    - greedy is a bool.
    - random_optim is a bool.

    post:
    - returns a list representing the random solution.
    """
    if greedy:
        solution = run_greedy_random(area, amount_trajects, max_time, amount_stations,
                                     used_for_hill_climbing=True, printed=False, info=True)[3]
    elif random_optim:
        solution = run_random_amount_of_trajects_opt(area, amount_trajects, max_time, amount_stations,
                                          printed=False, info=True)[3]
    else:
        solution = run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations,
                                      printed=False, info=True)[3]
    return solution


def evaluate_solution(solution: list[Traject], area: Rail_NL, amount_stations, max_time) -> float:
    """
    Evaluate the solution for the hill climbing optimization.

    pre:
    - solution is a list representing the solution.
    - area is an instance of Rail_NL.

    post:
    - returns a tuple with the objective function value (K), fraction_done, number of trajectories, and total time.
    """
    area.reset()
    p, Min = run_trajects(area, len(solution), amount_stations, max_time, solution, False)

    # calculate the score function
    K = p * 10000 - (len(solution) * 100 + Min)
    return K


def get_neighbors(solution: list[Traject], area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int,
                  amount_neighbors: int, list_stations: list[str] = None, greedy: bool = False,
                  random_optim: bool = False) -> list[list[Traject]]:
    """
    Generate neighbors for the hill climbing optimization.

    pre:
    - solution is a list representing the current solution.
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.

    post:
    - returns a list of neighbors.
    """
    neighbors = []

    # replace every traject of solution
    for i in range(len(solution)):
        for j in range(amount_neighbors):
            neighbor = solution[:]

            # replace by the a track of the chosen algorithm
            if greedy:
                neighbor[i] = run_greedy_track_random(area, amount_stations, max_time, list_stations,
                                                      printed=False)[2].traject_connections
            elif random_optim:
                neighbor[i] = run_random_traject_opt(area, amount_stations, max_time, 
                                                     printed=False)[2].traject_connections
            else:
                neighbor[i] = run_random_traject(area, amount_stations, max_time, 
                                                 printed=False, info=True)[2].traject_connections
            area.reset()
            neighbors.append(neighbor)
    return neighbors
