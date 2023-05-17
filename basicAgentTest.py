from basicLogic import basicAgent
from Board import Board
from basicLogic.basicKnowledgeBase import BasicKnowledgeBase

dim =30
myBoard = Board(dim)
myBoard.generateBoard(270)
hi = BasicKnowledgeBase(dim)

basicAgent.basicSolveMines(myBoard, hi, True)
for locs in hi.knownMines:
    if locs not in myBoard.mines:
        print("BAD MINE: "+str(locs))