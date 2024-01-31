# Team-Trein

The assignment of RailNL is to create a lining system of intercity trains in the Netherlands or Holland utilizing heuristics and various algorithms.
The goal is to maximize the objective function
K = p \*10000 - (T\*100 + Min) by trying out different algorithms. In this objective function, K is the quality of the lining system,
p is the fraction of connections that have been ridden, T is the amount of routes used and Min is the total amount of minutes used by all the routes together. This objective function has two
constrictions, namely a maximum amount of routes we can choose (so T has an upper bound) and a maximum amount of minutes we can use per route.

## Getting started
### Requirements
Please run the following line of code in your terminal:
```
sudo apt-get install tcl-dev tk-dev python-tk python3-tk
```
Therafter, run
```
pip install -r requirements.txt
```
or
```
conda install --file requirements.txt
```
to get everything you need.

### Usage
to run an algorithm that find a regular solution:
```
python main.py large/small iterate_algorithm number_of_iterations {all/hist}
```
or by:
```
python main.py large/small iterate_algorithm time minutes
```
For iterate_algorithm you can choose between
- annealing
- random
- random_optim
- greedy_random
- greedy_optim
- double_greedy
- hill_climbing
- hill_climbing_greedy
- hill_climbing_optim

##### to look at the explanation of each of these options please look at the algorithms part.

By typing large you run the chosen algorithm on the Netherlands and by typing small you only use Holland.

Adding hist after iterations to the command creates a histogram using the result, adding all also gives the average and uses plotter to add fitted lines. These results will be bad if to little iterations are run. This can only be used on iterations not on time.

to run the plant propagation algorithm you use:
```
python main.py large/small plant
```
To find a solution that uses all connections (part 1) use:
```
python main.py large/small find_p
```
to find a solution for part 5 of the project use:
```
python main.py large part5 number_of_different_RailNL_objects_created iterations_per_object > part5.csv
```
this will print out a list, the lower the value the more important the connection with that index is.
number_of_different_RailNL_objects_created and iterations_per_object are both integers\
to run an algorithm with a station removed use:
```
python main.py station_name greedy number_of_iterations
```
which will return the best result found in those iterations with the station excluded.
to find the shortened version of the station names that consist of multiple words please look at

To reproduce an experiment, run the following line:
```
python main.py large/small [experiment] minutes
```
the following experiments are possible
- test_weighted
- test_plant
- test_simulated
- test_hill_climbing
- test hill_climbing_greedy

minutes is the amount of time spent per changed parameter not the amount of time spent on the experiment.

To get the output from the pickle files run the following:
```
python main.py large/small pickle pickled_algorithm
```
For pickled_algorithm you can fill in the following algorithms
- simulated
- weighted
- plant
- greedy
- hill_climbing

It does not matter if you type large or small, the pickle files will be ran anyway.

### algorithms
Here below is a list of explanations of the command-line arguments of the algorithms:
- annealing represents the algorithm of simulated annealing
- random represents running the completely random algorithm
- random_optim represents running the random algorithm which accounts for connections that have already been ridden
- greedy_random runs the basic implementation of the greedy algorithm with random starting stations
- greedy_optim is a brute force algorithm that looks at all possible permutations of starting stations for greedy, thus finding the best possible set of greedy tracks
- double_greedy runs the greedy algorithm with the heuristic of looking forward 2 connections
- hill_climbing represents the hill climbing algorithm with a random start and random way of selecting neighbors
- hill_climbing_greedy represents the hill climbing algorithm with a greedy start and greedy neighbors
- hill_climbing_optim represents the hill climbing algorithm with a random optim start and random optim neighbors
- plant is the plant propagation algorithm, it is ran a 1000 iterations and a graph is created
- find_p finds a solution for part1 (using all possible connections) using the greedy algorithm


### Structure
The following list shows where you can find the most important files and folders of this project:
- **/code:** holds all the code of our project
    - **/code/algorithms:** posseses the code of all the algorithms we used, divided into subfolders
    - **/code/classes:** contains the 4 classes we use, this describes the inherent structure of our problem
    - **/code/visualisation:** contains the code for the visualisation of the stations and corresponding connections
- **/data:** contains all the data files that are used to run the algorithms and perform the visualisation
- **/docs:**

### Results
#### Holland:
Our highest score is 9210, this is always found by greedy_optim and is regularly found by greedy (90% chance of finding it using 10.000 iterations).
#### Netherlands
Our highest score is found using greedy, it is 7308.

## Authors
- Sebastiaan van Deursen
- Mathijs Leons
- Ties Veltman