from code.classes.rail_NL import Rail_NL
import random

def depth_first_search(Area):
    # Make a list of all stations and initialize stack
    visited = []
    list_stations = []
    for station_name in Area.stations:
        list_stations.append(station_name)
    # Get a random starting stations from the list of stations
    random_number = random.randint(0, amount_stations-1)
    start_station = list_stations[random_number]
    visited.append(start_station)
    # Make a traject with our chosen starting station and move to each station it's connected to
    first_traject = Area.create_traject(start_station, Area)
    for i in range(0, len(list_stations)):
        connection_names = list(first_traject.current_station.connections.keys())
        print(f"1{connection_names}")
        if connection_names[0] not in visited:
            first_traject.move(connection_names[0])
            print(f"2{first_traject.traject_connections}")
            visited.append(connection_names[0])
            print(f"3{visited}")
        else:
            first_traject.move(connection_names[1])
            print(f"2{first_traject.traject_connections}")
            visited.append(connection_names[1])
            print(f"3{visited}")

if __name__ == "__main__":
    map = "Holland"
    amount_trajects = 7
    amount_stations = 22
    max_time = 120
    area = Rail_NL(map, amount_trajects, amount_stations, max_time)
    depth_first_search(area)
