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
AvailCoor= []
statusboard = []
outputfile = "next_state.txt"
logfile = "traverse_log.txt"

for i in range(5):
  statusboard.append([])
  for j in range(5):
    statusboard[i].append("0")

def calculateScores(score1,score2,ismyplayer):
  if ismyplayer:
    return score1+score2
  elif not(ismyplayer):
    return score1-score2

def getjpos(j):
  if j==0:
    return 'A'
  elif j==1:
    return 'B'
  elif j==2:
    return 'C'
  elif j==3:
    return 'D'
  elif j==4:
    return 'E'

def isEmpty():
  if not AvailCoor:
    return True
  else:
    return False

def changeboard():
  global positions
  global myplayer_score
  global oppplayer_score
  global AvailCoor
  global statusboard

  AvailCoor.remove((max_i,max_j))
  positions[max_i][max_j]=myplayer
  pos=getjpos(max_j)
  myplayer_score = myplayer_score + board[max_i][max_j]
  print statusboard
  print positions
  if statusboard[max_i][max_j]=="R":
    if max_i-1 >= 0:
      if positions[max_i-1][max_j]==oppplayer:
	positions[max_i-1][max_j]=myplayer
        oppplayer_score = calculateScores(oppplayer_score,board[max_i-1][max_j],False)
        myplayer_score = calculateScores(myplayer_score,board[max_i-1][max_j],True) 
    if max_j-1 >= 0:
      if positions[max_i][max_j-1]==oppplayer:
	positions[max_i][max_j-1]=myplayer
        oppplayer_score = calculateScores(oppplayer_score,board[max_i][max_j-1],False)
        myplayer_score = calculateScores(myplayer_score,board[max_i][max_j-1],True) 
    if max_j+1 < 5:
      if positions[max_i][max_j+1]==oppplayer:
	positions[max_i][max_j+1]=myplayer
        oppplayer_score = calculateScores(oppplayer_score,board[max_i][max_j+1],False)
        myplayer_score = calculateScores(myplayer_score,board[max_i][max_j+1],True)
    if max_i+1 < 5:
      if positions[max_i+1][max_j]==oppplayer:
	positions[max_i+1][max_j]=myplayer
        oppplayer_score = calculateScores(oppplayer_score,board[max_i+1][max_j],False)
        myplayer_score = calculateScores(myplayer_score,board[max_i+1][max_j],True)
  statusboard[max_i][max_j]=myplayer
  print pos + str(max_i+1)
	
def evaleach(i,j):
  val = statusboard[i][j]
  final_val=0
  global max_score 
  temp_player_score = myplayer_score + board[i][j]
  temp_opp_score = oppplayer_score
  if val=="R":
    if i-1 >= 0:
      if positions[i-1][j]==oppplayer:
	temp_opp_score = calculateScores(temp_opp_score,board[i-1][j],False)
        temp_player_score = calculateScores(temp_player_score,board[i-1][j],True)
    if j-1 >= 0:
      if positions[i][j-1]==oppplayer:
	temp_opp_score = calculateScores(temp_opp_score,board[i][j-1],False)
        temp_player_score = calculateScores(temp_player_score,board[i][j-1],True)
    if j+1 < 5:
      if positions[i][j+1]==oppplayer:
        temp_opp_score = calculateScores(temp_opp_score,board[i][j+1],False)
        temp_player_score = calculateScores(temp_player_score,board[i][j+1],True)
    if i+1 < 5:
      if positions[i+1][j]==oppplayer:
        temp_opp_score = calculateScores(temp_opp_score,board[i+1][j],False)
        temp_player_score = calculateScores(temp_player_score,board[i+1][j],True)
    final_val = calculateScores(temp_player_score,temp_opp_score,False) 
  if val=="S":
    final_val = calculateScores(temp_player_score,temp_opp_score,False)
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
 
def definemove(cur_player):
  global statusboard
  global AvailCoor
  for i in range(5):
    for j in range(5):
      raid=False
      sneak=False
      if positions[i][j]=="*":
	AvailCoor.append((i,j))
	if i-1 >= 0 and not(raid):
	  if positions[i-1][j]==cur_player:
	    raid=True
	  else:
	    sneak=True
	if j-1 >= 0 and not(raid):
	  if positions[i][j-1]==cur_player:
            raid=True
          else:
            sneak=True
	if j+1 < 5 and not(raid):
	  if positions[i][j+1]==cur_player:
            raid=True
          else:
            sneak=True
	if i+1 < 5 and not(raid):
	  if positions[i+1][j]==cur_player:
            raid=True
          else:
            sneak=True
        if(raid):
          statusboard[i][j]="R"
        else:
          statusboard[i][j]="S"
      else:
	statusboard[i][j]=positions[i][j]
  return;

def InitialPlayersPositions(filehandle):
  global positions
  for i in range(5):
    row1_state = filehandle.readline()
    positions.append([state for state in row1_state.strip()])

def BoardValues(filehandle):
  global board
  for i in range(5):
    row = filehandle.readline()
    board.append([int(val) for val in row.strip().split(" ")])

def findPlayers(myplayer):
  global oppplayer
  if myplayer=="X":
    oppplayer = "O"
  else:
    oppplayer = "X"

#Main function starts over here
inputfile=sys.argv[2]
filehandle = open(inputfile,"r")
taskno = (filehandle.readline()).strip()
myplayer = (filehandle.readline()).strip()
cutoffdepth = (filehandle.readline()).strip()

findPlayers(myplayer)

#Creating a 2 dimensional array for board values and player positions
board = []
positions = []

BoardValues(filehandle)
InitialPlayersPositions(filehandle)
evalscore()
definemove(myplayer)
evalMaxValue()
changeboard()

for pos in positions:
    print ' '.join(pos)

target_file_handle = open(outputfile,"w")
for pos in positions:
    target_file_handle.write(''.join(pos))
    target_file_handle.write("\n")

log_file_handle = open(logfile,"w")

log_file_handle.close()
target_file_handle.close()
filehandle.close()

