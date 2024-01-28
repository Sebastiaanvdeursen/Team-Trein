import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL

import itertools as iter
from math import comb

def run_greedy_combinations(area, amount_trajects, max_time, amount_stations,
                             used_for_hill_climbing = False, longer = False):
    """
    function that tries out all combinations of greedy tracks, the longer version
    will remake all tracks for all possible combinations, while longer == False
    will use precalculated tracks

    """
    if longer == False:
        possible = []
        for i in range(0, amount_stations):
            possible.append(run_greedy_track_comb(area, max_time, i, False)[0])
            area.reset()

    results = []
    if longer:
        possible_trajects_combs = list(iter.permutations(range(amount_stations), amount_trajects - 3))
    else:
        possible_trajects_combs = list(iter.combinations(range(amount_stations), amount_trajects))
    amount = comb(amount_stations, amount_trajects)
    if longer == False:
        for i in range(amount):
            visit = []
            for j in possible_trajects_combs[i]:
                visit.append(possible[j])
            results.append(run_trajects(area, amount_trajects, amount_stations, max_time, visit, False))
            area.reset()
        max_index = results.index(max(results))
        area.reset()
        time  = 0
        solution = []
        for j in possible_trajects_combs[max_index]:
            passed, time_track, track = run_greedy_track_comb(area, max_time, j, False)
            time += time_track
            solution.append(track)

    if longer == True:
        best_track = []
        best_score = 0
        for i in possible_trajects_combs:
            current = []
            area.reset()
            for j in i:
                passed, time_track, track = run_greedy_track_comb(area, max_time, j, False)
                current.append(passed)
            area.reset()
            current = removing_lines(area, len(current), amount_stations, max_time, current)
            area.reset()
            current = remove_end(area, amount_stations, max_time, current)
            area.reset()
            score = run_trajects(area, len(current), amount_stations, max_time, current, False)
            if score > best_score:
                best_score = score
                best_track = current

    if longer == False:
        n_done = 0
        for station in area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1

        fraction_done = (n_done / 2) / area.total_connections
    else:
        fraction_done, time = run_trajects(area, len(best_track), amount_stations, max_time, best_track, False, True)
        solution = best_track

    if used_for_hill_climbing == False:
        return time, len(solution), fraction_done, solution
    if used_for_hill_climbing:
        return solution


def run_greedy_track_comb(Area, max_time, number, printed: bool):
    passed = []
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)


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

def run_trajects(area, amount_trajects, amount_stations, max_time,
                  trajects, printed: bool, final = False):
    time = 0
    solution = []
    for i in range(amount_trajects):
        traject = area.create_traject(trajects[i][0], area)
        solution.append(traject)
        for j in range(1, len(trajects[i])):
            traject.move(trajects[i][j])
        time += traject.total_time
        if printed:
            traject.show_current_traject()


    n_done = 0
    for station in area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1

    fraction_done = (n_done / 2) / area.total_connections
    if final:
        return fraction_done, time
    else:
        return fraction_done * 10000 - time - (len(trajects) * 100)

##dit moet worden opgelost
def removing_lines(area, amount_trajects, amount_stations, max_time, trajects):
    area.reset()
    score = run_trajects(area, amount_trajects, amount_stations, max_time, trajects, False)
    area.reset()
    loop_counter = amount_trajects -1
    i = 0
    while True:
        if i == loop_counter or len(trajects) == 1:
            break
        current = []
        j = amount_trajects - 1
        for a in trajects:
            if j != i:
                current.append(a)
            j -= 1
        test = run_trajects(area, len(current), amount_stations, max_time, current, False)
        area.reset()
        if score < test:
            trajects = current
            score = test
        i += 1
    return trajects

def remove_end(area, amount_stations, max_time, trajects):
    area.reset()
    score = run_trajects(area, len(trajects), amount_stations, max_time, trajects, False)
    area.reset()
    while True:
        changes = 0
        for i in range(len(trajects)):
            current = []
            for j in range(len(trajects)):
                if j == i:
                    current.append(trajects[j][:-1])
                else:
                    current.append(trajects[j])
                current_score = run_trajects(area, len(current), amount_stations, max_time, current, False)
                area.reset()
                if current_score > score:
                    trajects = current
                    score = current_score
                    changes += 1
        if changes == 0:
            break
    return trajects


