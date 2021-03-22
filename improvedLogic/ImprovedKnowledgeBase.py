from random import randint
from collections import deque
import LibraryFunctions


class ImprovedKnowledgeBase():
        def __init__(self,dim):
            self.dim=dim
            # hash values for knownValues
            # mines (False)
            # safeSquares (True,numMinesGivenByClue)
            self.knownValues={}
            # equations
            # each equation is (location is key, val is coefficient {},RHS value)
            self.equations=deque()

        # THIS METHOD ASSUMES THERE IS A VALID CANCELLATION POSSIBLE
        # returns the equation that represents the reduction between both equations
        def reductionEquation(self,firstEquation,secondEquation):
            # subtract smaller RHS value equation from larger one
            larger = None
            smaller = None
            if (secondEquation[1]>firstEquation[1]):
                larger=secondEquation
                smaller = firstEquation
            else:
                larger=firstEquation
                smaller=secondEquation
            # actual subtraction
            newEquationDict = {}
            # updating based on larger equation
            for val in larger[0]:
                newEquationDict[val]=larger[0][val]
            # updating value
            newRHS=larger[1]-smaller[1]
            # updating based on negative values of smaller equation
            for val in smaller[0]:
                if val in newEquationDict:
                    newEquationDict[val]=newEquationDict[val]-smaller[0][val]
                    if newEquationDict[val]==0:
                        # we need to remove this
                        del newEquationDict[val]
                else:
                    newEquationDict[val]= -smaller[0][val]
            return (newEquationDict,newRHS)

        # newDiscovery is a tuple (1/0, loc)
            # 1/0 indicates if mine or not
            # location is the (row,col) of discovered info about entry
        # returns list of equations that can be solved (already removed from our knowledge base)
        def substitution(self,newDiscovery):
            # removing any solved equations
            # we need to check for a certain special case
                # we need to check if this value is already known, then we can skip
            removedList = deque()
            solvedList = deque()
            reducedList = deque()

            for equation in self.equations:
                if newDiscovery[1] in equation[0]:
                    lhs = equation[0]
                    rhs = equation[1]
                    # modification is the new value on LHS based on discovered value of this entry
                    # getting coefficient
                    modification = lhs[newDiscovery[1]]
                    # multiplying coefficient with known value
                    modification *= newDiscovery[0]
                    # subtracting from rhs
                    rhs -= modification
                    # removing variable from our equation after substitution
                    del lhs[(newDiscovery[1])]
                    # accounting for RHS being negative
                    if rhs<0:
                        for coefficients in lhs:
                            lhs[coefficients]=-lhs[coefficients]
                        rhs = - rhs
                    reducedEquation = (lhs,rhs)
                    if not reducedEquation[0]:
                        # this means that variable coefficents are empty, we should just remove the equation
                        removedList.append(equation)
                        continue
                    if self.canBeSolved(reducedEquation):
                        # we want to return solved list in the end and remove the associated
                            # old versions of the solvable equations from our knowledge base
                        solvedList.append(reducedEquation)
                        removedList.append(equation)
                    else:
                        # in this case, the reduced equation is not solvable
                            # we want to update the old equation in KB with the reduced version
                        reducedList.append(reducedEquation)
                        removedList.append(equation)
            # removing it from our actual knowledge base
            for removable in removedList:
                self.equations.remove(removable)
            for reducable in reducedList:
                # adding in reduced equations that arent solvable
                self.equations.append(reducable)
            return solvedList

        # solves an equation detected by isSolvable method
            # returns the values found in the form:
            # returns a list of mines and a list of free spots found
        def solvedEquationSolver(self,equation):

            # solved variables are any variables solved of the form (1/0, loc) where 1 is a mine, 0 safe
            foundMines=deque()
            foundSafes=deque()
            for ourVar in equation[0]:

                if ourVar in self.knownValues:
                    continue

                # logic for if rhs is zero and all coefficients are same sign (all are free)
                if equation[1] == 0:
                    # then this is safe
                    foundSafes.append(ourVar)
                    continue
                # logic for if all positive terms on lhs equals rhs (positive terms are mines), everything else is free
                if equation[0][ourVar] > 0:
                    # this is a mine
                    self.knownValues[ourVar]=False
                    foundMines.append(ourVar)
                else:
                    # then this is safe
                    foundSafes.append(ourVar)

            return foundMines,foundSafes




        # simple helper to scale a solved equation to final value (i.e -A=-1, 2A=2,etc.)
        def solvedEquationScalar(self,equation):
            for key in equation[0]:
                if equation[0][key]!=1:
                    equation[1]/=equation[0][key]
                    equation[0][key]=1
                    return key

        # helper to query cell from board and update our info about known squares
            # queries initiate the substitute->reduce->solve->substitute loop
        # returns loc,None if the square is a mine
            # otherwise, returns loc,EQUATION if the square is free
                # loc is (row,col) and EQUATION is the equation built from clue to add to knowledge base
        def queryCellFromBoard(self, loc,Board):
            if loc in self.knownValues:
                # we do not try and query the same thing twice
                # returning location with an empty equation
                # returning empty deque
                return deque()
            numMinesClue = Board.queryPosition(loc)
            if numMinesClue == -1:
                # then agent queried a mine
                # this is a mine
                self.knownValues[loc] = False
                # getting result of substitution
                toSolve = self.substitution((1,loc))
                return toSolve
            else:
                # this is safe, we can update our info and use the clue to generate an equation

                equationLHS = {}
                equationRHS=numMinesClue
                neighbors = LibraryFunctions.getValidNeighbors(self.dim,loc)
                numSafeSquares=0
                numMines=0
                for neighbor in neighbors:
                    if neighbor in self.knownValues:
                        if self.knownValues[neighbor] is False:
                            # this is a mine
                            numMines +=1
                            equationRHS -=1
                        else:
                            # this is safe
                            numSafeSquares+=1
                    else:
                        # then this is part of a generated equation with the clue
                            #with coefficient of 1
                        equationLHS[neighbor]=1
                # updating info about safe square
                self.knownValues[loc] = True,numMinesClue
                # this is a free square
                # updating info about the clue associated with query
                newEquation = equationLHS,equationRHS
                # plugging in newEquation and substitution
                toSolve = self.substitution((0,loc))
                otherSolvable = self.finalAddReduce(newEquation)
                for solvable in otherSolvable:
                    toSolve.append(solvable)
                return toSolve

        # idea here is that we find the best reduction possible for each equation
        def finalPassReduce(self):
            didReducing = False
            toSolve = deque()
            toRemove = deque()
            toAdd = deque()
            for i in range(len(self.equations)):
                first = self.equations[i]

                if first in toRemove:
                    # then we shouldnt do more reduction with this
                    continue

                if self.canBeSolved(first):
                    if first not in toSolve:
                        toSolve.append(first)
                    if first not in toRemove:
                        toRemove.append(first)
                    continue
                reductionToUse=None
                secondToUse = None
                for j in range(i+1,len(self.equations)):
                    second = self.equations[j]
                    if second in toRemove:
                        # then we shouldnt do any more reduction with this
                        continue
                    sameOne=True
                    sameTwo=True
                    for vars in first[0]:
                        if vars not in second[0]:
                            sameOne = False
                            break
                    for vars in second[0]:
                        if vars not in first[0]:
                            sameTwo=False
                            break
                    if sameTwo and sameOne:
                        # cant reduce with same equation!
                        # in fact, we should remove one of them
                        toRemove.append(second)
                        continue

                    if self.canBeSolved(second):
                        if second not in toSolve:
                            toSolve.append(second)
                        if second not in toRemove:
                            toRemove.append(second)
                        continue
                    reductionToCheck = self.reductionEquation(first, second)
                    if self.canBeSolved(reductionToCheck):
                        # then I should append this to the solvable list
                        if reductionToCheck not in toSolve:
                            toSolve.append(reductionToCheck)
                    if len(reductionToCheck[0])<len(second[0]):
                        if reductionToUse is None:
                            didReducing = True
                            reductionToUse=reductionToCheck
                            secondToUse=second
                        else:
                            reductionToUse = reductionToCheck
                            secondToUse = second
                    elif len(reductionToCheck[0])<len(first[0]):
                        if reductionToUse is None:
                            didReducing = True
                            reductionToUse=reductionToCheck
                            secondToUse=first
                        else:
                            reductionToUse = reductionToCheck
                            secondToUse = first
                if reductionToUse is None:
                    # no other equations for reduction
                    continue
                if self.canBeSolved(reductionToUse):
                    if reductionToUse not in toSolve:
                        toSolve.append(reductionToUse)
                else:
                    toAdd.append(reductionToUse)
                if secondToUse not in toRemove:
                    toRemove.append(secondToUse)
            # removing equations first
            for removable in toRemove:
                self.equations.remove(removable)
            # adding equations second
            for addable in toAdd:
                self.equations.append(addable)
            # returning values
            return didReducing, toSolve

        # wrapper where we pass reduce after adding the given equation
        def finalAddReduce(self, equation):
            toSolve = deque()
            if equation[0]:
                # this is not empty
                self.equations.append(equation)
            # going through reductions
            result = self.finalPassReduce()
            for solvable in result[1]:
                toSolve.append(solvable)
            while (result[0]):
                result = self.finalPassReduce()
                for solvable in result[1]:
                    toSolve.append(solvable)
            return toSolve

        # returns True if equations is in solvable form, false otherwise
            # Solvable Forms
                # If sum of positive coefficients equals RHS, then every positive coefficient term is a mine, others are free
                    #i.e A+B-C-D = 2 --> A and B are mines, C and D are safe
                    # C+D-A-B = -2 --> A and B are mines (need to scale negative equations)
                # If rhs is zero and every coefficient is same sign, then every term is free
        def canBeSolved(self,equation):
            lhsSum = 0
            lastSign=None
            allSame = True
            for ourVar in equation[0]:
                if equation[0][ourVar] > 0:
                    lhsSum += equation[0][ourVar]
                    if lastSign is None:
                        lastSign='+'
                    elif lastSign=='-':
                        allSame=False
                else:
                    if lastSign is None:
                        lastSign='-'
                    elif lastSign=='+':
                        allSame=False
            # if lhsSum == equation[1] (rhs), then this is solvable
            if lhsSum==equation[1]:
                return True
            elif allSame and equation[1]==0:
                # if rhs is 0 and every lhs term is the same, then every term in the equation represents a free square
                return True
            else:
                return False

        # deciding which cell to query if we cannot proceed with reduction/substitution
            # returns the cell to query
            # idea, all possibly known safe cells have already been queried
                # so we need to find a cell with low probability of being a mine
                # idea: go through each cell that has been identified as free
                    # go through each hidden neighbor
                    # pick any hidden neighbor from cell with lowest (CLUE-minesIdentified)/numHiddenNeighbors
        def probabilityCellToQuery(self):
            # initial value is any random cell
            lowestProbLoc = self.randomCellToQuery()
            lowestProb=1
            for cells in self.knownValues:
                if self.knownValues[cells]==False:
                    # only want to consider cells identified as safe with a clue
                    continue
                neighbors = LibraryFunctions.getValidNeighbors(self.dim,cells)
                numHidden=0
                numMines=0
                hiddenNeighbor=None
                for neighbor in neighbors:
                    if neighbor not in self.knownValues:
                        numHidden+=1
                        hiddenNeighbor=neighbor
                    elif self.knownValues[neighbor]==False:
                        # then this neighbor is a mine
                        numMines+=1
                if numHidden ==0:
                    continue
                givenProbability =(self.knownValues[cells][1] - numMines)/numHidden
                if ( givenProbability< lowestProb):
                    # then we choose a neighbor from here
                    lowestProbLoc=hiddenNeighbor
                    lowestProb=givenProbability
            # returning the next cell to query
            return lowestProbLoc

        # generates random cell to query
            #versus our improved above method (although I think that is still naive)
        def randomCellToQuery(self):
            # getting list of all vacant locations
            unknowns = []
            for i in range(self.dim):
                for j in range(self.dim):
                    if (i,j) not in self.knownValues:
                        unknowns.append((i,j))
            # now unknowns is a list of unknown locations (we just pick randomly from this list)
            pos = randint(0,len(unknowns)-1)
            return unknowns[pos]

        # idea here is to query the location that is involved in the most equations
            # the intuition is that querying this location will result in smaller equations sizes or lead to better information
        def equationCellToQuery(self):
            # finding the location with most appearances in our equations
            mostFound = None
            largest={}
            for equation in self.equations:
                if not mostFound:
                    for loc in equation[0]:
                        largest[loc]=0
                else:
                    for loc in equation[0]:
                        if loc in largest:
                            largest[loc]+=1
                        else:
                            largest[loc]=0
            # getting largest
            for location in largest:
                if mostFound is None:
                    mostFound=location
                else:
                    if largest[mostFound]<largest[location]:
                        mostFound=location
            if mostFound is None:
                # then we have no equations, we refer to probabililty query
                return self.probabilityCellToQuery()
            else:
                # then we found a place to query
                return mostFound

        # global selector
            # this takes into account global number of mines when selecting a mine to query
            # notice that the length of the deque returned
                # for confirmed safe values is greater than 1
                # but for guesses it is equal to 1
        def globalCellToQuery(self,numMinesRemaining,lastLocQueried):
            toQuery = deque()
            if numMinesRemaining==0:
                # then we can pick any spot as its safe
                toAdd = self.randomCellToQuery()
                return toQuery
            if lastLocQueried is None or self.knownValues[lastLocQueried] is False:
                res = self.probabilityCellToQuery()
                toQuery.append(res)
                return toQuery
            neighbors = LibraryFunctions.getValidNeighbors(self.dim,lastLocQueried)
            numSafeFound =0
            numMinesFound =0
            for neighbor in neighbors:
                if neighbor in self.knownValues:
                    if self.knownValues[neighbor]:
                        # then safe
                        numSafeFound+=1
                    else:
                        # then mine
                        numMinesFound+=1
            indicator = self.knownValues[lastLocQueried][1]-numMinesFound
            hiddenNeighbors = len(neighbors) - numSafeFound - numMinesFound
            if indicator == numMinesRemaining:
                # then we know everything else (not a neighbor) is a mine, so we can just query those first
                for i in range(0,self.dim):
                    for j in range(0,self.dim):
                        if (i, j) not in self.knownValues and (i, j) not in neighbors:
                            # then we can add this to a list to query
                            toQuery.append((i, j))
                if not toQuery:
                    # then there are no squares outside that are valid
                    toQuery.append(self.randomCellToQuery())
                return toQuery
            else:
                if hiddenNeighbors!=0:
                    if (((1.0)*indicator)/((1.0)*hiddenNeighbors)) <((1.0)*(numMinesRemaining-indicator))/((1.0)*(self.dim**2 - len(self.knownValues))):
                        # this means that the probability of finding a mine in neighbors is less than in board outside neighbors
                        for neighbor in neighbors:
                            if neighbor not in self.knownValues:
                                toQuery.append(neighbor)
                                break
                        if not toQuery:
                            toQuery.append(self.randomCellToQuery())
                        return toQuery
                    else:
                        # then we pick any spot outside neighbors
                        breakIndicator = False
                        for i in range(self.dim):
                            if breakIndicator:
                                break
                            for j in range(self.dim):
                                if (i, j) not in neighbors and (i, j) not in self.knownValues:
                                    toQuery.append((i, j))
                                    breakIndicator=True
                                    break
                        if not toQuery:
                            toQuery.append(self.randomCellToQuery())
                        return toQuery
                else:
                    # we refer to probability selector
                    res = self.probabilityCellToQuery()
                    toQuery.append(res)
                    return toQuery

        # method to support user entering clues and knowledge base adapting from there
            # clue is of the form (loc,numMines)
                # if numMines ==-1 , then the location user queried is a mine
        # return value is a deque of any solvable equations after this substitution
                # from these solvable equations, we can identify mines and free spaces
        # this will facilitate the loop after this step
        def feedFromUser(self,clue):
            # basically just updating what the user sent in
            numMinesClue = clue[1]
            loc = clue[0]
            if numMinesClue == -1:
                # then agent queried a mine
                # this is a mine
                self.knownValues[loc] = False
                # getting result of substitution
                toSolve = self.substitution((1,loc))
                return toSolve
            else:
                # this is safe, we can update our info and use the clue to generate an equation

                equationLHS = {}
                equationRHS=numMinesClue
                neighbors = LibraryFunctions.getValidNeighbors(self.dim,loc)
                numSafeSquares=0
                numMines=0

                for neighbor in neighbors:
                    if neighbor in self.knownValues:
                        if self.knownValues[neighbor]:
                            # this is safe
                            numSafeSquares+=1
                        else:
                            # this is a mine
                                # this decrements from the mine clue as well
                            numMines+=1
                            equationRHS-=1
                    else:
                        # then this is part of a generated equation with the clue
                            #with coefficient of 1
                        equationLHS[neighbor]=1
                # updating info about safe square
                self.knownValues[loc]=True,numMinesClue
                # this is a free square
                # updating info about the clue associated with query
                newEquation = equationLHS,equationRHS
                # plugging in newEquation and substitution
                toSolve = self.substitution((0,loc))
                otherSolvable = self.finalAddReduce(newEquation)
                for solvable in otherSolvable:
                    toSolve.append(solvable)
                return toSolve


        # debugging print that prints the knowledge base so far and the equations inside it
        def printKnowledgeBase(self):
            print("printing known values:")
            for value in self.knownValues:
                print("location:"+str(value)+" info : "+str(self.knownValues[value]))
            print("---------------")
            print("---------------")
            print("---------------")
            print("Printing equations:")
            for equation in self.equations:
                print(equation)
            print("ENDING PRINT")











