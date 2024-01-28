import code.algorithms.greedy_random_start as greedy
import code.algorithms.weighted_greedy as weighted
from code.algorithms.greedy_best_comb import run_trajects

def find_improvement(area, amount_trajects, max_time, amount_stations, trajects):
    list_stations = []

    for station_name in area.stations:
        list_stations.append(station_name)
    area.reset()
    current_score = run_trajects(area, len(trajects), amount_stations, max_time, trajects, False, False)
    print(current_score)
    if len(trajects) < amount_trajects:
        count = 0
        while True:
            count += 1
            run_trajects(area, len(trajects), amount_stations, max_time, trajects, False, False)
            new = weighted.weighted_track(area, amount_stations, max_time, list_stations, False, 1)[2].traject_connections
            trajects.append(new)
            print(trajects)
            new_score = run_trajects(area, len(trajects), amount_stations, max_time, trajects, False, False)
            print(new_score)

            if current_score < new_score:
                print("succes")
                current_score = new_score
                break
            else:
                trajects.pop()
            area.reset()
            if count > 1000000:
                break

    return(trajects)