# Greedy Algorithms
### by Team Trein

#### Warning run all code using main.py

### Greedy_random_start.py
Greedy_random_start is the basic implementation of the greedy algorithm.
You put in the amount of tracks you want and a clean RailNL object and the algorithm creates the tracks and returns the fraction done, the final amount of tracks, the tracks as list of list of strings and the total amount of time used.
The algorithm consists of two functions:
#### run_greedy_random:
this algorithm initializes the creation and returns the completed tracks. It also performs the calculations on the complete set of tracks.
Furthermore it also runs the optimisation algorithms on the complete set to improve the tracks (It only does this if it is not used for hill climbing, indicated by the bool).
#### run_greedy_track:
This is the actual greedy algorithm. The algorithm works by always selecting the shortest possible unused connection.
If there are no unused connections it can use already used connections, however it only uses them if there is twice the amount of time available as that connection uses. This is to curcimvent useless additions at the end of the process of creating the track.
Furthermore it also stops if it has to use two used connections in a row.
If it is needed you can put in the starting station, if you did not it will use a random starting station.
It is necessary to provide a list of all the stations within the RailNL object to curcimvent errors
### Greedy_best_combo:
This version utilizes brute force to go trough all possible combinations of greedy tracks. For most people it is only possible to run this on the Holland data set as it will otherwise kill the process. It utilizes Itertools.permutations to calculate all possible combinations and runs them using run_greedy_track from greedy_random_start making use of the start option. This algorithm will provide you with the best outcome of greedy tracks. It will also only return the best combination.
### double_greedy:
double_greedy is a modified version of the greedy algorithm based upon our own heuristics. It differs from the regular because instead of looking ahead oe connection it looks for two. So it will loop trough all the connected stations and looks at their connections. It will move to the station which provides the shortest combined time (time it takes to move to first station and then continue to the next), it will not move two stations ahead at once.
It differs with used connections to the first station differently than used connections to the second, for the first it is handled the same way as in the regular greedy algorithm. If the second connection is used (connection between the station that you can move to and the second station) and the first isn't it handles it by multiplying the amount of time used by the second station by two.
### weighted_greedy
weighted greedy is a semi random algorithm we created our self. It assigns probabilities of using a connection based upon the time the connection takes and whether it is already used. It assigns the probabilities the following way: $ p_i = \frac{\frac{1}{time_i^power}}{\sum_{j = 1}^{n}(\frac{1}{time_j^power})}$
## Usage
All algorithms can only be used from the root directory of the git.
There they are performed by using main.py and then filling in the correct commandline arguments:
### All examples
*when map is used on commandline it means that the user can either put in large, large_random, small, small_random or a station he wants to exclude for more information please check the main README.
*number means a positive integer for the amount of time the user wants to run the algorithm, or the amount of minutes the user want to spend.
*the / is used when the user can use either of the options, but not both at the same time.
#### greedy_random_start:
python3 main.py map greedy/greedy_random number {hist/all/fitter}\
python3 main.py map greedy/greedy_random time number
#### greedy_best_comb
python3 main.py small greedy_optim
#### double_greedy
python3 main.py map double/double_greedy number {hist/all/fitter}\
python3 main.py map double/double_greedy number
#### Weighted greedy
python3 main.py map weight number {hist/all/fitter}\
python3 main.py map weight number
