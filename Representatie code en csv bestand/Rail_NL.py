import csv
import random
from station import Station
from traject import Traject

random.seed(8)

class Rail_NL:
    def __init__(self):
        self.stations = {}
        self.load_connections("ConnectiesHolland.csv")
    
    
    def load_connections(self, filename):
        with open(filename) as csv_bestand:
            csv_read = csv.reader(csv_bestand, delimiter=',')
            line_count = 0
            for row in csv_read:
                if line_count != 0:
                    self.add_station(row[0])
                    self.add_station(row[1])
                    self.add_connection(row[0], row[1], int(row[2]))
                    self.add_connection(row[1], row[0], int(row[2]))
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

def run_random_traject(Area):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)
    
    random_number = random.randint(0, 21)

    random_traject = Area.create_traject(list_stations[random_number], Area)

    while True:
        if random_traject.total_time + 36 > 120:
            break
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)
        random_number = random.randint(0, len(random_traject.current_station.connections) - 1)
        random_traject.move(list_stations_current[random_number])
        random_int_2 = random.randint(0, 9)
        if random_int_2 == 9:
            break


    random_traject.show_current_traject()

    time = random_traject.total_time
    return [time, Area]




def run_random_amount_of_trajects(Area):
    random_number = random.randint(1, 7)

    time = []
    for i in range(0, random_number):
        time.append(run_random_traject(Area)[0])

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
    Noord_Holland = Rail_NL()
    print("train,stations")
    Min, T, p = run_random_amount_of_trajects(Noord_Holland)
    K = p*10000 - (T*100 + Min)
    print(f"score,{K}")
                


    

