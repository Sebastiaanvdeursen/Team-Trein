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





def run_random_traject(Area, amount_stations, max_time):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)
    
    random_number = random.randint(0, amount_stations)

    random_traject = Area.create_traject(list_stations[random_number], Area)

    while True:
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)
        random_number = random.randint(0, len(random_traject.current_station.connections) - 1)
        if random_traject.total_time + random_traject.current_station.connections[list_stations_current[random_number]].time > max_time:
            break
        random_traject.move(list_stations_current[random_number])
        random_int_2 = random.randint(0, 9)
        if random_int_2 == 9:
            break


    random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area]




def run_random_amount_of_trajects(Area, amount_trajects, max_time, amount_stations):
    random_number = random.randint(1, amount_trajects)

    time = []
    for i in range(0, random_number):
        time.append(run_random_traject(Area, amount_stations, max_time)[0])

    n_done = 0
    n_not_done = 0
    for station in Area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1
    
    fraction_done = (n_done / 2) / Area.total_connections
    return sum(time), random_number, fraction_done


# Main script
if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "large":
            map = "NL"
            amount_trajects = 20
            amount_stations = 61
            max_time = 180
        else:
            map = "Holland"
            amount_trajects = 7
            amount_stations = 22
            max_time = 120
    else:
        map = "Holland"
        amount_trajects = 7
        amount_stations = 22
        max_time = 120
    
    Noord_Holland = Rail_NL(map, amount_trajects, amount_stations, max_time)
    print("train,stations")
    Min, T, p = run_random_amount_of_trajects(Noord_Holland, amount_trajects, max_time, amount_stations)
    K = p*10000 - (T*100 + Min)
    print(f"score,{K}")
                


    

