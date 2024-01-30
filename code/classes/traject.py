from code.classes.station import Station

class Traject:
    train_count = 0

    def __init__(self, starting_station, rail_instance):
        self.total_time = 0
        self.starting_station = starting_station
        self.current_station = starting_station
        self.traject_connections = [starting_station.name]
        self.rail_instance = rail_instance
        Traject.train_count += 1

    def move(self, destination):
        connection = self.current_station.connections[destination]
        connection2 = self.rail_instance.stations[destination].connections[self.current_station.name]

        connection.done = True
        connection2.done = True

        self.traject_connections.append(connection.destination)
        self.total_time += connection.time
        self.current_station = self.rail_instance.stations.get(connection.destination)
    
    def show_current_traject(self):
        stations_str = ', '.join(self.traject_connections)
        print(f"train_{self.train_count},\"[{stations_str}]\"")

