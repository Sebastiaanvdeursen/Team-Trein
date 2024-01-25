import sys
import csv
import numpy as np
from PIL import Image
from bokeh.plotting import figure, show, output_file
from bokeh.models import Range1d

def scatterplot(coords):
    places = {}
    with open(f"../../data/coordinates{coords}.csv") as data:
        csv_read = csv.reader(data, delimiter=',')
        line_count = 0
        for row in csv_read:
            if line_count != 0:
                places[row[0]] = [float(row[1]), float(row[2])]
            line_count += 1

    l_x = []
    l_y = []
    for a in places:
        l_x.append(places[a][1])
        l_y.append(places[a][0])

    p = figure(title="Scatter Plot", width=1100, height=850, x_axis_label="x", y_axis_label="y")

    p.image_url(url=['map_netherlands.jpg'], x=3.05, y=53.7, w=4.4, h=3.1)

    p.circle(l_x, l_y, color = "black")
    # return places  # If not used, you can remove this line
    return p, places

def draw_lines(lines, places, p):
    with open(f"../../data/Connecties{lines}.csv") as line_info:
        csv_file = csv.reader(line_info, delimiter=',')
        line_count = 0
        for row in csv_file:
            if line_count != 0:
                p.line([places[row[0]][1], places[row[1]][1]], [places[row[0]][0], places[row[1]][0]], color = "black")
            line_count += 1
    show(p)  # Show the lines plot immediately

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "large":
            coords = "Long"
            lines = "NL"
        else:
            coords = "Short"
            lines = "Holland"
    else:
        coords = "Short"
        lines = "Holland"

    # places = scatterplot(coords)  # Uncomment this line if you want to use the places variable elsewhere
    p, places = scatterplot(coords)
    draw_lines(lines, places, p)  # If places is not used elsewhere, you can remove it from the arguments

