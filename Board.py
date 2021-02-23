# this file will simulate our minesweeper board and allow us to query certain spots for info
from LibaryFunctions import getValidNeighbors


class Board():
    def __init__(self,dim):
       # dimension needed for board
       self.dim = dim
       # boards only differ in their mine locations
            #mines are stored as tuple here (row,col)
       self.mines = set()
    # generates random board with number of mines desired
    def generateBoard(self,numMines):
        pass
    # pass board from txt file
    def getBoardFromFile(self):
        pass
    # method below for querying a location: returns -1 if loc is mine, else returns # of mines from neighbors
    def queryPosition(self,loc):
        if loc in self.mines:
            # then this is a mine
            return -1;
        else:
            count =0
            neighbors = getValidNeighbors(self.dim,loc)
            for neighbor in neighbors:
                if neighbor in self.mines:
                    count+=1
            return count
    #printing status of board
    def printBoard(self):
        pass
