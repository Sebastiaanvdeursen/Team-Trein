import csv
import random
import sys
from station import Station
from traject import Traject
from rail_NL import Rail_NL

def double_greedy_random(Area, amount_trajects, max_time, amount_stations):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

    time = []
    for i in range(0, amount_trajects):
        numbers = []
        while True:
            random_number = random.randint(0, amount_stations - 1)
            if random_number not in numbers:
                numbers.append(random_number)
                break
        time.append(run_greedy_track(Area, amount_stations, max_time, random_number)[0])

    n_done = 0
    for station in Area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1

    fraction_done = (n_done / 2) / Area.total_connections
    return sum(time), amount_trajects, fraction_done

def run_greedy_track(Area, amount_stations, max_time, random_number):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

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
                        if random_traject.current_station.connections[list_stations_current[i]].time + 3 * Area.stations[list_stations_current[i]].connections[j].time < time:
                            destination = list_stations_current[i]
                            time = 2 * random_traject.current_station.connections[list_stations_current[i]].time
                    elif random_traject.current_station.connections[list_stations_current[i]].time + Area.stations[list_stations_current[i]].connections[j].time < time:
                        destination = list_stations_current[i]
                        time = random_traject.current_station.connections[list_stations_current[i]].time

        if destination == "":
            went_back += 1
            if went_back > 1:
                break
            if random_traject.total_time + random_traject.current_station.connections[going_back].time > max_time:
                break
            random_traject.move(going_back)
        else:
            if random_traject.total_time + random_traject.current_station.connections[destination].time > max_time:
                break
            went_back = 0
            random_traject.move(destination)

    random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area]