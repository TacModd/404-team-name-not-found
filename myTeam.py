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

#######################
# TUNING OF BEHAVIOUR #
#######################

class MonteCarlo:
  DEPTH = 5
  ITERATIONS = 50

class OffensiveWeights:
  STATE_SCORE = 60
  NUM_FOODS = 60
  SUM_DIST_FOOD = -5
  CLOSEST_ENEMY = -10
  TEAMMATE_DIST = -90
  CAPSULE_DIST = 80

class Offence:
  # Go back and save eaten food when eaten more than 4 pieces
  FOOD_LIMIT = 4

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

  ###############################
  # CHOOSE WHICH ACTION TO TAKE #
  ###############################
   
  def chooseAction(self, gameState):

    self.updateOpponentPositions(gameState)
    self.updateOpponentDetected(gameState)
    self.updateDefenceDestination(gameState)
    self.updateBehaviourState(gameState)

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

  ##########################
  # UPDATE DATA ATTRIBUTES #
  ##########################

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
            minDistance, minPosition, minIndex = distance, position, index
      if minIndex == self.index:
        self.opponentDetected = minPosition
        return
      else:
        for position in opponentPositions:
          if not position == minPosition:
            self.opponentDetected = position
            return
    else:
      self.opponentDetected =  None

  def updateOpponentPositions(self, gameState):
    self.opponentPrevPositions = self.opponentPositions.copy()
    self.opponentPositions = self.getOpponentPositionsDict(gameState)

  def updateBehaviourState(self,gameState):
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

  ##################################
  # GET INFORMATION FROM GAMESTATE #
  ##################################

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

  #######################################
  # CALCULATE AND RETURN DESIRED VALUES #
  #######################################

  #returns index, distance to the teammember that are closest to a given position.
  def closestTeammember(self, gameState, position):
    minDistance = 99999
    for index in self.teamIndices:
      distance = self.getMazeDistance(gameState.getAgentPosition(index), position)
      if distance < minDistance:
        minDistance, minIndex = distance, index
    return minIndex,minDistance

  #returns the distance the the closest ghost. 
  #Returns 999 if no ghosts are observable or ghosts are scared for at least 3 more rounds
  def nearestGhostDistance(self,gameState):
    minDistance = 999
    for index in self.opponentIndices:
      if self.opponentPositions[index] != None:
        oppState = gameState.getAgentState(index)
        if gameState.getAgentState(index).scaredTimer > 3:
          print self.index, 'nearestGhostDist scared: ', minDistance
          return minDistance
        distance = self.getMazeDistance(self.opponentPositions[index],gameState.getAgentPosition(self.index))
        if distance < minDistance and not oppState.isPacman:
          minDistance = distance
    return minDistance

  #returns list of positions where opponent ate food the previous round. 
  def foodEatenByOpponent(self, gameState):
    foodEatenByOpponent = []
    for x in range(gameState.getWalls().width):
      for y in range(gameState.getWalls().height):
        if self.prevFoodState[x][y] == True and self.getFoodYouAreDefending(gameState)[x][y] == False and self.inHomeTerritory(gameState, (x,y), 0):
          foodEatenByOpponent = foodEatenByOpponent + [(x,y)]
    self.prevFoodState = self.getFoodYouAreDefending(gameState)
    return foodEatenByOpponent

 ###########################################
 # CHECK IF A SITUATION HAS OCCURED OR NOT #
 ###########################################

  def destinationReached(self,gameState,destination):
    if destination == None:
      return False
    return self.getMazeDistance(gameState.getAgentPosition(self.index),destination) == 0

  def isDead(self, gameState):
    if self.getMazeDistance(gameState.getAgentPosition(self.index),gameState.getInitialAgentPosition(self.index)) <= 2:
      return True 
    return False

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

  def foodInProximity(self,gameState):
    foodList = self.getFood(gameState).asList()
    if len(foodList) <= 0:
      return False
    minDistance = min([self.getMazeDistance(gameState.getAgentState(self.index).getPosition(), food) for food in foodList])
    if minDistance>8:
      return False
    return True
    

  def shouldIAttack(self,gameState):
    minDistance = 99999999
    minTeamIndex = None
    if self.opponentIsDead(gameState):
      for opponentIndex in self.opponentIndices:
        opponentPosition = gameState.getAgentPosition(opponentIndex)
        if opponentPosition != None:
          teamIndex,distance = self.closestTeammember(gameState, opponentPosition)
          if distance < minDistance:
            minDistance, minTeamIndex = distance, teamIndex
    else:
      return False

    if minTeamIndex == None:
      return self.index == min(self.teamIndices)
    elif(self.index) != minTeamIndex:
      return True
    return False

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

  def tooMuchFood(self):
    if self.eatenFood > Offence.FOOD_LIMIT:
      return True
    return False

  def resetFoodCount(self):
    self.eatenFood = 0

  #########################   
  #'GUARD' BEHAVIOUR CODE #
  #########################
  
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
    features = util.Counter()
    successorPosition = self.getSuccessor(gameState, action).getAgentState(self.index).getPosition()
    features['distanceToCenter'] = self.getMazeDistance(successorPosition, self.center)
    return features

  def getGuardWeights(self, gameState, action):
    return {'distanceToCenter': -1} 
  
  ############################
  # 'OFFENCE' BEHAVIOUR CODE #
  ############################
  
  def chooseOffensiveAction(self, gameState):
    # get a list of actions for MonteCarloSearch()
    actions = gameState.getLegalActions(self.index)
    actions.remove(Directions.STOP)
    values = []

    for a in actions:
      successor = self.getSuccessor(gameState, a)
      monValues = self.monteCarloSearch(MonteCarlo.DEPTH, successor, MonteCarlo.ITERATIONS)
      value = sum(monValues)
      values.append(value)

    if not self.foodInProximity(gameState):
    #if not food in proximity, return actions that reduces the distance to the closest piece of food
      minDistance = 999999999
      foodList = self.getFood(gameState).asList()
      for food in foodList:
        distance = self.getMazeDistance(gameState.getAgentPosition(self.index),food)
        if distance<minDistance:
          minDistance, minFood = distance, food
      minDistance = 999999999
      for action in actions:
        position = self.getSuccessor(gameState, action).getAgentState(self.index).getPosition()
        distance = self.getMazeDistance(position,minFood)
        if distance<minDistance:
          minDistance, minAction = distance, action
      bestAction = minAction

    else:
      maxValue = max(values)
      bestActions = [a for a, v in zip(actions, values) if v == maxValue]
      bestAction = random.choice(bestActions)

    successor = self.getSuccessor(gameState, bestAction)
    foodList = self.getFood(gameState).asList()
    successorFoodList = self.getFood(successor).asList()
    if len(successorFoodList) < len(foodList):
        self.eatenFood += 1

    return bestAction

  def monteCarloSearch(self, depth, gameState, iterations):
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
        tree = depth
        while tree > 0:
          actions = searchState.getLegalActions(self.index)
          actions.remove(Directions.STOP)
          rev = Directions.REVERSE[searchState.getAgentState(self.index).configuration.direction]
          if rev in actions and len(actions) > 1:
            actions.remove(rev)
          
          action = random.choice(actions)
          searchState = self.getSuccessor(searchState, action)
          tree -= 1
        endStates.append(searchState)
        
      iterations -= 1
   
    maxval = -100000
    pls = None
    for endState in endStates:
      if self.evaluateOffensive(endState) > maxval:
          maxval = self.evaluateOffensive(endState)
          pls = self.getOffensiveFeatures(endState)
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
    sumFoods, sumDistance = 0, 0
    for food in betterFoodList:
      sumFoods += 1
      sumDistance += self.getMazeDistance(myPos, food)
    features['numFoods'] = sumFoods
    features['sumDistanceToFood'] = sumDistance

    ghostDistance = self.nearestGhostDistance(gameState)
    if ghostDistance == 0:
      ghostDistance = 0.01
    if ghostDistance < 6:
      features['closestEnemy'] = 5 - ghostDistance #float(1)/(5-minDistance**0.5)
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

    return features

  def getOffensiveWeights(self, gameState):
    return {'stateScore': OffensiveWeights.STATE_SCORE, 
            'numFoods': OffensiveWeights.NUM_FOODS, 
            'sumDistanceToFood': OffensiveWeights.SUM_DIST_FOOD, 
            'closestEnemy': OffensiveWeights.CLOSEST_ENEMY, 
            'teammateDistance': OffensiveWeights.TEAMMATE_DIST,
            'closestCapsuleDistance': OffensiveWeights.CAPSULE_DIST}
 
  ############################
  # 'DEFENCE' BEHAVIOUR CODE #
  ############################

  def chooseDefensiveAction(self, gameState):
    # get a list of actions
    actions = gameState.getLegalActions(self.index)
    actions.remove(Directions.STOP)

    for action in actions:
      successorPosition = self.getSuccessor(gameState,action).getAgentState(self.index).getPosition()
      if not self.inHomeTerritory(gameState,successorPosition,0) and not gameState.getAgentState(self.index).isPacman:
        actions.remove(action)

    values = [self.evaluateDefensive(gameState, a) for a in actions]
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
    features = util.Counter()
    successorPosition = self.getSuccessor(gameState, action).getAgentState(self.index).getPosition()
    minDistance = 99999999
    if self.defenceDestination != None and self.getMazeDistance(successorPosition,self.defenceDestination) < minDistance:
      minDistance = self.getMazeDistance(successorPosition, self.defenceDestination)
    features['distanceToCenter'] = minDistance
    return features

  def getDefensiveWeights(self, gameState, action):
    #
    return {'distanceToCenter': -1}

  #########################
  # 'FLEE' BEHAVIOUR CODE #
  #########################

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

#########################################################################

class Top(DummyAgent):
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