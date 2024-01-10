import csv
from station import Station

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
            for destination, time in station.connections.items():
                print(f"  To: {destination}, Time: {time} minutes")

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

# Main script
if __name__ == "__main__":
    from Rail_NL import Rail_NL

    Noord_Holland = Rail_NL()

    # Toon verbindingen
    Noord_Holland.display_connections()

    print(Noord_Holland.stations["Amsterdam Zuid"].connections)

