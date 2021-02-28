# basic implementation of knowledge base required
from LibaryFunctions import getValidNeighbors


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
        neighbors = getValidNeighbors(loc)
        numMines=0
        numSafe=0
        numHidden=0
        for neighbor in neighbors:
            if neighbor in self.knownMines:
                numMines+=1
            elif neighbor in self.safeSquares:
                numSafe+=1
            else:
                numHidden +=1
        return (numMinesClue,numSafe,numMines,numHidden)

    def allMinesNearby(loc,self):
        added = False
        newMines=set()
        if (self.safeSquares[loc])[0]-(self.safeSquares[loc])[2] == (self.safeSquares[loc])[3]:
            neighbors = getValidNeighbors(loc)
            for neighbor in neighbors:
                if neighbor not in self.safeSquares:
                    self.knownMines.add(neighbor)
                    newMines.add(neighbor)
                    added=True
        return added,newMines

    def allSafeNearby(loc,self):
        added =False
        newSafe=set()
        if 8-(self.safeSquares[loc])[0]-(self.safeSquares[loc])[1]== (self.safeSquares[loc])[3]:
            neighbors = getValidNeighbors(loc)
            for neighbor in neighbors:
                if neighbor not in self.knownMines:
                    numMinesClue = getQueryFromBoard(neighbor)
                    locData = self.getDataHelper(neighbor,numMinesClue)
                    self.safeSquares[neighbor]=locData
                    added=True
                    newSafe.add(neighbor)
        return added,newSafe
    def queryCellFromBoard(self,loc):
        numMinesClue =getQueryFromBoard(loc)
        if numMinesClue==-1:
            # then agent queried a mine
            self.knownMines.add(loc)
            return True,loc
        else:
            # this is safe, we can update our info
            data = self.getDataHelper(loc,numMinesClue)
            self.safeSquares[loc]=data
            return False,loc


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
