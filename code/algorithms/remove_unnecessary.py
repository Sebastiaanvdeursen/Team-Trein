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
        if i == loop_counter or len(trajects) == 1:
            break
        current = []
        j = amount_trajects - 1
        for a in trajects:
            if j != i:
                current.append(a)
            j -= 1
        test = run_trajects(area, len(current), amount_stations, max_time, current, False)
        area.reset()
        if score < test:
            trajects = current
            score = test
        i += 1
    return trajects
