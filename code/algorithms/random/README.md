# Random Directory README

## Team-Trein Random and Random Optimized Algorithm

This directory contains the implementation of a Random algorithm and the Random Optimized algorithm. The Random algorithm runs a random amount of random tracks. The Random Optimized algorithm does the same, except it uses a heuristic to try and improve results.

## Overview

### Random
The Random algorithm starts every track at a randomly chosen station. Then, it finds all connections from that station and chooses a random one from that list. Every time a this happens, there is a 10 percent chance that the track stops there. Also if the time of the next chosen connection, makes the time of the traject go over the time limit, the traject stops.

### Random Optimized
The Random Optimized algorithm does the same, only it uses the following heuristic: A track only goes over connections that are "not done" yet. So when a track is at a station, it finds all the tracks that are "not done" and chooses one randomly. If there are no connections from a station that are "not done", the track stops there. Also if the time of the next chosen connection, makes the time of the traject go over the time limit, the traject stops.

## Usage

python main.py small/large random/random_optim number_of_iterations 

## Warning

Run these algorithms only from main.py
