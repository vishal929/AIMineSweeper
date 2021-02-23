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
        initialSize = self.knownMines.size()
        if (self.safeSquares[loc])[0]-(self.safeSquares[loc])[2] == (self.safeSquares[loc])[3]:
            neighbors = getValidNeighbors(loc)
            for neighbor in neighbors:
                if isValid(dim,neighbor):
                    if neighbor not in self.safeSquares:
                        self.knownMines.add(neighbor)
        if initialSize !=self.knownMines.size():
            return True
        else:
            return False

    def allSafeNearby(loc,self):
        initialSize = self.safeSquares.size()
        if 8-(self.safeSquares[loc])[0]-(self.safeSquares[loc])[1]== (self.safeSquares[loc])[3]:
            neighbors = getValidNeighbors(loc)
            for neighbor in neighbors:
                if neighbor not in self.knownMines:
                    numMinesClue = getQueryFromBoard(neighbor)
                    locData = self.getDataHelper(neighbor,numMinesClue)
                    self.safeSquares[neighbor]=locData
        if initialSize!=self.safeSquares.size():
            return True
        else:
            return False

    def queryCellFromBoard(self,loc):
        numMinesClue =getQueryFromBoard(loc)
        if numMinesClue==-1:
            # then agent is dead
            # this is a mine
            self.knownMines.add(loc)
        else:
            # this is safe, we can update our info
            data = self.getDataHelper(loc,numMinesClue)
            self.safeSquares[loc]=data



