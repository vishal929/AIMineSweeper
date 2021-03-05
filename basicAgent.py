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

# step by step implementation of basicSolveMines above
def basicSolveMinesStep(dim,knowledgeBase):
    # seeing if existing data can be updated
    minesToUpdate = set()
    safesToUpdate = set()

    if (knowledgeBase is None):
        # then we initialize it
        knowledgeBase = BasicKnowledgeBase(dim)
        return True,minesToUpdate,safesToUpdate
    # doing a single step
    # a single step involves using knowledge base to update data
        # and then performing a query if no data can be updated
    if knowledgeBase.safeSquares.size() + knowledgeBase.knownMines.size()==dim*dim:
        # then our agent has visited every space we are done
        return False,minesToUpdate,safesToUpdate


    for safes in knowledgeBase.safeSquares:
        result = knowledgeBase.allMinesNearby(safes)
        for mines in result[1]:
            minesToUpdate.add(mines)
        result = knowledgeBase.allSafeNearby(safes)
        for safeSquares in result:
            safesToUpdate.add(safeSquares)


    if len(minesToUpdate)==0 and len(safesToUpdate)==0:
        # then we pick a place to query
        while True:
            rand = randint(0, dim * dim)
            col = rand % dim
            row = (rand - col) / dim
            if (row, col) not in knowledgeBase.safeSquares and (row, col) not in knowledgeBase.knownMines:
                # then we can query this
                result=knowledgeBase.queryCellFromBoard((row, col))
                if result:
                    # then we hit a mine
                    minesToUpdate.add(result[1])
                else:
                    # then this is a safe square
                    safesToUpdate.add(result[1])
                break
    return True,minesToUpdate,safesToUpdate

