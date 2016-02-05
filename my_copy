#!/usr/bin/python

import sys

myplayer=()
oppplayer=()
myplayer_score=0
oppplayer_score=0
cutoffdepth=0
board=[]
positions=[]
statusboard=[]
max_i=0
max_j=0

statusboard = []
for i in range(5):
  statusboard.append([])
  for j in range(5):
    statusboard[i].append("0")

def changeboard():
  max_i_v = max_i
  max_j_v = max_j
  global positions
  global myplayer_score
  global oppplayer_score
  if statusboard[max_i_v][max_j_v]=="S":
    positions[max_i_v][max_j_v]=myplayer
    myplayer_score = myplayer_score + board[max_i_v][max_j_v]
  if statusboard[max_i_v][max_j_v]=="R":
    positions[max_i_v][max_j_v]=myplayer
    if i-1 > 0:
      if positions[i-1][j]==oppplayer:
	positions[i-1][j]=myplayer
        oppplayer_score = oppplayer_score - board[i-1][j]
        myplayer_score = myplayer_score + board[i-1][j] + board[max_i_v][max_j_v]
    if j-1 > 0:
      if positions[i][j-1]==oppplayer:
	positions[i][j-1]=myplayer
        oppplayer_score = oppplayer_score - board[i][j-1]
        myplayer_score = myplayer_score + board[i][j-1] + board[max_i_v][max_j_v]
    if j+1 < 5:
      if positions[i][j+1]==oppplayer:
	positions[i][j+1]=myplayer
        oppplayer_score = oppplayer_score - board[i][j+1]
        myplayer_score = myplayer_score + board[i][j+1] + board[max_i_v][max_j_v]
    if i+1 <5:
      if positions[i+1][j]==oppplayer:
	positions[i+1][j]=myplayer
        oppplayer_score = oppplayer_score - board[i+1][j]
        myplayer_score = myplayer_score + board[i+1][j] + board[max_i_v][max_j_v]
	
def evaleach(i,j):
  val = statusboard[i][j]
  final_val=0
  global max_score 
  temp_player_score = myplayer_score + board[i][j]
  temp_opp_score = oppplayer_score
  if val=="R":
    if i-1 > 0:
      if positions[i-1][j]==oppplayer:
	temp_opp_score = temp_opp_score - board[i-1][j]
        temp_player_score = temp_player_score + board[i-1][j]
    if j-1 > 0:
      if positions[i][j-1]==oppplayer:
	temp_opp_score = temp_opp_score - board[i][j-1]
        temp_player_score = temp_player_score + board[i][j-1]
    if j+1 < 5:
      if positions[i][j+1]==oppplayer:
        temp_opp_score = temp_opp_score - board[i][j+1]
        temp_player_score = temp_player_score + board[i][j+1]
    if i+1 < 5:
      if positions[i+1][j]==oppplayer:
        temp_opp_score = temp_opp_score - board[i+1][j]
        temp_player_score = temp_player_score + board[i+1][j]
    final_val = temp_player_score - temp_opp_score 
  if val=="S":
    final_val = temp_player_score - temp_opp_score
  return final_val

def evalMaxValue():
  max_score =0
  for i in range(5):
    for j in range(5):
      val = evaleach(i,j)
      if max_score < val:
	global max_i
	global max_j
	max_i = i
	max_j = j
	max_score=val
	
def evalscore():
  global myplayer_score
  global oppplayer_score
  for i in range(5):
    for j in range(5):
      if positions[i][j]==myplayer:
	myplayer_score=myplayer_score+board[i][j]
      if positions[i][j]==oppplayer:
	oppplayer_score=oppplayer_score+board[i][j]
 
def move():
  global statusboard
  for i in range(5):
    for j in range(5):
      raid=False
      sneak=False
      if positions[i][j]=="*":
	if i-1 > 0 and not(raid):
	  if positions[i-1][j]=="*":
	    sneak=True
	  else:
	    raid=True
	if j-1 > 0 and not(raid):
	  if positions[i][j-1]=="*":
            sneak=True
          else:
            raid=True
	if j+1 < 5 and not(raid):
	  if positions[i][j+1]=="*":
            sneak=True
          else:
            raid=True
	if i+1 < 5 and not(raid):
	  if positions[i+1][j]=="*":
            sneak=True
          else:
            raid=True
        if(raid):
          statusboard[i][j]="R"
        else:
          statusboard[i][j]="S"
      else:
	statusboard[i][j]=positions[i][j]
  return;

#Main function starts over here
inputfile=sys.argv[2]
filehandle = open(inputfile,"r")
taskno = (filehandle.readline()).strip()
myplayer = (filehandle.readline()).strip()

if myplayer=="X":
  oppplayer = "O"
else:
  oppplayer = "X"

cutoffdepth = (filehandle.readline()).strip()

#Creating a 2 dimensional array for board values
board = []

for i in range(5):
 row = filehandle.readline()
 board.append([int(val) for val in row.strip().split(" ")])

#Creating a 2 dimensional array for player positions
positions = []

for i in range(5):
 row1_state = filehandle.readline()
 positions.append([state for state in row1_state.strip()])

for val in board:
    print ' '.join('%02s' % val1 for val1 in val)

for pos in positions:
    print ' '.join(pos)

evalscore()
move()
evalMaxValue()
changeboard()

target_file = open("next_state.txt","w")
for pos in positions:
    target_file.write(''.join(pos))
    target_file.write("\n")

target_file.close()
filehandle.close()

