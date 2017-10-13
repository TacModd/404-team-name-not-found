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

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'Top', second = 'Bottom'):
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

class DummyAgent(CaptureAgent):
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
    
    CaptureAgent.registerInitialState(self, gameState)
    
    '''
    Your initialization code goes here, if you need any.
    '''
    #### CALCULATE MIDDLEXPOS CONSTANT DURING INITIALIZATION? ####
    self.behaviourState = 'Guard'
    self.setCenter(gameState)
    self.eatenFood = 0
    self.prevFoodState = self.getFoodYouAreDefending(gameState)
    self.opponentIndices = self.getOpponents(gameState)
    self.teamIndices = self.getTeam(gameState)
    self.teammateIndex = self.getTeam(gameState)[:]
    self.teammateIndex.remove(self.index)
    self.defenceDestination = None
    self.attackDestination = None
    self.opponentPositions = {}
    self.opponentPrevPositions = {}
  
  def destinationReached(self,gameState,destination):
    if destination == None:
      return False
    else:
      return self.getMazeDistance(gameState.getAgentPosition(self.index),destination) == 0


  def updateDefenceDestination(self,gameState):
    if self.destinationReached(gameState, self.defenceDestination):
      self.defenceDestination = self.opponentDetected(gameState)
    else:
      if not self.opponentDetected(gameState) == None:
        self.defenceDestination = self.opponentDetected(gameState)
      else:
        if self.defenceDestination == None:
          return 
        elif not self.inHomeTerritory(gameState,self.defenceDestination,-1):
          self.defenceDestination = None
        else: 
          return 

  def killedOpponent(self, gameState,teamIndex):

    for index in self.opponentIndices:
      if self.opponentPositions[index] == gameState.getInitialAgentPosition(index):
        return True
      elif not self.opponentPrevPositions[index] == None:
        if self.opponentPositions[index] == None and util.manhattanDistance(gameState.getAgentPosition(teamIndex), self.opponentPrevPositions[index])<2:
          return True
    return False

  def opponentIsDead(self, gameState):
    dead = False
    for teamIndex in self.teamIndices:
      dead = (dead or self.killedOpponent(gameState,index))
    return dead

  def isDead(self, gameState):
    if gameState.getAgentPosition(self.index) == gameState.getInitialAgentPosition(self.index):
      return True 
    return False

  def tooMuchFood(self):
    if self.eatenFood > 2:
      return True
    return False

  def resetFoodCount(self):
    self.eatenFood = 0

  def updateOpponentPositions(self, gameState):
    self.opponentPrevPositions = self.opponentPositions.copy()
    self.opponentPositions = self.getOpponentPositionsDict(gameState)

  def nextBehaviourState(self,gameState):
    #defenceDestinationCandidate = self.opponentDetected(gameState)

    self.updateOpponentPositions(gameState)
    self.updateDefenceDestination(gameState)

    if self.behaviourState == 'Guard':
      if not self.defenceDestination == None:
        self.behaviourState = 'Defence'
      else:
        return
    elif self.behaviourState == 'Defence':
      if self.killedOpponent(gameState,self.index):
         self.behaviourState = 'Offence'
      elif self.defenceDestination == None:
        self.behaviourState = 'Guard'
      else:
        return

    elif self.behaviourState == 'Offence':
      if self.isDead(gameState):
        self.resetFoodCount()
        self.behaviourState = 'Guard'
      elif self.tooMuchFood():
        self.behaviourState = 'Flee'
        self.setFleeDestination(gameState)
        return 
      else:
        return

    elif self.behaviourState == 'Flee':
      #if self.middleReached(gameState, position):
      if self.inHomeTerritory(gameState, gameState.getAgentPosition(self.index),-1) or self.isDead(gameState):
        self.resetFoodCount()
        self.behaviourState = 'Guard'
      else:
        return

    else:
      print 'State not defined'
      self.behaviourState = 'Guard'
    
  
  def chooseAction(self, gameState):
    # check behaviourState value

    self.nextBehaviourState(gameState)
    print self.behaviourState
    if self.behaviourState == 'Guard':
      return self.chooseGuardAction(gameState)
    elif self.behaviourState == 'Defence':
      return self.chooseDefensiveAction(gameState)

    elif self.behaviourState == 'Offence':
      return self.chooseOffensiveAction(gameState)

    elif self.behaviourState == 'Flee':
      return self.chooseFleeAction(gameState)

    else:
      print 'State not defined'
      return Directions.STOP
    

  
  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != util.nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor
    
    
  ###### 'GUARD' BEHAVIOUR CODE ######
  
  def chooseGuardAction(self, gameState):
    # use greedyBFS to get to middle
      # one goes top, one goes bottom (see 'Top' and 'Bottom' classes)
    
    actions = gameState.getLegalActions(self.index)
    
    values = [self.evaluateGuard(gameState, a) for a in actions]
    
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    
    #return bestAction
    return random.choice(bestActions)
      
  def evaluateGuard(self, gameState, action):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getGuardFeatures(gameState, action)
    weights = self.getGuardWeights(gameState, action)
    return features * weights

  def getGuardFeatures(self, gameState, action):
    # distanceToCenter
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    successorState = successor.getAgentState(self.index)
    successorPos = successorState.getPosition()
    minDistance = 99999999
    if self.getMazeDistance(successorPos,self.center) < minDistance:
      #bestAction = action
      minDistance = self.getMazeDistance(successorPos,self.center)
    features['distanceToCenter'] = minDistance
    return features

  def getGuardWeights(self, gameState, action):
    #
    return {'distanceToCenter': -1}

    
  ###### 'OFFENCE' BEHAVIOUR CODE ######
  
  def chooseOffensiveAction(self, gameState):
    # get a list of actions for MonteCarloSearch()
    actions = gameState.getLegalActions(self.index)
    actions.remove(Directions.STOP)
    minAll = 99999999999999
    maxAll = -99999999999999
    values = []
    for a in actions:
      successor = self.getSuccessor(gameState, a)
      monValues = self.MonteCarloSearch(8, successor, 40)
      value = sum(monValues)
      maxVal = max(monValues)
      minVal = min(monValues)
      minAll = min(minVal,minAll)
      maxAll = max(maxVal,maxAll)
      values.append(value)
    if minAll == maxAll:
      print 'random'
      minDistance = 999999999
      foodList = self.getFood(gameState).asList()
      for food in foodList:
        distance = self.getMazeDistance(gameState.getAgentPosition(self.index),food)
        if distance<minDistance:
          minDistance = distance
          minFood = food
      minDistance = 999999999
      for action in actions:
        position = self.getSuccessor(gameState, action).getAgentState(self.index).getPosition()
        distance = self.getMazeDistance(position,minFood)
        if distance<minDistance:
          minDistance = distance
          minAction = action
      return minAction
    else:
    # choose action with best value
      maxValue = max(values)
      bestActions = [a for a, v in zip(actions, values) if v == maxValue]

      choice = random.choice(bestActions)
      successor = self.getSuccessor(gameState, choice)
      foodList = self.getFood(gameState).asList()
      successorFoodList = self.getFood(successor).asList()
      if len(successorFoodList) < len(foodList):
        self.eatenFood += 1
      return choice
    
    

  def MonteCarloSearch(self, depth, gameState, iterations):
    # define a gameState that we will iteratively search through
    searchState = None

    # get the distance to the nearest food
    foodList = self.getFood(gameState).asList()
    if len(foodList) > 0:
      minDistance = min([self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), food)
                         for food in foodList])

    # keep track of discovered endstates
    endStates = []
    # do random searches for the number of iterations defined
    while iterations > 0:

      
      searchState = gameState.deepCopy()

      # if minDistance = 0, we want the action that called MonteCarlo
      if minDistance == 0:
        endStates.append(gameState)
      # otherwise commit to random searches for depth specified
      else:
        while depth > 0:
          actions = searchState.getLegalActions(self.index)
          # stopping is a waste of time
          actions.remove(Directions.STOP)

          # reversing direction is also a waste of time
          rev = Directions.REVERSE[searchState.getAgentState(self.index).configuration.direction]
          if rev in actions and len(actions) > 1:
            actions.remove(rev)

          a = random.choice(actions)
          searchState = self.getSuccessor(searchState, a)

          depth -= 1
        endStates.append(searchState)
        
      iterations -= 1
    # return values (to chooseOffensiveAction)
    return [self.evaluateOffensive(endState) for endState in endStates]
  
  def evaluateOffensive(self, gameState):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getOffensiveFeatures(gameState)
    weights = self.getOffensiveWeights(gameState)
    return features * weights
  
  def getOffensiveFeatures(self, gameState):
    # distancetofood, foodremaining?, ghost?, capsule?/distancetocapsule?
    features = util.Counter()

    foodList = self.getFood(gameState).asList()
    features['stateScore'] = -len(foodList)

    myPos = gameState.getAgentState(self.index).getPosition()
    betterFoodList = [f for f in foodList if self.getMazeDistance(myPos, f) <= 8]
    sumFoods = 0
    sumDistance = 0
    for food in betterFoodList:
      sumFoods += 1
      sumDistance += self.getMazeDistance(myPos, food)
    features['numFoods'] = sumFoods
    features['sumDistanceToFood'] = sumDistance

    #Calculate Distance to nearest ghost
    minDistance = 999999999999
    opponentDict = self.getOpponentPositionsDict(gameState)
    for index in self.opponentIndices:
      if opponentDict[index] != None:
        distance = self.getMazeDistance(opponentDict[index],gameState.getAgentPosition(self.index))
        if gameState.getAgentState(index).scaredTimer > 0:
          distance = distance*999999
        if distance < minDistance:
          minDistance = distance
    features['closestEnemy'] = 1/minDistance

    return features

  def getOffensiveWeights(self, gameState):
    # what weights? check other implementations for a rough idea
    return {'stateScore': 80, 'numFoods': 8, 'sumDistanceToFood': -1, 'closestEnemy': -100000}

    
  ###### 'DEFENCE' BEHAVIOUR CODE ######
  def inHomeTerritory(self,gameState,position,offset):
    homeX = gameState.getWalls().width/2
    if self.red:
      homeX = homeX - (1+offset)
    else:
      homeX = homeX + offset
    if self.red and position[0] >= homeX:
      return False
    elif not self.red and position[0] <= homeX:
      return False
    else:
      return True


  def chooseDefensiveAction(self, gameState):
    # get a list of actions
    actions = gameState.getLegalActions(self.index)
    actions.remove(Directions.STOP)
    for action in actions:
      successor = self.getSuccessor(gameState,action)
      successorState = successor.getAgentState(self.index)
      successorPos = successorState.getPosition()
      if not self.inHomeTerritory(gameState,successorPos,-1):
        actions.remove(action)
    # get a list of values (call evaluate?) OR call evaluateDefensive
      # evaluate defensive features/weights
    values = [self.evaluateDefensive(gameState, a) for a in actions]
    # choose action with best value
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    return random.choice(bestActions)

  def evaluateDefensive(self, gameState, action):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getDefensiveFeatures(gameState, action)
    weights = self.getDefensiveWeights(gameState, action)
    return features * weights

  # def getDefensiveFeatures(self, gameState, action):
  #   # enemyagent, enemyagentdistance, scared? - maybe move to nextBehaviourState function, distancetocentre, reverse, STOP
  #   # tell it to hover somehow using reverse/STOP
  #   features = util.Counter()
  #   successor = self.getSuccessor(gameState, action)
  #   features['featureName'] = self.getFeatureInfo(successor)

  # def getDefensiveWeights(self, gameState, action):
  #   # what weights? check other implementations for a rough idea
  #   return {'featureName': weighting}

  def getDefensiveFeatures(self, gameState, action):
    # distanceToCenter
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    successorState = successor.getAgentState(self.index)
    successorPos = successorState.getPosition()
    minDistance = 99999999
    if (not self.defenceDestination == None) and self.getMazeDistance(successorPos,self.defenceDestination) < minDistance:
      #bestAction = action
      minDistance = self.getMazeDistance(successorPos,self.defenceDestination)
    features['distanceToCenter'] = minDistance
    return features

  def getDefensiveWeights(self, gameState, action):
    #
    return {'distanceToCenter': -1}

  def foodEatenByOpponent(self, gameState):
    foodEatenByOpponent = []
    for x in range(gameState.getWalls().width):
      for y in range(gameState.getWalls().height):
        if self.prevFoodState[x][y] == True and self.getFoodYouAreDefending(gameState)[x][y] == False and self.inHomeTerritory(gameState, (x,y), -1):
          foodEatenByOpponent = foodEatenByOpponent + [(x,y)]
    self.prevFoodState = self.getFoodYouAreDefending(gameState)
    return foodEatenByOpponent

  def getOpponentPositionsDict(self, gameState):
    opponentPositionsDict = {}
    for index in self.opponentIndices:
      opponentPositionsDict[index] = gameState.getAgentPosition(index)
    return opponentPositionsDict

  def getOpponentPositionsList(self, gameState):
    opponentPositionsList = []
    for index in self.opponentIndices:
      if not gameState.getAgentPosition(index) == None:
        opponentPositionsList = opponentPositionsList + [gameState.getAgentPosition(index)]
    return opponentPositionsList


  def closestTeammember(self, gameState, position):
    minDistance = 99999
    for index in self.teamIndices:
      distance = self.getMazeDistance(gameState.getAgentPosition(index), position)
      if distance < minDistance:
        minDistance = distance
        minIndex = index
    return minIndex,minDistance


  def opponentDetected(self,gameState):

    opponentPositions = self.getOpponentPositionsList(gameState)
    foodEatenByOpponent = self.foodEatenByOpponent(gameState)
    if len(opponentPositions)<2 and len(foodEatenByOpponent)>0:
      for opEatFood in foodEatenByOpponent:
        for opponentPosition in opponentPositions:
          if self.getMazeDistance(opEatFood,opponentPosition) > 1:
            opponentPositions = opponentPositions + [opEatFood]

    if len(opponentPositions) == 1:
      for position in opponentPositions:
        if self.closestTeammember(gameState, position)[0] == self.index:
          return position
    elif len(opponentPositions) > 1:
      minDistance = 99999999
      for position in opponentPositions:
        index, distance = self.closestTeammember(gameState,position)
        if distance < minDistance:
            minDistance = distance
            minPosition = position
            minIndex = index
      if minIndex == self.index:
        return minPosition
      else:
        for position in opponentPositions:
          if not position == minPosition:
            return position
    return None

  ###### 'FLEE' BEHAVIOUR CODE ######

  def setFleeDestination(self,gameState):
    x = gameState.getWalls().width/2
    offset = 0
    if self.red:
      x = x - (1+offset)
    else:
      x = x + offset
    minDistance = 9999999
    yMax = gameState.getWalls().height
    for y in xrange(1,yMax):
      if not  gameState.hasWall(x,y):
        distance = self.getMazeDistance(gameState.getAgentPosition(self.index),(x,y))
        if distance < minDistance:
          minDistance = distance
          minY = y
    self.fleeDestination = (x,minY)

  def chooseFleeAction(self, gameState):
    #
    actions = gameState.getLegalActions(self.index)
    
    values = [self.evaluateFlee(gameState, a) for a in actions]
    
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def evaluateFlee(self, gameState, action):
    #
    features = self.getFleeFeatures(gameState, action)
    weights = self.getFleeWeights(gameState, action)
    return features * weights

  def getFleeFeatures(self, gameState, action):
    # features are distancetocenter, nearbyghost?
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    successorState = successor.getAgentState(self.index)
    successorPos = successorState.getPosition()
    minDistance = 99999999
    if self.getMazeDistance(successorPos,self.center) < minDistance:
      #bestAction = action
      minDistance = self.getMazeDistance(successorPos,self.fleeDestination)
    features['distanceToCenter'] = minDistance
    return features

  def getFleeWeights(self, gameState, action):
    #
    return {'distanceToCenter': -1}

#########################################################################33


class Top(DummyAgent):
# go top somehow
  def setCenter(self,gameState):
    #get center of map and maxHeight

    x = gameState.getWalls().width/2
    offset = 1
    if self.red:
      x = x - (1+offset)
    else:
      x = x + offset
    y = gameState.getWalls().height/2
    yMax = gameState.getWalls().height
    yCenter = int(round(yMax/3*2))
    for i in xrange(0,yMax):
      yCandidate = yCenter+i
      if not  gameState.hasWall(x,yCandidate):
        break
      yCandidate = yCenter-i
      if not  gameState.hasWall(x,yCandidate):
        break
    self.center = (x,yCandidate)
    print self.center

  

class Bottom(DummyAgent):
# go bottom somehow
  def setCenter(self,gameState):
    #get center of map and maxHeight
    x = gameState.getWalls().width/2
    offset = 1
    if self.red:
      x = x - (1+offset)
    else:
      x = x + offset
    y = gameState.getWalls().height/2
    yMax = gameState.getWalls().height
    yCenter = int(round(yMax/3))
    for i in xrange(0,yMax):
      yCandidate = yCenter+i
      if not  gameState.hasWall(x,yCandidate):
        break
      yCandidate = yCenter-i
      if not  gameState.hasWall(x,yCandidate):
        break
    self.center = (x,yCandidate)
    print self.center
