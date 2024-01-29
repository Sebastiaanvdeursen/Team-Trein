from code.classes.traject import Traject
from code.classes.rail_NL import Rail_NL

def run_trajects(area: Rail_NL, amount_trajects: int, amount_stations: int, max_time: int,
                  trajects: list[list[str]], printed: bool, final: bool = False) -> [float, int] or float:
    time = 0
    solution = []
    for i in range(amount_trajects):
        traject = area.create_traject(trajects[i][0], area)
        solution.append(traject)
        for j in range(1, len(trajects[i])):
            traject.move(trajects[i][j])
        time += traject.total_time
        if printed:
            traject.show_current_traject()


    n_done = 0
    for station in area.stations.values():
            for connection in station.connections.values():
                if connection.done == True:
                    n_done += 1

    fraction_done = (n_done / 2) / area.total_connections
    if final:
        return fraction_done, time
    else:
        return fraction_done * 10000 - time - (len(trajects) * 100)