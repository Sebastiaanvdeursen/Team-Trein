import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject

class Rail_NL:
    def __init__(self, map, amount_trajects, amount_stations, max_time, randomizer = False, utrecht = True):
        self.map = map
        self.utrecht = utrecht
        self.stations = {}
        self.randomizer = randomizer
        self.load_connections(f"data/Connecties{map}.csv")
        self.amount_trajects = amount_trajects
        self.max_time = max_time
        self.amount_stations = amount_stations


    def load_connections(self, filename):
        remove ="Utrecht Centraal"
        with open(filename) as csv_bestand:
            csv_read = csv.reader(csv_bestand, delimiter=',')
            line_count = 0
            if self.randomizer:
                station_names = []
                numbers = []
                if map == "small":
                    amount_connections = 28
                else:
                    amount_connections = 89
                for _ in range(3):
                    numbers.append(random.randint(2, amount_connections))
            for row in csv_read:
                if line_count != 0:
                    if self.randomizer:
                        station_names.append(row[0])
                        self.add_station(row[0])
                        if line_count in numbers:
                            destination = random.choice(station_names)
                            time = random.randint(1, 40)
                            print(f"removed[{row[0]}, {row[1]}], {int(float(row[2]))}")
                            print(f"added: [{row[0]}, {destination}], {time}")
                            self.add_connection_stations(row[0], destination, time)
                            self.add_connection_stations(destination, row[0], time)
                        else:
                            self.add_station(row[1])
                            self.add_connection_stations(row[0], row[1], int(float(row[2])))
                            self.add_connection_stations(row[1], row[0], int(float(row[2])))
                    if self.utrecht == False:
                        if row[0] != remove and row[1] != remove:
                            self.add_station(row[0])
                            self.add_station(row[1])
                            self.add_connection_stations(row[0], row[1], int(float(row[2])))
                            self.add_connection_stations(row[1], row[0], int(float(row[2])))
                    else:
                        self.add_station(row[0])
                        self.add_station(row[1])
                        self.add_connection_stations(row[0], row[1], int(float(row[2])))
                        self.add_connection_stations(row[1], row[0], int(float(row[2])))
                line_count += 1
        self.total_connections = line_count - 1

    def add_station(self, station_name):
        if station_name not in self.stations:
            self.stations[station_name] = Station(station_name)

    def add_connection_stations(self, source, destination, time):
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

    def reset(self):
        for i in self.stations:
            for j in self.stations[i].connections:
                self.stations[i].connections[j].done = False

    def get_amount_stations(self):
        self.amount_stations = len(self.stations)
        return self.amount_stations


