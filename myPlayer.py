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
            val = self.maxValue(alpha,beta,profondeur,player)
            self._board.pop()
            if val > best_val:
                best_val = val
                my_moves = [move]
            if val == best_val:
                my_moves.append(move)
        best_move = my_moves[0]
        for move in my_moves:
            #print(WeightMap[move[1],move[2]])
            if (WeightMap[move[1],move[2]]) > WeightMap[best_move[1],best_move[2]]:
                best_move = move

        move = best_move  
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

    # count number of pieces of opponent pieces and mine 
    def evaluateCurrentPieces(self):
        myPieces = 0
        opponentPieces = 0
        for x in range(0,self._board._boardsize):
            for y in range(0,self._board._boardsize):
                if self._board._board[x][y] == self._mycolor :
                    myPieces += 1
                else:
                    opponentPieces += 1
        return [myPieces,opponentPieces]

    def evaluate(self, player):
        res = 0
        move_weight = 0
        move_weight_alpha = -99999
        move_weight_beta = 99999 
        moves = [m for m in self._board.legal_moves()]
        [myPieces,opponentPieces] = self.evaluateCurrentPieces()

        if player == 1:
             
            for move in moves:
                move_weight = WeightMap[move[1],move[2]]
                if (move_weight_alpha < move_weight):
                    move_weight_alpha = move_weight
            return move_weight_alpha 

        if player == 0: 
            
            for move in moves:
                if move_weight_beta > WeightMap[move[1],move[2]] :
                    move_weight_beta = WeightMap[move[1],move[2]]
        return move_weight_beta

    def maxValue(self,alpha,beta,depthMax, playerWhite=True):
        if depthMax == 0 :
            return self.evaluate(1) if playerWhite else self.evaluate(0)
        for move in self._board.legal_moves():
            self._board.push(move)
            alpha = max(alpha,self.minValue(alpha,beta,depthMax-1,playerWhite))
            self._board.pop()
            if alpha >= beta:
                return beta
        return alpha

    def minValue(self,alpha,beta,depthMax=3, playerWhite=False):
        #traiter game over
        if depthMax == 0 :
            return self.evaluate(1) if playerWhite else self.evaluate(0)
        for move in self._board.legal_moves():
            self._board.push(move)
            beta = min(beta,self.maxValue(alpha,beta,depthMax-1,playerWhite))
            self._board.pop()
            if alpha >= beta:
                return alpha
        return beta
