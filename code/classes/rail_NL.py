"""
Algorithms & Heuristics

Group: Team-Trein

This is the Rail_NL class.
"""

import csv
import random
from code.classes.station import Station
from code.classes.traject import Traject


class Rail_NL:
    """
    Represents a simulation of a railway network.

    Methods:
    - __init__(self, map, amount_trajects, amount_stations, max_time, randomizer=False, removing=""):
        Initializes a Rail_NL instance.

    - load_connections(self, filename):
        Loads connections from a CSV file into the Rail_NL instance.

    - add_station(self, station_name):
        Adds a station to the Rail_NL instance.

    - add_connection_stations(self, source, destination, time):
        Adds a connection between stations in the Rail_NL instance.

    - display_connections(self):
        Displays information about connections in the Rail_NL instance.

    - create_traject(self, starting_station_name, rail_instance):
        Creates a Traject instance.

    - reset(self):
        Resets the status of connections in the Rail_NL instance.

    - get_amount_stations(self):
        Gets the number of stations in the Rail_NL instance.

    - remove_station(self):
        Removes a station from the Rail_NL instance.

    - get_ids(self):
        Gets a list of random numbers.
    """

    def __init__(self, map: str, amount_trajects: int, amount_stations: int,
                 max_time: int, randomizer: bool = False, removing: str = ""):
        """
        Initialize a Rail_NL instance.

        pre:
        - map is a string representing the map name.
        - amount_trajects is an integer representing the number of trajects.
        - amount_stations is an integer representing the number of stations.
        - max_time is an integer representing the maximum time.
        - randomizer is a boolean indicating whether randomization is enabled.
        - removing is a string representing the station to be removed.

        post:
        - initializes a Rail_NL instance.
        """
        self.removing = removing
        self.map = map
        self.stations: dict[str, Station] = {}
        self.randomizer = randomizer
        self.load_connections(f"data/Connecties{map}.csv")
        self.amount_trajects = amount_trajects
        self.max_time = max_time
        self.amount_stations = amount_stations

    def load_connections(self, filename):
        """
        Load connections from a CSV file.

        pre:
        - filename is a string representing the path to the CSV file.

        post:
        - loads connections into the Rail_NL instance.
        """
        self.total_connections = 0
        remove = ""
        if self.removing != "":
            remove = self.remove_station()
        with open(filename) as csv_bestand:
            line_count = 0
            csv_read = csv.reader(csv_bestand, delimiter=',')
            if self.randomizer:
                station_names = []
                self.numbers = []
                if map == "small":
                    amount_connections = 28
                else:
                    amount_connections = 89
                for _ in range(3):
                    self.numbers.append(random.randint(1, amount_connections))
            for row in csv_read:
                if line_count != 0:
                    if self.randomizer:
                        change = []
                        station_names.append(row[0])
                        self.add_station(row[0])
                        if line_count in self.numbers:
                            change.append(row[0])
                        else:
                            self.add_station(row[1])
                            self.add_connection_stations(row[0], row[1], int(float(row[2])))
                            self.add_connection_stations(row[1], row[0], int(float(row[2])))
                            self.total_connections += 1
                    if remove != "":
                        if row[0] != remove and row[1] != remove:
                            self.add_station(row[0])
                            self.add_station(row[1])
                            self.add_connection_stations(row[0], row[1], int(float(row[2])))
                            self.add_connection_stations(row[1], row[0], int(float(row[2])))
                            self.total_connections += 1
                    else:
                        self.add_station(row[0])
                        self.add_station(row[1])
                        self.add_connection_stations(row[0], row[1], int(float(row[2])))
                        self.add_connection_stations(row[1], row[0], int(float(row[2])))
                        self.total_connections += 1
                line_count += 1
            if self.randomizer:
                for start_station in change:
                    time = random.randint(5, 70)
                    destination = random.choice(station_names)
                    self.add_connection_stations(start_station, destination, time)
                    self.add_connection_stations(destination, start_station, time)
                    self.total_connections += 1

    def add_station(self, station_name):
        """
        Add a station to the Rail_NL instance.

        pre:
        - station_name is a string representing the name of the station.

        post:
        - adds a station to the Rail_NL instance.
        """
        if station_name not in self.stations:
            self.stations[station_name] = Station(station_name)

    def add_connection_stations(self, source, destination, time):
        """
        Add a connection between stations.

        pre:
        - source is a string representing the source station.
        - destination is a string representing the destination station.
        - time is an integer representing the time of the connection.

        post:
        - adds a connection between stations in the Rail_NL instance.
        """
        self.stations[source].add_connection(destination, time)

    def display_connections(self):
        """
        Display information about connections.

        post:
        - displays information about connections in the Rail_NL instance.
        """
        for station_name, station in self.stations.items():
            print(f"Station: {station_name}")
            for destination, connection in station.connections.items():
                status = "Done" if connection.done else "Not Done"
                print(f"  To: {destination}, Time: {connection.time} minutes, Status: {status}")

    def create_traject(self, starting_station_name, rail_instance):
        """
        Create a traject.

        pre:
        - starting_station_name is a string representing the starting station name.
        - rail_instance is a Rail_NL instance.

        post:
        - returns a Traject instance.
        """
        starting_station = self.stations[starting_station_name]
        traject = Traject(starting_station, rail_instance)
        return traject

    def reset(self):
        """
        Reset the status of connections.

        post:
        - resets the status of connections in the Rail_NL instance.
        """
        for i in self.stations:
            for j in self.stations[i].connections:
                self.stations[i].connections[j].done = False

    def get_amount_stations(self):
        """
        Get the number of stations.

        post:
        - returns the number of stations in the Rail_NL instance.
        """
        self.amount_stations = len(self.stations)
        return self.amount_stations

    def remove_station(self):
        """
        Remove a station.

        post:
        - returns the name of the station to be removed.
        """
        remove = ""
        if self.removing == "Utrecht":
            remove = "Utrecht Centraal"
        elif self.removing == "Almere":
            remove = "Almere Centrum"
        elif self.removing == "Amstel":
            remove = "Amsterdam Amstel"
        elif self.removing == "Centraal":
            remove = "Amsterdam Centraal"
        elif self.removing == "Sloterdijk":
            remove = "Amsterdam Sloterdijk"
        elif self.removing == "Zuid":
            remove = "Amsterdam Zuid"
        elif self.removing == "Arnhem":
            remove = "Amsterdam Centraal"
        elif self.removing == "Den_haag":
            remove = "Den Haag Centraal"
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
        """
        Get random numbers.

        post:
        - returns a list of random numbers.
        """
        return self.numbers
