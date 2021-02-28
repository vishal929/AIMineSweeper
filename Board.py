# this file will simulate our minesweeper board and allow us to query certain spots for info
from random import randint

from LibaryFunctions import getValidNeighbors

# BOARD KEEPS TRACK OF QUERIES THAT RESULTED IN AGENT BLOWING UP
class Board():
    def __init__(self,dim):
       # dimension needed for board
       self.dim = dim
       # boards only differ in their mine locations
            #mines are stored as tuple here (row,col)
       self.mines = set()
       # the board keeps track of the # of times that the agent guessed wrong (hit a mine)
       self.numTriggers=0
    # generates random board with number of mines desired
    def generateBoard(self,numMines):
        genNum=0
        while genNum!=numMines:
            row = randint(0,self.dim-1)
            col = randint(0,self.dim-1)
            if (row,col) in self.mines:
                # this is repeat we continue
                continue
            self.mines.add((row,col))
            genNum+=1
    # pass board from txt file
        #txt file has format 0 and 1 where 1 is a mine
        # calling this method with a file may overwrite the given DIMENSION!
    def getBoardFromFile(self):
        pass
    # method below for querying a location: returns -1 if loc is mine, else returns # of mines from neighbors
    def queryPosition(self,loc):
        if loc in self.mines:
            # then this is a mine
            self.numTriggers+=1
            return -1;
        else:
            count =0
            neighbors = getValidNeighbors(self.dim,loc)
            for neighbor in neighbors:
                if neighbor in self.mines:
                    count+=1
            return count
    #printing status of board
        # this is from the boards perspective!
        # this means that this will include TOTAL INFO!
        # if you want printout from agent's perspective, please call print from there instead
        # this method will print every mine and every free space (0s and 1s)
    def printBoard(self):
        for i in range(self.dim):
            for j in range(self.dim):
                if (i,j) in self.mines:
                    print(" 1 ",end="")
                else:
                    print(" 0 ",end="")
            print()
