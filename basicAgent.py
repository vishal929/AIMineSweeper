# this is a script to solve a board with our basic agent
from random import randint
from basicKnowledgeBase import BasicKnowledgeBase

def basicSolveMines(dim,hi):
    while hi.safeSquares.size()+hi.knownMines.size()!=dim*dim:
        logicUpdated=False
        for safes in hi.safeSquares:
            if hi.allMinesNearby(safes) or hi.allSafeNearby(safes):
                # then we found some stuff in our logic
                logicUpdated=True
        # need to query and pick randomly
        if not logicUpdated:
            while True:
                rand= randint(0,dim*dim)
                col=rand%dim
                row=(rand-col)/dim
                if (row,col) not in hi.safeSquares and (row,col) not in hi.knownMines:
                    # then we can query this
                    hi.queryCellFromBoard((row,col))
                    break

def basicSolveMinesStep(dim,knowledgeBase):
    if (knowledgeBase is None):
        # then we initialize it
        knowledgeBase = BasicKnowledgeBase(dim)
        return True
    # doing a single step
    # a single step involves using knowledge base to update data
        # and then performing a query if no data can be updated
    if knowledgeBase.safeSquares.size() + knowledgeBase.knownMines.size()==dim*dim:
        # then our agent has visited every space we are done
        return False

    # seeing if existing data can be updated
    logicUpdated = False
    for safes in knowledgeBase.safeSquares:
        if knowledgeBase.allMinesNearby(safes) or knowledgeBase.allSafeNearby(safes):
            logicUpdated=True

    if not logicUpdated:
        # then we pick a place to query
        while True:
            rand = randint(0, dim * dim)
            col = rand % dim
            row = (rand - col) / dim
            if (row, col) not in hi.safeSquares and (row, col) not in hi.knownMines:
                # then we can query this
                hi.queryCellFromBoard((row, col))
                break
    return True

