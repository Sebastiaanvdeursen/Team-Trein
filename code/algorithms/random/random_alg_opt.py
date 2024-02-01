"""
Algorithms & Heuristics

Group: Team-Trein

The Random Optimized Algorithm combines the Random Algorithm with a heuristic. The choice of which connection
the trajects follows is only between the connections that are "not done". If the only options are connections
that are "done", stop the traject.

By: Sebastiaan van Deursen
"""

from code.classes.rail_NL import Rail_NL
from code.classes.traject import Traject
from code.other.remove_unnecessary import removing_lines
from code.other.run import run_trajects
import random


def run_random_traject_opt(area: Rail_NL, amount_stations: int, max_time: int, used_for_hill_climbing: bool = False,
                           printed: bool = True) -> tuple[int, Rail_NL, Traject]:
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
    list_stations = list(area.stations.keys())

    # draw a random number
    random_number = random.randint(0, amount_stations - 1)

    # create a traject starting at a random station
    random_traject = area.create_traject(list_stations[random_number], area)

    while True:
        list_stations_current = []
        list_stations_current_not_done = []

        # collect stations, for which the connections from the current station
        # have not been done yet
        for station_name in random_traject.current_station.connections:
            if random_traject.current_station.connections[station_name].done is False:
                list_stations_current_not_done.append(station_name)
            list_stations_current.append(station_name)

        # if all connections are done, break the loop
        if len(list_stations_current_not_done) == 0:
            break

        # randomly select a station to move to from the connections that are not done yet
        random_number = random.randint(0, len(list_stations_current_not_done) - 1)

        # check if adding the selected connection exceeds the maximum allowed time
        if random_traject.total_time + random_traject.current_station.connections[list_stations_current_not_done[random_number]].time \
           > max_time:
            break

        # move to the selected station
        random_traject.move(list_stations_current_not_done[random_number])

    # print the generated trajectory if not used for hill climbing and printed is True
    if not used_for_hill_climbing and printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    return time, area, random_traject


def run_random_amount_of_trajects_opt(area: Rail_NL, amount_trajects: int, max_time: int, amount_stations: int, printed: bool = True,
                                      info: bool = False) -> tuple[int, int, float, list[list[str]]] | tuple[int, int, float]:
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
    trajects = []
    solution = []
    for i in range(0, random_number):
        track_info = run_random_traject_opt(area, amount_stations, max_time, printed=printed)
        time.append(track_info[0])
        solution.append(track_info[2].traject_connections)
        if info:
            trajects.append(track_info[2].traject_connections)

    solution = removing_lines(area, len(solution), amount_stations, max_time, solution)

    area.reset()

    # find p, Min  for the solution
    p, Min = run_trajects(area, len(solution), amount_stations, max_time, solution, False)

    if info:
        return Min, len(solution), p, solution
    else:
        return Min, len(solution), p
