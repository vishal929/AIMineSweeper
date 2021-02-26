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
    #changes is tuple (True/False, locList)
        #true for changing to mine, false for free square
        # locList is a list of locations to change
    def updateRepresentation(self,changes):
        # updates the color of our representation based on any changes made
        color=None
        if changes[0]:
            color="red"
        else:
            color="blue"
        for loc in changes[1]:
            self.ourCanvas.itemconfig(self.canvasLabels[loc[0]][loc[1]],fill=color)

    def doStepBasicKnowledgeBase(self):
        # actually doing something and then reflecting changes by updateRepresentation
        toContinue=basicAgent.basicSolveMinesStep(self.dim,self.knowledgeBase)
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
