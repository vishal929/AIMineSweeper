import ImprovedKnowledgeBase
from random import randint


# this agent is a driver for our improved knowledge base


def improvedSolveBoard(board,improvedKnowledge):
    while (True):
        if (improvedKnowledge.knownValues.size() == board.dim):
            # then we solved the board, we can break
                # then the board can print out the output or something
            break
        else:
            # then we can guess a square
                # this will lead to a query --> reduce --> solve --> substitute loop
            toQuery = improvedKnowledge.cellToQuery()
            # actually querying the square
            result = improvedKnowledge.queryCellFromBoard(board,toQuery)
            if result[1] is None:
                # then the agent queried a mine
                print("OH NO! We queried a mine!")
            else:
                # then the agent queried a safe spot

# idea of this method is for the user to feed our knowledge base clues and then the knowledge base will
    # respond with known mines, known safe spots, and the recommended cell to query
    # ultimate choice of query is up to user though
    # clue is of the form (loc,numMines) input by user
        # if numMines =-1, then loc was queried as a mine by the user
        # user starts this with None to get an initial recommendation
def improvedSolveBoardFeed(improvedKnowledge,clue):
    if clue is None:
        # then the user just started
        # we recommend the user to pick the middle of the board to query
        return None,None,(improvedKnowledge.dim/2,improvedKnowledge.dim/2)
    else:
        # we can include the clue in our knowledge base if not already present
        if clue in improvedKnowledge.knownValues:
            # user put a clue which was already given at some point
            print("THIS WAS ALREADY REPORTED BY OUR KNOWLEDGE BASE! Please put another clue!")
            # this is error we return all None
            return None,None,None
        else:
            # we add to clue to knowledge base, get all the safes, and mines, in total from this step
                # then we can recommend a square for the user to query
            result = improvedKnowledge.feedFromUser(clue)
            # if we have as many squares in knowledge as squares in the board, we are done
            if len(improvedKnowledge.knownValues) == improvedKnowledge.dim**2:
                # then we are done
                print("BOARD IS SOLVED!")
                return None, None, (-1,-1)
            # if the equation is NONE, then we can move right to substitution of mine
                # if not, we need to go through substitution of the free space
                    # NEED TO CONSIDER IF EQUATION TO ADD CHANGES OR NOT!!!!
            if result[1] is None:
                # then this was a mine, we can go to substitution
                toSolve = improvedKnowledge.substitution((1,result[0]))
                foundMines=dequeue()
                foundSafes=dequeue()
                # to solve is a dequeue of solvable equations
                    #(already removed from list of equations in knowledge base)
                for solvable in toSolve:
                    result = improvedKnowledge.solvedEquationSolver(solvable)
                    for mines in result[0]:
                        toSolve+=improvedKnowledge.substitution((1,mines))
                        foundMines.append(mines)
                    for safes in result[1]:
                        toSolve+=improvedKnowledge.substitution((0,safes))
                        foundSafes.append(safes)
                # after this loop is finished we have found all possible mines/free squares
                    # we can display them to the user
                    # then user must choose to input a clue from the list of free mines
                # we will always recommend user to query the first square on the safe list
                return foundMines,foundSafes,foundSafes[0]
            else:
                pass





