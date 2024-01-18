from code.classes.connection import Connection

class Station:
    def __init__(self, name):
        self.name = name
        self.connections = {}

    def add_connection(self, destination, time):
        self.connections[destination] = Connection(destination, time)

