# this is a script to solve a board with our basic agent
from random import randint

import basicKnowledgeBase

def basicSolveMines(dim):
    hi =basicKnowledgeBase(dim)

    while hi.safeSquares.size()+hi.knownMines.size()!=dim*dim:
        logicUpdated=False
        for safes in safeSquares:
            if allMinesNearby(safes) or allSafeNearby(safes):
                # then we found some stuff in our logic
                logicUpdated=True
        # need to query and pick randomly
        if not logicUpdated:
            while True:
                rand= randint(0,dim*dim)
                col=rand%dim
                row=(rand-col)/dim
                if (row,col) not in self.safeSquares and (row,col) not in self.knownMines:
                    # then we can query this
                    hi.queryCellFromBoard((row,col))
                    break
