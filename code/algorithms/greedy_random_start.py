import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.remove_unnecessary import remove_end
from code.algorithms.run import run_trajects

def run_greedy_random(Area: Rail_NL, amount_trajects: int, max_time: int,
                       amount_stations: int, used_for_hill_climbing: bool = False,
                       printed: bool = True, info: bool = False
                       ) -> tuple[int, int, float] | tuple[int, int, float, list[list[str]]]:
    """
    runs the greedy algorithm with random starting stations, runs removing_lines and remove_end to
    improve the trajects

    pre:
        - area object of type Rail_NL both small or large
        - amount_trajects is an int corresponding to the amount of trajects allowed
        - max_time is an int corresponding to the amount of time allowed per traject
        - used_for_hill_climbing is a bool
        - printed is a bool, if positive the trajects are printed out instead of returned
        - info is a bool that returns that makes the function return the trajects too

    post:
        - amount of time spent by trajects as int
        - amount of trajects used as int
        - the fraction of connections used as a float
        - if info == True:
            - the trajects as list[list[str]]
    """
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

    time = []
    track_info = []
    trajects = []
    for i in range(0, amount_trajects):
        track_info = run_greedy_track_random(Area, amount_stations, max_time,
                                              used_for_hill_climbing, printed)
        time.append(track_info[0])
        trajects.append(track_info[2].traject_connections)
    time = sum(time)

    if used_for_hill_climbing == False:
        trajects = removing_lines(Area, amount_trajects, amount_stations, max_time, trajects)
        fraction_done, time, trajects = remove_end(Area, amount_stations, max_time, trajects)

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

def run_greedy_track_random(Area, amount_stations, max_time, used_for_hill_climbing,
                             printed = True) -> tuple[int, Rail_NL, Traject]:
    """
    runs a greedy track, always chooses the shortest connection that has not been used
    if no unused track is available it uses the shortest done connection.

    pre:

    post:

    """
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

            if (random_traject.total_time + random_traject.current_station.connections[going_back].time
                 > max_time):
                break
            if going_back != "":
                random_traject.move(going_back)
            else:
                break
        else:
            if (random_traject.total_time + random_traject.current_station.connections[destination].time
            > max_time):
                break
            went_back = 0
            random_traject.move(destination)

    if used_for_hill_climbing == False and printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area, random_traject]