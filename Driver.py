# users can run our project from here
    # ask user for dimension of the board
    # ask user if they want to randomly generate or specify a txt file to include with a board
    # ask user if they want basic agent to solve it or improved agent
    #ask user if they just want to feed data into a knowledge base for help with their game

    #ask flow
        #first ask for feedData or not
            # if feed data, then ask for basic or advanced agent
        #if not feedData, then ask if user is giving txt file or not
            # if txtFile, then we can ask user for basic or advanced
            # if not txtFile, then we can ask user for dimension
from Board import Board
# then we can ask user for basic or advanced

# method to ask user for dimension of board
def askDimension():
    res=input("Please enter the dimension of the board you wish to use!")
    return int(res.strip())

# method to ask user for how many mines they want in the board
def askMines():
    res = input("Please enter the number of mines you want in the board")
    return int(res)

# method to ask generation or txt file
def askGeneration():
    res = input("Please enter 0 if you have a txt file ready for input. Otherwise enter 1 if you wish for us to generate the board for you!")
    return int(res)


# method to ask user for txt file for board or not
def askTXTFile():
    fileURL = input("Please enter the name (without .txt part) of the file with board configuration. \
                    Make sure that mines are labeled 1 and free spaces are not 1 (can be anything)")
    fileURL.strip()
    fileURL+=".txt"
    return fileURL

#method to ask user for basic agent or improved agent
def askBasicOrAdvanced():
    res = input("Enter 0 for using basic agent, enter 1 for using advanced agent")
    return int(res)

def askSelectionMethod():
    res = input("Enter 0 for random selection, 1 for probabilistic selection, 2 for equation driven selection,"+\
                "3 for global agent (knows the # of mines in advance)")
    return int(res)

#method to ask user for feeding data or not
def askFeedData():
    res = input("Enter 0 for if you wish to feed clues to a knowledge base (on your own game). Enter 1 if you have a board ready to input or want us to generate one for you!")
    return int(res)

def askPlayByPlay():
    res = input("Enter 0 if you want play-by-play status, or 1 if you only want the final result")
    return int(res)


dim = askDimension()
if askFeedData()==1:
    # then user has opted to feed clues to our knowledge base from their own game
    if askBasicOrAdvanced()==1:
        # user wants advanced
        # now we need to ask the user for a selection mechanism
        pass
    else:
        # user wants basic
        pass
else:
    # user wants to input a board or direct us to txt file for a board
    if askGeneration()==1:
        # user wants us to generate a board
        numMines = askMines()
        # generating the board
        ourBoard = Board(dim)
        # generating the mines
        ourBoard.generateBoard(numMines)
    else:
        # user has txt file ready for input
        txtFile = askTXTFile()
        # generating board
        ourBoard = Board(dim)
        # filling from txtfile
        ourBoard.getBoardFromFile(txtFile)
    # asking user for basic or advanced
    agentType = askBasicOrAdvanced()
    if agentType==0:
        # then basic
        pass
    else:
        # then advanced
        # need to ask about selection mechanism now
        pass