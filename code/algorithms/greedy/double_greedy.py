"""
Double Greedy is an algorithm based upon the basic greedy algorithm
however we came up with our own heuristic of choosing the shortest
path by looking forward 2 connections instead of one. It however moves
forward only one station and than looks again

By: Mathijs Leons, Team-Trein
"""
from code.classes.rail_NL import Rail_NL
from code.other.remove_unnecessary import remove_end
from code.other.remove_unnecessary import removing_lines

import random


def double_greedy_random(Area: Rail_NL, amount_trajects: int, max_time: int,
                        amount_stations: int, printed: bool = True) -> tuple[int, int, float, list[list[str]]]:
    """
    Runs the double greedy algorithm on the provided RailNL object, returns the info and
    and the trajects. The double greedy algorithm selects the station
    which has the shortest path to a second station.

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

        info = run_double_greedy_track(Area, max_time,
                                       random_number, list_stations, printed)
        trajects.append(info[2])

    # optimizes and gets the information
    trajects = removing_lines(Area, amount_trajects, amount_stations, max_time, trajects)
    fraction_done, Min, trajects = remove_end(Area, amount_stations, max_time, trajects)

    return Min, len(trajects), fraction_done, trajects


def run_double_greedy_track(Area: Rail_NL, max_time: int,
                            random_number: int, list_stations: list[str],
                            printed: bool = False) -> tuple[int, object, list[str]]:
    """
    creates a track based upon the double greedy method

    pre:
        - Area is an object of type RailNL,
          where the other tracks are already loaded
        - max_time is an int corresponding to the maximum amount of time per track
        - random_number is an int corresponding to the index of the starting station
        - list_stations is a list of strings with the names
          of all the stations in the RailNL object
        - printed is a bool, if printed it prints the track

    post:
        - time as an integer
        - area as a RailNL object
        - the track as a list of strings
    """
    # create the track
    random_traject = Area.create_traject(list_stations[random_number], Area)

    # start the creation process
    went_back = 0
    while True:

        # finds the possoble connections
        list_stations_current = []
        if len(random_traject.current_station.connections) == 0:
            break

        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)

        destination = ""
        time = 200

        # loops trough the connections two find the shortest combination
        for station in list_stations_current:
            current_connections = random_traject.current_station.connections
            # if you already used a connection it is saved here instead
            if current_connections[station].done:
                going_back = station

            else:
                for j in Area.stations[station].connections:
                    current_time = current_connections[station].time
                    next_time = Area.stations[station].connections[j].time
                    # seperate calculation of time if second connection is used
                    if Area.stations[station].connections[j].done:
                        if (current_time + 3 *  next_time < time):
                            destination = station
                            time = 2 * current_time

                    # save times of unused combinations
                    elif (current_time + next_time < time):
                        destination = station
                        time = current_time

        # if no unused connection is found and you already used
        # a used connection in the one before break else move there
        total = random_traject.total_time

        if destination == "":
            went_back += 1
            if went_back > 1:
                break

            # check if move is within time limit and move
            if (total + current_connections[going_back].time >
                max_time):
                break

            random_traject.move(going_back)

        # if unused connections found move the shortest double connection
        else:
            if (total + current_connections[destination].time >
                max_time):
                break

            went_back = 0
            random_traject.move(destination)

    # if selected you print the track
    if printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    return time, Area, random_traject.traject_connections
