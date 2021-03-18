from Board import Board
from ImprovedKnowledgeBase import ImprovedKnowledgeBase
import ImprovedAgent

dim =30
myBoard = Board(dim)
myBoard.generateBoard(1)
myKnowledge = ImprovedKnowledgeBase(dim)

# our test of improved agent
#ImprovedAgent.improvedSolveBoard(myBoard,myKnowledge,ImprovedKnowledgeBase.probabilityCellToQuery)
ImprovedAgent.globalSolveBoard(myBoard,myKnowledge)
