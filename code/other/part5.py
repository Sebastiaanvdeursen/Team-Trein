from code.algorithms.greedy.greedy_random_start import run_greedy_random

from code.classes.rail_NL import Rail_NL

import matplotlib.pyplot as plt
import sys



if __name__ == "__main__":
    made_area = False

    map = "NL"
    amount_trajects = 20
    amount_stations = 61
    max_time = 180
    area2 = Rail_NL(map, amount_trajects, amount_stations, max_time)
    amount_stations_2 = area2.get_amount_stations()
    results1 = []
    for i in range(0, int(sys.argv[2])):
        Min, T, p, current = run_greedy_random(area2, amount_trajects, max_time, amount_stations, printed = False, info = True)
        area2.reset()
        results1.append( p * 10000 - (T * 100 + Min))
    maximum = max(results1)



    list = [0] * 89
    count = [0] * 89
    for i in range(int(sys.argv[1])):
        results = []
        area1 = Rail_NL(map, amount_trajects, amount_stations, max_time, randomizer = True)
        numbers = area1.get_ids()
        amount_stations_1 = area1.get_amount_stations()
        for j in range(0, int(sys.argv[2])):
            Min, T, p, current = run_greedy_random(area1, amount_trajects, max_time, amount_stations, printed = False, info = True)
            area1.reset()
            results.append( p * 10000 - (T * 100 + Min))
        max_random = max(results)
        difference = max_random - maximum
        for i in numbers:
            list[i - 1] += difference
            count[i - 1] += 1
    for i in range(0, 89):
        print(int(list[i] / count[i]))










