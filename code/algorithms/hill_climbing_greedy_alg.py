from copy import deepcopy
from code.algorithms.random_alg import run_random_amount_of_trajects
from code.classes.rail_NL import Rail_NL
import random


def hill_climbing_greedy(area, amount_trajects, amount_stations, max_time):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area)
    area.reset()

    while True:
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        
        # Selecteer het beste buur
        best_neighbor = max(neighbors, key=lambda neighbor: evaluate_solution(neighbor, area))

        # Als het beste buur beter is dan de huidige oplossing, update de oplossing en score
        if evaluate_solution(best_neighbor, area) > current_score:
            current_solution = best_neighbor
            current_score = evaluate_solution(current_solution, area)
        else:
            # Stop als er geen verbetering is
            break
        area.reset()

    for i in range(0, amount_trajects):
        stations_str = ', '.join(current_solution[i].traject_connections)
        print(f"train_{i + 1},\"[{stations_str}]\"")
    
    return current_solution, current_score

def generate_random_solution(area, amount_trajects, amount_stations, max_time):
    solution = []
    for i in range(amount_trajects):
        solution.append(run_greedy_track(area, amount_stations, max_time)[2])

    return solution

def evaluate_solution(solution, area):
    # Hier implementeer je de evaluatie van de doelfunctie K voor de gegeven oplossing
    # Je kunt de p-waarde, T-waarde en Min-waarde berekenen zoals beschreven in je doelfunctie.
    total_time = 0
    for i in range(0, len(solution)):
        total_time += solution[i].total_time

    n_done = 0
    for station in area.stations.values():
        for connection in station.connections.values():
            if connection.done:
                n_done += 1

    fraction_done = (n_done / 2) / area.total_connections

    return fraction_done * 10000 - (len(solution) * 100 + total_time)


def get_neighbors(solution, area, amount_trajects, amount_stations, max_time):
    neighbors = []
    for i in range(amount_trajects):
        neighbor = deepcopy(solution)
        neighbor[i] = run_greedy_track(area, amount_stations, max_time)[2]
        neighbors.append(neighbor)
    return neighbors


def run_greedy_track(Area, amount_stations, max_time):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)

    random_number = random.randint(0, amount_stations - 1)

    random_traject = Area.create_traject(list_stations[random_number], Area)
    went_back = 0
    while True:
        list_stations_current = []
        for station_name in random_traject.current_station.connections:
            list_stations_current.append(station_name)
        destination = ""
        time = 200

        for i in range(len(random_traject.current_station.connections)):
            if random_traject.current_station.connections[list_stations_current[i]].done == True:
                going_back = list_stations_current[i]
            elif random_traject.current_station.connections[list_stations_current[i]].time < time:
                destination = list_stations_current[i]
                time = random_traject.current_station.connections[list_stations_current[i]].time
        if destination == "":
            went_back += 1
            if went_back > 1:
                break
            if random_traject.total_time + random_traject.current_station.connections[going_back].time > max_time:
                break
            random_traject.move(going_back)
        else:
            if random_traject.total_time + random_traject.current_station.connections[destination].time > max_time:
                break
            went_back = 0
            random_traject.move(destination)

    time = random_traject.total_time
    return [time, Area, random_traject]