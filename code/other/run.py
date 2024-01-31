"""
runs a list of list to test out a created trajects, it adds it to the RailNL object
and returns the score

by: Mathijs Leons, Team-Trein
"""
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL

def run_trajects(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int,
                  trajects: list[list[str]], printed: bool = False) -> tuple[float, int]:
    """
    runs the traject based upon the list of list object and returns the p and Min

    pre:
        - area is a empty Rail_Nl object
        - amount_trajects is the amount of trajects used as an int
        - amount_stations is the amount of stations as an int
        - max_time, is the maximum amount of time per track as an int
        - traject is a list of list of strings with valid trajects
            so all connections must be possible
        - printed is a bool'

    post:
        - returns the fraction done as an int
        - the time used as an int
        - if printed:
            - prints the trajects used
    """
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

    return fraction_done, time
