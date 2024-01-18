import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject

def run_random_traject_opt(Area, amount_stations, max_time, used_for_hill_climbing):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

    random_number = random.randint(0, amount_stations - 1)

    random_traject = Area.create_traject(list_stations[random_number], Area)

    while True:
        list_stations_current = []
        list_stations_current_not_done = []
        for station_name in random_traject.current_station.connections:
            if random_traject.current_station.connections[station_name].done == False:
                list_stations_current_not_done.append(station_name)
            list_stations_current.append(station_name)
        if len(list_stations_current_not_done) == 0:
            break

        random_number = random.randint(0, len(list_stations_current_not_done) - 1)
        if random_traject.total_time + random_traject.current_station.connections[list_stations_current_not_done[random_number]].time > max_time:
            break
        random_traject.move(list_stations_current_not_done[random_number])

    if used_for_hill_climbing == False:
        random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area, random_traject]




def run_random_amount_of_trajects_opt(Area, amount_trajects, max_time, amount_stations):
    random_number = random.randint(1, amount_trajects)

    time = []
    for i in range(0, random_number):
        time.append(run_random_traject_opt(Area, amount_stations, max_time)[0])

    n_done = 0
    for station in Area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1

    fraction_done = (n_done / 2) / Area.total_connections
    return sum(time), random_number, fraction_done