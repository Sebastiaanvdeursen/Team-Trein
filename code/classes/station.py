from code.classes.connection import Connection
from typing import Dict

class Station:
    def __init__(self, name: str):
        """
        Initialize a Station instance.

        pre:
        - name is a string representing the name of the station.

        post:
        - initializes a Station instance with the given name.
        """
        self.name: str = name
        self.connections: Dict[str, Connection] = {}

    def add_connection(self, destination: str, time: int):
        """
        Add a connection to the station.

        pre:
        - destination is a string representing the destination station.
        - time is an integer representing the time it takes to reach the destination.

        post:
        - adds a connection to the station with the given destination and time.
        """
        self.connections[destination] = Connection(destination, time)


