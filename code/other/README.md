# Other code
### part 1
part 1 finds the solution to the first part of the rail_nl problem using a greedy algorithm.
It can be used on small and large but works considerably faster on small.
### part 5
part 5 finds the solution for the fifth problem, specifically on the greedy algorithm since it is our best algorithm.
it creates a new railnl object with 3 moved connections and compares the score to the score found in the regular Rail_nl object.
that difference is added in the list for each of the moved connections.\
In the end it prints out the average change for each of the connections.
### remove unnecessary
This file contains the code for two functions that can improve the score.
#### removing lines:
This function loops trough all the tracks in the set and looks if the score is higher without it.
If this is true it is removed
#### remove_end:
loops trough the list of tracks and removes the ends of each track if it is better without it, it will be permanently removed and the new end is tested again.
### run
run.py contains one function that takes in a list tracks, it runs them and returns the fraction of the connections used and the time used.
it also modifies the RailNL object.
### timed
