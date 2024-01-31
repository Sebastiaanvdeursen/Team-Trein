# Visualization Repository README

## Team-Trein Visualization

This repository contains a Python script for visualizing train routes in the Netherlands. The script takes a CSV file containing train routes and displays them on a map of the Netherlands. The visualization includes scatter plots of coordinates, connections between places, and arrows for the tracks (different colors for different tracks).

## Overview

### visualization.py
visualization.py first takes the CSV file containing all the coördinates of the train stations in the Netherlands (for small only Holland), and then makes a scatterplot of this on a map of the Netherlands. Then takes a CSV file containing the train routes. For every track, it chooses a corresponding color and then makes arrows with this color showing the track on the map. Then it also makes a legend showing the track names with the corresponding colors. 

### plot_simulated.py
(Ties hier wat schrijven)


## File Structure

- `visualisation.py`: Main script for visualization.
- `plot_simulated`: (Ties hier wat schrijven)
- `map/map_netherlands`: A png file containing a map of the Netherlands

## Usage

### Main visualization

First output your solution to output.csv in the main directory. Example:
python main.py small random 1 > output.csv

Then run the visualization as follows (if you ran small, choose small. If you ran large, choose large):
python main.py small/large vis/visualization


### Authors

- Sebastiaan van Deursen