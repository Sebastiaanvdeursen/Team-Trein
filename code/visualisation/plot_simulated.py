from code.algorithms.simulated_annealing.sim_annealing_alg import simulated_annealing
import matplotlib.pyplot as plt

def Plot_simulated(area, amount_trajects, amount_stations, max_time, initial_temperature, exponent):
    result = simulated_annealing(area, amount_trajects, amount_stations, max_time, initial_temperature, exponent)
    trajects = result[2]
    count = 1
    for a in trajects:
        stations_str = ', '.join(a)
        print(f"train_{count},\"[{stations_str}]\"")
        count += 1
    print(f"score, {result[3]}")
    scoresplot = result[4]
    temperatureplot = result[5]
    iterationstemperatureplot = range(len(temperatureplot))
    iterationsplot = range(len(scoresplot))
    plt.plot(iterationstemperatureplot, temperatureplot)
    plt.plot(iterationsplot, scoresplot)
    plt.xlabel('Iterations')
    plt.ylabel('Score')
    plt.title('Simulated Annealing for the Netherlands')
    plt.show()