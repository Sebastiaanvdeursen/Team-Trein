from code.classes.station import Station
from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL
from code.other.run import run_trajects

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
    # makes sure area is empty
    area.reset()

    # gets starting score
    fraction_done, Min = run_trajects(area, amount_trajects, amount_stations, max_time, trajects)
    score = fraction_done * 10000 - (len(trajects) * 100 + Min)

    area.reset()

    # loops trough all lines
    loop_counter = amount_trajects -1
    i = 0
    while True:
        if i == loop_counter or len(trajects) == 1:
            break
        current = []

        # makes a list of all trajects except the one
        j = amount_trajects - 1
        for a in trajects:
            if j != i:
                current.append(a)
            j -= 1

        # test the score
        test_fraction_done, test_Min = run_trajects(area, len(current), amount_stations, max_time, current)
        test = test_fraction_done * 10000 - (len(current) * 100 + test_Min)
        area.reset()

        # replaces the trajects if the new combination is better
        if score < test:
            trajects = current
            score = test
        i += 1
    return trajects

def remove_end(area: Rail_NL, amount_stations: int, max_time: int,
                trajects: list[list[str]]) -> tuple[float,  int,  list[list[str]]]:
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
    fraction_done, time= run_trajects(area, len(trajects), amount_stations, max_time, trajects)
    score = fraction_done * 10000 - time - (len(trajects) * 100)

    for i in range(len(trajects)):
        while True:
            changes = 0
            current = []
            for j in range(len(trajects)):
                if j == i:
                    if len(trajects[j][:-1]) > 1:
                        current.append(trajects[j][:-1])
                else:
                    if len(trajects[j]) > 1:
                        current.append(trajects[j])
            area.reset()
            current_fraction_done, current_time= run_trajects(area, len(current), amount_stations, max_time,
                                                                current)
            current_score = current_fraction_done * 10000 - current_time - (len(current) * 100)
            if current_score > score:
                trajects = current
                score = current_score
                fraction_done = current_fraction_done
                time = current_time
                changes += 1
            if changes == 0:
                break
    return fraction_done, time, trajects



