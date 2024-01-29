from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL
from code.algorithms.run import run_trajects

def removing_lines(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int,
                    trajects: list[list[str]]) -> list[list[str]]:
    """
    removes lines that decrease the combined score, it does this by looping trough all of them
    and removing and adding them back in one by one

    pre:
        - area object of type Rail_NL
        - amount_trajects as an int
        - amount_stations as an int
        - max_time as an int
        - trajects as a list of list of strings

    post:
        - returns the optimized trajects as a list of list of strings
    """
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

def remove_end(area: Rail_NL, amount_stations: int, max_time: int,
                trajects: list[list[str]]) -> list[list[str]]:
    """
    checks if the end station of each traject actually decreases the score, it loops trough
    until it stops finding improvements

    pre:
        - area object of type Rail_NL
        - amount_trajects as an int
        - amount_stations as an int
        - max_time as an int
        - trajects as a list of list of strings

    post:
        - returns the optimized trajects as a list of list of strings
    """
    area.reset()
    fraction_done, time= run_trajects(area, len(trajects), amount_stations, max_time, trajects, False, True)
    score = fraction_done * 10000 - time - (len(trajects) * 100)
    area.reset()
    while True:
        changes = 0
        for i in range(len(trajects)):
            current = []
            for j in range(len(trajects)):
                if j == i:
                    current.append(trajects[j][:-1])
                else:
                    current.append(trajects[j])
            area.reset()
            current_fraction_done, current_time= run_trajects(area, len(current), amount_stations, max_time,
                                                                current, False, True)
            current_score = fraction_done * 10000 - time - (len(trajects) * 100)
            area.reset()
            if current_score > score:
                trajects = current
                score = current_score
                fraction_done = current_fraction_done
                time = current_time
                changes += 1
        if changes == 0:
            break
    return fraction_done, time, trajects



