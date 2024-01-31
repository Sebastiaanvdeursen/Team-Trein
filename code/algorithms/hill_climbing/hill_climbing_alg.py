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

from typing import List, Tuple
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL

from code.algorithms.random.random_alg import run_random_traject
from code.algorithms.greedy.greedy_random_start import run_greedy_track_random
from code.algorithms.random.random_alg_opt import run_random_traject_opt

from code.other.remove_unnecessary import removing_lines
from code.other.run import run_trajects


def hill_climbing(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int, 
                    amount_neighbors: int = 1, greedy: bool = False, random_optim: bool = False) -> Tuple[List[Traject], float, List[List[str]]]:
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


    # check if both greedy and random_optim are True, to avoid problems
    if greedy == True and random_optim == True:
        greedy = False

    # generate a random solution
    current_solution = generate_solution(area, amount_trajects, amount_stations, max_time, greedy, random_optim)

    # calculate the score of this solution
    current_score = evaluate_solution(current_solution, area, amount_stations, max_time)

    # set all the connections to "not done"
    area.reset()

    # run algorithm until no improvements are found
    while True:
        # make neighbours
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time, amount_neighbors, greedy, random_optim)
        
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

    # find p, Min  for the solution
    p, Min = run_trajects(area, len(current_solution_list), amount_stations, max_time, current_solution_list, False)

    return p, Min, current_solution_list

def generate_solution(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int,
                            greedy: bool = False, random_optim: bool = False) -> List[Traject]:
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
    - Returns a list representing the random solution.
    """
    solution = []

    for i in range(amount_trajects):
        if greedy:
            solution.append(run_greedy_track_random(area, amount_stations, max_time, printed=False)[2])
        elif random_optim:
            solution.append(run_random_traject_opt(area, amount_stations, max_time, printed=False)[2])
        else:
            solution.append(run_random_traject(area, amount_stations, max_time, printed=False, info=True)[2])

    return solution

def evaluate_solution(solution: List[Traject], area: Rail_NL, amount_stations, max_time) -> float:
    """
    Evaluate the solution for the hill climbing optimization.

    pre:
    - solution is a list representing the solution.
    - area is an instance of Rail_NL.

    post:
    - Returns a tuple with the objective function value (K), fraction_done, number of trajectories, and total time.
    """
    area.reset()
    solution_list = []
    for i in range(len(solution)):
        solution_list.append(solution[i].traject_connections)
    p, Min = run_trajects(area, len(solution), amount_stations, max_time, solution_list, False)

    # calculate the score function
    K = p * 10000 - (len(solution) * 100 + Min)
    return K

def get_neighbors(solution: List[Traject], area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int, amount_neighbors: int,
                greedy: bool = False, random_optim: bool = False) -> List[List[Traject]]:
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
            
            # replace by the a track of the chosen algorithm
            if greedy == True:
                neighbor[i] = run_greedy_track_random(area, amount_stations, max_time, printed=False)[2]
            elif random_optim == True:
                neighbor[i] = run_random_traject_opt(area, amount_stations, max_time, printed=False)[2]
            else:
                neighbor[i] = run_random_traject(area, amount_stations, max_time, printed=False, info=True)[2]
            area.reset()
            neighbors.append(neighbor) 
    return neighbors
