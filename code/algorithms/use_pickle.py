import pickle
import math

if __name__ == "__main__":
    file = open('../../results.pickle', 'rb')
    results = pickle.load(file)
    file.close()
    count = 0
    amount = 0
    for i in results:
        count += 1
        if i == 9199.0:
            amount += 1
    prob = amount/count
    print(amount)
    print(count)
    print(prob)
    print(f" 90 % = {math.log(0.1, 1- prob)}")
    print(f" 99 % = {math.log(0.01, 1- prob)}")
    print(f" 99.9 % = {math.log(0.001, 1- prob)}")
    print(f" 99.99 % = {math.log(0.0001, 1- prob)}")
    print(f" 99.999 % = {math.log(0.00001, 1- prob)}")
    print(f" 99.9999 % = {math.log(0.000001, 1- prob)}")
    print(f" 99.99999 % = {math.log(0.0000001, 1- prob)}")
    print(f" 99.999999 % = {math.log(0.00000001, 1- prob)}")