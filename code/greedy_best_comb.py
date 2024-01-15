import csv
import random
import sys
from station import Station
from traject import Traject
from rail_NL import Rail_NL
import itertools as iter
from math import comb

def run_greedy_combinations(map, amount_trajects, max_time, amount_stations):
    possible = []
    area = Rail_NL(map, amount_trajects, amount_stations, max_time)
    for i in range(0, amount_stations):
        possible.append(run_greedy_track(area, max_time, i))
        area.reset()

    results = []
    possible_trajects_combs = list(iter.combinations(range(amount_stations), amount_trajects - 3))
    amount = comb(amount_stations, amount_trajects - 3)
    area = Rail_NL(map, amount_trajects, amount_stations, max_time)
    for i in range(amount):
        visit = []
        for j in possible_trajects_combs[i]:
            visit.append(possible[j])
        results.append(run_trajects(area, amount_trajects, amount_stations, max_time, visit, False))
        area.reset()
    max_index = results.index(max(results))
    visit = []
    for j in possible_trajects_combs[max_index]:
        print(j)
        visit.append(possible[j])
    run_trajects(area, amount_trajects, amount_stations, max_time, visit, True)
    print(f"score,{max(results)}")


def run_greedy_track(Area, max_time, number):
    passed = []
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)


    random_traject = Area.create_traject(list_stations[number], Area)
    print(list_stations[number])
    passed.append(list_stations[number])
    went_back = 0
    while True:
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)
        destination = ""
        time = 200

        for i in range(len(random_traject.current_station.connections)):
            if random_traject.current_station.connections[list_stations_current[i]].done == True:
                going_back = list_stations_current[i]
            elif random_traject.current_station.connections[list_stations_current[i]].time < time:
                destination = list_stations_current[i]
                time = random_traject.current_station.connections[list_stations_current[i]].time
        if destination == "":
            went_back += 1
            if went_back > 1:
                break
            if random_traject.total_time + random_traject.current_station.connections[going_back].time > max_time:
                break
            passed.append(going_back)
            random_traject.move(going_back)
        else:
            if random_traject.total_time + random_traject.current_station.connections[destination].time > max_time:
                break
            went_back = 0
            passed.append(destination)
            random_traject.move(destination)
    print(passed)
    return passed

def run_trajects(area, amount_trajects, amount_stations, max_time, trajects, printed: bool):
    time = 0
    for i in range(amount_trajects - 3):
        traject = area.create_traject(trajects[i][0], area)
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
    return fraction_done * 10000 - time - (len(trajects) * 100)



