from code.algorithms.random_alg import run_random_amount_of_trajects
from code.classes.rail_NL import Rail_NL
from code.algorithms.greedy_random_start import run_greedy_track_random
from code.algorithms.greedy_best_comb import run_greedy_combinations
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.run import run_trajects
from code.algorithms.hill_climbing_alg import evaluate_solution
from code.algorithms.hill_climbing_greedy_alg import get_neighbors_greedy
from code.classes.traject import Traject
from typing import List, Tuple

def list_to_trajects(area: Rail_NL, list_string: List[List[str]]) -> List[Traject]:
    """
    Convert a list containing lists of station names to a list containing traject objects 

    pre:
    - area is an instance of Rail_NL.
    - list_string is a list of strings

    post:
    - Returns a list containing traject objects
    """
    solution = []
    # for every list in list_string, convert the station names to trajects 
    # and add it to solution
    for i in range(len(list_string)):
        traject = area.create_traject(list_string[i][0], area)
        solution.append(traject)
        for j in range(1, len(list_string[i])):
            traject.move(list_string[i][j])
    return solution


def hill_climbing_greedy_comb(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int) -> Tuple[List[Traject], float, List[List[str]]]:
    """
    Perform hill climbing optimization using a combination of the greedy best combination algorithm.

    pre:
    - area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - amount_stations is a positive integer.
    - max_time is a positive integer.

    post:
    - Returns a tuple containing the optimized solution, the objective function value (K), and the list of trajectories.
    """
    # generate a random optimized solution
    current_solution_string = run_greedy_combinations(area, amount_trajects, max_time, amount_stations, True, longer=True)

    # go from list of string stations, to list of trajects
    current_solution = list_to_trajects(area, current_solution_string)

    # calculate the score of this solution
    current_score = evaluate_solution(current_solution, area)

    # set all the connections to "not done"
    area.reset()

    # run algorithm until no improvements are found
    while True:
        # make neighbors
        neighbors = get_neighbors_greedy(current_solution, area, len(current_solution), amount_stations, max_time)
        
        # selecteer the best neighbor (highest K)
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
    for i in range(len(current_solution)):
        current_solution_list.append(current_solution[i].traject_connections)
    
    # remove the trajects that make K lower
    current_solution_list = removing_lines(area, len(current_solution_list), amount_stations, max_time, current_solution_list)

    # print the solution
    for i in range(len(current_solution_list)):
        stations_str = ', '.join(current_solution_list[i])
        print(f"train_{i + 1},\"[{stations_str}]\"")
    
    area.reset()

    # find K for the solution
    K = run_trajects(area, len(current_solution_list), amount_stations, max_time, current_solution_list, False)

    return current_solution, K, current_solution_list
