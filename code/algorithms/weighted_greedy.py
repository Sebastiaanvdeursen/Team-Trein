import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.greedy_best_comb import run_trajects

def run_weighted(Area, amount_trajects, max_time, amount_stations, printed = True, info = False, power = 1):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

    time = []
    track_info = []
    trajects = []
    for i in range(0, amount_trajects):
        track_info = weighted_track(Area, amount_stations, max_time, list_stations, printed, power)
        time.append(track_info[0])
        trajects.append(track_info[2].traject_connections)
    time = sum(time)

    Area.reset()
    trajects = removing_lines(Area, amount_trajects, amount_stations, max_time, trajects)
    Area.reset()
    fraction_done, time = run_trajects(Area, len(trajects), amount_stations, max_time, trajects, False, True)

    if info:
        return time, len(trajects), fraction_done, trajects
    return time, len(trajects), fraction_done

def weighted_track(Area, amount_stations, max_time, list_stations, printed = True, power = 1):
    random_number = random.randint(0, amount_stations - 1)

    random_traject = Area.create_traject(list_stations[random_number], Area)
    while True:
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)
        list_possibilities = []
        summation = 0
        for i in range(len(random_traject.current_station.connections)):
            if random_traject.current_station.connections[list_stations_current[i]].done == True:
                if random_traject.current_station.connections[list_stations_current[i]].time * 2 + random_traject.total_time < max_time:
                    list_possibilities.append([list_stations_current[i], (25 * random_traject.current_station.connections[list_stations_current[i]].time) ** power] )
                    summation += (25 * random_traject.current_station.connections[list_stations_current[i]].time) ** power
            else:
                if random_traject.current_station.connections[list_stations_current[i]].time + random_traject.total_time < max_time:
                    list_possibilities.append([list_stations_current[i], random_traject.current_station.connections[list_stations_current[i]].time ** power])
                    summation += (random_traject.current_station.connections[list_stations_current[i]].time) ** power
        if len(list_possibilities) == 0:
            break
        elif len(list_possibilities) == 1:
            random_traject.move(list_possibilities[0][0])
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
            for q in range(length):
                if q > 0:
                    probabilities[q] += probabilities[q - 1]
            for w in range(length):
                if selected < probabilities[w]:
                    random_traject.move(list_possibilities[w][0])
                    break



    if printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area, random_traject]