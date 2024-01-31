from code.algorithms.greedy.greedy_random_start import run_greedy_track_random
from code.algorithms.greedy.weighted_greedy import run_weighted
from code.algorithms.greedy.weighted_greedy import weighted_track
from code.classes.rail_NL import Rail_NL
from code.other.remove_unnecessary import remove_end
from code.other.remove_unnecessary import removing_lines
from code.other.run import run_trajects

import matplotlib.pyplot as plt
import random


class plant:
    """
    plant class is used to perform the plant propagation algorithm on the RailNL problem.
    plant propagation is simplified to fit this specific problem.
    It utilizes the greedy_weighted algorithm with a selected starting station to create minor
    deviations from the original.
    The runners are selected using tournament style selection

    methods:
        - init(area: object, amount_trajects: int, max_time: int,
          amount_stations: int, iterations: int, power = 1)
            - creates the necessary variables for continued operation
              and creates the first runners

        - run_program()
            - runs the program the selected amount of time using
              the create_children and select_children function
            - prints the result using the print function

        - create_children()
            - creates runners using the greedy_track function from greedy_random_start
              and the weighted_track from greedy_weighted. Furthermore it optimizes them using
              removing_lines and remove_ends
            - runs select_children()

        - select_children()
            - selects the best sets of tracks from the runners and the original 5 using tournament
              style selection and saves them in self.tracks

        - self.print(traject: list[list[str]], score: float)
            - runs a final removing_lines on the trajects
            - prints the results in the correct style including the score

        - self.get_data() -> list[floats]
            - returns the list of the highest score of each iteration
    """
    def __init__(self, area: Rail_NL, amount_trajects: int, max_time: int,
                 amount_stations: int, iterations: int,
                 power: float = 1) -> None:
        """
        pre:
        - area is a railNL object (can be large or small map)
        - the amount of trajects allowed as an int
        - the maximum amount of time per traject as an int
        - the amount of stations in the area object
        - the amount of iterations as an int.

        post:
        - saves all input in self. format for use in other functions
        - initializes empty list that saves the highest score of each iteration
        - sets the starting power for weighted greedy
        - creates a list of the names of all the stations as strings.
        - Creates the first trajects and runs select_children
          to select the best 5 of them.
        """
        # The list with all the best results of each iteration
        self.data: list[float] = []
        self.power = 0.25
        self.replace_power = power

        # 15 is an arbritrary amount that can be changed hower,
        # if it isnt divided by iterations
        # it will moest likely cause an integer overflow (values over 30 cause error)
        self.power_increase = 5 / (iterations)

        # Saving the input variables
        self.amount_stations = amount_stations
        self.amount_trajects = amount_trajects
        self.max_time = max_time
        self.area = area

        # Making sure that the area object is clean
        self.area.reset()
        self.succes = 0
        self.list_stations = []
        self.iterations = iterations

        # Creating a list of all stations
        for station_name in area.stations:
            self.list_stations.append(station_name)

        self.children: list[list[list[str]]] = []
        self.tracks: list[list[list[str]]] = []
        self.highest_score = 0
        self.best: list[list[str]] = []

        # Creating the starting trajects, we start with 25 and select 5 as opposed to the regular formula
        # of just starting with 5
        start_power = 0.25
        for _ in range(30):
            self.children.append(run_weighted(self.area, amount_trajects,
                                              max_time, amount_stations, printed=False, info=True,
                                              power=start_power)[3])
            start_power += 0.1

        # Selecting the 5 best of the starting trajects
        self.select_children(True)

    def run_program(self) -> None:
        """
        runs the plant propagation algorithm the amount of times that was put in, in init.

        pre: uses the variables that where created in init

        post: runs the print function which prints the best score and best traject, the area object
        will be modified based upon the last iteration ran
        """
        for _ in range(self.iterations):
            self.create_children()

        self.print(self.best, self.highest_score)

    def print(self, traject: list[list[str]], score: float) -> None:
        """
        prints the inputed trajects and score in the correct manner so that it can be used for check50

        pre:
            - takes the score as a float or integer, takes traject as a list of list of strings

        post:
            - print function which prints the best score and best traject
            - makes a plot of the best result of each iteration
        """
        i = 1
        traject = removing_lines(self.area, len(traject), self.amount_stations, self.max_time, traject)
        for a in traject:
            stations_str = ', '.join(a)
            print(f"train_{i},\"[{stations_str}]\"")
            i += 1
        print(f"score,{score}")
        plt.plot(range(self.iterations + 1), self.data)
        plt.show()

    def create_children(self) -> None:
        """
        creates the new trajects based upon the previous results, change is based upon how great the
        solution is.

        pre:
            - self.tracks is a list of list of list of strings, the strings are stations
                they need to be connected and in the correct order

        post:
            - creates the children object as a list of list of list of strings
            - runs the select_children function on the children object
        """
        # Creates the necessary variables
        self.children  = []
        first = True
        amount_children = [7, 6, 5, 4, 3, 3]
        counter = 0
        probs_remove = [1, 3, 5, 6, 7, 8]

        # Runs the algorithm for each instance of the current population
        for parent in self.tracks:
            max_additions = self.amount_trajects - len(parent)
            current = []
            for _ in range(amount_children[counter]):
                # Loads in the connections currently used
                run_trajects(self.area, len(parent),
                             self.amount_stations, self.max_time, parent)

                # Adds a new trraject if probabilities are met
                if not first:
                    if max_additions > 0:
                        if random.randint(0, 10) < probs_remove[counter]:
                            additions = random.randint(0, max_additions)
                        else:
                            additions = 0
                        if additions > 0:
                            for _i in range(additions):
                                current.append(weighted_track(self.area, self.amount_stations, self.max_time,
                                                              self.list_stations, printed=False, power=self.power
                                                              )[2].traject_connections)
                else:
                    first = False

                # Replaces a random traject with either a weighted from the same start
                # or a greedy track from a random start
                replace = random.randint(0, len(parent) - 1)
                count = 0

                for i in parent:
                    if count == replace and len(current) < self.amount_trajects:
                        if random.randint(0, 10) > probs_remove[counter]:
                            new = weighted_track(self.area, self.amount_stations,
                                                 self.max_time, self.list_stations,
                                                 printed=False,
                                                 start=self.list_stations.index(i[0]),
                                                 power=self.replace_power)
                        else:
                            new = run_greedy_track_random(self.area, self.amount_stations, self.max_time,
                                                          self.list_stations,
                                                          False, printed=False)

                        current.append(new[2].traject_connections)
                    elif len(current) < self.amount_trajects:
                        current.append(i)

                    count += 1

                # Optimises the trajects and adds them to the list
                current = removing_lines(self.area, len(current),
                                         self.amount_stations,
                                         self.max_time, current)
                self.children.append(current)
            counter += 1
            self.power += self.power_increase

        # Runs the selection code
        self.select_children()

    def select_children(self, first: bool = False) -> None:
        """
        selects the best runners using tournament style selection,
        randomly assigns each set of tracks to a list and calculates it score
        sorts them by score (descending) and takes the set with the highest
        score from each list

        pre:
            - self.children needs to be of length 25 or 30 (only
              first iteration) and needs to be list of list of strings
              with functioning tracks

        post:
            - adds the selected runners to a list called tracks
              this list will always be 5 long and will be used to create new runners
            - adds the highest score to the data list for later use in graph
        """
        # Creates the index list for the tournament selection
        list_indexes = [0] * 6 + [1] * 6 + [2] * 6 + [3] * 6 + [4] * 6
        random.shuffle(list_indexes)

        list_of_values = [None] * 5

        # Add the 5 tracks from previous round to tournament
        if not first:
            for i in range(5):
                self.area.reset()
                p, Min = run_trajects(self.area, len(self.tracks[i]),
                                      self.amount_stations, self.max_time,
                                      self.tracks[i])
                k = p * 10000 - (len(self.tracks[i]) * 100 + Min)
                index = list_indexes.pop(0)
                if list_of_values[index] is None:
                    list_of_values[index] = [[self.tracks[i], k]]
                else:
                    list_of_values[index].append([self.tracks[i], k])

        if first:
            amount = 30
        else:
            amount = 25

        # Add the runners to the tournament
        for i in range(amount):
            p, Min, self.children[i] = remove_end(self.area, self.amount_stations,
                                                  self.max_time, self.children[i])
            score = p * 10000 - (len(self.children[i]) * 100 + Min)
            index = list_indexes.pop(0)
            if list_of_values[index] is None:
                list_of_values[index] = [[self.children[i], score]]
            else:
                list_of_values[index].append([self.children[i], score])

        # Select the highest from each of the list
        self.selected = []
        for index in range(5):
            list_of_values[index].sort(key=lambda x: x[1], reverse=True)
            self.selected.append(list_of_values[index][0])

        self.selected.sort(key=lambda x: x[1], reverse=True)
        if self.highest_score < self.selected[0][1]:
            self.best = self.selected[0][0]
            self.highest_score = self.selected[0][1]

        # Save the selected set of tracks
        self.data.append(self.selected[0][1])
        self.tracks = []
        for track in self.selected:
            self.tracks.append(track[0])

    def get_data(self) -> list[float]:
        """
        returns the best value of each iteration, can be used for plots

        pre:
            - self.data needs to exist

        post:
            - returns a list of floats
        """
        return self.data
