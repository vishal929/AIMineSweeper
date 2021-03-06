# if we cannot update our knowledge base at some point
        # we proceed with trying to obtain contradictions at unknown points



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
            # mines (True)
            # safeSquares (False)
              # of mines given by clue, # safeSquares, # mines identified for sure around it
            self.knownValues={}
            # equations
            # each equation is (location is key, val is coefficient {},RHS value)
            self.equations=set()

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
        def allMinesNearby(loc, self):
            added = False
            newMines = []
            if (self.safeSquares[loc])[0] - (self.safeSquares[loc])[2] == (self.safeSquares[loc])[3]:
                neighbors = LibraryFunctions.getValidNeighbors(loc)
                for neighbor in neighbors:
                    if neighbor not in self.safeSquares:
                        self.knownMines.add(neighbor)
                        newMines.append(neighbor)
                        added = True
            return added, newMines

        #if number of safe neighbors (8-clue) - number of revealed safe =  # hidden neighbors
            #then every hidden neighbor is safe
        # need to adapt this to knowledge base
        def allSafeNearby(loc, self, Board):
            added = False
            newSafe = []
            if 8 - (self.safeSquares[loc])[0] - (self.safeSquares[loc])[1] == (self.safeSquares[loc])[3]:
                neighbors = LibraryFunctions.getValidNeighbors(loc)
                for neighbor in neighbors:
                    if neighbor not in self.knownMines:
                        numMinesClue = self.queryCellFromBoard(neighbor, Board)
                        locData = self.getDataHelper(neighbor, numMinesClue)
                        self.safeSquares[neighbor] = locData
                        added = True
                        newSafe.append(neighbor)
            return added, newSafe

        #idea as we add equations, we can compare them against the rest to see if reduction is possible
        # if reduction is possible, we keep the smaller one along with the smaller result
        def addEquation(self,equation):
            # do reduction against every possibility in knowledge base
            pass

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
            newRHS=0
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
                else:
                    newEquationDict[val]=smaller[0][val]
            newRHS -= smaller[1]
            return newEquationDict,newRHS

        # newDiscovery is a tuple (1/0, loc)
            # 1/0 indicates if mine or not
            # location is the (row,col) of discovered info about entry
        def substitution(self,newDiscovery):
            # removing any solved equations
            removedList = dequeue()
            for equation in self.equations:
                if newDiscovery[1] in equation[0]:
                    # modification is the new value on LHS based on discovered value of this entry
                    # getting coefficient
                    modification = equation[0][newDiscovery[1]]
                    # multiplying coefficient with known value
                    modification*=newDiscovery[0]
                    # subtracting from rhs
                    equation[1]-=modification
                    # removing variable from our equation after substitution
                    equation[0].pop(newDiscovery[1])
                # if the equation is now in solvable state after substitution, then we can update it and remove
                if self.canBeSolved(equation):
                    removedList.push(equation)
                    # removing it from our actual knowledge base
                    self.equations.remove(equation)
                return removedList



        # simple helper to detect a solved equation (i.e of the form A=0, B=1)
            #also need to consider cases like A+B=2, A-B=1 etc.
            # if A+B=2, then A and B are both mines
            # if A-B=1, then we know for sure that A is a mine and B is safe
                # in general, if # of positive coefficients equals RHS, then every positive var is a mine
                    # it follows everything else is a safe square
        # returns true if equation is solved
        def solvedEquationDetector(self,equation):
            #getting sum of all positive coefficients on the lhs of equation

            '''
            lhsSum=0
            for vars in equation[0]:
                if equation[0][vars]>0:
                    lhsSum += equation[0][vars]
            if (equation[0].size()==1):
                #return True
                key =self.solvedEquationScalar(equation);
                solvedInfo = (equation[1],key)
                # removing equation from considered equations (we are separating equations from known squares)
                #self.equations.remove(equation)
                # based on if this is a mine or safe square we do different things
                    # if mine
                        # do not query, we put immediately into known mines
                    # if not mine (safe square)
                        # we query the board for this, compile clues/other info and then update our known info
                if solvedInfo[0]==1:
                    # this is a mine
                    self.knownValues[key]=False
                    solvedVariables.push((1,key))
                else:
                    # safe square
                        # we can query and get other info and add it to known values
                    solvedVariables.push((0,key))
                    pass
            elif equation[0].size()==lhsSum and lhsSum==equation[1]:
            '''
                # then we know that every positive variable is a mine
                    # follows that every other variable is safe
            toQuery=dequeue()
            # solved variables are any variables solved of the form (1/0, loc) where 1 is a mine, 0 safe
            solvedVariables = dequeue()
            for vars in equation[0]:
                if equation[0][vars]>0:
                    # this is a mine
                    self.knownValues[vars]=False
                    solvedVariables.push((1,vars))
                else:
                    # then this is safe
                    # we can query this and add to knowledge base
                    toQuery.push(vars)
                    solvedVariables.push((0,vars))
                # removing the equation from our equation set, as we extracted all info
                #self.equations.remove(equation)

            if solvedVariables :
                # we found some new discoveries
                # we can substitute that in our knowledge base
                toSolve=dequeue()
                for solved in solvedVariables:
                    toSolve+= self.substitution(solved)
                #now toRemove is a list of all equations to solve and then remove
                #return toRemove
            # now toQuery is a list of locations to query that are safe
            # toRemove is a list of equations to solve and then remove
                #the equations in toSolve were already removed by substitution()
                    # we just need to solve them

            # we start with the query, then we solve again with the new list
            for queriesToDo in toQuery:
                self.queryCellFromBoard(queriesToDo,Board)
            for equations in toSolve:
                self.solvedEquationDetector(equations)




        # simple helper to scale a solved equation to final value (i.e -A=-1, 2A=2,etc.)
        def solvedEquationScalar(self,equation):
            for key in equation[0]:
                if equation[0][key]!=1:
                    equation[1]/=equation[0][key]
                    equation[0][key]=1
                    return key

        # helper to query cell from board and update our info about known squares
        def queryCellFromBoard(self, loc,Board):
            numMinesClue = Board.queryPosition(loc)
            if numMinesClue == -1:
                # then agent queried a mine
                self.knownValues[loc]=False
                # substitution now that we know this is a mine
                toSolve=self.substitution((1,loc))
                # toSolve is a list of solvable equations obtained after substitution
                    # they are already removed from our knowledge base, we just need to extract the data
                        #i.e we start a solve->substitution loop
                for solved in toSolve:
                    self.solvedEquationDetector(solved)
                return True, loc
            else:
                # this is safe, we can update our info and use the clue to generate an equation
                #representation is F/T mine or not, #safeSquares around, # mines around for sure

                equationLHS = {}
                equationRHS=numMinesClue
                neighbors = LibraryFunctions.getValidNeighbors(loc,self.dim)
                numSafeSquares=0
                numMines=0
                for neighbor in neighbors:
                    if neighbor in self.knownValues:
                        if self.knownValues[neighbor]:
                            # this is safe
                            numSafeSquares+=1
                        else:
                            # this is a mine
                            numMines+=1
                    else:
                        # then this is part of a generated equation with the clue
                            #with coefficient of 1
                        equationLHS[neighbor]=1
                # updating info about safe square
                self.knownValues[loc]=True,numSafeSquares,numMines
                # updating info about the clue associated with query
                newEquation = (equationLHS,equationRHS)
                self.equations.add(newEquation)
                # substitution now that we know this is a safe square
                toSolve = self.substitution((0, loc))
                # toSolve is a list of solved equations obtained after substitution
                # we will initiate the solve process here before going into a reduce->solve->substitute loop below with the clue
                for solved in toSolve:
                    self.solvedEquationDetector(solved)
                #checking if we can reduce anything in our knowledge base
                self.checkReduce(newEquation)
                return False, loc
        # compares given equation with every other equation in the knowledge base to try and reduce
        def checkReduce(self,equation):
            canSubtract=False
            equationsToRemove=dequeue()
            equationsToAdd=dequeue()
            equationsToSolve=dequeue()
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
                    equationsToRemove.push(otherEquation)
                    # checking if the new equation can be solved
                    if self.canBeSolved(newEquation):
                        # this is solved we dont need to add it to our knowledge base
                            # but we need to add it to a solved list
                        equationsToSolve.push(newEquation)
                    else:
                        equationsToAdd.push(newEquation)
            # initiating solve loop
                #solve will substitute values and remove associated equations from our knowledge base
            #ORDER MATTERS!!!!
                # we are first removing redundant equations before possibly going into a solve->reduce loop
                # we will add the newer equations before going into a solve->reduce loop
                # then, we will initiate the solve->reduce loop, which will remove solved equations in substitution()
            for redundantEquations in equationsToRemove:
                self.equations.remove(redundantEquations)
            for newerEquation in equationsToAdd:
                self.equations.add(newerEquation)
            for equations in equationsToSolve:
                self.solvedEquationDetector(equations)


        # returns True if equations is in solvable form, false otherwise
        def canBeSolved(self,equation):
            lhsSum = 0
            for vars in equation[0]:
                if equation[0][vars] > 0:
                    lhsSum += equation[0][vars]
            # if lhsSum == equation[1] (rhs), then this is solvable
            if lhsSum==equation[1]:
                return True
            else:
                return False



