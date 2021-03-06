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
import util
from util import Queue

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
    self.opponentDetected = None
    for opponentIndex in self.opponentIndices:
      self.opponentPositions[opponentIndex] = None
      self.opponentPrevPositions[opponentIndex] = None

  def updateDefenceDestination(self,gameState):
    if self.destinationReached(gameState, self.defenceDestination):
      self.defenceDestination = self.opponentDetected
    else:
      if self.opponentDetected != None:
        self.defenceDestination = self.opponentDetected
      else:
        if self.defenceDestination == None:
          return 
        elif not self.inHomeTerritory(gameState,self.defenceDestination,0):
          self.defenceDestination = None
        else: 
          return 

  def updateOpponentDetected(self,gameState):
    opponentPositions = self.getOpponentPositionsList(gameState)
    foodEatenByOpponent = self.foodEatenByOpponent(gameState)
    if len(opponentPositions)<2 and len(foodEatenByOpponent)>0:
      if len(opponentPositions) == 0:
        opponentPositions = foodEatenByOpponent
      else:
        for opEatFood in foodEatenByOpponent:
          for opponentPosition in opponentPositions:
            if self.getMazeDistance(opEatFood,opponentPosition) > 1:
              opponentPositions = opponentPositions + [opEatFood]
    if len(opponentPositions) == 1:
      if self.closestTeammember(gameState, opponentPositions[0])[0] == self.index:
        self.opponentDetected = opponentPositions[0]
        return
      else:
        self.opponentDetected = None
        return
    elif len(opponentPositions) > 1:
      minDistance = 99999999
      for position in opponentPositions:
        index, distance = self.closestTeammember(gameState,position)
        if distance < minDistance:
            minDistance = distance
            minPosition = position
            minIndex = index
      if minIndex == self.index:
        self.opponentDetected = minPosition
        return
      else:
        for position in opponentPositions:
          if not position == minPosition:
            self.opponentDetected =  position
            return
    else:
      self.opponentDetected =  None

  def updateOpponentPositions(self, gameState):
    self.opponentPrevPositions = self.opponentPositions.copy()
    self.opponentPositions = self.getOpponentPositionsDict(gameState)

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

  def destinationReached(self,gameState,destination):
    if destination == None:
      return False
    return self.getMazeDistance(gameState.getAgentPosition(self.index),destination) == 0

  def killedOpponent(self, gameState,index):
    for opponentIndex in self.opponentIndices:
      if self.opponentPositions[opponentIndex] == gameState.getInitialAgentPosition(opponentIndex):
        return True
      elif not self.opponentPrevPositions[opponentIndex] == None:
        if self.opponentPositions[opponentIndex] == None and util.manhattanDistance(gameState.getAgentPosition(index), self.opponentPrevPositions[opponentIndex])<2:
          return True
    return False
    
  def opponentIsDead(self, gameState):
    for teamIndex in self.teamIndices:
      if self.killedOpponent(gameState,teamIndex):
        return True
    return False

  def shouldIAttack(self,gameState):
    minDistance = 99999999
    minTeamIndex = None
    if self.opponentIsDead(gameState):
      for opponentIndex in self.opponentIndices:
        opponentPosition = gameState.getAgentPosition(opponentIndex)
        if opponentPosition != None:
          teamIndex,distance = self.closestTeammember(gameState, opponentPosition)
          if distance < minDistance:
            minDistance = distance
            minTeamIndex = teamIndex
    else:
      return False

    if minTeamIndex == None:
      return self.index == min(self.teamIndices)
    elif(self.index) != minTeamIndex:
      return True
    return False

  def isDead(self, gameState):
    if self.getMazeDistance(gameState.getAgentPosition(self.index),gameState.getInitialAgentPosition(self.index)) <= 2:
      return True 
    return False

  def tooMuchFood(self):
    if self.eatenFood > 3:
      return True
    return False

  def resetFoodCount(self):
    self.eatenFood = 0

  def nextBehaviourState(self,gameState):
    self.updateOpponentPositions(gameState)
    self.updateOpponentDetected(gameState)
    self.updateDefenceDestination(gameState)
   
    if gameState.getAgentState(self.index).scaredTimer>10:
      self.behaviourState = 'Offence'

    elif self.behaviourState == 'Guard':
      if not self.defenceDestination == None:
        self.behaviourState = 'Defence'
      elif self.shouldIAttack(gameState):
         self.behaviourState = 'Offence'
      return
     
    elif self.behaviourState == 'Defence':
      if gameState.getAgentState(self.index).isPacman:
        self.behaviourState = 'Flee'
      elif self.shouldIAttack(gameState):
        self.behaviourState = 'Offence'
      elif self.defenceDestination == None:
        self.behaviourState = 'Guard'
      return

    elif self.behaviourState == 'Offence':
      if self.tooMuchFood() or (self.nearestGhostDistance(gameState) <= 3 and gameState.getAgentState(self.index).isPacman):
        self.behaviourState = 'Flee'
      elif not self.defenceDestination == None:# and self.inHomeTerritory(gameState,gameState.getAgentPosition(self.index),0):
        self.behaviourState = 'Defence'
      elif self.isDead(gameState):
        self.resetFoodCount()
        self.behaviourState = 'Guard'
      return

    elif self.behaviourState == 'Flee':
      if self.inHomeTerritory(gameState, gameState.getAgentPosition(self.index),0) or self.isDead(gameState):
        self.resetFoodCount()
        self.behaviourState = 'Guard'
      return

    else:
      self.updateOpponentPositions(gameState)
      self.behaviourState = 'Guard'
    
  def chooseAction(self, gameState):
    self.nextBehaviourState(gameState)
    if self.behaviourState == 'Guard':
      return self.chooseGuardAction(gameState)
    elif self.behaviourState == 'Defence':
      return self.chooseDefensiveAction(gameState)
    elif self.behaviourState == 'Offence':
      return self.chooseOffensiveAction(gameState)
    elif self.behaviourState == 'Flee':
      return self.chooseFleeAction(gameState)
    else:
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
    return successor

  def closestTeammember(self, gameState, position):
    minDistance = 99999
    for index in self.teamIndices:
      distance = self.getMazeDistance(gameState.getAgentPosition(index), position)
      if distance < minDistance:
        minDistance = distance
        minIndex = index
    return minIndex,minDistance
      
  ###### 'GUARD' BEHAVIOUR CODE ######
  
  def chooseGuardAction(self, gameState):
    # use greedyBFS to get to middle
      # one goes top, one goes bottom (see 'Top' and 'Bottom' classes) 
    actions = gameState.getLegalActions(self.index)
    values = [self.evaluateGuard(gameState, a) for a in actions]
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
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
      #monValues = self.MonteCarloSearch(8, successor, 40)
      monValues = self.MonteCarloSearch(5, successor, 50)
      value = sum(monValues)
      values.append(value)
    if not self.FoodInProximity(gameState):
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
      successor = self.getSuccessor(gameState, minAction)
      foodList = self.getFood(gameState).asList()
      successorFoodList = self.getFood(successor).asList()
      if len(successorFoodList) < len(foodList):
        self.eatenFood += 1
      return minAction
    else:
    # choose action with best value
      maxValue = max(values)
      bestActions = [a for a, v in zip(actions, values) if v == maxValue]
      #print 'bestActions:', bestActions
      choice = random.choice(bestActions)
      successor = self.getSuccessor(gameState, choice)
      foodList = self.getFood(gameState).asList()
      successorFoodList = self.getFood(successor).asList()
      if len(successorFoodList) < len(foodList):
        self.eatenFood += 1
      return choice
    
  def FoodInProximity(self,gameState):
    foodList = self.getFood(gameState).asList()
    if len(foodList) > 0:
      minDistance = min([self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), food)
                         for food in foodList])
      if minDistance>8:
        return False
      return True
    return False

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
      #print searchState.getAgentState(self.index).getPosition()
      # if minDistance = 0, we want the action that called MonteCarlo
      if minDistance == 0:
        endStates.append(gameState)
      # otherwise commit to random searches for depth specified
      else:
        tree = depth
        while tree > 0:
          actions = searchState.getLegalActions(self.index)
          # stopping is a waste of time
          actions.remove(Directions.STOP)
          
          # reversing direction is also a waste of time
          rev = Directions.REVERSE[searchState.getAgentState(self.index).configuration.direction]
          if rev in actions and len(actions) > 1:
            actions.remove(rev)
          
          action = random.choice(actions)
          #print(action)
          searchState = self.getSuccessor(searchState, action)

          tree -= 1
        endStates.append(searchState)
        #print searchState.getAgentState(self.index).getPosition()
      iterations -= 1
    # return values (to chooseOffensiveAction)
    maxval = -100000
    pls = None
    for endState in endStates:
      if self.evaluateOffensive(endState) > maxval:
          maxval = self.evaluateOffensive(endState)
          pls = self.getOffensiveFeatures(endState)
    return [self.evaluateOffensive(endState) for endState in endStates]

  def nearestGhostDistance(self,gameState):
    minDistance = 999999
    for index in self.opponentIndices:
      if self.opponentPositions[index] != None:
        oppState = gameState.getAgentState(index)
        distance = self.getMazeDistance(self.opponentPositions[index],gameState.getAgentPosition(self.index))
        
        if gameState.getAgentState(index).scaredTimer > 0:
          distance = distance*1000
        if oppState.isPacman:
          distance = distance*1000
        if distance < minDistance:
          minDistance = distance
    return minDistance
  
  def evaluateOffensive(self, gameState):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getOffensiveFeatures(gameState)
    weights = self.getOffensiveWeights(gameState)
    #print features * weights
    return features * weights
  
  def getOffensiveFeatures(self, gameState):
    # distancetofood, foodremaining?, ghost?, capsule?/distancetocapsule?
    features = util.Counter()

    foodList = self.getFood(gameState).asList()
    features['stateScore'] = -len(foodList)

    myPos = gameState.getAgentState(self.index).getPosition()
    betterFoodList = [f for f in foodList if self.getMazeDistance(myPos, f) <= 8]
    #print betterFoodList
    sumFoods = 0
    sumDistance = 0
    for food in betterFoodList:
      sumFoods += 1
      sumDistance += self.getMazeDistance(myPos, food)
    features['numFoods'] = sumFoods
    features['sumDistanceToFood'] = sumDistance

    #Calculate Distance to nearest ghost
    minDistance = 999999
    for index in self.opponentIndices:
      if self.opponentPositions[index] != None:
        oppState = gameState.getAgentState(index)
        distance = self.getMazeDistance(self.opponentPositions[index],gameState.getAgentPosition(self.index))
        
        if gameState.getAgentState(index).scaredTimer > 0:
          distance = distance*1000
        if oppState.isPacman:
          distance = distance*1000
        if distance < minDistance:
          minDistance = distance
    if minDistance == 0:
      minDistance = 0.01
    if minDistance < 6:
      features['closestEnemy'] = 5 - minDistance #float(1)/(5-minDistance**0.5)
    else:
      features['closestEnemy'] = 0 #float(1)/(5**0.5)

    distance = self.getMazeDistance(gameState.getAgentPosition(self.teammateIndex[0]),gameState.getAgentPosition(self.index))
    if distance > 0:
      features['teammateDistance'] = float(1)/distance
    else:
      features['teammateDistance'] = 5

    capsules = self.getCapsules(gameState)
    minDistance = 9999999
    for capsule in capsules:
      distance =self.getMazeDistance(gameState.getAgentPosition(self.index), capsule)
      if distance < minDistance:
        minDistance = distance
    if minDistance == 0:
      minDistance = 0.01
    if minDistance > 1000:
      features['closestCapsuleDistance'] = 1
    else: 
      features['closestCapsuleDistance'] = float(1)/minDistance

    # distance = self.getMazeDistance(gameState.getAgentPosition(self.teammateIndex[0]),gameState.getAgentPosition(self.index))
    # if distance > 0:
    #   features['teammateDistance'] = float(1)/distance
    # else:
    #   features['teammateDistance'] = 5

    return features

  def getOffensiveWeights(self, gameState):
    # what weights? check other implementations for a rough idea
    #return {'stateScore': 60, 'numFoods': 60, 'sumDistanceToFood': -5, 'closestEnemy': -400, 'teammateDistance': -30,'closestCapsuleDistance': 40}
    return {'stateScore': 60, 'numFoods': 60, 'sumDistanceToFood': -5, 'closestEnemy': -10, 'teammateDistance': -90,'closestCapsuleDistance': 80}
 
  ###### 'DEFENCE' BEHAVIOUR CODE ######

  def inHomeTerritory(self,gameState,position,offset):
    homeX = gameState.getWalls().width/2
    if self.red:
      homeX = homeX - (1+offset)
    else:
      homeX = homeX + offset

    if self.red and position[0] > homeX:
      return False
    elif not self.red and position[0] < homeX:
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
      if not self.inHomeTerritory(gameState,successorPos,0) and not gameState.getAgentState(self.index).isPacman:
        actions.remove(action)
    # get a list of values (call evaluate?) OR call evaluateDefensive
      # evaluate defensive features/weights
    values = [self.evaluateDefensive(gameState, a) for a in actions]
    # choose action with best value
    if len(values) > 0:
      maxValue = max(values)
    else:
      return Directions.STOP
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    return random.choice(bestActions)

  def evaluateDefensive(self, gameState, action):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getDefensiveFeatures(gameState, action)
    weights = self.getDefensiveWeights(gameState, action)
    return features * weights

  def getDefensiveFeatures(self, gameState, action):
    # distanceToCenter
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    successorState = successor.getAgentState(self.index)
    successorPos = successorState.getPosition()
    minDistance = 99999999
    if (not self.defenceDestination == None) and self.getMazeDistance(successorPos,self.defenceDestination) < minDistance:
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
        if self.prevFoodState[x][y] == True and self.getFoodYouAreDefending(gameState)[x][y] == False and self.inHomeTerritory(gameState, (x,y), 0):
          foodEatenByOpponent = foodEatenByOpponent + [(x,y)]
    self.prevFoodState = self.getFoodYouAreDefending(gameState)
    return foodEatenByOpponent

  ###### 'FLEE' BEHAVIOUR CODE ######

  def chooseFleeAction(self, gameState):
    #
    q = Queue()
    q.push((gameState, []))
    visited = []
    i = 0
    while not q.isEmpty():
      i = i+1
      state, route = q.pop()
      if self.nearestGhostDistance(state) <= 1 and state != gameState:
        continue
      elif state.getAgentPosition(self.index) in visited:
        continue
      elif self.inHomeTerritory(state,state.getAgentPosition(self.index),0):
        if len(route) == 0:
          return Directions.STOP
        else:
          return route[0]
      visited = visited + [state.getAgentPosition(self.index)]
      actions = state.getLegalActions(self.index)
      rev = Directions.REVERSE[state.getAgentState(self.index).configuration.direction]
      if rev in actions and len(actions) > 1 and i!=1:
        actions.remove(rev)
      for action in actions:
        q.push((self.getSuccessor(state,action),route+[action]))
    return random.choice(gameState.getLegalActions(self.index))

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
    yCenter = int(round(yMax/4*3))
    for i in xrange(0,yMax):
      yCandidate = yCenter+i
      if yCandidate <= yMax and yCandidate > 0:
        if not gameState.hasWall(x,yCandidate):
          break
      yCandidate = yCenter-i
      if yCandidate <= yMax and yCandidate > 0:
        if not  gameState.hasWall(x,yCandidate):
          break
    self.center = (x,yCandidate)

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
    yCenter = int(round(yMax/4))
    for i in xrange(0,yMax):
      yCandidate = yCenter+i
      if yCandidate <= yMax and yCandidate > 0:
        if not  gameState.hasWall(x,yCandidate):
          break
      yCandidate = yCenter-i
      if yCandidate <= yMax and yCandidate > 0:
        if not  gameState.hasWall(x,yCandidate):
          break
    self.center = (x,yCandidate)