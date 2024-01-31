# Simulated Annealing

#### Warning run all code using main.py

### sim_annealing_alg.py
Simulated annealing is an iterative algorithm which is very comparable to hill climbing,
the only difference is that we can accept worse solutions with a certain probability.
This probability is based on how much worse the solution is and on the value of a temperature function that
decreases based on how much iterations are already done.

### Usage
All algorithms can only be used from the root directory of the git.
There they are performed by using main.py and then filling in the correct commandline arguments:
Run the code by typing
```
python3 main.py large/small simulated number
```
For number you can fill in any amount of iterations.