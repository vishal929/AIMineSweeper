from Board import Board
from ImprovedKnowledgeBase import ImprovedKnowledgeBase
import ImprovedAgent

dim =50
myBoard = Board(dim)
myBoard.generateBoard(1400)
myKnowledge = ImprovedKnowledgeBase(dim)

# our test of improved agent
ImprovedAgent.improvedSolveBoard(myBoard,myKnowledge,ImprovedKnowledgeBase.probabilityCellToQuery)
