import csv
import random
import sys
import itertools as iter
from math import comb

from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL
from code.other.run import run_trajects
from code.other.remove_unnecessary import removing_lines
from code.other.remove_unnecessary import remove_end


def run_greedy_combinations(area: Rail_NL, amount_trajects: int, max_time: int, amount_stations: int,
                            used_for_hill_climbing: bool = False,
                            longer: bool = False) -> tuple[int,  int, float, list[list[str]]] | list[list[str]]:
    """
    function that tries out all combinations of greedy tracks, the longer version
    will remake all tracks for all possible combinations, while longer == False
    will use precalculated tracks, Longer == True creates new tracks for each permutation.
    It returns the best combination it finds

    pre:
    - takes an area object of type railNL, it has to be based upon the small map
    or it will crash,
    - the amount of trajects allowed as an int
    - the maximum amount of time per traject as an int
    - the amount of stations in the area object
    - The used for hill climbing bool has to be False unless
    for that specific use. Longer is a bool.

    post:
    - returns the best combination/ permutation it can find as list of list
    - if not used for hill climbing:
        - returns a time integer
        - the len(list) as an int
        - fraction of connections used as a float
    """
    # pre determines the routes for if longer is false, this is done using the greedy_track function
    list_stations = []

    for station_name in area.stations:
        list_stations.append(station_name)
    if longer == False:
        possible = []
        for i in range(0, amount_stations):
            possible.append(run_greedy_track_comb(area, max_time, i, False, list_stations)[0])
            area.reset()

    results = []


    # makes all the combinations/ permutations in to a list, depending on what is needed
    if longer:
        possible_trajects_combs = list(iter.permutations(range(amount_stations), amount_trajects - 3))
    else:
        possible_trajects_combs = list(iter.combinations(range(amount_stations), amount_trajects))
    amount = comb(amount_stations, amount_trajects)

    # if longer is false it loops to all possible combinations using the pre determined tracks
    if longer == False:
        for i in range(amount):
            visit = []
            for j in possible_trajects_combs[i]:
                visit.append(possible[j])
            fraction_done, Min = run_trajects(area, amount_trajects, amount_stations, max_time, visit)
            k = fraction_done * 10000 - (len(visit) * 100 + Min)
            results.append()
            area.reset()

        #find the maximum value of all the combinations that where tried
        max_index = results.index(max(results))
        area.reset()
        time  = 0
        solution = []
        for j in possible_trajects_combs[max_index]:
            passed, time_track, track = run_greedy_track_comb(area, max_time, j, False, list_stations)
            time += time_track
            solution.append(track)

    # runs trough all starting startion permutations and creates new tracks for each
    if longer == True:
        best_track = []
        best_score = 0
        for i in possible_trajects_combs:
            current = []

            # reset the railNL object for each iteration
            area.reset()
            for j in i:
                passed, time_track, track = run_greedy_track_comb(area, max_time, j, False, list_stations)
                current.append(passed)

            # optimize the results and calculate the value
            current = removing_lines(area, len(current), amount_stations, max_time, current)
            current_fraction_done, current_time, current = remove_end(area, amount_stations, max_time, current)
            score = current_fraction_done * 10000 - (len(current) * 100 + current_time)

            # saving the highest score/ best tracks
            if score > best_score:
                best_score = score
                best_track = current
                fraction_done = current_fraction_done
                time = current_time

    if longer == False:
        n_done = 0
        for station in area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1

        fraction_done = (n_done / 2) / area.total_connections

    if used_for_hill_climbing == False:
        return time, len(best_track), fraction_done, best_track
    if used_for_hill_climbing:
        return solution


def run_greedy_track_comb(Area, max_time: int, number: int, printed: bool, list_stations: list[str]) -> tuple[list[list[str]], int, Traject]:
    passed = []


    random_traject = Area.create_traject(list_stations[number], Area)
    passed.append(list_stations[number])
    went_back = 0
    while True:
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)
        destination = ""
        time = 200
        going_back = ""
        for i in range(len(random_traject.current_station.connections)):
            if random_traject.current_station.connections[list_stations_current[i]].done == True:
                if going_back == "":
                    going_back = list_stations_current[i]
                elif (random_traject.current_station.connections[going_back].time >
                       random_traject.current_station.connections[list_stations_current[i]].time):
                    going_back = list_stations_current[i]
            elif random_traject.current_station.connections[list_stations_current[i]].time < time:
                destination = list_stations_current[i]
                time = random_traject.current_station.connections[list_stations_current[i]].time
        if destination == "":
            went_back += 1
            if went_back > 1:
                break
            if going_back != "":
                if random_traject.total_time + random_traject.current_station.connections[going_back].time > max_time:
                    break
                passed.append(going_back)
                random_traject.move(going_back)
            else:
                break
        else:
            if random_traject.total_time + random_traject.current_station.connections[destination].time > max_time:
                break
            else:
                went_back = 0
                passed.append(destination)
                random_traject.move(destination)
    if printed:
        random_traject.show_current_traject()
    return passed, random_traject.total_time, random_traject