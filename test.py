from Board import Board
from improvedLogic.ImprovedKnowledgeBase import ImprovedKnowledgeBase
from improvedLogic import ImprovedAgent

dim =50
myBoard = Board(dim)
myBoard.generateBoard(875)
myKnowledge = ImprovedKnowledgeBase(dim)

# our test of improved agent
#ImprovedAgent.improvedSolveBoard(myBoard, myKnowledge, ImprovedKnowledgeBase.probabilityCellToQuery)
ImprovedAgent.globalSolveBoard(myBoard,myKnowledge)
for locs in myKnowledge.knownValues:
    if myKnowledge.knownValues[locs] is False:
        if locs not in myBoard.mines:
            print(locs)
