"""
Code to find the solution for part 1

by: Mathijs Leons, Team-Trein
"""
from code.algorithms.greedy.greedy_random_start import run_greedy_random
from code.classes.rail_NL import Rail_NL

def find_p(area: Rail_NL, amount_trajects: int, max_time: int, amount_stations:int) -> None:

    # Continues searching until solution is found
    while True:

        # Runs the greedy algorithm to find possible solutions
        Min, T, p, trajects = run_greedy_random(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
        if p == 1:
            count = 1

            # Print out correct solution
            for a in trajects:
                stations_str = ', '.join(a)
                print(f"train_{count},\"[{stations_str}]\"")
                count += 1
            print(f"score,{p * 10000 - (T * 100 + Min)}")
            break
        area.reset()