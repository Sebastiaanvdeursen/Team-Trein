from station import Station

class Traject:
    train_count = 0

    def __init__(self, starting_station, rail_instance):
        self.connections = []
        self.total_time = 0
        self.current_station = starting_station
        self.rail_instance = rail_instance
        Traject.train_count += 1

    def move(self, destination):
        connection = self.current_station.connections[destination]

        assert self.total_time + connection.time <= 120, "Went over time limit of 2 hours"

        connection.done = True

        self.connections.append(connection.destination)
        self.total_time += connection.time
        self.current_station = self.rail_instance.stations.get(connection.destination)
    
    def show_current_traject(self):
        stations_str = ', '.join(self.connections)
        print(f"train_{self.train_count},\"[{stations_str}]\"")

