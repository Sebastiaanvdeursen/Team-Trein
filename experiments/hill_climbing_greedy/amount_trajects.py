import sys
from code.classes.rail_NL import Rail_NL

def timed_hill_climbing_greedy(area, amount_trajects, max_time, amount_stations, time_to_run):
    list_amount_trajects = list(range(1, amount_trajects + 1))

    for i in range(amount_trajects):
        start = time.time()
        results = []
        best = []
        current_max = 0
        while True:
            if (time.time() - start) / 60 > time_to_run:
                break
            result = hill_climbing_greedy(area, list_amount_trajects[i], amount_stations, max_time, printed = False)
            current_traject = result[0]
            score = result[1]
            area.reset()
            if score > current_max:
                current_max = score
                best = current_traject
            results.append(score)
        count = 1
        for a in best:
            count += 1

        file_name = f'results_{list_amount_trajects[i]}.pickle'
        with open(file_name, 'wb') as f:
            pickle.dump(results, f)
    
    average_list = []
    i_list = []
    for i in range(amount_trajects):
        i_list.append(i)
        file = open(f'results_{i + 1}.pickle', 'rb')
        results = pickle.load(file)
        file.close()
        count = 0
        for j in results:
            count += 1
        print(i + 1)
        print(f"amount of results, {count}")
        print(f"max, {max(results)}")
        average = sum(results) / len(results)
        average_list.append(average)
        print(f"average, {sum(results) / len(results)}")
        print(f"std, {np.std(results)}")
    plt.plot(i_list, average_list)
    plt.show()
    
    