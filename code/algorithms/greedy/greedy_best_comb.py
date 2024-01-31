"""
brute force method, with amount of possibilities reduced by only considering
greedy tracks. Can only be used on Holland data set or will crash because of
lack of RAM.

By: Mathijs Leons, Team-Trein
"""
import itertools as iter
from math import comb

from code.algorithms.greedy.greedy_random_start import run_greedy_track_random
from code.classes.rail_NL import Rail_NL
from code.classes.traject import Traject
from code.other.run import run_trajects
from code.other.remove_unnecessary import removing_lines
from code.other.remove_unnecessary import remove_end


def run_greedy_combinations(area: Rail_NL, amount_trajects: int, max_time: int, amount_stations: int,
                            longer: bool = False) -> tuple[int,  int, float, list[list[str]]] | list[list[str]]:
    """
    function that tries out all combinations of greedy tracks,
    the longer version will remake all tracks for all possible
    combinations, while longer == False will use precalculated
    tracks, Longer == True creates new tracks
    for each permutation.
    It returns the best combination it finds.

    pre:
    - takes an area object of type railNL, it has to be based upon
      the small map or it will crash
    - the amount of trajects allowed as an int
    - the maximum amount of time per traject as an int
    - the amount of stations in the area object
    - The used for hill climbing bool has to be False unless
    for that specific use. Longer is a bool.

    post:
    - returns the best combination/ permutation it can find as list of list
    - returns a time integer
    - the len(list) as an int
    - fraction of connections used as a float
    """
    # Loads in the list of stations as strings
    list_stations = []
    for station_name in area.stations:
        list_stations.append(station_name)

    # Pre determines the routes for if longer is false,
    # this is done using the greedy_track function
    if not longer:
        possible = []
        for i in range(0, amount_stations):
            # runs the greedy algorithm on each station with a clean area each time
            output = run_greedy_track_random(area, amount_stations, max_time,
                                             start=i, printed=False,
                                             list_stations=list_stations)
            possible.append(output[2].traject_connections)
            area.reset()

    results = []

    # Makes all the combinations/ permutations in to a list, depending on what is needed
    if longer:
        possible_trajects_combs = list(iter.permutations(range(amount_stations),
                                                         amount_trajects - 3))
    else:
        possible_trajects_combs = list(iter.combinations(range(amount_stations),
                                                         amount_trajects))
        amount = comb(amount_stations, amount_trajects)

    # If longer is false it loops to all possible combinations
    # using the pre determined tracks
    if not longer:
        for i in range(amount):
            visit = []

            # Load in the correct list of strings to run the track
            for j in possible_trajects_combs[i]:
                visit.append(possible[j])

            # Run the track and save the score
            fraction_done, Min = run_trajects(area, amount_trajects, amount_stations,
                                              max_time, visit)
            k = fraction_done * 10000 - (len(visit) * 100 + Min)
            results.append(k)
            area.reset()

        # Find the maximum value of all the combinations that where tried
        max_index = results.index(max(results))
        area.reset()
        time = 0
        solution = []
        for j in possible_trajects_combs[max_index]:
            info = run_greedy_track_random(area, amount_stations, max_time, list_stations,
                                           False, False, start=j)
            time_track = info[0]
            track = info[2].traject_connections
            time += time_track
            solution.append(track)

        best_track = solution

    # Runs trough all starting startion permutations and creates new tracks for each
    if longer:
        best_track = []
        best_score: float = 0
        for combo in possible_trajects_combs:
            current = []
            info_gen: list[tuple[int, Rail_NL, Traject]] = []

            # Reset the railNL object for each iteration
            area.reset()
            for j in combo:
                info_gen = [run_greedy_track_random(area, amount_stations, max_time, list_stations,
                                                    False, False, start=j)]
                time_track = info_gen[0][0]
                passed = info_gen[0][2].traject_connections
                current.append(passed)

            # Optimize the results and calculate the value
            current = removing_lines(area, len(current), amount_stations, max_time, current)
            current_fraction_done, current_time, current = remove_end(area, amount_stations, max_time, current)
            score = current_fraction_done * 10000 - (len(current) * 100 + current_time)

            # Saving the highest score/ best tracks
            if score > best_score:
                best_score = score
                best_track = current
                fraction_done = current_fraction_done
                time = current_time

    # Calculates P for longer since it hasn't before
    if not longer:
        n_done = 0
        for station in area.stations.values():
            for connection in station.connections.values():
                if connection.done:
                    n_done += 1

        fraction_done = (n_done / 2) / area.total_connections

    # Returns the correct info
    return time, len(best_track), fraction_done, best_track

