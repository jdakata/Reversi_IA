# -*- coding: utf-8 -*-

import time
import Reversi
import numpy
from random import randint
from playerInterface import *


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

#def generatetree(root):
   # root.get


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
        moves = [m for m in self._board.legal_moves()]
        move = moves[randint(0, len(moves) - 1)]
        self._board.push(move)
        print("I am playing ", move)
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