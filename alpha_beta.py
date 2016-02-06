#!/usr/bin/python

import sys
import copy

myplayer=()
oppplayer=()
myplayer_score=0
oppplayer_score=0
cutoffdepth=0
board=[]
positions=[]


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

def calculateScores(score1,score2,ismyplayer):
  if ismyplayer:
    return score1+score2
  elif not(ismyplayer):
    return score1-score2

def calculategain(board_state):
  my_player_score=0
  opp_player_score=0
  my_player = myplayer
  opp_player = oppplayer
  for i in range(5):
    for j in range(5):
      if board_state[i][j]==my_player:
        my_player_score=my_player_score+board[i][j]
      if board_state[i][j]==opp_player:
        opp_player_score=opp_player_score+board[i][j]
  gain = my_player_score-opp_player_score
  return gain

def changeboard(i,j,board_state,player):
  my_player = player
  opp_player = findOppPlayer(player) 
  board_state[i][j]=my_player
  pos=getjpos(j)
  my_player_score,opp_player_score = evalscore(board_state,player) 
  my_player_score = my_player_score + board[i][j]
  if getAction(i,j,board_state,my_player)=="R":
    if i > 0:
      if board_state[i-1][j]==opp_player:
        board_state[i-1][j]=my_player
        opp_player_score = calculateScores(opp_player_score,board[i-1][j],False)
        my_player_score = calculateScores(my_player_score,board[i-1][j],True)
    if j > 0:
      if board_state[i][j-1]==opp_player:
        board_state[i][j-1]=my_player
        opp_player_score = calculateScores(opp_player_score,board[i][j-1],False)
        my_player_score = calculateScores(my_player_score,board[i][j-1],True)
    if j < 4:
      if board_state[i][j+1]==opp_player:
        board_state[i][j+1]=my_player
        opp_player_score = calculateScores(opp_player_score,board[i][j+1],False)
        my_player_score = calculateScores(my_player_score,board[i][j+1],True)
    if i < 4:
      if board_state[i+1][j]==opp_player:
        board_state[i+1][j]=my_player
        opp_player_score = calculateScores(opp_player_score,board[i+1][j],False)
        my_player_score = calculateScores(my_player_score,board[i+1][j],True)
  if player==myplayer:
    num = 1
  else:
    num = 2
  gain = calculategain(board_state)
  #for pos in board_state:
    #print ' '.join(pos)
  return board_state

def minimax(board_state,depth):
  val = float("-inf")
  print "Node,Depth,Value,Alpha,Beta"
  print "root,0,-Infinity,-Infinity,Infinity"
  avail_moves = getAllMoves(board_state)
  for coor in avail_moves:
    temp_max_board = copy.deepcopy(board_state)
    return_max_board = changeboard(coor[0],coor[1],temp_max_board,myplayer)
    pos=getjpos(coor[1])
    gain = calculategain(return_max_board)
    #print pos + str(coor[0]+1) + "," + str(depth) +","+str(gain)
    cur_score = min_play(coor,return_max_board,int(depth+1),int(cutoffdepth),float("-inf"),float("inf"))
    if cur_score > val:
      val=cur_score
    print "root,0," + str(val)

def max_play(coord,board_state,depth,cutoffdepth,alpha,beta):
  #print "depth at max play:" + str(depth)
  #print ("Depth = %d, Cutoffdepth = %d" % (depth, cutoffdepth))
  pos=getjpos(coord[1])
  if depth==cutoffdepth:
    score=calculategain(board_state)
    print pos + str(coord[0]+1) + "," + str(depth) +","+str(score)+str(alpha)+","+str(beta)
    return score
  val = float("-inf")
  avail_moves = getAllMoves(board_state)
  print pos + str(coord[0]+1) + "," + str(depth) +","+"-Infinity"+str(alpha)+","+str(beta)
  for coor in avail_moves:
    temp_max_board = copy.deepcopy(board_state)
    return_max_board = changeboard(coor[0],coor[1],temp_max_board,myplayer)
    print pos + str(coor[0]+1) + "," + str(depth) +","+str(calculategain(return_max_board)) + str(alpha) +","+ str(beta)
    cur_score = min_play(coor,return_max_board,depth+1,cutoffdepth,alpha,beta)
    if cur_score > val:
      val=cur_score
    if val >= beta:
      return val
    if alpha < val:
      alpha = val
    print pos + str(coord[0]+1) + "," + str(depth) +","+str(val)+str(alpha)+","+str(beta)
  return val

def min_play(coord,board_state,depth,cutoffdepth,alpha,beta):
  #print "depth at min play:" + str(depth)
  pos=getjpos(coord[1])
  if depth==cutoffdepth:
    score=calculategain(board_state)
    print pos + str(coord[0]+1) + "," + str(depth) +","+str(score)+str(alpha)+","+str(beta)
    return score
  val = float("inf")
  avail_moves = getAllMoves(board_state)
  print pos + str(coord[0]+1) + "," + str(depth) +","+"Infinity"+str(alpha)+","+str(beta)
  for coor in avail_moves:
    temp_min_board = copy.deepcopy(board_state)
    return_min_board = changeboard(coor[0],coor[1],temp_min_board,oppplayer)
    cur_score = max_play(coor,return_min_board,depth+1,cutoffdepth,alpha,beta)
    if cur_score < val:
      val=cur_score
    if val <= alpha:
      return val
    if beta > val:
      beta = val
    print pos + str(coord[0]+1) + "," + str(depth) +","+str(val)+str(alpha)+","+str(beta)
  return val

def evalscorefor(board_state,player):
  player_score=0
  for i in range(5):
    for j in range(5):
      if board_state[i][j]==player:
        player_score=player_score+board[i][j]
  return player_score

def evalscore(board_state,player):
  my_player_score=0
  opp_player_score=0
  opp_player = findOppPlayer(player)
  my_player = player
  for i in range(5):
    for j in range(5):
      if board_state[i][j]==my_player:
        my_player_score=my_player_score+board[i][j]
      if board_state[i][j]==opp_player:
        opp_player_score=opp_player_score+board[i][j]
  return my_player_score,opp_player_score

def getAction(i,j,board_state,player):
  raid=False
  sneak=False
  cur_player=player
  if i>0 and not(raid):
    if board_state[i-1][j]==cur_player:
      raid=True
    else:
      sneak=False 
  if j>0 and not(raid):
    if board_state[i][j-1]==cur_player:
      raid=True
    else:
      sneak=False
  if i<4 and not(raid):
    if board_state[i+1][j]==cur_player:
      raid=True
    else:
      sneak=False
  if j<4 and not(raid):
    if board_state[i][j+1]==cur_player:
      raid=True
    else:
      sneak=False
  if(raid):
    return "R"
  else:
    return "S"

def getAllMoves(board_state):
  AvailCoor = []
  for i in range(5):
    for j in range(5):
      if board_state[i][j]=="*":
 	  AvailCoor.append((i,j))
  return AvailCoor

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

def findOppPlayer(my_player):
  if my_player=="X":
    opp_player = "O"
  else:
    opp_player = "X"
  return opp_player

#Main function starts over here
inputfile=sys.argv[2]
filehandle = open(inputfile,"r")
taskno = (filehandle.readline()).strip()
myplayer = (filehandle.readline()).strip()
cutoffdepth = (filehandle.readline()).strip()

oppplayer = findOppPlayer(myplayer)

#Creating a 2 dimensional array for board values and player positions
board = []
positions = []

BoardValues(filehandle)
InitialPlayersPositions(filehandle)
init_player_score,init_opp_score = evalscore(positions,myplayer)
possiblemoves=getAllMoves(positions)
minimax(positions,0)
