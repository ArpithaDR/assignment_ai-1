#!/usr/bin/python

import sys
import copy
import os

myplayer=()
oppplayer=()
myplayer_score=0
oppplayer_score=0
cutoffdepth=0
board=[]
positions=[]
outputfile = "next_state.txt"
logfile = "traverse_log.txt"
tracefile= "trace_state.txt"
statusboard=[]
max_i=0
max_j=0
AvailCoor= []
init_player_score=0
init_opp_score=0
coor_list=[]
myplayer_algo=()
oppplayer_algo=()
myplayer_cutoffdepth=0
opplayer_cutoffdepth=0

for i in range(5):
  statusboard.append([])
  for j in range(5):
    statusboard[i].append("0")

def isEmpty(board_state):
  for i in range(5):
    for j in range(5):
      if board_state[i][j]=="*":
    	return False 
  return True

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

def greedy_changeboard():
  global positions
  global myplayer_score
  global oppplayer_score
  global statusboard
  positions[max_i][max_j]=myplayer
  pos=getjpos(max_j)
  myplayer_score = myplayer_score + board[max_i][max_j]
  if statusboard[max_i][max_j]=="R":
    if max_i-1 >= 0:
      if positions[max_i-1][max_j]==oppplayer:
        positions[max_i-1][max_j]=myplayer
        statusboard[max_i-1][max_j]=myplayer
        oppplayer_score = calculateScores(oppplayer_score,board[max_i-1][max_j],False)
        myplayer_score = calculateScores(myplayer_score,board[max_i-1][max_j],True) 
    if max_j-1 >= 0:
      if positions[max_i][max_j-1]==oppplayer:
        positions[max_i][max_j-1]=myplayer
        statusboard[max_i][max_j-1]=myplayer
        oppplayer_score = calculateScores(oppplayer_score,board[max_i][max_j-1],False)
        myplayer_score = calculateScores(myplayer_score,board[max_i][max_j-1],True) 
    if max_j+1 < 5:
      if positions[max_i][max_j+1]==oppplayer:
        positions[max_i][max_j+1]=myplayer
        statusboard[max_i][max_j+1]=myplayer
        oppplayer_score = calculateScores(oppplayer_score,board[max_i][max_j+1],False)
        myplayer_score = calculateScores(myplayer_score,board[max_i][max_j+1],True)
    if max_i+1 < 5:
      if positions[max_i+1][max_j]==oppplayer:
        positions[max_i+1][max_j]=myplayer
	statusboard[max_i+1][max_j]=myplayer
        oppplayer_score = calculateScores(oppplayer_score,board[max_i+1][max_j],False)
        myplayer_score = calculateScores(myplayer_score,board[max_i+1][max_j],True)
  statusboard[max_i][max_j]=myplayer
  return positions

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
  return board_state

def greedy_evaleach(i,j):
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

def greedy_evalMaxValue():
  max_score =0
  global max_i
  global max_j
  max_i=0
  max_j=0
  for i in range(5):
    for j in range(5):
      if positions[i][j]=="*":
        val = greedy_evaleach(i,j)
        if max_score < val:
          max_i = i
          max_j = j
          max_score=val

def greedy_evalscore():
  global myplayer_score
  global oppplayer_score
  for i in range(5):
    for j in range(5):
      if positions[i][j]==myplayer:
        myplayer_score=myplayer_score+board[i][j]
      if positions[i][j]==oppplayer:
        oppplayer_score=oppplayer_score+board[i][j]

def greedy_definemove(cur_player):
  global statusboard
  for i in range(5):
    for j in range(5):
      raid=False
      sneak=False
      if positions[i][j]=="*":
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

def minimax_ab(board_state,depth,maxdepth):
  global coor_list 
  val = float("-inf")
  log_file_handle.write("Node,Depth,Value,Alpha,Beta\n")
  log_file_handle.write("root,0,-Infinity,-Infinity,Infinity\n")
  avail_moves = getAllMoves(board_state)
  alpha = float("-inf")
  beta = float("inf")
  for coor in avail_moves:
    temp_max_board = [row[:] for row in board_state]
    return_max_board = changeboard(coor[0],coor[1],temp_max_board,myplayer)
    pos=getjpos(coor[1])
    cur_score = min_play_ab(coor,return_max_board,int(depth+1),int(maxdepth),alpha,beta)
    if cur_score > val:
      val=cur_score
      val_coor=coor
    if val>alpha:
      alpha=cur_score
    log_file_handle.write("root,0," + str(val)+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
  final_board =changeboard(val_coor[0],val_coor[1],board_state,myplayer)
  
  return final_board

def max_play_ab(coord,board_state,depth,maxdepth,alpha,beta):
  pos=getjpos(coord[1])
  avail_moves = getAllMoves(board_state)
  if isEmpty(board_state) or depth==maxdepth:
    score=calculategain(board_state)
    log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(score)+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
    return score
  val = float("-inf")
  log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+"-Infinity"+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
  for coor in avail_moves:
    temp_max_board = [row[:] for row in board_state]
    return_max_board = changeboard(coor[0],coor[1],temp_max_board,myplayer)
    cur_score = min_play_ab(coor,return_max_board,depth+1,maxdepth,alpha,beta)
    if cur_score > val:
      val=cur_score
    if val >= beta:
      log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(val)+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
      return val
    if alpha < val:
      alpha = val
    log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(val)+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
  return val

def min_play_ab(coord,board_state,depth,maxdepth,alpha,beta):
  pos=getjpos(coord[1])
  avail_moves = getAllMoves(board_state)
  if isEmpty(board_state) or depth==maxdepth:
    score=calculategain(board_state)
    log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(score)+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
    return score
  val = float("inf")
  log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+"Infinity"+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
  for coor in avail_moves:
    temp_min_board = [row[:] for row in board_state]
    return_min_board = changeboard(coor[0],coor[1],temp_min_board,oppplayer)
    cur_score = max_play_ab(coor,return_min_board,depth+1,maxdepth,alpha,beta)
    if cur_score < val:
      val=cur_score
    if val <= alpha:
      log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(val)+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
      return val
    if beta > val:
      beta = val
    log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(val)+","+str(print_ab(alpha))+","+str(print_ab(beta))+"\n")
  return val

def print_ab(val):
  if val==float("inf"):
    return "Infinity"
  if val==float("-inf"):
    return "-Infinity"
  else:
    return val


def minimax(board_state,depth,maxdepth):
  global coor_list
  val = float("-inf")
  log_file_handle.write("Node,Depth,Value\n")
  log_file_handle.write("root,0,-Infinity\n")
  avail_moves = getAllMoves(board_state)
  for coor in avail_moves:
    temp_max_board = [row[:] for row in board_state]
    return_max_board = changeboard(coor[0],coor[1],temp_max_board,myplayer)
    pos=getjpos(coor[1])
    cur_score = min_play(coor,return_max_board,int(depth+1),int(maxdepth))
    if cur_score > val:
      val=cur_score
      val_coor = coor
    log_file_handle.write("root,0," + str(val)+"\n")
  final_board =changeboard(val_coor[0],val_coor[1],board_state,myplayer)
  return final_board

def max_play(coord,board_state,depth,maxdepth):
  pos=getjpos(coord[1])
  avail_moves = getAllMoves(board_state)
  if isEmpty(board_state) or depth==maxdepth:
    score=calculategain(board_state)
    log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(score)+"\n")
    return score
  val = float("-inf")
  log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+"-Infinity\n")
  for coor in avail_moves:
    temp_max_board = [row[:] for row in board_state]
    return_max_board = changeboard(coor[0],coor[1],temp_max_board,myplayer)
    cur_score = min_play(coor,return_max_board,depth+1,maxdepth)
    if cur_score > val:
      val=cur_score
    log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(val)+"\n")
  return val

def min_play(coord,board_state,depth,maxdepth):
  pos=getjpos(coord[1])
  avail_moves = getAllMoves(board_state)
  if isEmpty(board_state) or depth==maxdepth:
    score=calculategain(board_state)
    log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(score)+"\n")
    return score
  val = float("inf")
  log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+"Infinity"+"\n")
  for coor in avail_moves:
    temp_min_board = [row[:] for row in board_state]
    return_min_board = changeboard(coor[0],coor[1],temp_min_board,oppplayer)
    cur_score = max_play(coor,return_min_board,depth+1,maxdepth)
    if cur_score < val:
      val=cur_score
    log_file_handle.write(pos + str(coord[0]+1) + "," + str(depth) +","+str(val)+"\n")
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

#Common Functions
def InitialPlayersPositions(filehandle):
  global positions
  for i in range(5):
    row1_state = filehandle.readline()
    positions.append([state for state in row1_state.strip()])

#Common FUnctions
def BoardValues(filehandle):
  global board
  for i in range(5):
    row = filehandle.readline()
    board.append([int(val) for val in row.strip().split(" ")])

#Common FUnction
def findOppPlayer(my_player):
  if my_player=="X":
    opp_player = "O"
  else:
    opp_player = "X"
  return opp_player

def call_greedy(doPrint):
  greedy_evalscore()
  greedy_definemove(myplayer)
  greedy_evalMaxValue()
  greedy_changeboard()
  if doPrint:
    target_file_handle = open(outputfile,"w")
    for pos in positions:
      target_file_handle.write(''.join(pos))
      target_file_handle.write("\n")
    target_file_handle.close()
  return positions

def call_minimax(maxdepth,doPrint):
  global init_player_score
  global init_opp_score
  init_player_score,init_opp_score = evalscore(positions,myplayer)
  final_board = minimax(positions,0,maxdepth)
  if doPrint:
    target_file_handle = open(outputfile,"w")
    for pos in final_board:
      target_file_handle.write(''.join(pos))
      target_file_handle.write("\n")
    target_file_handle.close()
  return final_board

def call_alpha_beta(maxdepth,doPrint):
  global init_player_score
  global init_opp_score
  init_player_score,init_opp_score = evalscore(positions,myplayer)
  final_board = minimax_ab(positions,0,maxdepth)
  if doPrint:
    target_file_handle = open(outputfile,"w")
    for pos in final_board:
      target_file_handle.write(''.join(pos))
      target_file_handle.write("\n")
    target_file_handle.close()
  return final_board

#Common FUnction
def initialsetup(filehandle):
  global myplayer
  global oppplayer
  global cutoffdepth
  myplayer = (filehandle.readline()).strip()
  cutoffdepth = (filehandle.readline()).strip()
  oppplayer = findOppPlayer(myplayer)
  BoardValues(filehandle)
  InitialPlayersPositions(filehandle)
  filehandle.close()

def initialgamesetup(filehandle):
  global myplayer
  global oppplayer
  global cutoffdepth
  global myplayer_algo
  global myplayer_cutoffdepth
  global oppplayer_algo
  global oppplayer_cutoffdepth
  myplayer = (filehandle.readline()).strip()
  myplayer_algo = (filehandle.readline()).strip()
  myplayer_cutoffdepth = (filehandle.readline()).strip()
  oppplayer = (filehandle.readline()).strip()
  oppplayer_algo = (filehandle.readline()).strip()
  oppplayer_cutoffdepth = (filehandle.readline()).strip()
  BoardValues(filehandle)
  InitialPlayersPositions(filehandle)
  filehandle.close()

def call_game_play():
  global positions
  global myplayer
  global oppplayer
  global myplayer_algo
  global oppplayer_algo
  trace_file_handle = open(tracefile,"w")
  while(not(isEmpty(positions))):
    if myplayer_algo == "1":
      positions = call_minimax(1,False)
    elif myplayer_algo == "2":
      postions = call_minimax(myplayer_cutoffdepth,False)
    elif myplayer_algo == "3":
      positions = call_alpha_beta(myplayer_cutoffdepth,False)
    for pos in positions:
      trace_file_handle.write(''.join(pos))
      trace_file_handle.write("\n")
    myplayer,oppplayer = oppplayer,myplayer
    if(not(isEmpty(positions))):
      if oppplayer_algo == "1":
        positions = call_minimax(1,False)
      elif oppplayer_algo == "2":
        positions = call_minimax(oppplayer_cutoffdepth,False)
      elif oppplayer_algo == "3":
        positions = call_alpha_beta(oppplayer_cutoffdepth,False)
      for pos in positions:
        trace_file_handle.write(''.join(pos))
        trace_file_handle.write("\n")
      myplayer,oppplayer = oppplayer,myplayer
  trace_file_handle.close()

#Main function starts over here
inputfile=sys.argv[2]
filehandle = open(inputfile,"r")
taskno = (filehandle.readline()).strip()

if taskno=="1":
   initialsetup(filehandle)
   all_possible_moves = getAllMoves(positions)
   if not all_possible_moves:
     sys.exit()
   call_greedy(True)
elif taskno=="2":
   initialsetup(filehandle)
   all_possible_moves = getAllMoves(positions)
   if not all_possible_moves:
     sys.exit()
   log_file_handle = open(logfile,"w")
   call_minimax(cutoffdepth,True)
   log_file_handle.close()
elif taskno=="3":
   initialsetup(filehandle)
   all_possible_moves = getAllMoves(positions)
   if not all_possible_moves:
     sys.exit()
   log_file_handle = open(logfile,"w")
   call_alpha_beta(cutoffdepth,True)
   log_file_handle.close()
elif taskno=="4":
   initialgamesetup(filehandle)
   all_possible_moves = getAllMoves(positions)
   if not all_possible_moves:
     sys.exit()
   log_file_handle = open(os.devnull,"w")
   call_game_play()
   log_file_handle.close()
