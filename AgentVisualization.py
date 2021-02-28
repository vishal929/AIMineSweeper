# this python file will handle GUI visualization from Agent's perspective
import tkinter
from Board import Board
import basicAgent
from basicKnowledgeBase import BasicKnowledgeBase


class resizableAgent(tkinter.tk):
    # agent has access to the board, but he doesnt access cells directly (he queries them from the board)
    def __init(self,dim):
        #cell sizes for canvas
        self.cellSize=30
        self.width = self.cellSize*len(self.maze)
        self.height = self.cellSize*len(self.maze)
        # dimension
        self.dim=dim
        # we have a board
        self.board=Board(dim)
        # we have a knowledge base
            #we will dynamically choose which knowledge base to use based on user's choice
            # for now this is just a basic knowledge base
        self.knowledgeBase=BasicKnowledgeBase(dim)
        # the "agent" is doing methods with our knowledge base
        #resizable canvas
        self.ourCanvas = ResizingCanvas(self,width=self.width,height=self.height,background="white")
        self.ourCanvas.bind()
        self.ourCanvas.pack(expand="yes")
        self.canvasLabels=[]
        #everything initialized as white at first
            # white--> unknown
            # blue--->safe
            # red ---> mine
        for i in range(dim):
            x=i*self.cellSize
            rects=[]
            for j in range(dim):
                y=j*self.cellSize
                rec=self.ourCanvas.create_rectangle(x,y,x+self.cellSize,y+self.cellSize,fill="white")
                rects.append(rec)
            self.canvasLabels.append(rects)
        # storing a canvas that the GUI will rewrite and update

    # updates given a set of mines
    def updateMines(self,mines):
        for mine in mines:
            self.ourCanvas.itemconfig(self.canvasLabels[mine[0]][mine[1]],fill="red")
    # updates given a set of safe squares
    def updateSafeSquares(self,safeSquares):
        for safes in safeSquares:
            self.ourCanvas.itemconfig(self.canvasLabels[safes[0]][safes[1]],fill="blue")
    def doStepBasicKnowledgeBase(self):
        # actually doing something and then reflecting changes by updateRepresentation
        results=basicAgent.basicSolveMinesStep(self.dim,self.knowledgeBase)
        self.updateMines(results[1])
        self.updateSafeSquares(results[2])
        if (results[0]):
            # gradual repetition
            self.after(1000,self.doStepBasicKnowledgeBase)

    def doBasicKnowledgeBaseGradual(self):
        # gradually calling step function
        self.doStepBasicKnowledgeBase()
        self.mainloop()

#resizing canvas code from
   # https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
class ResizingCanvas(tkinter.Canvas):
   def __init__(self, parent, **kwargs):
      tkinter.Canvas.__init__(self, parent, **kwargs)
      self.bind("<Configure>", self.on_resize)
      self.height = self.winfo_reqheight()
      self.width = self.winfo_reqwidth()

   def on_resize(self, event):
      # determine the ratio of old width/height to new width/height
      wscale = float(event.width) / self.width
      hscale = float(event.height) / self.height
      self.width = event.width
      self.height = event.height
      # resize the canvas
      self.config(width=self.width, height=self.height)
      # rescale all the objects tagged with the "all" tag
      self.scale("all", 0, 0, wscale, hscale)
