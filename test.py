from Board import Board
from ImprovedKnowledgeBase import ImprovedKnowledgeBase
import ImprovedAgent

dim =10
myBoard = Board(dim)
myBoard.generateBoard(20)
myKnowledge = ImprovedKnowledgeBase(dim)

# our test of improved agent
ImprovedAgent.improvedSolveBoard(myBoard,myKnowledge,ImprovedKnowledgeBase.randomCellToQuery)
