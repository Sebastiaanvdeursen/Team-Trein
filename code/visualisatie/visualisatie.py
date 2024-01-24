import sys
import csv
import matplotlib.pyplot as plt


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

    plt.scatter(l_x, l_y)
    return places


def draw_lines(lines, places):
    with open(f"../../data/Connecties{lines}.csv") as line_info:
        csv_file = csv.reader(line_info, delimiter=',')
        line_count = 0
        for row in csv_file:
            if line_count != 0:
                print(row[0], row[1])
                print(places[row[0]])
                print(places[row[1]])
                plt.plot([places[row[0]][1], places[row[1]][1]], [places[row[0]][0], places[row[1]][0]], 'k-', lw=2)
            line_count += 1


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

    places = {}
    places = scatterplot(coords)
    draw_lines(lines, places)

    if coords == "Short":
        plt.ylim(51.7, 53.5)
    else:
        plt.ylim(50.5, 54)
    plt.show()

