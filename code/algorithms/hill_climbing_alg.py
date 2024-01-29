from typing import List, Tuple
from code.classes.traject import Traject
from code.algorithms.random_alg import run_random_traject, run_random_amount_of_trajects
from code.classes.rail_NL import Rail_NL
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.run import run_trajects
import random

def hill_climbing(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int, amount_neighbors: int = 1) -> Tuple[List[Traject], float, List[List[str]]]:
    """
    Perform hill climbing optimization to improve a random solution.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.

    post:
    - Returns a tuple containing the optimized solution, the objective function value K, and the list of trajectories.
    """
    # generate a random solution
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)

    # calculate the score of this solution
    current_score = evaluate_solution(current_solution, area)

    # set all the connections to "not done"
    area.reset()

    # run algorithm until no improvements are found
    while True:
        # make neighbours
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time, amount_neighbors)
        
        # select the best neighbor (highest K)
        best_neighbor = max(neighbors, key=lambda neighbor: evaluate_solution(neighbor, area))

        eval_sol = evaluate_solution(best_neighbor, area)

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

    # print the solution
    for i in range(len(current_solution_list)):
        stations_str = ', '.join(current_solution_list[i])
        print(f"train_{i + 1},\"[{stations_str}]\"")
    
    area.reset()

    # find K for the solution
    K = run_trajects(area, len(current_solution_list), amount_stations, max_time, current_solution_list, False)

    return current_solution, K, current_solution_list

def generate_random_solution(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int) -> List[Traject]:
    """
    Generate a random solution for the hill climbing optimization.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.

    post:
    - Returns a list representing the random solution.
    """
    solution = []

    for i in range(amount_trajects):
        solution.append(run_random_traject(area, amount_stations, max_time, printed=False, info=True)[2])

    return solution

def evaluate_solution(solution: List[Traject], area: Rail_NL) -> float:
    """
    Evaluate the solution for the hill climbing optimization.

    pre:
    - solution is a list representing the solution.
    - area is an instance of Rail_NL.

    post:
    - Returns a tuple with the objective function value (K), fraction_done, number of trajectories, and total time.
    """
    # calculate the total time of the solution
    total_time = 0
    for i in range(0, len(solution)):
        total_time += solution[i].total_time

    # calculate the fraction of done trajects
    n_done = 0
    for station in area.stations.values():
        for connection in station.connections.values():
            if connection.done:
                n_done += 1
    fraction_done = (n_done / 2) / area.total_connections

    # calculate the score function
    K = fraction_done * 10000 - (len(solution) * 100 + total_time)
    return K

def get_neighbors(solution: List[Traject], area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int, amount_neighbors: int) -> List[List[Traject]]:
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
            neighbor = solution[:]
            neighbor[i] = run_random_traject(area, amount_stations, max_time, printed=False, info=True)[2]
            neighbors.append(neighbor)
            area.reset()
    return neighbors
