"""
Weighted greedy is a semi random algorithm based upon our own probability
calculations the probabilities are based on the time the connection takes,
the shorter the distance the higher the probability

by: Mathijs Leons
"""
from code.classes.rail_NL import Rail_NL
from code.classes.traject import Traject
from code.other.remove_unnecessary import removing_lines
from code.other.run import run_trajects

import random


def run_weighted(Area: Rail_NL, amount_trajects: int, max_time: int,
                 amount_stations: int, printed: bool = True, info: bool = False,
                 power: float = 1.6) -> tuple[int, int, float, list[list[str]]] | tuple[int, int, float]:
    """
    Runs the Weighted Greedy algorithm,
    to create the selected amount of tracks,
    for explanation of the workings please read the README
    in the folder with the code

    pre:
        - Area is a clean object of type Rail_NL
        - amount of trajects is an int corresponding
          to the amount of tracks the user wants/ are allowed
        - amount_stations is an int corresponding to the amount
          of stations in the rail_nl object
        - printed is a bool that makes it print the tracks
        - info is a bool that changes the bool to also return
          the list of list of strings with the connections
        - power is a float used in the algorithm

    post:
        - the time used by all the tracks as an int
        - the amount of tracks used as an int
        - the fraction of the connections used as a float
        - if info:
            - the tracks as a list of list of tracks
    """
    # Loads in the list of stations in the rail_NL object
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

    # Creates the selected amount of tracks
    time = []
    track_info = []
    trajects = []
    for _ in range(0, amount_trajects):
        track_info = weighted_track(Area, amount_stations, max_time,
                                    list_stations, printed, power)
        time.append(track_info[0])
        trajects.append(track_info[2].traject_connections)

    time = sum(time)

    # Optimises the tracks
    trajects = removing_lines(Area, amount_trajects, amount_stations,
                              max_time, trajects)

    fraction_done, time = run_trajects(Area, len(trajects),
                                       amount_stations, max_time, trajects)

    # returns the correct tracks
    if info:
        return time, len(trajects), fraction_done, trajects
    else:
        return time, len(trajects), fraction_done


def weighted_track(Area: Rail_NL, amount_stations: int, max_time: int,
                   list_stations: list[str], printed: bool = True, power: float = 1,
                   start: int = -1) -> tuple[int, Rail_NL, Traject]:
    """
    Runs the weighted track algorithm, if a start station is selected it starts there
    otherwise it starts from a random point, the power is set too one
    if it isn't selected, increasing the power will make it closer
    to the regular greedy algorithm more explanation in the README.

    pre:
        - Area is of type RailNL, it needs to contain the tracks already created
        - amount_stations is an int for the amount of stations in the railNL object
        - max_time is an int, it is the maximum amount of time the track may take in minutes
        - list_station is the list of all the stations as a list of strings
        - printed is a bool, if True it prints the track when it is created
        - power is a float used in the calculation of probabilities
        - start is an int corresponding to the index of the starting station,
          if its left at -1 it selects a random station to start

    post:
        - returns the time the track takes as an int
        - returns the modified RailNL object
        - returns the trajects as a Traject object
        - if printed:
            - prints the track
    """
    # Selects a starting station if one is not provided
    if start == -1:
        random_number = random.randint(0, amount_stations - 1)
    else:
        random_number = start

    # Creates the traject object
    random_traject = Area.create_traject(list_stations[random_number], Area)
    while True:

        # Loops trough all connections of current station
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)

        # initiate necessary variables
        list_possibilities = []
        summation = 0

        # Adds the info for all the connections regarding time and if already used
        # so that the probabilities can be calculated correctly
        for station in list_stations_current:
            time_selected = random_traject.current_station.connections[station].time
            if random_traject.current_station.connections[station].done:
                if (time_selected * 2 + random_traject.total_time < max_time):
                    list_possibilities.append([station,
                                              (10 * time_selected) ** power])
                    summation += ((10 * time_selected) ** power)

            else:
                if (time_selected + random_traject.total_time < max_time):
                    list_possibilities.append([station, time_selected ** power])
                    summation += ((time_selected) ** power)

        # Ends the track if no connections are found
        if len(list_possibilities) == 0:
            break

        # If there is just one possibility always go there
        elif len(list_possibilities) == 1:
            random_traject.move(list_possibilities[0][0])

        # Calculate the probabilities of all the connections
        else:
            length = len(list_possibilities)
            fractions = []
            probabilities = []
            for i in range(length):
                fractions.append(1 / list_possibilities[i][1])

            total = sum(fractions)

            for j in range(length):
                probabilities.append((fractions[j] / total) * 100)

            selected = random.randint(0, 100)

            # Choose the connection using the probabilities and a random generator
            for q in range(length):
                if q > 0:
                    probabilities[q] += probabilities[q - 1]

            for w in range(length):
                if selected < probabilities[w]:
                    random_traject.move(list_possibilities[w][0])
                    break

    # Print the track if desired
    if printed:
        random_traject.show_current_traject()

    # Return the correct info
    time = random_traject.total_time
    return time, Area, random_traject
