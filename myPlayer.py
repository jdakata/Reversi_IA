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
        #print("moves = ", moves)
        for move in moves:
            #print("move in player moves = ", move)
            self._board.push(move)
            val = self.maxValue(alpha,beta,profondeur,True)
            self._board.pop()
            #print("val: ",val)
            if val > best_val:
                #print("Refreshing best val from:",best_val, "to: ",val)
                #print("new pos = ", move)
                #time.sleep(10)
                best_val = val
                my_moves = [move]
            if val == best_val:
                my_moves.append(move)
        move = random.choice(my_moves)    
        self._board.push(move)
        print("I am playing ", move, "from my_choices good arry choice: ", my_moves)
        #time.sleep(5)
        (c, x, y) = move
        assert (c == self._mycolor)
        print("My current board :")
        print(self._board)
        #time.sleep(10)
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

    def evaluate(self, player):
        res = 0
        move_weight = 0
        move_weight_alpha = -99999
        move_weight_beta = 99999 
        #print(player)
        moves = [m for m in self._board.legal_moves()]

        if player == 1:
            #print("coucou player")
             
            for move in moves:
                move_weight = WeightMap[move[1],move[2]]
                #print("move_weight_alpha",move_weight_alpha)
                if (move_weight_alpha < move_weight):
                    move_weight_alpha = move_weight
            return move_weight_alpha

        if player == 0: 
            print("not coucou player")
            time.sleep(5)
            for move in moves:
                #print(move)
                #print("Debug not move_weight: ",move_weight_beta)
                if move_weight_beta > WeightMap[move[1],move[2]] :
                    move_weight_beta = WeightMap[move[1],move[2]]
        return move_weight_beta

    def maxValue(self,alpha,beta,depthMax, playerBlack=True):
        #traiter game over
        if depthMax == 0 :
            #print("Debug max alpha:", alpha,"Beta :", beta )
            return self.evaluate(1) if playerBlack else self.evaluate(0)
        for move in self._board.legal_moves():
            self._board.push(move)
            alpha = max(alpha,self.minValue(alpha,beta,depthMax-1,True))
            self._board.pop()
            if alpha >= beta:
                #print("Debug alpha:", alpha,"Beta :", beta )
                return beta
        #print("Debug alpha:", alpha,"Beta :", beta )
        return alpha

    def minValue(self,alpha,beta,depthMax=3, playerBlack=False):
        #traiter game over
        if depthMax == 0 :
            #print("Debug min alpha:", alpha,"Beta :", beta )
            return self.evaluate(1) if playerBlack else self.evaluate(0)
        for move in self._board.legal_moves():
            self._board.push(move)
            beta = min(beta,self.maxValue(alpha,beta,depthMax-1))
            self._board.pop()
            if alpha >= beta:
                #print("Debug min alpha cut:", alpha,"Beta :", beta )
                return alpha
        #print("Debug min alpha:", alpha,"Beta :", beta )
        return beta
    