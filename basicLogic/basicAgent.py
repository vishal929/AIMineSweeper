# this is a script to solve a board with our basic agent
from random import randint
from basicLogic.basicKnowledgeBase import BasicKnowledgeBase

def basicSolveMines(board,hi,stepByStep):
    while True:
        if len(hi.safeSquares)+len(hi.knownMines)== hi.dim**2:
            print("Board is solved!")
            print("Num Mines Triggered: "+str(board.numTriggers))
            print("Num Mines Identified: "+str(len(hi.knownMines)-board.numTriggers))
            break
        else:
            # then we get a query going
            locToQuery = hi.randomCellToQuery()
            if stepByStep:
                print("Querying cell: "+str(locToQuery))
            # actually querying the space
            res = hi.queryCellFromBoard(locToQuery,board)
            if stepByStep:
                if res[0]:
                    print("Query resulted in a mine!")
                else:
                    print("Query resulted in a safe square!")
            # seeing if we can apply some rules
            minesFound=set()
            safesFound=set()
            while True:
                resOne = mineLoopHelper(hi)
                resTwo = safeLoopHelper(board,hi)
                if not resOne[0] and not resTwo[0]:
                    # then no deductions were made
                    break
                else:
                    for mine in resOne[1]:
                        minesFound.add(mine)
                    for safe in resTwo[1]:
                        safesFound.add(safe)
            if stepByStep:
                print("Mines Found: "+str(minesFound))
                print("Safes Found: "+str(safesFound))

    # user feeds in a clue in the form (loc,clue) where clue=-1 if the location is a mine
def basicAgentFeed(knowledge, clue, nonQueriedSafeSquares):
    if clue[0] in knowledge.knownMines or clue[0] in knowledge.safeSquares:
        # then this location is in the KB already!
        print("LOCATION WAS ALREADY IN THE KB!")
        if nonQueriedSafeSquares:
            return nonQueriedSafeSquares[0]
        else:
            return knowledge.randomCellToQuery()
    else:
        # then we should feed the clue into our knowledge base
        if clue[0] in nonQueriedSafeSquares:
            nonQueriedSafeSquares.remove(clue[0])
        knowledge.feedClue(clue)
        minesFound = set()
        safesFound = set()
        while True:
            resOne = mineLoopHelper(knowledge)
            resTwo = feedSafeLoopHelper(knowledge)
            if not resOne[0] and not resTwo[0]:
                # then no deductions were made
                break
            else:
                for mine in resOne[1]:
                    minesFound.add(mine)
                for safe in resTwo[1]:
                    safesFound.add(safe)
        for safe in safesFound:
            if safe not in nonQueriedSafeSquares:
                nonQueriedSafeSquares.append(safe)
        if nonQueriedSafeSquares:
            return nonQueriedSafeSquares[0]
        else:
            return knowledge.randomCellToQuery()




def mineLoopHelper(hi):
    minesFound=set()
    reductionDone=False
    for loc in hi.safeSquares:
        res = hi.allMinesNearby(loc)
        if len(res[1])>0:
            reductionDone=True
            for mines in res[1]:
                minesFound.add(mines)
    return reductionDone,minesFound

def safeLoopHelper(board,hi):
    safesFound = set()
    reductionDone = False
    for loc in hi.safeSquares:
        res = hi.allSafeNearby(loc)
        if len(res[1])>0:
            reductionDone=True
            for safes in res[1]:
                safesFound.add(safes)
    # adding new locations to our KB
    for safes in safesFound:
        hi.queryCellFromBoard(safes,board)
    return reductionDone, safesFound

def feedSafeLoopHelper(hi):
    safesFound = set()
    reductionDone = False
    for loc in hi.safeSquares:
        res = hi.allSafeNearby(loc)
        if len(res[1]) > 0:
            reductionDone = True
            for safes in res[1]:
                safesFound.add(safes)
    # adding new locations to our KB
    return reductionDone, safesFound


