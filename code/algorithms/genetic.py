from code.algorithms.greedy_random_start import run_greedy_random
from code.algorithms.greedy_best_comb import run_trajects

import random

class genetic:
    def __init__(self, area, amount_trajects, max_time, amount_stations, iterations):
        self.area = area
        self.area.reset()
        self.list_stations = []
        self.iterations = iterations
        for station_name in area.stations:
            self.list_stations.append(station_name)
        self.tracks = []
        for _ in range(5):
            self.tracks.append(run_greedy_random(self.area, amount_trajects,
                                                  max_time, amount_stations, printed = False, info = True)[3])

    def run_program(self):
        for _ in range(self.iterations):
            self.create_children()
        score = 0
        result = []
        for finalist in self.tracks:
            self.area.reset()
            current = run_trajects(self.area, self.amount_trajects,
                                   self.amount_stations, self.max_time, finalist, False)
            self.area.reset()
            if score < current:
                score = current
                result  = finalist
        self.print(result, score)

    def print(traject, score):
        i = 0
        for a in traject:
            print(f"train_{i}:{a}")
        print(f"score,{score}")

    def create_children(self):
        self.children = []
        for parent in self.tracks:
            for _ in range(5):
                random_change = random.randint(0, len(parent) - 1)
                start_change = random.randint(0, len(parent[random_change]) - 1)
                connections =
        self.select_children(self)


    def select_children(self):
        self.selected = []
        self.area.reset()
        for i in range(5):
            self.selected[i] = [self.children[i],
                                 run_trajects(self.area, self.amount_trajects,
                                               self.amount_stations, self.max_time, self.children[i], False)]
        self.selected.sort(key = lambda x: x[1])
        for i in range(5, 25):
            score = run_trajects(self.area, self.amount_trajects,
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




