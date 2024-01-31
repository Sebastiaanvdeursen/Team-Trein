# Visualization Repository README

## Team-Trein Visualization

This repository contains a Python script for visualizing train routes in the Netherlands. The script takes a CSV file containing train routes and displays them on a map of the Netherlands. The visualization includes scatter plots of coordinates, connections between places, and arrows for the tracks (different colors for different tracks).

## Overview

### visualization.py

visualization.py first takes the CSV file containing all the coördinates of the train stations in the Netherlands (for small only Holland), and then makes a scatterplot of this on a map of the Netherlands. Then takes a CSV file containing the train routes. For every track, it chooses a corresponding color and then makes arrows with this color showing the track on the map. Then it also makes a legend showing the track names with the corresponding colors. 

### plot_simulated.py

plot_simulated.py plots both the exponential temperature function and the score of the solution chosen over time. You can plot the algorithm for both small and large the amount of iterations, namely 10000, is fixed, since the score will almost always converge after that point with the chosen parameters of 500 for the initial temperature and 0.4 for the exponent.

## File Structure

- `visualisation.py`: Main script for visualization.
- `plot_simulated.py`: Script to plot the score and temperature function of the simulated annealing algorithm.
- `map/map_netherlands`: A png file containing a map of the Netherlands.

## Usage

### Main visualization

First output your solution to output.csv in the main directory. Example:
```
python main.py small random 1 > output.csv
```

Then run the visualization as follows (if you ran small, choose small. If you ran large, choose large):
```
python main.py small/large vis/visualization
```

### Simulated annealing visualization

You can run the visualization for simulated annealing by running
```
python main.py **size** simulatedplot
```
With **size** having the input of either:
- **large**    
- **small**
