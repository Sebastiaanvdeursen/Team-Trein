import csv
import matplotlib.pyplot as plt


if __name__ == "__main__":
    places = {}
    with open("coordinatesLong.csv") as data:
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

    with open("ConnectiesNL.csv") as line_info:
        csv_file = csv.reader(line_info, delimiter=',')
        line_count = 0
        for row in csv_file:
            if line_count != 0:
                print(row[0], row[1])
                print(places[row[0]])
                print(places[row[1]])
                plt.plot([places[row[0]][1], places[row[1]][1]], [places[row[0]][0], places[row[1]][0]], 'k-', lw=2)
            line_count += 1

    ##plt.xlim(51.7, 53.5)
    plt.ylim(50.5, 54)
    plt.show()

