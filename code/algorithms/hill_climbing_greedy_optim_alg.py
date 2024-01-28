from code.algorithms.random_alg import run_random_amount_of_trajects
from code.classes.rail_NL import Rail_NL
from code.algorithms.greedy_random_start import run_greedy_track_random
from code.algorithms.greedy_best_comb import run_greedy_combinations
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.greedy_best_comb import run_trajects
from code.algorithms.hill_climbing_alg import evaluate_solution
from code.algorithms.hill_climbing_greedy_alg import get_neighbors_greedy


def hill_climbing_greedy_optim(area, amount_trajects, amount_stations, max_time):
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
    current_solution = run_greedy_combinations(area, amount_trajects, max_time, amount_stations, True)

    # calculate the score of this solution
    current_score = evaluate_solution(current_solution, area)

    # set all the connections to "not done"
    area.reset()

    # run algorithm until no improvements are found
    while True:
        # make neighbors
        neighbors = get_neighbors_greedy(current_solution, area, amount_trajects, amount_stations, max_time)
        
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