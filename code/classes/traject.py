from typing import List
from code.classes.station import Station

class Traject:
    train_count: int = 0

    def __init__(self, starting_station: Station, rail_instance):
        """
        Initialize a Traject instance.

        pre:
        - starting_station is a Station instance representing the starting station.
        - rail_instance is an instance of Rail_NL.

        post:
        - initializes a Traject instance with the given starting station and rail instance.
        """
        self.total_time: int = 0
        self.starting_station: Station = starting_station
        self.current_station: Station = starting_station
        self.traject_connections: List[str] = [starting_station.name]
        self.rail_instance = rail_instance
        Traject.train_count += 1

    def move(self, destination: str):
        """
        Move the traject to the given destination.

        pre:
        - destination is a string representing the name of the destination station.

        post:
        - updates the traject's information based on the move to the destination.
        """
        connection = self.current_station.connections[destination]
        connection2 = self.rail_instance.stations[destination].connections[self.current_station.name]

        connection.done = True
        connection2.done = True

        self.traject_connections.append(connection.destination)
        self.total_time += connection.time
        self.current_station = self.rail_instance.stations.get(connection.destination)
    
    def show_current_traject(self):
        """
        display the current state of the traject.
        """
        stations_str = ', '.join(self.traject_connections)
        print(f"train_{self.train_count},\"[{stations_str}]\"")


