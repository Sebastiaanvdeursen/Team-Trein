from code.algorithms.greedy_random_start import run_greedy_random
from code.algorithms.greedy_best_comb import run_trajects
from code.algorithms.random_alg import run_random_traject
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.weighted_greedy import run_weighted
from code.algorithms.weighted_greedy import weighted_track


import random

class plant:
    def __init__(self, area, amount_trajects, max_time, amount_stations, iterations):
        self.amount_stations = amount_stations
        self.amount_trajects = amount_trajects
        self.max_time = max_time
        self.area = area
        self.area.reset()
        self.succes = 0
        self.list_stations = []
        self.iterations = iterations
        for station_name in area.stations:
            self.list_stations.append(station_name)
        self.children = []
        self.tracks = []
        self.highest_score = 0
        self.best = []
        for _ in range(25):
            self.children.append(run_greedy_random(self.area, amount_trajects,
                                                  max_time, amount_stations, printed = False, info = True)[3])
        self.select_children()


    def run_program(self):
        for _ in range(self.iterations):
            self.create_children()

        self.print(self.best, self.highest_score)

    def print(self, traject, score):
        i = 0
        for a in traject:
            print(f"train_{i}:{a}")
            i += 1
        print(f"score,{score}")

    def create_children(self):
        self.children  = []
        first = True
        for parent in self.tracks:
            max_additions = self.amount_trajects - len(parent)
            current = []
            for _ in range(5):

                run_trajects(self.area, len(parent),
                                           self.amount_stations, self.max_time, parent, False)
                if first == False:
                    if max_additions > 0:
                        additions = random.randint(0, max_additions)
                        if additions > 0:
                            for i in range(additions):
                                current.append(weighted_track(self.area, self.amount_stations, self.max_time, self.list_stations, printed = False)[2].traject_connections)
                else:
                    first = False
                replace = -1
                replace_random = random.randint(0, 100)
                if replace_random > 95:
                    replace = random.randint(0, len(parent) - 1)
                count = 0
                for i in parent:
                    if count == replace and len(current) < self.amount_trajects:
                        current.append(weighted_track(self.area, self.amount_stations, self.max_time, self.list_stations, printed = False)[2].traject_connections)
                    elif len(current) < self.amount_trajects:
                        current.append(i)
                    count += 1
                self.area.reset()
                current = removing_lines(self.area, len(current), self.amount_stations, self.max_time, current)
                self.children.append(current)
        self.select_children()



    def select_children(self):
        self.selected = []
        for i in range(5):
            self.area.reset()
            self.selected.append([self.children[i],
                                 run_trajects(self.area, len(self.children[i]),
                                               self.amount_stations, self.max_time, self.children[i], False)])
        self.selected.sort(key = lambda x: x[1])
        if self.selected[4][1] > self.highest_score:
             self.highest_score = self.selected[4][1]
             self.best = self.selected[4][0]
        for i in range(5, 25):
            self.area.reset()
            score = run_trajects(self.area, len(self.children[i]),
                                               self.amount_stations, self.max_time, self.children[i], False)
            if score > self.selected[0][1]:
                self.selected[0]= [self.children[i], score]
                if score > self.selected[1][1]:
                    self.selected[0] = self.selected[1]
                    self.selected[1] = [self.children[i], score]
                    if score > self.selected[2][1]:
                        self.selected[1] = self.selected[2]
                        self.selected[2] = [self.children[i], score]
                        if score > self.selected[3][1]:
                            self.selected[2] = self.selected[3]
                            self.selected[3] = [self.children[i], score]
                            if score > self.selected[4][1]:
                                self.selected[3] = self.selected[4]
                                self.selected[4] = [self.children[i], score]
                                if score > self.highest_score:
                                    self.highest_score = score
                                    self.best = self.children[i]

        self.selected.sort(key = lambda x: x[1], reverse = True)

        self.tracks = []
        for track in self.selected:
            self.tracks.append(track[0])




