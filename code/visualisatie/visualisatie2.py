import sys
import csv
import numpy as np
import json
from PIL import Image
from random import randint
from bokeh.plotting import figure, show, output_file
from bokeh.models import Range1d


def convert_list_to_string(string_list):
    list = []
    number_of_comma = 0
    comma_index = 0
    for i in range(len(string_list)):
        if string_list[i] == "[":
            index = i
            while True:
                i += 1
                if string_list[i] == "," and index == 0:
                    list.append(string_list[index + 1: i])
                    index = i
                elif string_list[i] == ",":
                    list.append(string_list[index + 2: i])
                    index = i
                elif string_list[i] == "]":
                    list.append(string_list[index + 2: i])
                    break
    return list



def read_train_data(filename):
    train_data = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            train_name = row['train']
            string_stations = row['stations']
            stations = convert_list_to_string(string_stations)
            train_data[train_name] = stations
    return train_data

def assign_colors(train_data):
    train_colors = {}
    palette = []
    for i in range(len(train_data)):
        palette.append('#%06X' % randint(0, 0xFFFFFF))
    for i, train_name in enumerate(train_data):
        train_colors[train_name] = palette[i]
    return train_colors


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

def draw_lines_connections(lines, places, p):
    with open(f"../../data/Connecties{lines}.csv") as line_info:
        csv_file = csv.reader(line_info, delimiter=',')
        line_count = 0
        for row in csv_file:
            if line_count != 0:
                p.line([places[row[0]][1], places[row[1]][1]], [places[row[0]][0], places[row[1]][0]], color = "black")
            line_count += 1
    return p

def draw_lines_trajects(train_data, train_colors, places, p):
    start_to_end_station = {}
    trajectory_counts = {}

    for train_name, stations in train_data.items():
        color = train_colors[train_name]
        for i in range(len(stations) - 1):
            start_station = stations[i]
            end_station = stations[i + 1]

            trajectory_key = (start_station, end_station)
            count = trajectory_counts.get(trajectory_key, 0)
            trajectory_counts[trajectory_key] = count + 1

            vertical_offset = count * 0.025
            start_y = places[start_station][0] + vertical_offset
            end_y = places[end_station][0] + vertical_offset

            start_to_end_station[start_station] = end_station
            p.line([places[start_station][1], places[end_station][1]],
                   [start_y, end_y],
                   color=color, line_width=2)

    show(p)

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
    p = draw_lines_connections(lines, places, p)  # If places is not used elsewhere, you can remove it from the arguments

    input_filename = "../../output.csv"

    train_data = read_train_data(input_filename)

    train_colors = assign_colors(train_data)
    draw_lines_trajects(train_data, train_colors, places, p)

