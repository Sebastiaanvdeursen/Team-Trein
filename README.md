# Team-Trein

Dit is onze README!

##Getting started
###Requirements
Please run the following line of code in your terminal:
sudo apt-get install tcl-dev tk-dev python-tk python3-tk
Therafter, run 
pip install -r requirements.txt 
or
conda install --file requirements.txt
to get everything you need.

###Usage
Run the code by typing python main.py large/small algorithm size. You can also opt to not include size, then one iteration will be ran.
By typing large you run the chosen algorithm on the Netherlands and by typing small you only use Holland. For algorithms you can choose
between find_p, annealing, random, random_optim, greedy_random, greedy_random_max, greedy_optim, hill_climbing, hill_climbing/greedy,
hill_climbing/greedy_max, hill_climbing/greedy_optim, hill_climbing/greedy_optim_max or double_greedy.