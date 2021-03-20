# basic implementation of knowledge base required
from collections import deque
from random import randint
import LibraryFunctions
from LibraryFunctions import getValidNeighbors


class BasicKnowledgeBase():
    def __init__(self,dim):
        self.knownMines=set()
        # tuple of (# of mines given by clue, # safeSquares, # mines identified for sure around it, #unknown around it)
        self.safeSquares={}
        #location is a cell (x,y)
        #get data helper will query our database for a location and return all known info
        # helper to check if loc is in dimensions
        self.dim=dim

    def getDataHelper(self,loc,numMinesClue):
        neighbors = getValidNeighbors(self.dim, loc)
        numMines=0
        numSafe=0
        for neighbor in neighbors:
            if neighbor in self.knownMines:
                numMines+=1
            elif neighbor in self.safeSquares:
                numSafe+=1
        return (numMinesClue,numSafe,numMines)

    # all Mines rule from basic agent specification
        #if the clue - num
    def allMinesNearby(self,loc):
        added = False
        newMines=set()
        neighbors = LibraryFunctions.getValidNeighbors(self.dim,loc)
        # if the clue is equal to the number of neighbors minus found safe neighbors
            # then every hidden neighbor is a mine
        if self.safeSquares[loc][0] == len(neighbors)-self.safeSquares[loc][1]:
            # every hidden neighbor is a mine
            for neighbor in neighbors:
                if neighbor not in self.knownMines and neighbor not in self.safeSquares:
                    # then this is hidden
                    self.knownMines.add(neighbor)
                    newMines.add(neighbor)
                    added=True
        for mine in newMines:
            self.updateNeighbors(mine)
        return added,newMines

    # implementing safe rule from specification
    def allSafeNearby(self,loc):
        added =False
        newSafe=set()
        neighbors = LibraryFunctions.getValidNeighbors(self.dim,loc)
        # if number of total safe squares equals the number of neighbors - the number of mines found
            # then every hidden neighbor is safe
        if len(neighbors)-self.safeSquares[loc][0]== len(neighbors)-self.safeSquares[loc][2]:
            for neighbor in neighbors:
                if neighbor not in self.knownMines and neighbor not in self.safeSquares:
                    # this is hidden and we should mark it as safe
                    added=True
                    newSafe.add(neighbor)

        return added,newSafe
    def queryCellFromBoard(self,loc,board):
        numMinesClue = board.queryPosition(loc)
        if numMinesClue==-1:
            # then agent queried a mine
            self.knownMines.add(loc)
            self.updateNeighbors(loc)
            return True,loc
        else:
            # this is safe, we can update our info
            data = self.getDataHelper(loc,numMinesClue)
            self.safeSquares[loc]=data
            self.updateNeighbors(loc)
            return False,loc

    #returning random cell to query
    def randomCellToQuery(self):
        hidden=deque()
        for i in range(self.dim):
            for j in range(self.dim):
                loc = (i, j)
                if loc not in self.knownMines and loc not in self.safeSquares:
                    #this is hidden, we should consider this when picking randomly
                    hidden.append(loc)
        posToPick = randint(0,len(hidden)-1)
        return hidden[posToPick]

    # updating neighbors after successful add of mine or safe spot
    def updateNeighbors(self,loc):
        neighbors = LibraryFunctions.getValidNeighbors(self.dim,loc)
        isMine = False
        if loc in self.knownMines:
            isMine=True

        for neighbor in neighbors:
            # only interesting in updating safe square data
            if neighbor in self.safeSquares:
                if isMine:
                    self.safeSquares[neighbor]=self.safeSquares[neighbor][0],\
                                               self.safeSquares[neighbor][1],\
                                               self.safeSquares[neighbor][2]+1
                else:
                    self.safeSquares[neighbor] = self.safeSquares[neighbor][0], \
                                                 self.safeSquares[neighbor][1]+1 , \
                                                 self.safeSquares[neighbor][2]



    def printKnowledge(self):
        # method to print everything that knowledge base knows at this moment in time
        # unknown is question marks, free is 0, and mines are 1
        for i in range(self.dim):
            for j in range(self.dim):
                if (i,j) in self.knownMines:
                    print(" 1 ",end="")
                elif (i,j) in self.safeSquares:
                    print(" 0 ",end="")
                else:
                    # then we do not know
                    print(" ? ",end="")
            #newline
            print()

    # updates a given matrix representation with changes that the algorithm made
        #changes is a tuple of (True/False, listOfLocations)
        #True means the changes are mines for sure
        #False means the changes are free spaces for sure
        # list of location is a list of (row,col) pairs to set
    def setMatrix(self,matrix,changes):
        if changes[0]:
            # set these as mines
            for loc in changes[1]:
                matrix[loc[0]][loc[1]]=1
        else:
            # set these as free spaces
            for loc in changes[1]:
                matrix[loc[0]][loc[1]]=0

    #clue is of the form (loc,clue) where clue is -1 if its a mine
    def feedClue(self,clue):
        if clue[1]==-1:
            self.knownMines.add(clue[0])
            # then a mine
        else:
            # then safe
            # gathering info
            neighbors = LibraryFunctions.getValidNeighbors(self.dim,clue[0])
            numSafe = 0
            numMines = 0
            for neighbor in neighbors:
                if neighbor in self.knownMines:
                    numMines +=1
                elif neighbor in self.safeSquares:
                    numSafe +=1
            self.safeSquares[clue[0]]=clue[1], numSafe, numMines