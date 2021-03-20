from Board import Board
from improvedLogic.ImprovedKnowledgeBase import ImprovedKnowledgeBase
from improvedLogic import ImprovedAgent

dim =40
myBoard = Board(dim)
myBoard.generateBoard(800)
myKnowledge = ImprovedKnowledgeBase(dim)

# our test of improved agent
ImprovedAgent.improvedSolveBoard(myBoard, myKnowledge, ImprovedKnowledgeBase.probabilityCellToQuery)
#ImprovedAgent.globalSolveBoard(myBoard,myKnowledge)
for locs in myKnowledge.knownValues:
    if myKnowledge.knownValues[locs] is False:
        if locs not in myBoard.mines:
            print(locs)
