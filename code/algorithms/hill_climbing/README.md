# Hill Climbing Directory README

## Team-Trein Hill Climbing Algorithm

This directory contains the implementation of a Hill Climbing algorithm. The algorithm starts with an initial solution and iteratively attempts to improve it by making small modifications.

## Overview

The Hill Climbing algorithm optimizes a combination of train tracks. The algorithm starts by generating a solution. Then, for every track in this solution, the algorithm creates a certain (chosen) amount of neighbours. These neighbours are the same as the solution, except one of the tracks has been replaced. Then the algorithm finds the neighbour with the highest score. If this score is higher than the original score, replace the original solution by this "best neighbor" and repeat. If not, keep going until the number of iterations is achieved:

1. **Greedy Initialization:** The algorithm starts with a greedy track and replaces tracks by greedy tracks.
2. **Random Optimization Initialization:** The algorithm starts with a random optimized track and replaces tracks by random optimized tracks.
3. **Random Initialization:** If neither of the above options is chosen, the algorithm starts with a completely random track and replaces tracks with other random tracks.

The main script, `hill_climbing.py`, runs this algorithm and provides the final optimized solution along with the objective function value (K) and the list of trajectories.

## Usage

python main.py small/large hill_climbing/hill_climbing_optim/hill_climbing_greedy number_of_iterations 

## Warning

Run this algorithm only from main.py