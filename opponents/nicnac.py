# https://github.com/Tape09/pacmanCTF/blob/0302cedc95793da651ec8cbfb1f224297db283df/NicNacPacWack.py
# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import manhattanDistance
import math
import random, util
from game import Agent
from copy import copy, deepcopy
from capture import SONAR_NOISE_RANGE, SONAR_NOISE_VALUES, SIGHT_RANGE, COLLISION_TOLERANCE, MIN_FOOD


#################
# Team creation #
#################

def av(vals):
    average = 0.0
    n = 0.0
    for v in vals:
        n+=1
        average+=v
    average += min(vals)
    n+=1
    return average/n

#def setGlobalVariables(agentIndex)
#    agentValue[agentIndex] = agentIndex
SONAR_MAX = (SONAR_NOISE_RANGE - 1)/2

class enemyAgent(object):
    def __init__(self):
        self.id = 0
        self.startPos = []
        self.grid = []
        self.touchingAgent = [False, False]

    def setEnemyId(self, val):
        self.id = val

    def getEnemyId(self):
        return self.id

    def setGridSize(self, val):
        self.grid = [[0 for i in range(val[1])] for j in range(val[0])]
        #print "val: {}".format(val)

    def setGhostStart(self):
        self.grid = [[0 for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
        self.grid[self.startPos[0]][self.startPos[1]] = 1
        self.touchingAgent = [False, False]

    def setTouchingAgent(self, agent):
        self.touchingAgent[agent] = True

    def notTouchingAgent(self, agent):
        self.touchingAgent[agent] = False


    def updateGridMeasurment(self, selfcopy, gameState, measurement):

        Pos = gameState.getAgentState(selfcopy.index).getPosition()
        #print "gridmeasx: {}".format(len(self.grid[0]))
        #print "gridmeasy: {}".format(len(self.grid))
        #print "Pos: {}".format(Pos)
        #print "measurement: {}".format(measurement)       

        for x in range(0,len(self.grid)):
            #util.pause()
            for y in range(0,len(self.grid[0])):
                #print "x: {}, y: {}".format(x, y)
                #print "ghost: {}, location: [{},{}], value: {}".format(self.id, x, y, self.grid[y][x])
                if self.grid[x][y] > 0:
                    #selfcopy.debugDraw((x, y), [self.grid[x][y],0,self.grid[x][y]],False)
                    #print "distance: {}".format(util.manhattanDistance(Pos, (x,y)))
                    dist = util.manhattanDistance(Pos, (x,y))
                    if abs(dist - measurement) >= SONAR_MAX+2: #+2 is magic
                        self.grid[x][y] = 0
                        #selfcopy.debugDraw((x, y), [0,0,0],False)
                        #if selfcopy.playerId == 0:
                            #print "enemy: {}, distance: {}, measurement: {}".format(self.id, dist, measurement)
                    #print "distance: {}".format(selfcopy.distancer.getDistance(Pos, (x,y)))
                    #print "distance: {}".format(selfcopy.distancer.getDistanceOnGrid(Pos, (x,y)))
                    #print "distance: {}".format(selfcopy.getMazeDistance(Pos, (x,y)))
        #util.pause()



    def updateGridMotion(self, selfcopy, gameState):
        #print "x: {}".format(len(self.grid))
        #print "y: {}".format(len(self.grid[0]))
        prevgrid = deepcopy(self.grid)

        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        walls = gameState.getWalls()
        #print walls
        #print "type: {}".format(getattr(walls))
        
        minimum = 9001
        for row in self.grid:
            for i in range(0,len(self.grid[0])):
                if row[i] > 0 and row[i] < minimum:
                    minimum = row[i]
        #print minimum

        for x in range(0,len(self.grid)):
            #util.pause()
            for y in range(0,len(self.grid[0])):
                #print "x: {}, y: {}".format(x, y)
                #print "ghost: {}, location: [{},{}], value: {}".format(self.id, x, y, self.grid[x][y])
                if prevgrid[x][y] > 0:
                    for i in range(0,4):
                        #if x+dx[i] >= len(self.grid) or x+dx[i] < 0 or y+dy[i] >= len(self.grid[0]) or y+dy[i] < 0:
                        if not walls.data[x+dx[i]][y+dy[i]]:
                            try:
                                #if not self.grid[x+dx[i]][y+dy[i]] > 0.75:
                                self.grid[x+dx[i]][y+dy[i]] = minimum
                            except Exception:
                                raise
                                util.pause()
                        else:
                            #print "wall: {}, location: [{},{}], value: {}".format(self.id, x, y, self.grid[x][y])
                            #selfcopy.debugDraw((x+dx[i], y+dy[i]), [1,0,0],False)   
                            continue
        totalsum = 0
        for row in self.grid:
            totalsum += sum(row)
        #print "chugalug"
        #print totalsum
        for row in self.grid:
            if sum(row) > 0:
                row = [float(i)/totalsum for i in row]

    def exactPosition(self, measurement):
        self.grid = [[0 for i in range(len(self.grid[0]))] for j in range(len(self.grid))]
        self.grid[int(measurement[0])][int(measurement[1])] = 1

    def notInSight(self, posi):
        #print "Agent: {}, pos {}".format(selfcopy.index, pos)
        pos = (posi[1],posi[0])
        for i in range(0, SONAR_MAX):
            for j in range(0, SONAR_MAX):
                if i+j < SONAR_MAX:
                    x = int(i)
                    y = int(j)
                    #print "Agent: {}, pos {}, i: {}, j: {}".format(selfcopy.index, pos, i ,j)
                    if i+pos[0] < len(self.grid) and pos[1]+j < len(self.grid[0]):
                        self.grid[int(pos[0]+i)][int(pos[1]+j)] = 0
                    if pos[0]-i <= 0 and pos[1]+j < len(self.grid[0]):
                        self.grid[int(pos[0]-i)][int(pos[1]+j)] = 0
                    if pos[0]-i >= 0 and j-pos[1] >= 0:
                        self.grid[int(pos[0]-i)][int(pos[1]-j)] = 0
                    if pos[0]+i < len(self.grid) and j-pos[1] >= 0:                        
                        self.grid[int(pos[0]+i)][int(pos[1]-j)] = 0


    def drawGrid(self, selfcopy):
        for x in range(0,len(self.grid)):
            #util.pause()
            for y in range(0,len(self.grid[0])):
                #print "x: {}, y: {}".format(x, y)
                #print "ghost: {}, location: [{},{}], value: {}".format(self.id, x, y, self.grid[y][x])
                if self.grid[x][y] > 0:
                    selfcopy.debugDraw((x, y), [1,0,1],False)
        #print self.grid


# A shared memory class, containing a counter and a increment function. 
# This might get weird if you play the same team vs itself. If you want to do that just copy this file and play myteam vs myteamcopy.
class SharedMemory(CaptureAgent):
    # this is the constructor for the class. It gets called wehn you create an instance of the class. Inits counter to 0.
    def __init__(self):
        self.treeAction = [0, 0];
        
        self.enemy = []

        self.enemy.append(enemyAgent())
        self.enemy.append(enemyAgent())

        #print layout.getLayout( options.layout )
        #print self.enemy
        #util.pause()
        
    # returns the state of each pacman
    def setTreeAction(self, agent, act):
        self.treeAction[agent] = act

    def getTreeAction(self, agent):
        return self.treeAction[agent]

    def getEnemy(self, val):
        return enemy[val]
        
# create instance of the class. The "whatever" variable is in the global scope, so it can be accessed from your agents chooseAction function.
sharemem = SharedMemory();


#########################################################################################################################
###########################################  Our Team  ##################################################################
#########################################################################################################################



def createTeam(firstIndex, secondIndex, isRed,
    first = 'FrenchCanadianAgent', second = 'FrenchCanadianAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.
  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]


##########
# Agents #
##########

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.
    
    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()


class MultiAgentSearchAgent(CaptureAgent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.
    
    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.
    
    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.  
    """

    
    def registerInitialState(self, gameState):
        CaptureAgent.registerInitialState(self, gameState)
        self.depth = 2
        self.safe = self.safetyPlaces(gameState)

        for agent in self.getTeam(gameState):
            # Add opponents to list of enemies
            if not agent == self.index:
                agentId = agent

        #I don't know why I have this, but it's a thing. We have ally1 and ally2
        if self.index < agentId:
            self.playerId = 0
        else:
            self.playerId = 1

        #sets enemyID in sharemem
        i = 0
        for agent in self.getOpponents(gameState):
            sharemem.enemy[i].setEnemyId(agent)
            i += 1
        #print "sharemem = {}" .format(sharemem.enemy[0].id)
        #print "sharemem = {}" .format(sharemem.enemy[1].id)

        #finds Start Position in sharemem
        temp = []
        for emory in sharemem.enemy:
            #emory.startPos = gameState.getAgentState(emory.id).getPosition()
            emory.startPos = gameState.getInitialAgentPosition(emory.id)
            #print "startpos for agent {} = {}" .format(emory.id,emory.startPos)
            #self.debugDraw([emory.startPos], [0,1,0],False)
        
        #finds the Size of the group, depending if we're red or not (probably a terrible method, but it works)
        gridSize = []

        walls = gameState.getWalls()
        gridSize = [len(walls.data), len(walls.data[0])]
        #print gridSize       
        sharemem.enemy[0].setGridSize(gridSize)
        sharemem.enemy[1].setGridSize(gridSize)
        sharemem.enemy[0].setGhostStart()
        sharemem.enemy[1].setGhostStart()
        sharemem.enemy[0].updateGridMotion(self, gameState) 
        sharemem.enemy[1].updateGridMotion(self, gameState) 
        
        


    def safetyPlaces(self,gameState):
        safetyCoordinates = []
        x = gameState.data.layout.width/2
        ymax = gameState.data.layout.height
        if(self.red):
            x-=1
        for y in range(1,ymax-1):
            if(not gameState.hasWall(x,y)):
                safetyCoordinates.append((x,y))
                #self.debugDraw([[x,y]], [0,0,1])
        return safetyCoordinates
            
    def distanceToCamp(self,gameState):
        dmin = 999
        Pos = gameState.getAgentState(self.index).getPosition()
        goto = Pos
        for x in self.safe:
            if(self.getMazeDistance(Pos, x)<dmin):
                dmin=self.getMazeDistance(Pos, x)
                goto=x
        #self.debugDraw([goto], [0,1,0],True)
        return dmin
    
    def appxEnemyPos(self, gameState, a):
        if(a==None):
            ghostPositions = map(lambda g: g.getPosition(), ghostStates)
        return 0;

    def _getGhostScore(self, gameState):
        
        enemies = []
        for agent in self.getOpponents(gameState):
            enemies.append(gameState.getAgentState(agent))

        ghostStates = []
        for enemy in enemies:
            if not enemy.isPacman and enemy.getPosition() != None:
                ghostStates.append(enemy)

        ghostPositions = map(lambda g: g.getPosition(), ghostStates)
        if(len(ghostPositions)>0):
            distanceToClosestGhost = min(map(lambda x: self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), x), 
                                         ghostPositions))
        else:
            distanceToClosestGhost=100

        if distanceToClosestGhost == 0:
            ghostScore = -999  
        elif distanceToClosestGhost < 6:
            ghostScore = (1./distanceToClosestGhost)
        else:
            ghostScore = 0
        return ghostScore

    def getGhostScore(self, gameState, newGameState, a):
        pacself = newGameState.getAgentState(self.index)
        if not pacself.isPacman and not pacself.scaredTimer > 0:
            return 0

        Pos = pacself.getPosition()
        oldPos = gameState.getAgentState(self.index).getPosition()

        enemyPacmanPossiblePositions = {}
        #Find closest enemy and best position to intercept him 
        ReadyToMunch = False
        for agent in self.getOpponents(newGameState):
            # Add opponents to list of enemies
            enemy = newGameState.getAgentState(agent)
            currentEnemy = gameState.getAgentState(agent)


            if (not enemy.isPacman) and enemy.getPosition() != None:
                enemyPacmanPossiblePositions[agent] = map(lambda a: gameState.generateSuccessor(agent, a),gameState.getLegalActions(agent))
        PacmanFollowing = -1;
        distanceToEnemyPacman = 999
        goTo = None
        for id in enemyPacmanPossiblePositions:
            #print id
            for enemyP in enemyPacmanPossiblePositions[id]:
                if self.getMazeDistance(Pos, enemyP.getAgentPosition(id))<distanceToEnemyPacman:
                    #pacmanFollowing = id
                    distanceToEnemyPacman = self.getMazeDistance(Pos, enemyP.getAgentPosition(id))
                    #distanceToEnemyPacman = util.manhattanDistance(Pos, enemyP.getAgentPosition(id))
                    goTo = enemyP.getAgentPosition(id)

        if distanceToEnemyPacman < 2:
            pacmanScore = 10
            #print "RUN AWAY"
        elif distanceToEnemyPacman < 999:
            pacmanScore = 1/distanceToEnemyPacman
        else:
            pacmanScore = self.getPotentialGhosts(newGameState)
        return pacmanScore

    def getPotentialGhosts(self, newGameState):
        Pos = newGameState.getAgentState(self.index).getPosition()
        total = 0.0
        score = 0.0
        if not newGameState.isOnRedTeam(self.index):
            #they are pacman on the left side of the screen
            xSize = range(0,len(sharemem.enemy[0].grid)/-1)
        else:
            xSize = range(len(sharemem.enemy[0].grid)/2,len(sharemem.enemy[0].grid))
        for i in range(0,2):
            emy = sharemem.enemy[i]
            for x in xSize:
                for y in range(0,len(emy.grid[0])):
                    if emy.grid[x][y] > 0:
                        total += 1
                        if not self.getMazeDistance(Pos, (x,y)) == 0:
                            score += 1.0/self.getMazeDistance(Pos, (x,y))
        if not total == 0:
            return (score / total)
        return 0        


    def getFoodScore(self, newGameState, oldfood):

        food = self.getFood(newGameState)
        if food.asList():
            distanceToClosestFood = min(map(lambda x: self.getMazeDistance(newGameState.getAgentState(self.index).getPosition(), x), food.asList()))

            if(len(food.asList())==len(oldfood.asList())-1):    #I don't get why we have this. Is this saying that if we've eaten food, then we have a high food score?
                foodScore = 2                
            elif distanceToClosestFood == 0:
                foodScore = 0
                ghostScore += 2 #not sure how to treat this
            else:
                foodScore = 1./distanceToClosestFood
        else:
            #print "no food list"
            foodScore = 0
        return foodScore

    def getPacmanScore(self, gameState, newGameState, a):
        Pos = newGameState.getAgentState(self.index).getPosition()
        enemyPacmanPossiblePositions = {}
        #Find closest enemy and best position to intercept him 

        for agent in self.getOpponents(newGameState):
            # Add opponents to list of enemies
            enemy = newGameState.getAgentState(agent)
            currentEnemy = gameState.getAgentState(agent)

            if(enemy.getPosition() and currentEnemy.getPosition()):
                futuredist = self.getMazeDistance(Pos, enemy.getPosition())
                currentdist = self.getMazeDistance(Pos, currentEnemy.getPosition())
                if not futuredist == currentdist:
                    return 10

            if(enemy.isPacman and enemy.getPosition() != None):
                enemyPacmanPossiblePositions[agent] = map(lambda a: gameState.generateSuccessor(agent, a),gameState.getLegalActions(agent))
        PacmanFollowing = -1;
        distanceToEnemyPacman = 999
        goTo = None
        for id in enemyPacmanPossiblePositions:
            #print id
            for enemyP in enemyPacmanPossiblePositions[id]:
                if self.getMazeDistance(Pos, enemyP.getAgentPosition(id))<distanceToEnemyPacman:
                    #pacmanFollowing = id
                    distanceToEnemyPacman = self.getMazeDistance(Pos, enemyP.getAgentPosition(id))
                    #distanceToEnemyPacman = util.manhattanDistance(Pos, enemyP.getAgentPosition(id))
                    goTo = enemyP.getAgentPosition(id)

        if distanceToEnemyPacman < 1:
            pacmanScore = 2
        elif distanceToEnemyPacman < 999:
            pacmanScore = 1/distanceToEnemyPacman
        else:
            pacmanScore = self.getPotentialPacman(newGameState) #(newgamestate, isPacState)
        return pacmanScore


    def getPotentialPacman(self, newGameState):
        Pos = newGameState.getAgentState(self.index).getPosition()
        total = 0.0
        score = 0.0
        if newGameState.isOnRedTeam(self.index):
            #they are pacman on the left side of the screen
            xSize = range(0,len(sharemem.enemy[0].grid)/-1)
        else:
            xSize = range(len(sharemem.enemy[0].grid)/2,len(sharemem.enemy[0].grid))
        for i in range(0,2):
            emy = sharemem.enemy[i]
            for x in xSize:
                for y in range(0,len(emy.grid[0])):
                    if emy.grid[x][y] > 0:
                        total += 1
                        if not self.getMazeDistance(Pos, (x,y)) == 0:
                            score += 1.0/self.getMazeDistance(Pos, (x,y))
        if not total == 0:
            return (score / total)
        return 0


    def getCaptureScore(self, newGameState, myOldState, myNewState):

        if (myOldState.isPacman and myOldState.numCarrying>0):
            d = self.distanceToCamp(newGameState)
            #print(str(d))
            if d==0:
                captureScore = 999
            else:
                captureScore = math.sqrt(myNewState.numCarrying) *1./self.distanceToCamp(newGameState)
        else:
            captureScore = 0
        return captureScore

    def getFriendScore(self, myNewState, friendState, a):
        Pos = myNewState.getPosition()
        if friendState.getPosition()!=None:
            if self.getMazeDistance(Pos, friendState.getPosition())>0:
                friendScore = 1/self.getMazeDistance(Pos, friendState.getPosition())
            else:
                friendScore = 1
        else:
            friendScore = 1
        return friendScore
    

    def getPillScore(self, newGameState, oldpills):
        Pos = newGameState.getAgentState(self.index).getPosition()
        food = self.getFood(newGameState)
        pills = self.getCapsules(newGameState)
        if food.asList():
            distanceToClosestPill = min(map(lambda x: self.getMazeDistance(Pos, x), food.asList()))
            if(len(pills)==len(oldpills)-1):
                pillScore = 2
            elif distanceToClosestPill == 0:
                pillScore = 0
            else:
                pillScore = 1./distanceToClosestPill
        else:
            pillScore = 0
        return pillScore
        

    def getWallScore(self, newGameState):
        if(len(newGameState.getLegalActions(self.index))<3):
            wallScore = 1
        else:
            wallScore = 0
        return wallScore

    # Main function
    # Used to calculate all the resulting features from an action.
    # So far takes into account: distance to the border, distance to closest ghost, distance to closest food and distance to closest pacman
    def getFeatures(self, gameState, a):
        """
        Returns a counter of features for the state
        """
        features = util.Counter()
        if(a==None):
            newGameState = gameState
        else:
            newGameState = gameState.generateSuccessor(self.index, a)
        myOldState = gameState.getAgentState(self.index)
        myNewState = newGameState.getAgentState(self.index)
        friendState = gameState.getAgentState((self.index+2)%4)      

        oldfood = self.getFood(gameState)
        oldpills = self.getCapsules(gameState)
        pills = self.getCapsules(newGameState)
        

        ghostScore = self.getGhostScore(gameState, newGameState, a)
        foodScore = self.getFoodScore(newGameState, oldfood)
        pacmanScore = self.getPacmanScore(gameState, newGameState, a)
        captureScore = self.getCaptureScore(newGameState, myOldState, myNewState)
        friendScore = self.getFriendScore(myNewState, friendState, a)
        pillScore = self.getPillScore(newGameState, oldpills)
        wallScore = self.getWallScore(newGameState)
        

        #if self.index ==2:
        #    print "{}: [{}, {}, {}, {}, {} , {}, {}]".format(a, foodScore, pillScore, ghostScore, captureScore, pacmanScore, friendScore, wallScore)
        features['foodScore'] = foodScore
        features['pileScore'] = pillScore
        features['ghostScore'] = ghostScore
        features['captureScore'] = captureScore
        features['pacmanScore'] = pacmanScore
        features['friendScore'] = friendScore
        features['wallScore'] = wallScore

        return features

    def getFeaturesMinMax(self, gameState, a, oldGameState):
        """
        Returns a counter of features for the state
        """
        features = util.Counter()
        if(a==None):
            newGameState = gameState
        else:
            newGameState = gameState.generateSuccessor(self.index, a)
        myOldState = oldGameState.getAgentState(self.index)
        myNewState = newGameState.getAgentState(self.index)
        friendState = gameState.getAgentState((self.index+2)%4)      
        
        oldfood = self.getFood(gameState)
        oldpills = self.getCapsules(oldGameState)
        pills = self.getCapsules(newGameState)
        
        

        ghostScore = self.getGhostScore(gameState, newGameState, a)
        foodScore = self.getFoodScore(newGameState, oldfood)
        pacmanScore = self.getPacmanScore(gameState, newGameState, a)
        captureScore = self.getCaptureScore(newGameState, myOldState, myNewState)
        friendScore = self.getFriendScore(myNewState, friendState, a)
        pillScore = self.getPillScore(newGameState, oldpills)
        wallScore = self.getWallScore(newGameState)

        #print(str(a)+":"+str(foodScore)+","+str(ghostScore)+","+str(captureScore)+","+str(myNewState))
        features['foodScore'] = foodScore
        features['pileScore'] = pillScore
        features['ghostScore'] = ghostScore
        features['captureScore'] = captureScore
        features['pacmanScore'] = pacmanScore
        features['friendScore'] = friendScore
        features['wallScore'] = wallScore


        return features
    
    # Define weights for each of the features.


    def getWeights(self, gameState):
        return ({'foodScore': self.foodScore, 
                 'pillScore': self.pillScore,
                 'ghostScore': self.ghostScore,
                 'captureScore': self.captureScore,
                 'pacmanScore':self.pacmanScore,
                 'friendScore':self.friendScore, 
                 'wallScore':self.wallScore})

    
    def evaluateState(self,gameState,a):
        features = self.getFeatures(gameState, a)
        weights = self.getWeights(gameState)
        return features * weights
    
    def isWon(self,gameState):
        return (self.getFood(gameState)<=2)
    
    def isLost(self,gameState,enemies):
        defenders = []
        distances_to_defenders = []
        current_position = gameState.getAgentState(self.index).getPosition()
        # Check enemies...
        for enemy in enemies:
            # If there is an enemy position that we can see...
            if not enemy.isPacman and enemy.getPosition() != None:
                # Add that enemy to the list of defenders
                defenders.append(enemy)
    
        # If there is a defender...
        if len(defenders) > 0:
            # Check the indices of defenders...
            for d in defenders:
                # Find the shortest distance to the defender from current position and add to list of defender distances
                distances_to_defenders.append(self.getMazeDistance(current_position, d.getPosition()))
            return (self.getFoodYouAreDefending(gameState)<=2 or min(distances_to_defenders)<1)
        else:
            return (self.getFoodYouAreDefending(gameState)<=2)


    def updateGridMeasurment(self, gameState):
        #print "self: {}, self+1%4: {}".format(self.index,(self.index+1)%4)
        enemyAfter = 0
        if not sharemem.enemy[enemyAfter].id == (self.index+1)%4:
            enemyAfter =1
        sharemem.enemy[enemyAfter].updateGridMotion(self, gameState)      #first updates motion model

        #sharemem.enemy[(self.index+1)%4].updateGridMotion(self, gameState)      #first updates motion model
        for emy in sharemem.enemy:

            """print "self"
            for attr_name in dir(self):
                attr_value = getattr(self, attr_name)
                print(attr_name, callable(attr_value))
            util.pause()"""

            emy.updateGridMeasurment(self, gameState, gameState.getAgentDistances()[emy.id])   #incorperates noisy sonar measurement
            #print gameState.isScared(self.index)


            if gameState.getAgentState(emy.id).getPosition() != None:       #if we see the enemy agent, update their position
                emy.exactPosition(gameState.getAgentState(emy.id).getPosition())

                if self.getMazeDistance(gameState.getAgentState(emy.id).getPosition(), gameState.getAgentState(self.index).getPosition()) < 1.5:
                    emy.setTouchingAgent(self.playerId)  #first check if agent is touching
                    #print "our agent {} is touching {}".format(self.index, emy.id)

            else:
                #print "team: {}, agentnum: {}, index: {}".format(self.getTeam(gameState),agentNum, self.index)
                if emy.touchingAgent[self.playerId]:   #the agent is out of range and has thus jumped 6 sonar levels
                        sizeofmove = util.manhattanDistance(gameState.getAgentState(self.index).getPosition(), self.previousLocation)
                        if not gameState.getAgentState(self.index).isPacman or gameState.getAgentState(emy.id).scaredTimer > 0:
                            if not abs(sizeofmove) >1:
                                emy.setGhostStart()
                                emy.updateGridMotion(self, gameState) 
                            else:
                                emy.notTouchingAgent(self.playerId)
                else:
                    emy.notTouchingAgent(self.playerId)  #otherwise everything is fine, carry on.
                    emy.notInSight(gameState.getAgentState(self.index).getPosition())

        self.getCapsules(gameState)


        #if self.playerId == 0:
        #    sharemem.enemy[0].drawGrid(self)   


class FrenchCanadianAgent(MultiAgentSearchAgent):
    """
    A Dummy agent to serve as an example of the necessary agent structure.
    You should look at baselineTeam.py for more details about how to
    create an agent as this is the bare minimum.
    """

    def registerInitialState(self, gameState):
        """
        This method handles the initial setup of the
        agent to populate useful fields (such as what team
        we're on).
        
        A distanceCalculator instance caches the maze distances
        between each pair of positions, so your agents can use:
        self.distancer.getDistance(p1, p2)
        
        IMPORTANT: This method may run for at most 15 seconds.
        """
        
        '''
        Make sure you do not delete the following line. If you would like to
        use Manhattan distances instead of maze distances in order to save
        on initialization time, please take a look at
        CaptureAgent.registerInitialState in captureAgents.py.
        '''
        MultiAgentSearchAgent.registerInitialState(self, gameState)

        self.setDefaultWeights()
        self.historicalActions = ['Go']
        
        '''
        Your initialization code goes here, if you need any.
        '''

    def gameOver(self, gameState, d):
        enemies = []
        # Check the indices of the opponents...
        for agent in self.getOpponents(gameState):
            # Add opponents to list of enemies
            enemies.append(gameState.getAgentState(agent))
        return self.isLost(gameState,enemies) or self.isWon(gameState) or d == 0
    
    
    def minmax(self, gameState, agentIndex, depth,isRed,initialGameState):
        "produces the min or max value for some game state and depth; depends on what agent."
        #print("Depth:"+str(depth)+",agent "+str(agentIndex))
        successorStates = map(lambda a: gameState.generateSuccessor(agentIndex, a),gameState.getLegalActions(agentIndex))
        if self.gameOver(gameState, depth): # at an end
            return self.evaluateStateMinMax(gameState,None,initialGameState)
        else:
            # use modulo so we can wrap around, have to skip agents we can't see
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            while gameState.getAgentState(nextAgent).getPosition()==None:
                nextAgent = (nextAgent + 1) % gameState.getNumAgents()
            #print("Next Agent: "+str(nextAgent))
            vals = map(lambda s: self.minmax(s, nextAgent, depth - 1,isRed,initialGameState),successorStates)
            if isRed:
                if nextAgent%2 == 0: # team member
                    return max(vals)
                else:
                    return min(vals)
            else:   
                if nextAgent%2 == 1: # team member
                    return max(vals)
                else:
                    return min(vals)


    def expectimax(self, gameState, agentIndex, depth,isRed,initialGameState):
        "produces the average or max value for some game state and depth; depends on what agent."
        #print("Depth:"+str(depth)+",agent "+str(agentIndex))
        successorStates = map(lambda a: gameState.generateSuccessor(agentIndex, a),gameState.getLegalActions(agentIndex))
        if self.gameOver(gameState, depth): # at an end
            return self.evaluateStateMinMax(gameState,None,initialGameState)
        else:
            # use modulo so we can wrap around, have to skip agents we can't see
            nextAgent = (agentIndex + 1) % gameState.getNumAgents()
            while gameState.getAgentState(nextAgent).getPosition()==None:
                nextAgent = (nextAgent + 1) % gameState.getNumAgents()
            #print("Next Agent: "+str(nextAgent))
            vals = map(lambda s: self.minmax(s, nextAgent, depth - 1,isRed,initialGameState),successorStates)
            if isRed:
                if nextAgent%2 == 0: # team member
                    return max(vals)
                else:
                    return av(vals)
            else:   
                if nextAgent%2 == 1: # team member
                    return max(vals)
                else:
                    return av(vals)

    def evaluateStateMinMax(self,gameState,a,firstGameState):
        features = self.getFeaturesMinMax(gameState, a,firstGameState)
        weights = self.getWeights(gameState)
        #print(features)
        return features * weights


    def setDefaultWeights(self):
        old = False
        new = True
        if old:
            self.foodScore = 1.0
            self.pillScore = 1.0
            self.ghostScore = -2.0
            self.captureScore = 1.0
            self.pacmanScore = 0.0
            self.friendScore = -0.75
            self.wallScore = -2.0
        elif new:
            self.foodScore = 2.0
            self.pillScore = 1.5
            self.ghostScore = -1.0
            self.captureScore = 1.5
            self.pacmanScore = 1.5  #changed from 0.5
            self.friendScore = -2.0 #changed from -2.0
            self.wallScore = -1.0   #changed from -1.0
        else:
            self.foodScore = 1.0
            self.pillScore = 1.0
            self.ghostScore = -2.0
            self.captureScore = 1.0
            self.pacmanScore = 0.0
            self.friendScore = -0.0
            self.wallScore = -0.0

    def setWeights(self, weight):
        self.foodScore = weight[0]
        self.pillScore = weight[1]
        self.ghostScore = weight[2]
        self.captureScore = weight[3]
        self.pacmanScore = weight[4]
        self.friendScore = weight[5]
        self.wallScore = weight[6]


    def evalRunningOutOfTime(self, gameState):
        time = gameState.data.timeleft
        toBase = self.distanceToCamp(gameState)*4
        THRESHOLD = 10*4 #turns
        if time < toBase + THRESHOLD and gameState.getAgentState(self.index).isPacman:
            return True
        return False


    def noFoodLeft(self, gameState):
        if len(self.getFood(gameState).asList()) <= MIN_FOOD:
            return True
        return False


    def _nextToPac(self, gameState):
        if gameState.getAgentState(self.index).scaredTimer > 0:
            return False
        Pos = gameState.getAgentState(self.index).getPosition()
        enemyPacmanPossiblePositions = {}
        #Find closest enemy and best position to intercept him 
        for agent in self.getOpponents(gameState):
            # Add opponents to list of enemies
            enemy = gameState.getAgentState(agent)
            if(enemy.isPacman and enemy.getPosition() != None):
                enemyPacmanPossiblePositions[agent] = map(lambda a: gameState.generateSuccessor(agent, a),gameState.getLegalActions(agent))
        PacmanFollowing = -1;
        distanceToEnemyPacman = 999
        goTo = None

        for id in enemyPacmanPossiblePositions:
            #print id
            for enemyP in enemyPacmanPossiblePositions[id]:
                if self.getMazeDistance(Pos, enemyP.getAgentPosition(id))<distanceToEnemyPacman:
                    #pacmanFollowing = id
                    #distanceToEnemyPacman = self.getMazeDistance(Pos, enemyP.getAgentPosition(id))
                    distanceToEnemyPacman = util.manhattanDistance(Pos, enemyP.getAgentPosition(id))
                    goTo = enemyP.getAgentPosition(id)

        if distanceToEnemyPacman < 1: #jonky
            util.pause()
            return True       
        return False


    def nextToPac(self, gameState):
        enemies = []
        for agent in self.getOpponents(gameState):
            enemies.append(gameState.getAgentState(agent))

        pacStates = []
        for enemy in enemies:
            if enemy.isPacman and enemy.getPosition() != None:
                pacStates.append(enemy)

        pacPositions = map(lambda g: g.getPosition(), pacStates)
        if(len(pacPositions)>0):
            distanceToClosestPac = min(map(lambda x: self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), x), 
                                         pacPositions))
        else:
            distanceToClosestPac=100

        if distanceToClosestPac < 1:
            print "dist=0"       
            util.pause()
            return True
             
        elif distanceToClosestPac < 6:
            ghostScore = (1./distanceToClosestPac)
        else:
            ghostScore = 0
        return False

    def isScared(self, gameState):
        if gameState.getAgentState(self.index).scaredTimer > 0:
            return True
        return False

    def isLuigi(self, gameState):
        if gameState.getAgentState(self.getOpponents(gameState)[0]).scaredTimer > 0:
            return True
        return False

    def isTrapped(self, gameState):
        if(len(gameState.getLegalActions(self.index))<3):
            return True
        return False

    def eatPacman(self):
        self.setWeights([0, 0, 0, 1, 0, 0, 0]) #food, pill, ghost, capture, pacman, friend, wall

    def leaveWalls(self):
        self.setWeights([0, 0, 1, 0, 0, 0, -1]) #food, pill, ghost, capture, pacman, friend, wall

    def tooSpooked(self, gameState):
        self.pacmanScore = -abs(self.pacmanScore)

    def vacuumGhosts(self, gameState):
        self.ghostScore = abs(self.ghostScore)

    def returnToBase(self):
        self.setWeights([0, 0.4, 1, 1, 0, 0, -2]) #food, pill, ghost, capture, pacman, friend, wall


    def behaviorTree(self, gameState):
        
        if self.isTrapped(gameState):
            action = 1
            self.leaveWalls()
        elif self.evalRunningOutOfTime(gameState):
            action = 2            
            self.returnToBase()
        elif self.noFoodLeft(gameState):
            action = 3
            self.returnToBase()
            #print "out of food"
        else:
            action = 0
            self.setDefaultWeights()
            #print "weights: {}".format(self.getWeights(gameState))

        #Modifiers/Interrupts
        if self.isScared(gameState):
            mod = 0
            self.tooSpooked(gameState)
            #print "thanks mr skeletal"
        if self.isLuigi(gameState):
            mod = 1
            self.vacuumGhosts(gameState)
            #print "Luigi Time"

        sharemem.setTreeAction(self.playerId, action)

        actions = gameState.getLegalActions(self.index)
        
        if self.historicalActions[0] == 'Stop' and len(set(self.historicalActions)) <= 1: #if contain the same value
            actions.remove('Stop')
            #print "NO BREAKS"
        
        mmax = False
        emax = False
        iterations = 2
        if mmax:
            t1 = time.clock()
            values = [self.evaluateState(gameState,a) for a in actions]
            valuesMinMax = [self.minmax(gameState.generateSuccessor(self.index, a),self.index,iterations,gameState.isOnRedTeam(self.index),gameState) for a in actions]
            finalValues = valuesMinMax #Choose which values to use for choosing optimal action
            maxValue = max(finalValues)
            bestActions = [a for a, v in zip(actions, finalValues) if v == maxValue]
            print(time.clock()-t1)
        elif emax:
            t1 = time.clock()
            values = [self.evaluateState(gameState,a) for a in actions]
            valuesExpectiMax = [self.expectimax(gameState.generateSuccessor(self.index, a),self.index,iterations,gameState.isOnRedTeam(self.index),gameState) for a in actions]
            finalValues = valuesExpectiMax #Choose which values to use for choosing optimal action
            maxValue = max(finalValues)
            bestActions = [a for a, v in zip(actions, finalValues) if v == maxValue]
            print(time.clock()-t1)
        else:
            values = [self.evaluateState(gameState,a) for a in actions]
            """
            if self.index ==2:
                print "agent: {}".format(self.index)
                print actions
                print values"""
            maxValue = max(values)
            bestActions = [a for a, v in zip(actions, values) if v == maxValue]
        #Calls MinMax
        #values = [self.minmax(gameState.generateSuccessor(self.index, a),self.index,1) for a in actions]

        move = random.choice(bestActions)     

        return move

    def chooseAction(self, gameState):

        movement = self.behaviorTree(gameState)
        
        self.updateGridMeasurment(gameState)
        self.previousLocation = gameState.getAgentState(self.index).getPosition()

        self.historicalActions.append(movement)
        if len(self.historicalActions) > 3:
            self.historicalActions.pop(0)
                
        #print self.historicalActions
        #minimax(self, gameState, agentIndex, depth)

        return movement