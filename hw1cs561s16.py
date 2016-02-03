#!/usr/bin/python

import sys

inputfile=sys.argv[2]

print inputfile 

filehandle = open(inputfile,"r")
taskno = filehandle.readline()
myplayer = filehandle.readline()
cutoffdepth = filehandle.readline()

#Creating a 2 dimensional array for board values

board = []

for i in range(5):
 row = filehandle.readline()
 board.append([val for val in row.strip().split(" ")])

#Creating a 2 dimensional array for player positions
positions = []

for i in range(5):
 row1_state = filehandle.readline()
 positions.append([state for state in row1_state.strip()])

for val in board:
    print ' '.join('%02s' % val1 for val1 in val)

for pos in positions:
    print ' '.join(pos)

print taskno
print myplayer
print cutoffdepth

filehandle.close()
