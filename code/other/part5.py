"""
Code to find the solution for part 5, it prints out the effect on the max score
if you remove an object.

by: Mathijs Leons
"""
from code.algorithms.greedy.greedy_random_start import run_greedy_random
from code.classes.rail_NL import Rail_NL

import matplotlib.pyplot as plt
import sys



def Part5() -> None:
    made_area = False
    # Run it on a regular Rail_NL area
    map = "NL"
    amount_trajects = 20
    amount_stations = 61
    max_time = 180
    area2 = Rail_NL(map, amount_trajects, amount_stations, max_time)
    amount_stations_2 = area2.get_amount_stations()
    results1 = []
    for i in range(0, int(sys.argv[4])):
        Min, T, p, current = run_greedy_random(area2, amount_trajects, max_time, amount_stations, printed = False, info = True)
        area2.reset()
        results1.append( p * 10000 - (T * 100 + Min))
    maximum = max(results1)


    # With each iteration create a new rail_nl object and run a certain amount of greedy tracks
    # Print out the average impact on the maximum if you remove that track
    list = [0] * 89
    count = [0] * 89
    for i in range(int(sys.argv[3])):
        results = []
        area1 = Rail_NL(map, amount_trajects, amount_stations, max_time, randomizer = True)
        numbers = area1.get_ids()
        amount_stations_1 = area1.get_amount_stations()

        # Run the greedy algorithm
        for j in range(0, int(sys.argv[4])):
            Min, T, p, current = run_greedy_random(area1, amount_trajects, max_time, amount_stations_1, printed = False, info = True)
            area1.reset()
            results.append( p * 10000 - (T * 100 + Min))
        max_random = max(results)
        difference = max_random - maximum
        # add the change in the maximum
        for i in numbers:
            list[i - 1] += difference
            count[i - 1] += 1

    # print the average effects
    for i in range(0, 89):
        if count[i] > 0:
            print(int(list[i] / count[i]))
        else:
            print(0)










