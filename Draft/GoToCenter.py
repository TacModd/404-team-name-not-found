#top search
# getWalls().width/2
# getWalls().height/2
# -1 if red
# offset
# xrange(1,y,1)
# xrange(y,maxheight,1)
# getDistance
# find Min Distance
# setmincenter
# __init__

#Top Agent Start Phase get next Move
def setCenter(self,gameState):
    #get center of map and maxHeight
    x = gameState.getWalls().width/2
    y = gameState.getWalls().height/2
    yMax = gameState.getWalls().height;

    #Shift center to home territory, with offset 1 away from wall
    offset = 1
    if self.red:
        x = x - (1+offset)
    else:
        x = x + offset

    #Find the closest position y-coordinate given the x-coordinate
    minYPosition = min([self.getMazeDistance(myPos,(x,y)) for y in xrange(y,yMax,1)])
    self.center = (x,y)

    #Bottom Agent Start Phase get next Move
def setCenter(self,gameState):
    #get center of map and maxHeight
    x = gameState.getWalls().width/2
    y = gameState.getWalls().height/2
    yMax = gameState.getWalls().height;

    #Shift center to home territory, with offset 1 away from wall
    offset = 1
    if self.red:
        x = x - (1+offset)
    else:
        x = x + offset
    #Find the closest position y-coordinate given the x-coordinate
    minYPosition = min([self.getMazeDistance(myPos,(x,y)) for y in xrange(1,y-1,1)])
    self.center = (x,y)

def chosoeAction:
    actions = gameState.getLegalActions(self.index)
    bestAction = min([self.getMazeDistance(myPos,self.getSuccessor(self, gameState, action)) for action in actions])
    return bestAction
