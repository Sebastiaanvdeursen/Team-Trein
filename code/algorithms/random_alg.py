import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject

def run_random_traject(Area, amount_stations, max_time,  printed = True, info = False):
    list_stations = []
    for station_name in Area.stations:
        list_stations.append(station_name)

    random_number = random.randint(0, amount_stations - 1)

    random_traject = Area.create_traject(list_stations[random_number], Area)

    while True:
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)
        random_number = random.randint(0, len(random_traject.current_station.connections) - 1)
        if random_traject.total_time + random_traject.current_station.connections[list_stations_current[random_number]].time > max_time:
            break
        random_traject.move(list_stations_current[random_number])
        random_int_2 = random.randint(0, 9)
        if random_int_2 == 9:
            break

    if printed:
        random_traject.show_current_traject()

    time = random_traject.total_time
    if info:
        return [time, Area, random_traject]
    return [time, Area]




def run_random_amount_of_trajects(Area, amount_trajects, max_time, amount_stations, printed = True, info = False):
    random_number = random.randint(1, amount_trajects)

    time = []
    track_info = []
    trajects = []
    for i in range(0, random_number):
        track_info = run_random_traject(Area, amount_stations, max_time, printed, info)
        time.append(track_info[0])
        if info:
            trajects.append(track_info[2].traject_connections)

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
