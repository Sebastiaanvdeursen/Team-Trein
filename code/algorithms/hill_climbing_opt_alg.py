from typing import List, Tuple
from code.algorithms.random_alg_opt import run_random_traject_opt
from code.algorithms.hill_climbing_alg import evaluate_solution
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.run import run_trajects
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL
import random
import copy

def hill_climbing_opt(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int, amount_neighbors = 1) -> Tuple[List[Traject], float, List[List[str]]]:
    """
    Perform hill climbing optimization to improve a random optimized solution.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.

    post:
    - Returns a tuple containing the optimized solution, the objective function value K, and the list of trajectories.
    """
    # generate a random solution
    current_solution = generate_random_optim_solution(area, amount_trajects, amount_stations, max_time)

    # calculate the score of this solution
    current_score = evaluate_solution(current_solution, area, amount_stations, max_time)

    # set all the connections to "not done"
    area.reset()

    # run algorithm until no improvements are found
    while True:
        # make neighbours
        neighbors = get_neighbors_random_opt(current_solution, area, amount_trajects, amount_stations, max_time, amount_neighbors)
        
        # select the best neighbor (highest K)
        best_neighbor = max(neighbors, key=lambda neighbor: evaluate_solution(neighbor, area, amount_stations, max_time))

        eval_sol = evaluate_solution(best_neighbor, area, amount_stations, max_time)

        # if best neighbor is better than current solution, replace current_solution
        # by best neighbor and start again
        if eval_sol > current_score:
            current_solution = best_neighbor
            current_score = eval_sol
            area.reset()
        
        # if not, stop algorithm
        else:
            break
    
    # make a list of the trajects of the solution, containing the 
    # station names (not traject objects)
    current_solution_list = []
    for i in range(amount_trajects):
        current_solution_list.append(current_solution[i].traject_connections)
    
    # remove the trajects that make K lower
    current_solution_list = removing_lines(area, amount_trajects, amount_stations, max_time, current_solution_list)
    
    area.reset()

    # find p, Min for the solution
    p, Min = run_trajects(area, len(current_solution_list), amount_stations, max_time, current_solution_list, False)

    return p, Min, current_solution_list

def generate_random_optim_solution(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int) -> List[Traject]:
    """
    Generate a random optimized solution for the hill climbing optimization.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.

    post:
    - Returns a list representing the random optimized solution.
    """
    solution = []
    for i in range(amount_trajects):
        solution.append(run_random_traject_opt(area, amount_stations, max_time, True)[2])

    return solution


def get_neighbors_random_opt(solution: List[Traject], area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int, amount_neighbors: int) -> List[List[Traject]]:
    """
    Generate neighbors for the hill climbing optimization.

    pre:
    - solution is a list representing the current solution.
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.

    post:
    - Returns a list of neighbors.
    """
    neighbors = []

    # replace every traject of solution
    for i in range(amount_trajects):
        for j in range(amount_neighbors):
            # make amount_neighbors neighbors for every traject in solution
            neighbor = solution[:]
            neighbor[i] = run_random_traject_opt(area, amount_stations, max_time, True)[2]
            neighbors.append(neighbor)
            area.reset()
    return neighbors
