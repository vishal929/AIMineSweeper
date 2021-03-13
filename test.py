from Board import Board
from ImprovedKnowledgeBase import ImprovedKnowledgeBase
import ImprovedAgent

dim =5
myBoard = Board(5)
myBoard.generateBoard(8)
myKnowledge = ImprovedKnowledgeBase(5)

# our test of improved agent
ImprovedAgent.improvedSolveBoard(myBoard,myKnowledge,ImprovedKnowledgeBase.randomCellToQuery)
