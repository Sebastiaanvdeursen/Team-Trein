from code.algorithms.greedy.greedy_random_start import run_greedy_random

def find_p(area, amount_trajects, max_time, amount_stations):
    while True:
        Min, T, p, trajects = run_greedy_random(area, amount_trajects, max_time, amount_stations, printed = False, info = True)
        if p == 1:
            count = 1
            for a in trajects:
                stations_str = ', '.join(a)
                print(f"train_{count},\"[{stations_str}]\"")
                count += 1
            print(f"score,{p * 10000 - (T * 100 + Min)}")
            break
        area.reset()