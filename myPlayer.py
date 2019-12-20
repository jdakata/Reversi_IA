# -*- coding: utf-8 -*-

import time
import Reversi
import numpy
from random import randint
from playerInterface import *

WeightMap = numpy.array([[500, -250, 150, 100, 80, 80, 100, 150, -250, 500],
                         [-250, -350,  0, 1, 1, 1, 1,  0, -450, -350],
                         [ 150,   0,  3, 2, 1, 1, 2,  3,   0,  150],
                         [ 100,   1,  2, 1, 1, 1, 1,  2,   1,   100],
                         [  80,   1,  2, 1, 16, 16, 1,  2,   1,   80],
                         [  80,   1,  2, 1, 16, 16, 1,  2,   1,   80],
                         [ 100,   1,  2, 1, 1, 1, 1,  2,   1,   100],
                         [ 150,   0,  3, 2, 1, 1, 2,  3,   0,  150],
                         [-250, -350,  0, 1, 1, 1, 1,  0, -350, -250],
                         [500, -250, 150, 100, 80, 80, 100, 150, -250, 500]])

class myPlayer(PlayerInterface):

    def __init__(self):
        self._board = Reversi.Board(10)
        self._mycolor = None

    def getPlayerName(self):
        return "my Player"

    def getPlayerMove(self):
        if self._board.is_game_over():
            #print("Referee told me to play but the game is over!")
            return (-1, -1)
        [value,move] = self.maxValue(-9999,9999,0,3,[])
        self._board.push(move)
        #print("I am playing ", move)
        (c, x, y) = move
        assert (c == self._mycolor)
        #print("My current board :")
        #print(self._board)
        return (x, y)

    def playOpponentMove(self, x, y):
        assert (self._board.is_valid_move(self._opponent, x, y))
        #print("Opponent played ", (x, y))
        self._board.push([self._opponent, x, y])
        if x == 0 and y == 0:
            WeightMap[1][0]-=250
            WeightMap[0][1]-=250
            WeightMap[1][1]-=250
        if x == 9 and y == 9:
            WeightMap[8][9]-=250
            WeightMap[9][8]-=250
            WeightMap[8][8]-=250
        if x == 0 and y == 9:
            WeightMap[0][8]-=250
            WeightMap[1][9]-=250
            WeightMap[1][8]-=250
        if x == 9 and y == 0:
            WeightMap[9][1]-=250
            WeightMap[8][0]-=250
            WeightMap[8][1]-=250

    def newGame(self, color):
        self._mycolor = color
        self._opponent = 1 if color == 2 else 2

    def endGame(self, winner):
        pass
        # if self._mycolor == winner:
        #     print("I won!!!")
        # else:
        #     print("I lost :(!!")

    def maxValue(self,alpha,beta,depth,depthMax,bestMove):
        if depth == depthMax:
            return [self.evaluate(),bestMove]

        moves = self._board.legal_moves()

        if depth == 0:
            for move in self._board.legal_moves():
                [player,x,y] = move
                if (x == 0 and y == 0) or (x == 9 and y == 9) or (x == 0 and y == 9) or (x == 9 and y == 0):
                    return [0,move]
                

        for move in moves:
            self._board.push(move)
            if depth == 0:
                bestMove = move
            [value,bestMove_] = self.minValue(alpha,beta,depth+1,depthMax,bestMove)
            if alpha<value:
                alpha = value
                bestMove = bestMove_
            self._board.pop()
            if alpha >= beta:
                return [beta,bestMove]
        return [alpha,bestMove]

    def minValue(self,alpha,beta,depth,depthMax,bestMove):
        if depth == depthMax:
            return [self.evaluate(),bestMove]
            
        for move in self._board.legal_moves():
            self._board.push(move)
            if depth == 0:
                bestMove = move
            [value,bestMove_] = self.maxValue(alpha,beta,depth+1,depthMax,bestMove)
            if beta>value:
                beta = value
                bestMove = bestMove_
            self._board.pop()
            if alpha >= beta:
                return [alpha,bestMove]
        return [beta,bestMove]
    
    def getMovesBlackAndWhite(self):
        backup = self._board._nextPlayer
        self._board._nextPlayer = self._opponent
        opponentMoves = self._board.legal_moves()
        self._board._nextPlayer = self._mycolor
        myMoves = self._board.legal_moves()
        self._board._nextPlayer = backup
        return [myMoves,opponentMoves]

    # compare total weight of opponent pieces and mine 
    def evaluateCurrentPiecesWeight(self):
        myPiecesWeight = 0
        opponentPiecesWeight = 0
        for x in range(0,self._board._boardsize):
            for y in range(0,self._board._boardsize):
                if self._board._board[x][y] == self._mycolor :
                    myPiecesWeight += WeightMap[x][y]
                else:
                    opponentPiecesWeight += WeightMap[x][y]
        return [myPiecesWeight,opponentPiecesWeight]

    # the total weight of a set of moves
    def getMovesWeight(self,moves):
        sumW = 0
        for i in range (len(moves)):
            [player,x,y] = moves[i]
            sumW += WeightMap[x][y]
        return sumW

    def evaluateMobility(self):
        [myMoves,opponentMoves] = self.getMovesBlackAndWhite()
        opponentMovesWeight = self.getMovesWeight(opponentMoves)
        myMovesWeight = self.getMovesWeight(myMoves)
        return [myMovesWeight,opponentMovesWeight]

    def evaluate(self):
        (black,white) = self._board.get_nb_pieces()
        # return self.evaluateMobility()
        # if black+white<30:
        #     print("Lsimooooooooooooooooon")
        #     if self._opponent == self._board._BLACK:
        #         return white-black
        #     else:
        #         return black-white
        #     return 750*self.evaluateMobility() + 250*self.evaluateCurrentPiecesWeight()
        # print("Zemmariiiiiiiiiiiiiiiiiiiiii")
        # return self.evaluateMobility()
        # return 450*self.evaluateMobility() + 650*self.evaluateCurrentPiecesWeight()

        [myMoves,opponentMoves] = self.getMovesBlackAndWhite()
        opponentMovesWeight = self.getMovesWeight(opponentMoves)
        myMovesWeight = self.getMovesWeight(myMoves)

        # return myMovesWeight + 15*(len(myMoves)-len(opponentMoves))
        if black+white<30:
            return len(myMoves)-len(opponentMoves)
        if black+white>=30:
            return myMovesWeight-opponentMovesWeight
