# if we cannot update our knowledge base at some point
        # we proceed with trying to obtain contradictions at unknown points
from random import randint
from collections import deque

# rules
'''

    2)
    3) try the sum thing (if clue is 2, sum hidden neighbors set equal to 2)
        do 3 until we can conclude a cell is safe or mine, then try repeating 1 and 2
    4) if not, pick a hidden square that is a neighbor of a safe square
        try getting a contradiction from these
        if nothing, try a hidden neighbor of a mine square
        if nothing, then try and use probability to pick a hidden square to query
'''

# representation
import LibraryFunctions


class ImprovedKnowledgeBase():
        def __init__(self,dim):
            self.dim=dim
            # hash values for knownValues
            # mines (False)
            # safeSquares (True)
              # of mines given by clue, # safeSquares, # mines identified for sure around it
            self.knownValues={}
            # equations
            # each equation is (location is key, val is coefficient {},RHS value)
            self.equations=deque()

        #TODO:
            #we should only call reduce if we find equations with overlapping elements
            # probability
        # we have 3 big operations
            '''
                1) reduce
                2) substitute
                3) detect "solved" equations
                Now what order should we pick?
                - we need to substitute and may detect solved equations while querying
                - with a clue, we might need to reduce, which would lead to solved equations,-->substitution
                    -substitution itself might lead to a solved equation, which leads to more substitution
                -IDEA: 
                    -while reducing, we keep a list of detected "solved" equations
                    -at the end, we call doSolve on each of these equations
                    -then, doSolve will find the values for each variable, and call substitution on each variable
                        -the list of solved equations detected after substitution is returned to doSolve
                        -do solve disposes of the old list (to clear up useless equations)
                        -while the list is not empty, it calls itself with the new list
                Basically, the issue is not with reduce, but with the substitution -> solve ->substitution loop, 
                    and I think this above IDEA solves the issue'''

        #1) if clue -  # revealed mines = # hidden neighbors
                #then every hidden neighbor is a mine
        #  need to adapt this to knowledge base
            # specifically, after adding this piece of data, we need to start substitution loop
        # returns a list of mines found, list of safe squares found
        def basicAgentLogic(self,loc):
            # idea, just go through each free square and see if we can use basic logic to deduce stuff
            newMinesFound=deque()
            newSafesFound = deque()

            for square in self.knownValues:
                if self.knownValues[square]!=False:
                    # then this is a square that is free with some clue information
                    clue = self.knownValues[square][1]
                    numMines = self.knownValues[square][3]
                    numSafe = self.knownValues[square][2]
                    neighbors=LibraryFunctions.getValidNeighbors(self.dim,square)
                    if clue==len(neighbors)-numSafe:
                        # then every hidden neighbor is a mine
                        for neighbor in neighbors:
                            if neighbor not in self.knownValues:
                                # then this should be marked as a mine
                                newMinesFound.append(neighbor)
                                self.knownValues[neighbor] = False
                                # need to update values of all neighbors
                                deeperNeighbors = LibraryFunctions.getValidNeighbors(self.dim, neighbor)
                                for space in deeperNeighbors:
                                    if space in self.knownValues and self.knownValues[space] != False:
                                        # neighbor is a free space with info
                                        # updating number of known mines
                                        self.knownValues[neighbors][3] += 1
                    elif clue == numMines:
                        # every other hidden neighbor is safe
                        for neighbor in neighbors:
                            if neighbor not in self.knownValues:
                                # then this should be marked as safe and should be setup for query
                                newSafesFound.append(neighbor)
                                self.knownValues[neighbor] = True
                                # need to update values of all neighbors
                                deeperNeighbors = LibraryFunctions.getValidNeighbors(self.dim, neighbor)
                                for space in deeperNeighbors:
                                    if space in self.knownValues and self.knownValues[space] != False:
                                        # neighbor is a free space with info
                                        # updating number of safeSpaces
                                        self.knownValues[neighbors][2] += 1
            # now we need to do some operations with the new mines found and the new safe squares found
            # returning the new mines found and the new safe squares found
            return newMinesFound,newSafesFound

        # THIS METHOD ASSUMES THERE IS A VALID CANCELLATION POSSIBLE
        # idea, we can just throw out the longer equation from the results
        def reductionEquation(self,firstEquation,secondEquation):
            # subtract smaller RHS value equation from larger one
            larger=None
            smaller=None
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
            newRHS=larger[1]
            # updating based on negative values of smaller equation
            for val in smaller[0]:
                if val in newEquationDict:
                    newEquationDict[val]=newEquationDict[val]-smaller[0][val]
                    if newEquationDict[val]==0:
                        # we need to remove this
                        del newEquationDict[val]
                else:
                    newEquationDict[val]= -smaller[0][val]
            newRHS -= smaller[1]
            # need to convert to frozen set for actual use
            return newEquationDict,newRHS

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
            if newDiscovery[1] in self.knownValues:
                # then we do not substitute
                return solvedList
            for equation in self.equations:
                if newDiscovery[1] in equation[0]:
                    lhs = equation[0]
                    rhs = equation[1]
                    # modification is the new value on LHS based on discovered value of this entry
                    # getting coefficient
                    #modification = equation[0][newDiscovery[1]]
                    modification = lhs[newDiscovery[1]]
                    # multiplying coefficient with known value
                    modification*=newDiscovery[0]
                    # subtracting from rhs
                    #equation[1]-=modification
                    rhs-=modification
                    # removing variable from our equation after substitution
                    #equation[0].pop(newDiscovery[1])
                    del lhs[newDiscovery[1]]
                    reducedEquation = (lhs,rhs)
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
                # if the equation is now in solvable state after substitution, then we can update it and remove
                #if self.canBeSolved(equation):
                    #removedList.append(equation)
            # removing it from our actual knowledge base
            for equation in removedList:
                self.equations.remove(equation)
            for equation in reducedList:
                # adding in reduced equations that arent solvable
                self.equations.append(equation)
            return solvedList

        # solves an equation detected by isSolvable method
            # returns the values found in the form:
            # returns a list of mines and a list of free spots found
        def solvedEquationSolver(self,equation):

            # solved variables are any variables solved of the form (1/0, loc) where 1 is a mine, 0 safe
            foundMines=deque()
            foundSafes=deque()
            for ourVar in equation[0]:
                # logic for if rhs is zero and all coefficients are same sign (all are free)
                if equation[1] == 0:
                    # then this is safe
                    # updating neighbors
                    neighbors = LibraryFunctions.getValidNeighbors(self.dim, ourVar)
                    for neighbor in neighbors:
                        if neighbor in self.knownValues and self.knownValues[neighbor] != False:
                            # neighbor is a free space with info
                            # updating number of known mines
                            #self.knownValues[neighbor][2] += 1
                            self.knownValues[neighbor] = \
                                self.knownValues[neighbor][0], self.knownValues[neighbor][1], \
                                self.knownValues[neighbor][2] +1, self.knownValues[neighbor][3]
                    # we can query this and add to knowledge base
                    # toQuery.push(ourVar)
                    # solvedVariables.push((0,ourVar))
                    foundSafes.append(ourVar)
                    continue
                # logic for if all positive terms on lhs equals rhs (positive terms are mines), everything else is free
                if equation[0][ourVar] > 0:
                    # this is a mine
                    self.knownValues[ourVar]=False
                    # need to update values of all neighbors
                    neighbors = LibraryFunctions.getValidNeighbors(self.dim,ourVar)
                    for neighbor in neighbors:
                        if neighbor in self.knownValues and self.knownValues[neighbor]!=False:
                            # neighbor is a free space with info
                            # updating number of known mines
                            #self.knownValues[neighbors][3]+=1
                            self.knownValues[neighbor] = \
                                self.knownValues[neighbor][0], self.knownValues[neighbor][1], \
                                self.knownValues[neighbor][2], self.knownValues[neighbor][3]+1

                    #solvedVariables.push((1,ourVar))
                    foundMines.append(ourVar)
                else:
                    # then this is safe
                    # updating neighbors
                    neighbors = LibraryFunctions.getValidNeighbors(self.dim, ourVar)
                    for neighbor in neighbors:
                        if neighbor in self.knownValues and self.knownValues[neighbor] != False:
                            # neighbor is a free space with info
                            # updating number of known mines
                            #self.knownValues[neighbors][2] += 1
                            self.knownValues[neighbor] = \
                                self.knownValues[neighbor][0], self.knownValues[neighbor][1], \
                                self.knownValues[neighbor][2] + 1, self.knownValues[neighbor][3]
                    # we can query this and add to knowledge base
                    #toQuery.push(ourVar)
                    #solvedVariables.push((0,ourVar))
                    foundSafes.append(ourVar)
                # removing the equation from our equation set, as we extracted all info
                #self.equations.remove(equation)

            # now toQuery is a list of locations to query that are safe
            # toRemove is a list of equations to solve and then remove
                #the equations in toSolve were already removed by substitution()
                    # we just need to solve them

            # we start with the query, then we solve again with the new list

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
            numMinesClue = Board.queryPosition(loc)
            if numMinesClue == -1:
                # then agent queried a mine
                # this is a mine
                self.knownValues[loc] = False
                # need to update values of all neighbors
                neighbors = LibraryFunctions.getValidNeighbors(self.dim,loc)
                for neighbor in neighbors:
                    if neighbor in self.knownValues and self.knownValues[neighbor] != False:
                        # neighbor is a free space with info
                        # updating number of known mines
                        #self.knownValues[neighbors][3] += 1
                        self.knownValues[neighbor] = \
                            self.knownValues[neighbor][0], self.knownValues[neighbor][1], self.knownValues[neighbor][2], self.knownValues[neighbor][3]+1

                return loc, None
            else:
                # this is safe, we can update our info and use the clue to generate an equation
                #representation is F/T mine or not, #safeSquares around, # mines around for sure

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
                self.knownValues[loc]=True,numMinesClue,numSafeSquares,numMines
                # this is a free square
                # need to update values of all neighbors
                neighbors = LibraryFunctions.getValidNeighbors(self.dim, loc)
                for neighbor in neighbors:
                    if neighbor in self.knownValues and self.knownValues[neighbor] != False:
                        # neighbor is a free space with info
                        # updating number of known mines
                        #self.knownValues[neighbor][2] += 1
                        self.knownValues[neighbor] = \
                            self.knownValues[neighbor][0],self.knownValues[neighbor][1],self.knownValues[neighbor][2]+1,self.knownValues[neighbor][3]
                # updating info about the clue associated with query
                newEquation = equationLHS,equationRHS
                #self.equations.add(newEquation)
                return loc, newEquation



        # compares given equation with every other equation in the knowledge base to try and reduce
            # reduces whatever it can
            # removes the old equations from knowledge base after reduction (redundant)
            # adds itself
            # returns a list of all equations that are solvable at the end
                # NEED TO ACCOUNT FOR SPECIAL CASE:
                    # if the equation given is solvable, we can just return it
                    # this is because solvable equations will be substituted back into knowledge base anyway
        def checkReduce(self,equation):

            equationsToRemove=deque()
            equationsToAdd=deque()
            equationsToSolve=deque()
            # checking if the equation is empty, if so, we can return nothing
            if not equation[0]:
                # then the dictionary of coefficients is emtpy, which means nothing
                return equationsToSolve
            # if the equation generated from the clue can be immediately solved, then we can just return it instead of
                # going through every equation in the equation base and comparing them
            if self.canBeSolved(equation):
                #print(equation)
                equationsToSolve.append(equation)
                return equationsToSolve
            for otherEquation in self.equations:
                canSubtract=False
                for var in equation[0]:
                    if var in otherEquation[0]:
                        # then we can subtract
                        canSubtract=True
                        break
                #subtracting from other equation
                if canSubtract:
                    newEquation = self.reductionEquation(otherEquation,equation)
                    equationsToRemove.append(otherEquation)
                    # checking if the new equation can be solved
                    if self.canBeSolved(newEquation):
                        # this is solved we dont need to add it to our knowledge base
                            # but we need to add it to a solved list
                        equationsToSolve.append(newEquation)
                    else:
                        equationsToAdd.append(newEquation)
            # adding reduction equation itself to the knowledgeBase
            equationsToAdd.append(equation)
            # removing all the old equations
            for equations in equationsToRemove:
                self.equations.remove(equations)
            # adding all the new equations that arent solvable
            for equations in equationsToAdd:
                self.equations.append(equations)
            # returning list of solvable equations for agent to handle in outer level
            return equationsToSolve



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
            #print("checking if equation can be solved: "+str(equation))
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
                # if rhs is 0 and every lhs term is positive, then every term in the equation represents a free square
                return True
            else:
                return False

        # deciding which cell to query if we cannot proceed with reduction/substitution
            # returns the cell to query
            # idea, all possibly known safe cells have already been queried
                # so we need to find a cell with low probability of being a mine
                # naive idea: go through each cell that has been identified as free
                    # go through each hidden neighbor
                    # pick any hidden neighbor from cell with lowest (CLUE-minesIdentified)/numHiddenNeighbors
        def probabilityCellToQuery(self):
            #initial value to test is the middle of the board (in case our base is empty)
            lowestProbLoc = (self.dim/2,self.dim/2)
            lowestProb=1
            for cells in self.knownValues:
                neighbors = LibraryFunctions.getValidNeighbors(self.dim,cells)
                numHidden=0
                numMines=0
                hiddenNeighbor=None
                for neighbor in neighbors:
                    if neighbor not in self.knownValues:
                        numHidden+=1
                        hiddenNeighbor=neighbor
                    elif self.knownValues[neighbor][0]==True:
                        # then this neighbor is a mine
                        numMines+=1
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

            loc = (randint(0,self.dim),randint(0,self.dim))
            # generating a location that is not known in our knowledge base
            while (loc in self.knownValues):
                loc=(randint(0,self.dim),randint(0,self.dim))
            return loc

        # method to support user entering clues and knowledge base adapting from there
            # clue is of the form (loc,numMines)
                # if numMines ==-1 , then the location user queried is a mine
        # return value is of the form loc,equation
            # if user gave a mine, equation is None
        # this will facilitate the loop after this step
        def feedFromUser(self,clue):
            # basically just updating what the user sent in
            if clue[1]==-1:
                # user queried a mine
                self.knownValues[clue[0]]=False
                # updating neighbors
                neighbors = LibraryFunctions.getValidNeighbors(self.dim,clue[0])
                for neighbor in neighbors:
                    if neighbor in self.knownValues:
                        # updating results in neighbor
                        self.knownValues[neighbor][3]+=1
                return clue[0],None
            else:
                # user queried a free space
                # updating neighbors
                newEquationDict={}
                neighbors = LibraryFunctions.getValidNeighbors(self.dim, clue[0])
                numMines=0
                numSafe=0
                for neighbor in neighbors:
                    if neighbor in self.knownValues:
                        # updating results in neighbor
                        if self.knownValues[neighbor]!=False:
                            #updating safe square count around safe squares
                            newEquationDict[0][neighbor]=1
                            numSafe+=1
                            self.knownValues[neighbor][2] += 1
                        else:
                            # this neighbor is a mine
                            newEquationDict[0][neighbor]=1
                            numMines+=1
                self.knownValues[clue[0]]=True,clue[1],numSafe,numMines
                # creating equation for user
                    #lhs are the locations and coefficients in dictionary
                    #rhs is the clue value
                newEquation = newEquationDict,clue[1]
                return clue[0],newEquation

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











