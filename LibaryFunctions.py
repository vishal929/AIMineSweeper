# file has common functions that we might need across modules


def getValidNeighbors(dim, loc):
    # returns every possible neighbor
    # STILL NEED TO CHECK IF NEIGHBOR IS VALID!!!
    neighbors = [(loc[0], loc[1] + 1), (loc[0], loc[1] - 1), (loc[0] - 1, loc[1]), (loc[0] + 1, loc[1]),
                 (loc[0] + 1, loc[1] + 1), (loc[0] + 1, loc[1] - 1), (loc[0] - 1, loc[1] - 1),
                 (loc[0] - 1, loc[1] + 1)]
    finalNeighbors = []
    for neighbor in neighbors:
        if neighbor[0]<dim and neighbor[0]>=0 and neighbor[1]<dim and neighbor[1]>=0:
            finalNeighbors.append(neighbor)
    return finalNeighbors