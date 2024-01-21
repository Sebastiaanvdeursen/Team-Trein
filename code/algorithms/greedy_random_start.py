import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.greedy_best_comb import run_trajects

def run_greedy_random(Area, amount_trajects, max_time, amount_stations, used_for_hill_climbing = False, printed = True, info = False):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

    time = []
    track_info = []
    trajects = []
    for i in range(0, amount_trajects):
        track_info = run_greedy_track_random(Area, amount_stations, max_time, used_for_hill_climbing, printed)
        time.append(track_info[0])
        trajects.append(track_info[2].traject_connections)
    time = sum(time)

    if used_for_hill_climbing == False:
        Area.reset()
        trajects = removing_lines(Area, amount_trajects, amount_stations, max_time, trajects)
        Area.reset()
        fraction_done, time = run_trajects(Area, len(trajects), amount_stations, max_time, trajects, False, True)
    else:
        n_done = 0
        for station in Area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1
        fraction_done = (n_done / 2) / Area.total_connections
    if info:
        return time, len(trajects), fraction_done, trajects
    return time, len(trajects), fraction_done

def run_greedy_track_random(Area, amount_stations, max_time, used_for_hill_climbing, printed = True):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

    random_number = random.randint(0, amount_stations - 1)

    random_traject = Area.create_traject(list_stations[random_number], Area)
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

            random_traject.move(going_back)
        else:
            if random_traject.total_time + random_traject.current_station.connections[destination].time > max_time:
                break
            went_back = 0
            random_traject.move(destination)

    if used_for_hill_climbing == False and printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area, random_traject]