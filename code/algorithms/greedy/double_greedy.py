"""
Double Greedy is an algorithm based upon the basic greedy algorithm
however we came up with our own heuristic of choosing the shortest path by looking forward
2 connections instead of one

By: Mathijs Leons
"""
from code.classes.rail_NL import Rail_NL
from code.other.remove_unnecessary import remove_end
from code.other.remove_unnecessary import removing_lines

import random

def double_greedy_random(Area: object, amount_trajects: int, max_time: int, amount_stations: int,
                            printed: bool = True) -> [int,  int, float, list[list[str]]]:
    """
    Runs the double greedy algorithm on the provided RailNL object, returns the info and
    and the trajects. The double greedy algorithm selects the station which has the shortest path to a
    second station.

    pre:
        - area object of type Rail_NL both small or large
        - amount_trajects is an int corresponding to the amount of trajects allowed
        - max_time is an int corresponding to the amount of time allowed per traject
        - amount_stations is an int corresponding to the amount of stations in the RailNL object
        - printed is a bool, if True it prints the trajects

    post:
        - Min is an int corresponding to the amount of time used by all trajects
        - len(trajects) is an int
        - fraction done is a float corresponding to the percentage / 100 of the connections used
        - trajects is a list of list of strings with the connections used
    """
    # loads in the list of all the stations within the area as strings
    list_stations = []
    for station_name in Area.stations:
        list_stations.append(station_name)

    # initializes the tracks and runs the algorithm
    trajects = []
    for _ in range(0, amount_trajects):
        numbers = []

        # makes sure that all starting stations are different
        while True:
            random_number = random.randint(0, amount_stations - 1)
            if random_number not in numbers:
                numbers.append(random_number)
                break
        info = run_double_greedy_track(Area, amount_stations, max_time, random_number, list_stations, printed)
        trajects.append(info[2])

    # optimizes and gets the information
    trajects = removing_lines(Area, amount_trajects, amount_stations, max_time, trajects)
    fraction_done, Min, trajects= remove_end(Area, amount_stations, max_time, trajects)

    return Min, len(trajects), fraction_done, trajects

def run_double_greedy_track(Area: Rail_NL, max_time: int, random_number: int, list_stations: list[str], printed: bool = False):
    """
    creates a track based upon the double greedy method

    pre: Area is an object of type RailNL, where the other tracks are already loaded
    """
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

            else:
                for j in Area.stations[list_stations_current[i]].connections:
                    if  Area.stations[list_stations_current[i]].connections[j].done == True:
                        if (random_traject.current_station.connections[list_stations_current[i]].time +
                             3 * Area.stations[list_stations_current[i]].connections[j].time < time):
                            destination = list_stations_current[i]
                            time = 2 * random_traject.current_station.connections[list_stations_current[i]].time

                    elif (random_traject.current_station.connections[list_stations_current[i]].time +
                           Area.stations[list_stations_current[i]].connections[j].time < time):
                        destination = list_stations_current[i]
                        time = random_traject.current_station.connections[list_stations_current[i]].time

        if destination == "":
            went_back += 1
            if went_back > 1:
                break

            if (random_traject.total_time + random_traject.current_station.connections[going_back].time >
                 max_time):
                break
            random_traject.move(going_back)

        else:
            if (random_traject.total_time + random_traject.current_station.connections[destination].time >
                 max_time):
                break
            went_back = 0
            random_traject.move(destination)

    if printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area, random_traject.traject_connections]