import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject

def run_greedy_traject_opt(Area, amount_stations, max_time, used_for_hill_climbing=False, printed=True):
    """
    Generate a random train trajectory using some heuristics.

    pre:
    - Area is an instance of Rail_NL.
    - amount_stations is a positive integer.
    - max_time is a positive integer.
    - used_for_hill_climbing is a boolean.
    - printed is a boolean.

    post:
    - Returns a list containing total time, Area, and the generated Traject object.
    """
    # make a list containing all the stations
    list_stations = []
    for station_name in Area.stations:
        list_stations.append(station_name)

    # draw a random number
    random_number = random.randint(0, amount_stations - 1)

    # create a traject starting at a random station
    random_traject = Area.create_traject(list_stations[random_number], Area)

    while True:
        list_stations_current = []

        # collect stations, for which the connections from the current station
        # have not been done yet
        lowest_min = 50
        for station_name in random_traject.current_station.connections:
            if random_traject.current_station.connections[station_name].done == False:
                if random_traject.current_station.connections[station_name].time < lowest_min:
                    lowest_min = random_traject.current_station.connections[station_name].time
                    min_station_name = station_name
            list_stations_current.append(station_name)

        # if all connections are done, break the loop
        if lowest_min == 50:
            break

        # check if adding the selected connection exceeds the maximum allowed time
        if random_traject.total_time + random_traject.current_station.connections[min_station_name].time > max_time:
            break

        # move to the selected station
        random_traject.move(min_station_name)

    # print the generated trajectory if not used for hill climbing and printed is True
    if used_for_hill_climbing == False and printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area, random_traject]


def run_greedy_amount_of_trajects_opt(Area, amount_trajects, max_time, amount_stations, printed=True, info=False):
    """
    Generate a random amount of train trajectories for a given railway network with optimized conditions.

    pre:
    - Area is an instance of Rail_NL.
    - amount_trajects is a positive integer.
    - max_time is a positive integer.
    - amount_stations is a positive integer.
    - printed is a boolean.
    - info is a boolean.

    post:
    - If info is True, returns a list containing total time, the number of trajectories,
      fraction_done, and a list of trajects.
    - If info is False, returns a list containing total time, the number of trajectories, and fraction_done.
    """
    # draw a random number
    random_number = random.randint(1, amount_trajects)
    
    time = []
    track_info = []
    trajects = []
    for i in range(0, random_number):
        track_info = run_greedy_traject_opt(Area, amount_stations, max_time, printed=printed)
        time.append(track_info[0])
        if info:
            trajects.append(track_info[2].traject_connections)

    # calculate the fraction of done trajects
    n_done = 0
    for station in Area.stations.values():
        for connection in station.connections.values():
            if connection.done == True:
                n_done += 1

    fraction_done = (n_done / 2) / Area.total_connections
    if info:
        return sum(time), random_number, fraction_done, trajects
    else:
        return sum(time), random_number, fraction_done
