import ImprovedKnowledgeBase
from random import randint
from collections import deque

# this agent is a driver for our improved knowledge base

# board is the given board to solve
    # improvedKnowledge is our improved Knowledge base object
    # selectionFunction is a method function of improved knowledge that represents our selection algorithm
            # for the case when no safe squares can be found to query (we have to query something uncertain at this point)
def improvedSolveBoard(board,improvedKnowledge,selectionFunction):
    while (True):
        #print(improvedKnowledge.equations)
        if (len(improvedKnowledge.knownValues) == board.dim**2):
            # then we solved the board, we can break
                # then the board can print out the output or something
            print("Board is solved!")
            print("num mines triggered:"+str(board.numTriggers))
            print("num mines identified:"+str(len(board.mines)-board.numTriggers))
            break
        else:
            # then we can guess a square
                # this will lead to a query --> reduce --> solve --> substitute loop
            toQuery = selectionFunction(improvedKnowledge)
            # actually querying the square
            #print("Querying location: "+str(toQuery))
            toSolve = improvedKnowledge.queryCellFromBoard(toQuery,board)
            # run basic agent logic
            '''
            basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
            while basicMines or basicSafes:
                if basicMines:
                    mineLoopHelper(basicMines,basicSafes,improvedKnowledge,toSolve)
                    #improvedKnowledge.printKnowledgeBase()
                if basicSafes:
                    safeLoopHelper(basicMines,basicSafes,improvedKnowledge,toSolve,board)
                    #improvedKnowledge.printKnowledgeBase()
            '''

            # initiating loop to see if we can go further
            reduceLoop(improvedKnowledge,toSolve)
            while toSolve:
                # while we still have equations to solve, we pop one at a time
                equationToSolve = toSolve.pop()
                #print("popped equation:"+str(equationToSolve))
                # solving equations
                # equation solver returns list of discovered mines, and list of discovered free spots from solving the equation
                discoveredMines, discoveredFree = improvedKnowledge.solvedEquationSolver(equationToSolve)
                # run basic agent logic
                '''
                basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
                for mines in basicMines:
                    if mines not in discoveredMines:
                        discoveredMines.append(mines)
                for safes in basicSafes:
                    if safes not in discoveredFree:
                        discoveredFree.append(safes)
                '''

                # first we substitute the discovered mines and add any solvable equations to toSolve
                #newToSolve = deque()
                while discoveredMines or discoveredFree:
                    if discoveredMines:
                        mineLoopHelper(discoveredMines,discoveredFree,improvedKnowledge,toSolve)
                        #improvedKnowledge.printKnowledgeBase()
                    if discoveredFree:
                        safeLoopHelper(discoveredMines,discoveredFree,improvedKnowledge,toSolve,board)
                        # then we have free squares to try and sub and equation reduce
                        #improvedKnowledge.printKnowledgeBase()
                # seeing if we can reduce further
                reduceLoop(improvedKnowledge,toSolve)
        #print(improvedKnowledge.equations)

    # implementation to globally solve the board
        # ideas to implement
            # if at any point the num Mines identified = numMines total, we mark the rest as safe and stop
            # if a clue denotes the last set of mines,
                # i.e 3 mines remaining and the clue says 3
                    # then, we can query everything else, knowing it is safe
            # for selection, we calculate the probabilities of a mine being in each neighbor set
                # if the probability is greater outside, then we do not query in the neighbor set
        # in addition, if we find the total number of safe spots, we can conclude that every other square is a mine
def globalSolveBoard(board,improvedKnowledge):
    # saving total number of mines
    numMines = len(board.mines)
    lastLocQueried=None
    while (True):
        #print(improvedKnowledge.equations)
        if (len(improvedKnowledge.knownValues) == board.dim ** 2):
            # then we solved the board, we can break
            # then the board can print out the output or something
            print("Board is solved!")
            print("num mines triggered:" + str(board.numTriggers))
            print("num mines identified:" + str(len(board.mines) - board.numTriggers))
            break
        elif (numMines ==0):
            # then everything else is safe
            for i in range(board.dim):
                for j in range(board.dim):
                    if (i,j) not in improvedKnowledge.knownValues:
                        # then this should be queried as it is safe
                        #print("FOUND GLOBAL SAFE: " +str((i,j)))
                        improvedKnowledge.queryCellFromBoard((i,j),board)
            # we are done here, on next loop iteration, it will print board is solved
        elif len(improvedKnowledge.knownValues)+numMines == (board.dim**2) :
            # then we know that everything else is a mine
                # this is just saying:
                    # if known safe +known mines + remaining mines = number of all spots
                    # then all the remining spots must be mines
            for i in range(board.dim):
                for j in range(board.dim):
                    loc = (i, j)
                    if loc not in improvedKnowledge.knownValues:
                        #print("FOUND GLOBAL MINE: "+str(loc))
                        improvedKnowledge.knownValues[loc] = False
        else:
            # then we can guess a square
            # this will lead to a query --> reduce --> solve --> substitute loop
            toSolve=deque()
            toQuery = improvedKnowledge.globalCellToQuery(numMines,lastLocQueried)
            for locToQuery in toQuery:
                toSolve+=improvedKnowledge.queryCellFromBoard(locToQuery,board)
                lastLocQueried=locToQuery
            # actually querying the square
            # print("Querying location: "+str(toQuery))
            #toSolve = improvedKnowledge.queryCellFromBoard(toQuery, board)
            #lastLocQueried=toQuery
            # run basic agent logic
            '''
            basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
            while basicMines or basicSafes:
                if basicMines:
                    mineLoopHelper(basicMines, basicSafes, improvedKnowledge, toSolve)
                    # improvedKnowledge.printKnowledgeBase()
                if basicSafes:
                    safeLoopHelper(basicMines, basicSafes, improvedKnowledge, toSolve, board)
                    # improvedKnowledge.printKnowledgeBase()
            '''

            # initiating loop to see if we can go further
            reduceLoop(improvedKnowledge, toSolve)
            while toSolve:
                # while we still have equations to solve, we pop one at a time
                equationToSolve = toSolve.pop()
                # print("popped equation:"+str(equationToSolve))
                # solving equations
                # equation solver returns list of discovered mines, and list of discovered free spots from solving the equation
                discoveredMines, discoveredFree = improvedKnowledge.solvedEquationSolver(equationToSolve)
                # run basic agent logic
                '''
                basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
                for mines in basicMines:
                    if mines not in discoveredMines:
                        discoveredMines.append(mines)
                for safes in basicSafes:
                    if safes not in discoveredFree:
                        discoveredFree.append(safes)
                '''


                # first we substitute the discovered mines and add any solvable equations to toSolve
                # newToSolve = deque()
                while discoveredMines or discoveredFree:
                    if discoveredMines:
                        mineLoopHelper(discoveredMines, discoveredFree, improvedKnowledge, toSolve)
                        # improvedKnowledge.printKnowledgeBase()
                    if discoveredFree:
                        safeLoopHelper(discoveredMines, discoveredFree, improvedKnowledge, toSolve, board)
                        # then we have free squares to try and sub and equation reduce
                        # improvedKnowledge.printKnowledgeBase()
                # seeing if we can reduce further
                reduceLoop(improvedKnowledge, toSolve)
            # updating number of mines
            numMinesUpdate = 0
            for locs in improvedKnowledge.knownValues:
                if improvedKnowledge.knownValues[locs] is False:
                    numMinesUpdate += 1
            numMines=len(board.mines)-numMinesUpdate
        #print(improvedKnowledge.equations)


# idea of this method is for the user to feed our knowledge base clues and then the knowledge base will
    # respond with known mines, known safe spots, and the recommended cell to query
    # ultimate choice of query is up to user though
    # clue is of the form (loc,numMines) input by user
        # if numMines =-1, then loc was queried as a mine by the user
        # user starts this with None to get an initial recommendation
    # selection function is the function we use to select squares to query if no further safe squares can be found
        # either random, probabilistic or something else
        # so selectionFunction is a FUNCTION OBJECT/Pointer
    #nonQueriedSafeSquares is a deque of safe squares detected by our knowledge base, but the user has not queried yet
        # this is provided so that these can be repeatedly shown to the user to query from
def improvedSolveBoardFeed(improvedKnowledge,clue,selectionFunction,nonQueriedSafeSquares):
    # if we have as many squares in knowledge as squares in the board, we are done
    if len(improvedKnowledge.knownValues) == improvedKnowledge.dim ** 2:
        # then we are done
        print("BOARD IS SOLVED!")
        return (-1, -1)
    else:
        # we can include the clue in our knowledge base if not already present, if this clue was given from the tracked list of free squares toQuery, we can remove it
        if clue[0] in improvedKnowledge.knownValues:
            # user put a clue which was already given at some point
            #print("THIS WAS ALREADY REPORTED BY OUR KNOWLEDGE BASE! Please put another clue!")
            # this is error we return all None
            return (-1,0)
        else:
            if clue[0] in nonQueriedSafeSquares:
                nonQueriedSafeSquares.remove(clue[0])
            # we add to clue to knowledge base, get all the safes, and mines, in total from this step
                # then we can recommend a square for the user to query
            toSolve = improvedKnowledge.feedFromUser(clue)
            toSolve+= improvedKnowledge.finalPassReduce()
            foundSafes = deque()
            while toSolve:
                # solving equation, appending mines/safe squares and proceeding
                solvable = toSolve.pop()
                # solving equation and getting values found for mines and safes
                discoveredMines, discoveredFree = improvedKnowledge.solvedEquationSolver(solvable)
                # first we substitute the discovered mines and add any solvable equations to toSolve
                while discoveredMines:
                    if discoveredMines:
                        mineLoopHelper(discoveredMines, discoveredFree, improvedKnowledge, toSolve)
                        #improvedKnowledge.printKnowledgeBase()
                    if discoveredFree:
                        foundSafes.append(discoveredFree.pop())
                # seeing if we can reduce further
                reduceLoop(improvedKnowledge, toSolve)
            # at this point we have substituted every mine and we have a list of free spaces for the user to query
            for safe in foundSafes:
                if safe not in nonQueriedSafeSquares:
                    nonQueriedSafeSquares.append(safe)
            if not nonQueriedSafeSquares:
                # then we should refer to selection function to advise user
                return selectionFunction(improvedKnowledge)
            else:
                # then we can just return the first safe value we found
                return nonQueriedSafeSquares[0]

# method for user to feed in clues to solve on a global board (agent knows # of mines)
    # user enters number of mines in the board to begin with
def globalImprovedSolveBoardFeed(improvedKnowledge,clue,nonQueriedSafeSquares,numMinesRemaining):
    if len(improvedKnowledge.knownValues) == improvedKnowledge.dim ** 2:
        # then we are done
        print("BOARD IS SOLVED!")

        return (-1, -1),numMinesRemaining
    if numMinesRemaining==0:
        # then say the board is solved
        print("BOARD IS SOLVED, EVERY NON-QUERIED SQUARE IS SAFE!")
        return (-1,-1),0
    # getting number of nonqueried/identified squares
    numNonQueried=0
    for i in range(improvedKnowledge.dim):
        for j in range(improvedKnowledge.dim):
            loc = (i, j)
            if loc not in improvedKnowledge.knownValues:
                numNonQueried+=1
    if numNonQueried==numMinesRemaining:
        # then everything left is a mine
        print("BOARD IS SOLVED, EVERY NON-QUERIED SQUARE IS A MINE!")
        return (-1,-1),numMinesRemaining

    # we can include the clue in our knowledge base if not already present, if this clue was given from the tracked list of free squares toQuery, we can remove it
    if clue[0] in improvedKnowledge.knownValues:
        # user put a clue which was already given at some point
        #print("THIS WAS ALREADY REPORTED BY OUR KNOWLEDGE BASE! Please put another clue!")
        # this is error we return all None
        return (-1,0),numMinesRemaining
    else:
        # getting initial number of mines in KB
        initialMines = 0
        for i in range(improvedKnowledge.dim):
            for j in range(improvedKnowledge.dim):
                loc = (i, j)
                if loc in improvedKnowledge.knownValues:
                    if not improvedKnowledge.knownValues[loc]:
                        # then this is a known mine
                        initialMines += 1
        if clue[0] in nonQueriedSafeSquares:
            nonQueriedSafeSquares.remove(clue[0])
        lastLocQueried = clue[0]
        # we add to clue to knowledge base, get all the safes, and mines, in total from this step
            # then we can recommend a square for the user to query
        toSolve = improvedKnowledge.feedFromUser(clue)
        toSolve+= improvedKnowledge.finalPassReduce()
        foundSafes = deque()

        while toSolve:
            # solving equation, appending mines/safe squares and proceeding
            solvable = toSolve.pop()
            # solving equation and getting values found for mines and safes
            discoveredMines, discoveredFree = improvedKnowledge.solvedEquationSolver(solvable)

            # first we substitute the discovered mines and add any solvable equations to toSolve
            while discoveredMines or discoveredFree:
                if discoveredMines:
                    mineLoopHelper(discoveredMines, discoveredFree, improvedKnowledge, toSolve)
                    #improvedKnowledge.printKnowledgeBase()
                if discoveredFree:
                    foundSafes.append(discoveredFree.pop())
            # seeing if we can reduce further
            reduceLoop(improvedKnowledge, toSolve)
        # at this point we have substituted every mine and we have a list of free spaces for the user to query
        # getting final count of mines
        finalMines =0
        for i in range(improvedKnowledge.dim):
            for j in range(improvedKnowledge.dim):
                loc = (i, j)
                if loc in improvedKnowledge.knownValues:
                    if not improvedKnowledge.knownValues[loc]:
                        finalMines +=1
        minesIdentifiedThisRound = finalMines-initialMines
        numMinesRemaining -=minesIdentifiedThisRound

        for safe in foundSafes:
            if safe not in nonQueriedSafeSquares:
                nonQueriedSafeSquares.append(safe)
        if not nonQueriedSafeSquares:
            # then we should refer to selection function to advise user
            result = improvedKnowledge.globalCellToQuery(numMinesRemaining,lastLocQueried)
            if len(result)>1:
                # then using global strategy we found the remaining safe spaces
                for safes in result:
                    nonQueriedSafeSquares.append(safes)
                return nonQueriedSafeSquares[0], numMinesRemaining
            return improvedKnowledge.probabilityCellToQuery(), numMinesRemaining
        else:
            # then we can just return the first safe value we found
            return nonQueriedSafeSquares[0], numMinesRemaining

# step by step printing while solving
def stepByStepImprovedSolveBoard(board,improvedKnowledge,selectionFunction):
    while (True):
        #print(improvedKnowledge.equations)
        if (len(improvedKnowledge.knownValues) == board.dim**2):
            # then we solved the board, we can break
                # then the board can print out the output or something
            print("Board is solved!")
            print("num mines triggered:"+str(board.numTriggers))
            print("num mines identified:"+str(len(board.mines)-board.numTriggers))
            break
        else:
            # then we can guess a square
                # this will lead to a query --> reduce --> solve --> substitute loop
            toQuery = selectionFunction(improvedKnowledge)
            # actually querying the square
            print("Querying location: "+str(toQuery))
            toSolve = improvedKnowledge.queryCellFromBoard(toQuery,board)
            print("Found solvable equations: " + str(toSolve))
            # run basic agent logic
            '''
            basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
            while basicMines or basicSafes:
                if basicMines:
                    mineLoopHelper(basicMines,basicSafes,improvedKnowledge,toSolve)
                    #improvedKnowledge.printKnowledgeBase()
                if basicSafes:
                    safeLoopHelper(basicMines,basicSafes,improvedKnowledge,toSolve,board)
                    #improvedKnowledge.printKnowledgeBase()
            '''

            # initiating loop to see if we can go further
            reduceLoop(improvedKnowledge,toSolve)
            while toSolve:
                # while we still have equations to solve, we pop one at a time
                equationToSolve = toSolve.pop()
                print("Solving Solvable Equation: "+str(equationToSolve))
                #print("popped equation:"+str(equationToSolve))
                # solving equations
                # equation solver returns list of discovered mines, and list of discovered free spots from solving the equation
                discoveredMines, discoveredFree = improvedKnowledge.solvedEquationSolver(equationToSolve)
                print("Found mines at "+str(discoveredMines))
                print("Found Safes at "+str(discoveredFree))
                # run basic agent logic
                '''
                basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
                for mines in basicMines:
                    if mines not in discoveredMines:
                        discoveredMines.append(mines)
                for safes in basicSafes:
                    if safes not in discoveredFree:
                        discoveredFree.append(safes)
                '''

                # first we substitute the discovered mines and add any solvable equations to toSolve
                #newToSolve = deque()
                while discoveredMines or discoveredFree:
                    if discoveredMines:
                        print("Substituting known mine into equations")
                        mineLoopHelper(discoveredMines,discoveredFree,improvedKnowledge,toSolve)
                        #improvedKnowledge.printKnowledgeBase()
                    if discoveredFree:
                        print("Substituting safe spot into equations and building query from safe clue")
                        safeLoopHelper(discoveredMines,discoveredFree,improvedKnowledge,toSolve,board)
                        # then we have free squares to try and sub and equation reduce
                        #improvedKnowledge.printKnowledgeBase()
                # seeing if we can reduce further
                reduceLoop(improvedKnowledge,toSolve)
            improvedKnowledge.printKnowledgeBase()


def stepByStepGlobalSolveBoard(board,improvedKnowledge):
    # saving total number of mines
    numMines = len(board.mines)
    lastLocQueried=None
    while (True):
        #print(improvedKnowledge.equations)
        if (len(improvedKnowledge.knownValues) == board.dim ** 2):
            # then we solved the board, we can break
            # then the board can print out the output or something
            print("Board is solved!")
            print("num mines triggered:" + str(board.numTriggers))
            print("num mines identified:" + str(len(board.mines) - board.numTriggers))
            break
        elif (numMines ==0):
            # then everything else is safe
            for i in range(board.dim):
                for j in range(board.dim):
                    if (i,j) not in improvedKnowledge.knownValues:
                        # then this should be queried as it is safe
                        print("FOUND GLOBAL SAFE: " +str((i,j)))
                        improvedKnowledge.queryCellFromBoard((i,j),board)
            # we are done here, on next loop iteration, it will print board is solved
        elif len(improvedKnowledge.knownValues)+numMines == (board.dim**2) :
            # then we know that everything else is a mine
                # this is just saying:
                    # if known safe +known mines + remaining mines = number of all spots
                    # then all the remining spots must be mines
            for i in range(board.dim):
                for j in range(board.dim):
                    loc = (i, j)
                    if loc not in improvedKnowledge.knownValues:
                        print("FOUND GLOBAL MINE: "+str(loc))
                        improvedKnowledge.knownValues[loc] = False
        else:
            # then we can guess a square
            # this will lead to a query --> reduce --> solve --> substitute loop
            toSolve=deque()
            toQuery = improvedKnowledge.globalCellToQuery(numMines,lastLocQueried)
            for locToQuery in toQuery:
                print("Querying location: " + str(toQuery))
                toSolve+=improvedKnowledge.queryCellFromBoard(locToQuery,board)
                lastLocQueried=locToQuery
            print("Found solvable equations: " + str(toSolve))
            # actually querying the square
            #toSolve = improvedKnowledge.queryCellFromBoard(toQuery, board)
            #lastLocQueried=toQuery
            # run basic agent logic
            '''
            basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
            while basicMines or basicSafes:
                if basicMines:
                    mineLoopHelper(basicMines, basicSafes, improvedKnowledge, toSolve)
                    # improvedKnowledge.printKnowledgeBase()
                if basicSafes:
                    safeLoopHelper(basicMines, basicSafes, improvedKnowledge, toSolve, board)
                    # improvedKnowledge.printKnowledgeBase()
            '''

            # initiating loop to see if we can go further
            reduceLoop(improvedKnowledge, toSolve)
            while toSolve:
                # while we still have equations to solve, we pop one at a time
                equationToSolve = toSolve.pop()
                print("Solving Solvable Equation: " + str(equationToSolve))
                # print("popped equation:"+str(equationToSolve))
                # solving equations
                # equation solver returns list of discovered mines, and list of discovered free spots from solving the equation
                discoveredMines, discoveredFree = improvedKnowledge.solvedEquationSolver(equationToSolve)
                print("Found mines at " + str(discoveredMines))
                print("Found Safes at " + str(discoveredFree))
                # run basic agent logic
                '''
                basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
                for mines in basicMines:
                    if mines not in discoveredMines:
                        discoveredMines.append(mines)
                for safes in basicSafes:
                    if safes not in discoveredFree:
                        discoveredFree.append(safes)
                '''


                # first we substitute the discovered mines and add any solvable equations to toSolve
                # newToSolve = deque()
                while discoveredMines or discoveredFree:
                    if discoveredMines:
                        print("Substituting known mine into equations")
                        mineLoopHelper(discoveredMines, discoveredFree, improvedKnowledge, toSolve)
                        # improvedKnowledge.printKnowledgeBase()
                    if discoveredFree:
                        print("Substituting safe spot into equations and building query from safe clue")
                        safeLoopHelper(discoveredMines, discoveredFree, improvedKnowledge, toSolve, board)
                        # then we have free squares to try and sub and equation reduce
                        # improvedKnowledge.printKnowledgeBase()
                # seeing if we can reduce further
                reduceLoop(improvedKnowledge, toSolve)
            # updating number of mines
            numMinesUpdate = 0
            for locs in improvedKnowledge.knownValues:
                if improvedKnowledge.knownValues[locs] is False:
                    numMinesUpdate += 1
            numMines=len(board.mines)-numMinesUpdate
            improvedKnowledge.printKnowledgeBase()


# helper method to clean up code in first method
    #basicMines is a deque of known mines
    # basicSafes is a dequeue of known safe squares
    # improved knowledge is our improved knowledge base
    # toSolve is a dequeue of solvable equations
def mineLoopHelper(basicMines,basicSafes,improvedKnowledge,toSolve):
    mineToSub = basicMines.pop()
    newToSolve = improvedKnowledge.substitution((1, mineToSub))
    for newSolvable in newToSolve:
        toSolve.append(newSolvable)

    # then we have mines to try and sub
    # run basic agent logic
    '''
    otherMines, otherSafes = improvedKnowledge.basicAgentLogic()
    for mines in otherMines:
        if mines not in basicMines:
            basicMines.append(mines)
    for safes in otherSafes:
        if safes not in basicSafes:
            basicSafes.append(safes)
    '''

# global implementation where we know total number of mines
def globalMineLoopHelper(basicMines,basicSafes,improvedKnowledge,toSolve,minesRemaining,minesQueried):
    numMinesToReturn = minesRemaining
    mineToSub = basicMines.pop()
    if mineToSub not in minesQueried:
        # this is a brand new mine we identified
        numMinesToReturn -= 1
        minesQueried.add(mineToSub)

    newToSolve = improvedKnowledge.substitution((1, mineToSub))
    for newSolvable in newToSolve:
        toSolve.append(newSolvable)

    # then we have mines to try and sub
    # run basic agent logic
    '''
    otherMines, otherSafes = improvedKnowledge.basicAgentLogic()
    for mines in otherMines:
        if mines not in basicMines:
            basicMines.append(mines)
    for safes in otherSafes:
        if safes not in basicSafes:
            basicSafes.append(safes)
    '''
    return numMinesToReturn

# same parameters as above equation
def safeLoopHelper(discoveredMines,discoveredFree,improvedKnowledge,toSolve,board):
    newSafe = discoveredFree.pop()
    # getting equation from clue from query
    toSolve+= improvedKnowledge.queryCellFromBoard(newSafe,board)
    # run basic agent logic
    '''
    basicMines, basicSafes = improvedKnowledge.basicAgentLogic()
    for mines in basicMines:
        if mines not in discoveredMines:
            discoveredMines.append(mines)
    for safes in basicSafes:
        if safes not in discoveredFree:
            discoveredFree.append(safes)
    '''


# helper to initiate the loop to keep reducing
def reduceLoop(improvedKnowledge, toSolve):
    keepReducing = improvedKnowledge.finalPassReduce()
    for solvable in keepReducing[1]:
        toSolve.append(solvable)
    while (keepReducing[0]):
        keepReducing=improvedKnowledge.finalPassReduce()
        for solvable in keepReducing[1]:
            toSolve.append(solvable)



