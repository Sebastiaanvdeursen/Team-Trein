import sys
from code.classes.rail_NL import Rail_NL

def timed_hill_climbing(area, amount_trajects, max_time, amount_stations, time_to_run):
        list_amount_trajects = list(range(1, amount_trajects + 1))
        for i in range(amount_trajects):
            start = time.time()
            results = []
            best = []
            current_max = 0
            while True:
                if (time.time() - start) / 60 > time_to_run:
                    break
                result = hill_climbing(area, list_amount_trajects[i], amount_stations, max_time)
                current_traject = result[0]
                score = result[1]
                area.reset()
                if score > current_max:
                    current_max = score
                    best = current_traject
                results.append(score)
            count = 1
            for a in best:
                print(f"train_{count},{a.traject_connections}")
                count += 1
            print(f"score,{max(results)}")
            print(results)

            file_name = f'results_{list_amount_trajects[i]}.pickle'
            with open(file_name, 'wb') as f:
                pickle.dump(results, f)
        for i in range(amount_trajects):
            file = open(f'results_{i + 1}.pickle', 'rb')
            results = pickle.load(file)
            file.close()
            count = 0
            for j in results:
                count += 1
            print(i + 1)
            print(f"amount of results, {count}")
            print(f"max, {max(results)}")
            print(f"average, {sum(results) / len(results)}")
            print(f"std, {np.std(results)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "large":
            map = "NL"
            amount_trajects = 20
            amount_stations = 61
            max_time = 180
        else:
            map = "Holland"
            amount_trajects = 7
            amount_stations = 22
            max_time = 120
        if len(sys.argv) > 2:
            area = Rail_NL(map, amount_trajects, amount_stations, max_time)
            time = float(sys.argv[2])
            timed_hill_climbing(area, amount_trajects, max_time, amount_stations, time)
        else:
            print("not correct input")
    else:
        print("not correct input")