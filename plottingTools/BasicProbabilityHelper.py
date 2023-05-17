from basicLogic import basicAgent, basicKnowledgeBase
import Board
# this file serves just to have a separate probability helper for our basic agent


    # we will test for a board of size 40x40
        # and for each density, we will do 25 trials


def basicProbabilityHelper(dim,numTrials):
    # generates a new board everytime with specified dim in increments of mine densities
    inputOutput=[]
    # y axis is success --> numMines identified / numMinesTotal
    # if mine density is zero, then vacuously has 100% success rate
    inputOutput.append((0,1))
    currDensity =0.05
    while (currDensity<1):
        print("curr Density: "+str(currDensity))
        resultSum = 0
        currTrials=0
        while currTrials<numTrials:
            print("current Trial: "+str(currTrials))
            testBoard = Board.Board(dim)
            #generating mines for current density
            testBoard.generateBoard(int(currDensity*(dim**2)))
            testKB =  basicKnowledgeBase.BasicKnowledgeBase(dim)
            # running our solver
            basicAgent.basicSolveMines(testBoard, testKB, False)
            # getting the result
            numMinesIdentified = len(testBoard.mines)-testBoard.numTriggers
            result=((1.0)*numMinesIdentified)/((1.0)*len(testBoard.mines))
            print(result)
            resultSum+= result
            print(resultSum)
            currTrials+=1
        # dividing resultSum by number of trials now for average
        resultSum/=((1.0)*numTrials)
        print("To append: "+str(resultSum))
        inputOutput.append((currDensity,resultSum))
        # incrementing density for next test
        currDensity+=0.05
    # if mine density is 1, we cannot identify any mine safely
    inputOutput.append((1,0))
    return inputOutput
