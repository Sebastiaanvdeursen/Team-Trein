"""
Algorithms & Heuristics

Group: Team-Trein

Visualisation takes a csv file, containing train routes in the Netherlands and
visualises the routes on a map of the Netherlands.

By: Sebastiaan van Deursen
"""


import sys
import csv
from bokeh.plotting import figure, show
from bokeh.models import Arrow, VeeHead


def convert_list_to_string(string_list: str) -> list[str]:
    """
    Convert a string representation of a list to a Python list.

    pre:  string_list is a valid string representation of a list (for example: "[Gouda, Breda, Eindhoven]").
    post: Returns the corresponding Python list (["Gouda", "Breda", "Eindhoven"]).
    """
    list = []
    for i in range(len(string_list)):
        if string_list[i] == "[":
            index = i
            while True:
                i += 1
                # When we encounter the first comma, add the entire word after the
                # "[" to the list
                if string_list[i] == "," and index == 0:
                    list.append(string_list[index + 1: i])
                    index = i
                # When encountering a comma later, add the word before it to the list
                elif string_list[i] == ",":
                    list.append(string_list[index + 2: i])
                    index = i
                # When encountering the "]", so the end of the input, add the word before
                # it to the list
                elif string_list[i] == "]":
                    list.append(string_list[index + 2: i])
                    break
    return list


def read_train_data(filename: str) -> dict[str, list[str]]:
    """
    Read train data from a CSV file.

    pre:  filename is a valid path to a CSV file containing train data.
    post: Returns a dictionary with train names as keys and lists of stations as values.
    """
    train_data = {}
    # open the CSV file
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # for every line, add the train name and the corresponding
        # traject to the train_data dictionary
        for row in reader:
            train_name = row['train']
            string_stations = row['stations']
            stations = convert_list_to_string(string_stations)
            train_data[train_name] = stations
    return train_data


def assign_colors(train_data: dict[str, list[str]]) -> dict[str, str]:
    """
    Assign random colors to each train in the given train data.

    pre:  train_data is a dictionary with train names as keys and lists of stations as values.
    post: Returns a dictionary mapping each train name to a randomly generated color.
    """
    train_colors = {}
    colors = ["red", "green", "turqoise", "blue", "pink", "purple", "orange", "yellow",
              "magenta", "saddlebrown", "lightcoral", "mediumslateblue", "forestgreen", "gold",
              "firebrick", "navy", "darkorange", "olive", "cyan", "purple"]
    # make a list palette, to store all the colors
    palette = []
    for i in range(len(train_data)):
        # add a random color to the palette
        palette.append(colors[i])
    for i, train_name in enumerate(train_data):
        # now link every traject to a color
        train_colors[train_name] = palette[i]
    return train_colors


def scatterplot(coords: str) -> tuple[figure, dict[str, list[float]]]:
    """
    Create a scatter plot of coordinates with a map background.

    pre:  coords is either "Short" or "Long" indicating the type of coordinates to be plotted.
    post: Returns a Bokeh plot object and a dictionary of places with their coordinates.
    """
    # make the empty figure
    p = figure(title="Scatter Plot", width=1100, height=850, x_axis_label="x", y_axis_label="y")
    places = {}
    # read the coördinates data
    with open(f"data/Coordinates{coords}.csv") as data:
        csv_read = csv.reader(data, delimiter=',')
        line_count = 0
        for row in csv_read:
            if line_count != 0:
                # now link the station names to the x and y coördinates
                # in the dictionary places
                places[row[0]] = [float(row[1]), float(row[2])]
            line_count += 1

    l_x = []
    l_y = []
    # add all the x coördinates to l_x and y coördinates to l_y
    for a in places:
        l_x.append(places[a][1])
        l_y.append(places[a][0])

    # add the map of the Netherlands as background image
    p.image_url(url=['code/visualization/map/map_netherlands.jpg'], x=3.05, y=53.7, w=4.4, h=3.1)

    # add the coördinates as black circles to the figure
    p.circle(l_x, l_y, color="red", size=4.5)
    return p, places


def draw_lines_connections(lines: str, places: dict[str, list[float]], p: figure) -> figure:
    """
    Draw connections between places on the given Bokeh plot.

    pre:  lines is either "NL" or "Holland" indicating the type of connections to be drawn.
          places is a dictionary with place names as keys and their coordinates as values.
          p is a Bokeh plot object.
    post: Modifies the Bokeh plot to include lines connecting places based on the specified connections.
    """
    # open the connections data
    with open(f"data/Connecties{lines}.csv") as line_info:
        csv_file = csv.reader(line_info, delimiter=',')
        line_count = 0
        # now draw a line for every connection
        for row in csv_file:
            if line_count != 0:
                p.line([places[row[0]][1], places[row[1]][1]], [places[row[0]][0], places[row[1]][0]],
                       color="black")
            line_count += 1
    return p


def draw_lines_trajects(train_data: dict[str, list[str]], train_colors: dict[str, str],
                        places: dict[str, list[float]], p: figure) -> None:
    """
    Draw trajectories of trains on the given Bokeh plot.

    pre:  train_data is a dictionary with train names as keys and lists of stations as values.
          train_colors is a dictionary mapping train names to colors.
          places is a dictionary with place names as keys and their coordinates as values.
          p is a Bokeh plot object.
    post: Modifies the Bokeh plot to include arrows representing train trajectories.
    """
    # initialize dictionary to keep track of the amount of times
    # a trajectory has been drawn
    trajectory_counts = {}

    for train_name, stations in train_data.items():
        # get the color of the traject
        color = train_colors[train_name]
        for i in range(len(stations) - 1):
            start_station = stations[i]
            end_station = stations[i + 1]

            # there is no difference between a connection
            # being done one way or the other, so we have
            # to check both ways
            trajectory_key_1 = (start_station, end_station)
            trajectory_key_2 = (end_station, start_station)

            # get the amount of times the connection has been
            # done from the trajectory_counts dictionary
            count_1 = trajectory_counts.get(trajectory_key_1, 0)
            count_2 = trajectory_counts.get(trajectory_key_2, 0)

            # add one to the count for both ways
            trajectory_counts[trajectory_key_1] = count_1 + 1
            trajectory_counts[trajectory_key_2] = count_2 + 1

            # create an offset so the lines won't overlap
            offset = max([count_1, count_2]) * 0.025

            # check if traject moves more in the x or y direction
            # and add the offset accordingly
            if abs(places[start_station][1] - places[end_station][1]) > \
               abs(places[start_station][0] - places[end_station][0]):
                start_y = places[start_station][0] + offset
                end_y = places[end_station][0] + offset
                start_x = places[start_station][1]
                end_x = places[end_station][1]
            else:
                start_y = places[start_station][0]
                end_y = places[end_station][0]
                start_x = places[start_station][1] + offset
                end_x = places[end_station][1] + offset

            # add the trajects as arrows to the figure
            p.add_layout(Arrow(end=VeeHead(size=5), line_color=color,
                         x_start=start_x, y_start=start_y, x_end=end_x, y_end=end_y))

    show(p)


def visualization(command_arg: str, filename: str):
    # use command line arguments to choose between
    # Holland or the Netherlands
    if command_arg == "large":
        coords = "Long"
        lines = "NL"
    else:
        coords = "Short"
        lines = "Holland"

    # make a figure (p) containing the coördinates and
    # the map of the Netherlands
    p, places = scatterplot(coords)

    # draw the possible connection lines
    p = draw_lines_connections(lines, places, p)

    # get the train_data
    train_data = read_train_data(filename)

    # get the traject colors
    train_colors = assign_colors(train_data)

    # draw the traject arrows
    draw_lines_trajects(train_data, train_colors, places, p)
