# -*- coding: utf-8 -*-

import time
import Reversi
import numpy
from random import randint
from playerInterface import *
import sys
import random

class node:
    def __init__(self, NodeFather, NodeChildren, NodeBoard, NodeDepth):
        self._NodeFather = NodeFather
        self._NodeChildren = NodeChildren
        self._NodeBoard = NodeBoard
        self._NodeDepth = NodeDepth

    def isLeaf(self):
        return self._NodeChildren == []

    def getNodeBoard(self):
        return self._NodeBoard


WeightMap = numpy.array([[500, -25, 10, 5, 4, 4, 5, 10, -25, 500],
                         [-25, -45,  1, 1, 1, 1, 1,  1, -45, -25],
                         [ 10,   1,  3, 2, 1, 1, 2,  3,   1,  10],
                         [  5,   1,  2, 1, 1, 1, 1,  2,   1,   5],
                         [  5,   1,  2, 1, 1, 1, 1,  2,   1,   5],
                         [  5,   1,  2, 1, 1, 1, 1,  2,   1,   5],
                         [  5,   1,  2, 1, 1, 1, 1,  2,   1,   5],
                         [ 10,   1,  3, 2, 1, 1, 2,  3,   1,  10],
                         [-25, -45,  1, 1, 1, 1, 1,  1, -45, -25],
                         [500, -25, 10, 5, 4, 4, 5, 10, -25, 500]])

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "my Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            print("Referee told me to play but the game is over!")
            return (-1, -1)
        alpha = -99999999
        beta = 99999999
        profondeur = 3
        player = 2
        best_val = -9999999
        moves = [m for m in self._board.legal_moves()]
        my_moves = []
        for move in moves:
            self._board.push(move)
            val = self.maxValue(alpha,beta,profondeur,True)
            self._board.pop()
            if val > best_val:
                best_val = val
                my_moves = [move]
            if val == best_val:
                my_moves.append(move)
        move = random.choice(my_moves)    
        self._board.push(move)
        print("I am playing ", move, "from my_choices good arry choice: ", my_moves)
        (c, x, y) = move
        assert (c == self._mycolor)
        print("My current board :")
        print(self._board)
        return (x, y)

    def playOpponentMove(self, x, y):
        assert (self._board.is_valid_move(self._opponent, x, y))
        print("Opponent played ", (x, y))
        self._board.push([self._opponent, x, y])

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        if self._mycolor == winner:
            print("I won!!!")
        else:
            print("I lost :(!!")

    
    def getstable(self, color):
        board = self.convertToBinary()
        stable = [0,0,0]
        cind1 = [0,0,9,9]
        cind2 = [0,9,9,0]
        inc1 = [0,1,0,-1]
        inc2 = [1,0,-1,0]
        stop = [0,0,0,0]
        for i in range(4):
            if board[cind1[i]][cind2[i]] == color:
                stop[i] = 1
                stable[0] += 1
                for j in range(1,9):
                    if board[cind1[i]+inc1[i]*j][cind2[i]+inc2[i]*j] != color:
                        break
                    else:
                        stop[i] = j + 1
                        stable[1] += 1
        for i in range(4):
            if board[cind1[i]][cind2[i]] == color:
                for j in range(1,9-stop[i-1]):
                    if board[cind1[i]-inc1[i-1]*j][cind2[i]-inc2[i-1]*j] != color:
                        break
                    else:
                        stable[1] += 1
        print(stable)
        colfull = numpy.zeros((10, 10), dtype=numpy.int)
        colfull[:,numpy.sum(abs(board), axis = 0) == 10] = True
        rowfull = numpy.zeros((10, 10), dtype=numpy.int)
        rowfull[numpy.sum(abs(board), axis = 1) == 10,:] = True
        diag1full = numpy.zeros((10, 10), dtype=numpy.int)
        for i in range(19):
            diagsum = 0
            if i <= 9:
                sind1 = i
                sind2 = 0
                jrange = i+1
            else:
                sind1 = 9
                sind2 = i-9
                jrange = 19-i
            for j in range(jrange):
                diagsum += abs(board[sind1-j][sind2+j])
            if diagsum == jrange:
                for k in range(jrange):
                    diag1full[sind1-j][sind2+j] = True
        diag2full = numpy.zeros((10, 10), dtype=numpy.int)
        for i in range(19):
            diagsum = 0
            if i <= 9:
                sind1 = i
                sind2 = 9
                jrange = i+1
            else:
                sind1 = 9
                sind2 = 18-i
                jrange = 19-i
            for j in range(jrange):
                diagsum += abs(board[sind1-j][sind2-j])
            if diagsum == jrange:
                for k in range(jrange):
                    diag2full[sind1-j][sind2-j] = True
        stable[2] = sum(sum(numpy.logical_and(numpy.logical_and(numpy.logical_and(colfull, rowfull), diag1full), diag2full)))
        return stable

    def evaluate(self, player):
        res = 0
        move_weight = 0
        move_weight_alpha = -99999
        move_weight_beta = 99999 
        moves = [m for m in self._board.legal_moves()]
        stable = self.getstable(1)
        if player == 1:
             
            for move in moves:
                print("coucou player")
                move_weight = WeightMap[move[1],move[2]]
                if (move_weight_alpha < move_weight):
                    move_weight_alpha = move_weight
            return move_weight_alpha +10*sum(stable)

        if player == 0: 
            print("not coucou player")
            for move in moves:
                if move_weight_beta > WeightMap[move[1],move[2]] :
                    move_weight_beta = WeightMap[move[1],move[2]]
        #print(stable)            
        return move_weight_beta 

    def maxValue(self,alpha,beta,depthMax, playerBlack=True):
        if depthMax == 0 :
            #time.sleep(5)
            return self.evaluate(1) if playerBlack else self.evaluate(0)
        for move in self._board.legal_moves():
            self._board.push(move)
            alpha = max(alpha,self.minValue(alpha,beta,depthMax-1))
            self._board.pop()
            if alpha >= beta:
                return beta
        return alpha

    def minValue(self,alpha,beta,depthMax=3, playerBlack=False):
        #traiter game over
        if depthMax == 0 :
            return self.evaluate(0) if playerBlack else self.evaluate(1)
        for move in self._board.legal_moves():
            self._board.push(move)
            beta = min(beta,self.maxValue(alpha,beta,depthMax-1))
            self._board.pop()
            if alpha >= beta:
                return alpha
        return beta
    
    def convertToBinary(self):
        board = numpy.zeros((10,10))
        for i in range (10):
            for j in range(10):
                if (self._board._board[i][j] == 2):
                    board[i][j] = -1
                else:
                    board[i][j] = self._board._board[i][j]
        return board