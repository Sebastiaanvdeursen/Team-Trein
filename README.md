# Team-Trein

The assignment of RailNL is to create a lining system of intercity trains in the Netherlands or Holland utilizing heuristics and various constructive or iterative algorithms. 
The goal is to maximize the objective function    
K = p \*10000 - (T\*100 + Min) by trying out different algorithms. In this objective function, K is the quality of the lining system, 
p is the fraction of connections that have been ridden, T is the amount of routes used and Min is the total amount of minutes used by all the routes together. This object function has two 
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
Run the code by typing 
```
python main.py large/small algorithm size all/hist
```
You can also opt to not include size, then one iteration will be ran.
By typing large you run the chosen algorithm on the Netherlands and by typing small you only use Holland. 

For algorithms you can choose
between find_p, annealing, random, random_optim, greedy_random, greedy_random_max, greedy_optim, hill_climbing, hill_climbing/greedy,
hill_climbing/greedy_max, hill_climbing/greedy_optim, hill_climbing/greedy_optim_max or double_greedy. 
Adding hist to the command creates a histogram using the result, adding all also gives the average.

You can also use main.py large/small algorithm time minutes, to make the algorithm run for a certain amount of time, it saves all the results in a pickle file and displays the top result.

### Structure
The following list shows where you can find the most important files and folders of this project:
- **/code:** holds all the code of our project
    - **/code/algorithms:** posseses the code of all the algorithms we used
    - **/code/classes:** contains the 4 classes we use, this describes the inherent structure of our problem
    - **/code/visualisation:** contains the code for the visualisation of the stations and corresponding connections
- **/data:** contains all the data files that are used to run the algorithms and perform the visualisation

## Authors
- Sebastiaan van Deursen
- Mathijs Leons
- Ties Veltman