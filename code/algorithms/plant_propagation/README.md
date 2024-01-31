# Plant Propagation
## Explanation of the algorithm
This algorithm tries to fit the plant propagation algorithm on the RailNL object.
It does this using a couple heuristics and algorithms we created/ decided upon, furthermore it performs selection by tournament style.
First we start by creating a starting population of 30 and select the 5 best as the start position. We do this because we have noticed that the start is very important for the end_score.
The function creates runners using either by the regular greedy algorithm or the weighted, this is done by chance, probabilities change based upon the relative ranking of the original. The amount of runners that are created also depends on the ranking of the original.
The function automatically creates a plot of the improvement overtime of the best solution found.
