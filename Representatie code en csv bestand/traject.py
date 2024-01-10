from station import Station

class Traject:
    def __init__(self, starting_station, rail_instance):
        self.connections = []
        self.total_time = 0
        self.current_station = starting_station
        self.rail_instance = rail_instance

    def move(self, destination):
        connection = self.current_station.connections[destination]

        assert self.total_time + connection.time <= 120, "Went over time limit of 2 hours"

        connection.done = True

        self.connections.append((connection.destination, connection.time))
        self.total_time += connection.time
        self.current_station = self.rail_instance.stations.get(connection.destination)
    
    def show_current_traject(self):
        print("Here follows information about the current traject:")
        print(f"current connections {self.connections}")
        print(f"current total time {self.total_time}")
        print(f"current station {self.current_station.name}")

