from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL
from code.algorithms.greedy_best_comb import run_trajects

def removing_lines(area, amount_trajects, amount_stations, max_time, trajects):
    area.reset()
    score = run_trajects(area, amount_trajects, amount_stations, max_time, trajects, False)
    area.reset()
    loop_counter = amount_trajects -1
    i = 0
    while True:
        if i == loop_counter:
            break
        current = []
        j = 0
        for a in trajects:
            if j != i:
                current.append(a)
            j += 1
        test = run_trajects(area, len(current), amount_stations, max_time, current, False)
        area.reset()
        if score < test:
            trajects = current
            loop_counter -= 1
            score = test
            j -= 1
        else:
            i += 1
    return trajects
