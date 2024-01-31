# README Dicionary algorithms

## Team Trein

This directory contains the following folders:
- greedy
- hill_climbing
- plant_propagation
- random
- simulated_annealing

Here follows a summary of the content of all of these folders.

### greedy
In this directory you can find all variations of the greedy algorithm. There is a greedy with a random start present, a greedy that goes through all possible combinations, 
a greedy that looks ahead two connections and a greedy that calculates a probability of going on a track based on its time and whether the connection has been riden already or not.

### hill_climbing
In this directory there is a hill climbing algorithm file present which can start with a random track, greedy track or random optimized track. 
Neighbors are found and when an improvement in score is spotted, it is chosen always. If there is no improvement, it is not chosen.

### plant_propagation
In this directory there is the file of the evolutionary algorithm plant propagation. 

### random
In this directory we have a file of the random algorithm and random optimized algorithm. The random optimized algorithm checks if a connection has already been used, random does not.

### simulated_annealing
In this file we find the code for the algorithm for simulated annealing, which is the same as hill_climbing only know we can choose a worse solution with a probability.

For more specific information, please look at the README in any of these directories.
