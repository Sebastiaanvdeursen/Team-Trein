import csv
import random
import sys
from station import Station
from traject import Traject

random.seed(8)

class Rail_NL:
    def __init__(self, map, amount_trajects, amount_stations, max_time):
        self.stations = {}
        self.load_connections(f"../data/Connecties{map}.csv")
        self.amount_trajects = amount_trajects
        self.max_time = max_time
        self.amount_stations = amount_stations


    def load_connections(self, filename):
        with open(filename) as csv_bestand:
            csv_read = csv.reader(csv_bestand, delimiter=',')
            line_count = 0
            for row in csv_read:
                if line_count != 0:
                    self.add_station(row[0])
                    self.add_station(row[1])
                    self.add_connection(row[0], row[1], int(float(row[2])))
                    self.add_connection(row[1], row[0], int(float(row[2])))
                line_count += 1
        self.total_connections = line_count - 1

    def add_station(self, station_name):
        if station_name not in self.stations:
            self.stations[station_name] = Station(station_name)

    def add_connection(self, source, destination, time):
        self.stations[source].add_connection(destination, time)

    def display_connections(self):
        for station_name, station in self.stations.items():
            print(f"Station: {station_name}")
            for destination, connection in station.connections.items():
                status = "Done" if connection.done else "Not Done"
                print(f"  To: {destination}, Time: {connection.time} minutes, Status: {status}")


    def create_traject(self, starting_station_name, rail_instance):
        starting_station = self.stations[starting_station_name]
        traject = Traject(starting_station, rail_instance)
        return traject

