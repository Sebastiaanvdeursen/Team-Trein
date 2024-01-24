from code.algorithms.random_alg import run_random_amount_of_trajects
from code.classes.rail_NL import Rail_NL
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.greedy_best_comb import run_trajects
import random
import copy

def hill_climbing(area, amount_trajects, amount_stations, max_time):
    current_solution = generate_random_solution(area, amount_trajects, amount_stations, max_time)
    current_score = evaluate_solution(current_solution, area)
    area.reset()

    while True:
        neighbors = get_neighbors(current_solution, area, amount_trajects, amount_stations, max_time)
        
        # Selecteer het beste buur
        best_neighbor = max(neighbors, key=lambda neighbor: evaluate_solution(neighbor, area))

        # Als het beste buur beter is dan de huidige oplossing, update de oplossing en score
        eval_sol = evaluate_solution(best_neighbor, area)

        if eval_sol > current_score:
            current_solution = best_neighbor
            current_score = eval_sol
            area.reset()
        
        else:
            # Stop als er geen verbetering is
            break
        
    current_solution_list = []
    for i in range(amount_trajects):
        current_solution_list.append(current_solution[i].traject_connections)
    
    current_solution_list = removing_lines(area, amount_trajects, amount_stations, max_time, current_solution_list)

    for i in range(len(current_solution_list)):
        stations_str = ', '.join(current_solution_list[i])
        print(f"train_{i + 1},\"[{stations_str}]\"")
    
    area.reset()

    K = run_trajects(area, len(current_solution_list), amount_stations, max_time, current_solution_list, False)

    return current_solution, K, current_solution_list

def generate_random_solution(area, amount_trajects, amount_stations, max_time):
    solution = []
    for i in range(amount_trajects):
        solution.append(run_random_traject(area, amount_stations, max_time)[2])

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
        neighbor = copy.deepcopy(solution)
        neighbor[i] = run_random_traject(area, amount_stations, max_time)[2]
        neighbors.append(neighbor)
        area.reset()
    return neighbors

def run_random_traject(Area, amount_stations, max_time):
    list_stations = []

    for station_name in Area.stations:
        list_stations.append(station_name)
    
    random_number = random.randint(0, amount_stations - 1)

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

    time = random_traject.total_time
    return [time, Area, random_traject]