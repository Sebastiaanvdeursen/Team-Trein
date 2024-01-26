import csv
import random
import sys
from code.classes.station import Station
from code.classes.traject import Traject

class Rail_NL:
    def __init__(self, map, amount_trajects, amount_stations, max_time, randomizer = False, removing = ""):
        self.removing = removing
        self.map = map
        self.stations = {}
        self.randomizer = randomizer
        self.load_connections(f"data/Connecties{map}.csv")
        self.amount_trajects = amount_trajects
        self.max_time = max_time
        self.amount_stations = amount_stations


    def load_connections(self, filename):
        remove = ""
        if self.removing != "":
            remove = self.remove_station()
        with open(filename) as csv_bestand:
            csv_read = csv.reader(csv_bestand, delimiter=',')
            line_count = 0
            if self.randomizer:
                station_names = []
                self.numbers = []
                if map == "small":
                    amount_connections = 28
                else:
                    amount_connections = 89
                for _ in range(3):
                    self.numbers.append(random.randint(2, amount_connections))
            for row in csv_read:
                if line_count != 0:
                    if self.randomizer:
                        station_names.append(row[0])
                        self.add_station(row[0])
                        if line_count in self.numbers:
                            destination = random.choice(station_names)
                            time = random.randint(5, 70)
                            print(f"removed[{row[0]}, {row[1]}], {int(float(row[2]))}")
                            print(f"added: [{row[0]}, {destination}], {time}")
                            self.add_connection_stations(row[0], destination, time)
                            self.add_connection_stations(destination, row[0], time)
                        else:
                            self.add_station(row[1])
                            self.add_connection_stations(row[0], row[1], int(float(row[2])))
                            self.add_connection_stations(row[1], row[0], int(float(row[2])))
                    if remove != "":
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

    def remove_station(self):
        remove = ""
        if self.removing =="Utrecht":
                remove ="Utrecht Centraal"
        elif self.removing =="Almere":
                remove ="Almere Centrum"
        elif self.removing =="Amstel":
            remove ="Amsterdam Amstel"
        elif self.removing =="Centraal":
                remove ="Amsterdam Centraal"
        elif self.removing =="Sloterdijk":
                remove ="Amsterdam Sloterdijk"
        elif self.removing =="Zuid":
                remove ="Amsterdam Zuid"
        elif self.removing =="Arnhem":
                remove ="Amsterdam Centraal"
        elif self.removing =="Den_haag":
            remove ="Den Haag Centraal"
        elif self.removing == "NOI":
            remove = "Den Haag Laan v NOI"
        elif self.removing == "HS":
            remove = "Den Haag HS"
        elif self.removing == "leiden":
            remove = "Leiden Centraal"
        elif self.removing == "Alexander":
            remove = "Rotterdam Alexander"
        elif self.removing == "Rotterdam":
            remove = "Rotterdam Centraal"
        elif self.removing == "Blaak":
            remove = "Rotterdam Blaak"
        elif self.removing == "Schiedam":
            remove = "Schiedam Centrum"
        else:
            remove = self.removing
        return remove

    def get_ids(self):
         return self.numbers