from code.algorithms.greedy_random_start import run_greedy_random
from code.algorithms.greedy_random_start import run_greedy_track_random
from code.algorithms.greedy_best_comb import run_trajects
from code.algorithms.random_alg import run_random_traject
from code.algorithms.remove_unnecessary import removing_lines
from code.algorithms.weighted_greedy import run_weighted
from code.algorithms.weighted_greedy import weighted_track


import random

class plant:
    def __init__(self, area: object, amount_trajects: int, max_time: int, amount_stations: int, iterations: int):
        """
        plant class is used to perform the plant propagation algorithm on the RailNL problem
        plant propagation is simplified to fit this specific problem
        all necessary variables are created here.

        pre: uses a area object (can be large or small map), the amount of trajects allowed
        as an int, the maximum amount of time per traject as an int, the amount of stations in the area
        object and the amount of iterations as an int.

        post: saves all input in self. format for use in other functions, initializes empty list that saves
        the highest score of each iteration, sets the starting power for weighted greedy, creates a list of
        the names of all the stations as strings. Creates the first trajects and runs select_children
        to select the best 5 of them.
        """
        #the list with all the best results of each iteration
        self.data: list[float] = []
        self.power = 0.25

        ## 15 is an arbritrary amount that can be changed hower, if it isnt divided by iterations
        ## it will moest likely cause an integer overflow (values over 30 cause error)
        self.power_increase = 15 / (iterations)

        #saving the input variables
        self.amount_stations = amount_stations
        self.amount_trajects = amount_trajects
        self.max_time = max_time
        self.area = area

        #making sure that the area object is clean
        self.area.reset()
        self.succes = 0
        self.list_stations = []
        self.iterations = iterations

        #creating a list of all stations
        for station_name in area.stations:
            self.list_stations.append(station_name)
        self.children: list[list[list[str]]]= []
        self.tracks: list[list[list[str]]]= []
        self.highest_score = 0
        self.best: list[list[str]] = []

        #creating the starting trajects, we start with 25 and select 5 as opposed to the regular formula
        # of just starting with 5
        start_power = 0.25
        for _ in range(25):
            self.children.append(run_weighted(self.area, amount_trajects,
                                                  max_time, amount_stations, printed = False, info = True,
                                                    power = start_power)[3])
            start_power += 0.1

        #selecting the 5 best of the starting trajects
        self.select_children(True)


    def run_program(self):
        """
        runs the plant propagation algorithm the amount of times that was put in, in init.

        pre: uses the variables that where created in init

        post: runs the print function which prints the best score and best traject, the area object
        will be modified based upon the last iteration ran
        """
        for _ in range(self.iterations):
            self.create_children()

        self.print(self.best, self.highest_score)

    def print(self, traject: list[list[str]], score: float):
        """
        prints the inputed trajects and score in the correct manner so that it can be used for check50

        pre: takes the score as a float or integer, takes traject as a list of list of strings

        post: print function which prints the best score and best traject
        """
        i = 1
        for a in traject:
            print(f"train_{i}:{a}")
            i += 1
        print(f"score,{score}")

    def create_children(self):
        self.children  = []
        first = True
        chance = [99, 85, 75, 50, 25]
        amount_children = [7, 6, 5, 4, 3, 3]
        counter = 0
        probs_remove = [1, 3, 5, 6, 7]
        for parent in self.tracks:
            max_additions = self.amount_trajects - len(parent)
            current = []
            iterations = 4.5
            for _ in range(amount_children[counter]):

                run_trajects(self.area, len(parent),
                                           self.amount_stations, self.max_time, parent, False)
                if first == False:
                    if max_additions > 0:
                        additions = random.randint(0, max_additions)
                        if additions > 0:
                            for i in range(additions):
                                current.append(weighted_track(self.area, self.amount_stations, self.max_time,
                                                               self.list_stations, printed = False, power= self.power
                                                                 + iterations)[2].traject_connections)

                else:
                    first = False
                replace = -1
                replace_random = random.randint(0, 100)
                if replace_random > chance[counter]:
                    replace = random.randint(0, len(parent) - 1)
                chance[counter] -= 1
                count = 0

                for i in parent:
                    if count == replace and len(current) < self.amount_trajects:
                        if random.randint(0, 10) > 5:
                            current.append(weighted_track(self.area, self.amount_stations,
                                                       self.max_time, self.list_stations,
                                                         printed = False)[2].traject_connections)
                        else:
                            current.append(run_greedy_track_random(self.area, self.amount_stations, self.max_time,
                              False, printed = False)[2].traject_connections)
                    elif len(current) < self.amount_trajects:
                        current.append(i)
                    count += 1
                #if random.randint(0, 10) > probs_remove[counter]:
                self.area.reset()
                current = removing_lines(self.area, len(current), self.amount_stations, self.max_time, current)
                self.children.append(current)
                iterations -= 0.5
            counter += 1
            self.power += self.power_increase
        self.select_children()



    def select_children(self, first = False):
        self.selected = []
        if first:
            for i in range(5):
                self.area.reset()
                self.selected.append([self.children[i],
                                        run_trajects(self.area, len(self.children[i]),
                                               self.amount_stations, self.max_time,
                                                 self.children[i], False)])
            self.selected.sort(key = lambda x: x[1])
        else:
            for i in range(5):
                self.area.reset()
                self.selected.append([self.tracks[i],
                                        run_trajects(self.area, len(self.tracks[i]),
                                               self.amount_stations, self.max_time,
                                                 self.tracks[i], False)])
            self.selected.sort(key = lambda x: x[1])
        if self.selected[4][1] > self.highest_score:
            self.highest_score = self.selected[4][1]
            self.best = self.selected[4][0]
        for i in range(25):
            self.area.reset()
            score = run_trajects(self.area, len(self.children[i]),
                                               self.amount_stations,
                                                 self.max_time, self.children[i], False)
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
        self.data.append(self.selected[0][1])
        self.tracks = []
        for track in self.selected:
            self.tracks.append(track[0])

    def get_data(self):
        return self.data




