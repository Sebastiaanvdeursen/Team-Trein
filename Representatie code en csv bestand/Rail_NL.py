import csv
import random
from station import Station
from traject import Traject

class Rail_NL:
    def __init__(self):
        self.stations = {}
        self.load_connections("ConnectiesHolland.csv")

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

    def create_traject(self, starting_station_name, rail_instance):
        starting_station = self.stations[starting_station_name]
        traject = Traject(starting_station, rail_instance)
        return traject

def run_random_traject():
    Noord_Holland = Rail_NL()

    list_stations = []

    for station_name in Noord_Holland.stations:
        list_stations.append(station_name)
    
    random_number = random.randint(0, 21)

    random_traject = Noord_Holland.create_traject(list_stations[random_number], Noord_Holland)

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
    return [time, Noord_Holland]

def run_random_amount_of_trajects():
    random_number = random.randint(1, 7)
    time = []
    for i in range(1, random_number):
        time.append(run_random_traject()[0])
    print(sum(time))

    n_done = 0
    n_not_done = 0
    for station in run_random_traject()[1].stations.values():
            for connection in station.connections.values():
                if connection.done == False:
                    n_not_done += 1
                else:
                    n_done += 1
    
    fraction_done = n_done / (n_not_done + n_done)
    return sum(time), random_number, fraction_done


# Main script
if __name__ == "__main__":
    Min, T, p = run_random_amount_of_trajects()
    print(Min, T, p)
    K = p*10000 - (T*100 + Min)
    print(K)
                


    

