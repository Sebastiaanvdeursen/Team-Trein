import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject

def run_random_traject(area, amount_stations, max_time,  printed = True, info = False):
    """
    Generate a random train trajectory.

    pre:
    - area is an instance of Rail_NL.
    - amount_stations is a positive integer.
    - max_time is a positive integer.
    - printed is a boolean.
    - info is a boolean.

    post:
    - If info is True, returns a list containing total time, Area, and the generated Traject object.
    - If info is False, returns a list containing total time and Area.
    """
    # make a list containing all the stations
    list_stations = []
    for station_name in area.stations:
        list_stations.append(station_name)

    # draw a random number
    random_number = random.randint(0, amount_stations - 1)

    # create a traject starting at a random station
    random_traject = area.create_traject(list_stations[random_number], area)

    while True:
        # make a list containing all the stations that are connected to the current station
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)

        # draw a random number
        random_number = random.randint(0, len(random_traject.current_station.connections) - 1)

        # if going to next station goes over time limit of traject, break
        if random_traject.total_time + random_traject.current_station.connections[list_stations_current[random_number]].time > max_time:
            break

        # move to next station
        random_traject.move(list_stations_current[random_number])

        # 10 percent chance for traject to stop at station
        random_int_2 = random.randint(0, 9)
        if random_int_2 == 9:
            break

    # if printed is True, print the traject
    if printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    if info == True:
        return [time, area, random_traject]
    return [time, area]


def run_random_amount_of_trajects(area, amount_trajects, max_time, amount_stations, printed = True, info = False):
    """
    Generate a random amount of train trajectories for a given railway network.

    pre:
    - area is an instance of Rail_NL.
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
        track_info = run_random_traject(area, amount_stations, max_time, printed, info)
        time.append(track_info[0])
        if info:
            trajects.append(track_info[2].traject_connections)

    # calculate the fraction of done trajects
    n_done = 0
    for station in area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1

    fraction_done = (n_done / 2) / area.total_connections
    if info:
        return sum(time), random_number, fraction_done, trajects
    else:
        return sum(time), random_number, fraction_done
