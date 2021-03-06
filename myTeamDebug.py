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
    self.behaviourState = 'Start'
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


    '''
    print 'self.defenceDestination', self.defenceDestination
    if self.destinationReached(gameState,self.defenceDestination) == False and not self.opponentDetected(gameState) == None:
      self.defenceDestination = self.opponentDetected(gameState)
      print 'a'
    elif self.destinationReached(gameState,self.defenceDestination) == False and self.opponentDetected(gameState) == None and not self.defenceDestination == None:
      if not self.inHomeTerritory(gameState,self.defenceDestination,-1):
        self.defenceDestination = None
        print 'b'
    elif self.destinationReached(gameState,self.defenceDestination) == True and self.opponentDetected(gameState) == self.defenceDestination:
      self.defenceDestination = None
      print 'c'
      #self.opponentIsDead = True
    elif self.destinationReached(gameState,self.defenceDestination) == True and not (self.opponentDetected(gameState) == self.defenceDestination or self.opponentDetected(gameState) == None):
      self.defenceDestination = self.opponentDetected(gameState)
      #self.opponentIsDead = True
      print 'd'
    elif self.destinationReached(gameState,self.defenceDestination) == True and not self.opponentDetected(gameState) == None:
      self.defenceDestination = None
      #self.opponentIsDead = True
      print 'e'
    else:
      print 'f'
      return 
    '''

  def opponentIsDead(self, gameState):

    '''
    for position in self.opponentPrevPositions:
      if gameState.getAgentPosition(self.index) == position and self.inHomeTerritory(gameState, gameState.getAgentPosition(self.index), -1):
        return True
    return False

    '''
    for index in self.opponentIndices:
      if self.opponentPositions[index] == gameState.getInitialAgentPosition(index):
        return True
      elif not self.opponentPrevPositions[index] == None:
        if self.opponentPositions[index] == None and util.manhattanDistance(gameState.getAgentPosition(self.index), self.opponentPrevPositions[index])<2:
          return True
    return False

  def isDead(self, gameState):
    if gameState.getAgentPosition(self.index) == gameState.getInitialAgentPosition(self.index):
      return True 
    return False

  def tooMuchFood(self):
    if self.eatenFood > 0:
      return True
    return False

  def resetFoodCount(self):
    self.eatenFood = 0

  def updateOpponentPositions(self, gameState):
    self.opponentPrevPositions = self.opponentPositions.copy()
    self.opponentPositions = self.getOpponentPositionsDict(gameState)

  def nextBehaviourState(self,gameState):
    #defenceDestinationCandidate = self.opponentDetected(gameState)
    print ''
    print self.index

    self.updateOpponentPositions(gameState)
    self.updateDefenceDestination(gameState)

    if self.behaviourState == 'Start':
      if self.destinationReached(gameState,self.center):
        self.behaviourState = 'Guard'
      elif not self.defenceDestination == None:
        self.behaviourState = 'Defence'
      else:
        return

    elif self.behaviourState == 'Guard':
      if not self.defenceDestination == None:
        self.behaviourState = 'Defence'
      else:
        return

    elif self.behaviourState == 'Defence':
      if self.opponentIsDead(gameState):
         self.behaviourState = 'Offence'
      elif self.defenceDestination == None:
        self.behaviourState = 'Start'
      else:
        return

    elif self.behaviourState == 'Offence':
      if self.isDead(gameState):
        self.resetFoodCount()
        self.behaviourState = 'Start'
      elif self.tooMuchFood():
        self.behaviourState = 'Flee'
        return 
      else:
        return

    elif self.behaviourState == 'Flee':
      #if self.middleReached(gameState, position):
      if self.inHomeTerritory(gameState, gameState.getAgentPosition(self.index),-1) or self.isDead(gameState):
        self.resetFoodCount()
        self.behaviourState = 'Start'
      else:
        return

    else:
      print 'State not defined'
      self.behaviourState = 'Guard'

    print self.behaviourState

    
  
  def chooseAction(self, gameState):
    # check behaviourState value
    
    # if offensive:
      # call OffensiveBehaviour()
    # elif defensive:
      # call DefensiveBehaviour()
    # else:
      # call StartBehaviour()
      
    #### PLACEHOLDER CHOICES ####

    self.nextBehaviourState(gameState)
    print self.behaviourState
    if self.behaviourState == 'Start':
      return self.chooseStartAction(gameState)
    elif self.behaviourState == 'Guard':
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
    
    
  ###### 'START' BEHAVIOUR CODE ######
  
  def chooseStartAction(self, gameState):
    # use greedyBFS to get to middle
      # one goes top, one goes bottom (see 'Top' and 'Bottom' classes)
    
    actions = gameState.getLegalActions(self.index)
    
    values = [self.evaluateStart(gameState, a) for a in actions]
    
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    
    #return bestAction
    return random.choice(bestActions)
      
  def evaluateStart(self, gameState, action):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getStartFeatures(gameState, action)
    weights = self.getStartWeights(gameState, action)
    return features * weights

  def getStartFeatures(self, gameState, action):
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

  def getStartWeights(self, gameState, action):
    #
    return {'distanceToCenter': -1}

  ###### 'GUARD' BEHAVIOUR CODE ######
  def chooseGuardAction(self, gameState):
    return Directions.STOP
    
  ###### 'OFFENCE' BEHAVIOUR CODE ######
  
  def chooseOffensiveAction(self, gameState):
    # get a list of actions VIA MonteCarloSearch()
    
    # can return actions only and call evaluate here (more design consistent)
    # need to get a bunch of actions for multiple searches
    # actions = MonteCarloSearch(gameState)
    # values = [self.evaluate(gameState, a) for a in actions]
    originalState = gameState
    actions = gameState.getLegalActions(self.index)
    actions.remove(Directions.STOP)
    
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if rev in actions and len(actions) > 1:
      actions.remove(rev)
    values = []
    for a in actions:
      successor = self.getSuccessor(gameState, a)
      value = sum(self.MonteCarloSearch(6, successor, 72))
      values.append(value)
    

    # OR can return actions and values (MonteCarlo design more flexible)
    
    # choose action with best value
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    choice = random.choice(bestActions)
    successor = self.getSuccessor(gameState, choice)
    foodList = self.getFood(gameState).asList()
    successorFoodList = self.getFood(successor).asList()
    if len(successorFoodList) < len(foodList):
      print 'eat food'
      self.eatenFood += 1
    return choice
    
    

  def MonteCarloSearch(self, depth, gameState, iterations):
    # random searches to get list of actions
    searchState = None
    # call evaluate on actions to get list of values
      # get offensive features/weights for each final state only (for now)
    # return actions, values (to chooseOffensiveAction)
    endStates = []
    while iterations > 0:

      searchState = gameState.deepCopy()

      while depth > 0:
        actions = searchState.getLegalActions(self.index)
        actions.remove(Directions.STOP)

        rev = Directions.REVERSE[searchState.getAgentState(self.index).configuration.direction]
        if rev in actions and len(actions) > 1:
          actions.remove(rev)

        a = random.choice(actions)
        searchState = self.getSuccessor(searchState, a)

        depth -= 1

      endStates.append(searchState)
      iterations -= 1
      
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
    betterFoodList = [f for f in foodList if self.getMazeDistance(myPos, f) <= 6]
    sumDistance = 0
    for food in foodList:
      sumDistance += self.getMazeDistance(myPos, food)
    features['sumDistanceToFood'] = sumDistance
    
    return features

  def getOffensiveWeights(self, gameState):
    # what weights? check other implementations for a rough idea
    return {'stateScore': 100, 'sumDistanceToFood': -3}
    
    
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
    self.teamIndices.sort()
    for index in self.teamIndices:
      distance = self.getMazeDistance(gameState.getAgentPosition(index), position)
      if distance < minDistance:
        minDistance = distance
        minIndex = index
    return minIndex,minDistance

  
  def opponentDetected(self,gameState):

    opponentPositions = self.getOpponentPositionsList(gameState)
    foodEatenByOpponent = self.foodEatenByOpponent(gameState)
    print 'foodEatenByOpponent', foodEatenByOpponent
    if len(opponentPositions)<2 and len(foodEatenByOpponent)>0:
      for opEatFood in foodEatenByOpponent:
        for opponentPosition in opponentPositions:
          if self.getMazeDistance(opEatFood,opponentPosition) > 1:
            opponentPositions = opponentPositions + [opEatFood]

    print 'opponentPositions', opponentPositions

    if len(opponentPositions) == 1:
      for position in opponentPositions:
        if self.closestTeammember(gameState, position)[0] == self.index:
          print '1 opponentDetected', position
          return position
    elif len(opponentPositions) > 1:
      minDistance = 99999999
      for position in opponentPositions:
        #print 'pos in opponentPos', position
        index, distance = self.closestTeammember(gameState,position)
        #print 'dist, pos, index', distance, position, index
        if distance < minDistance:
            minDistance = distance
            minPosition = position
            minIndex = index
      #print 'MIN dis, pos, index', minDistance, minPosition, minIndex
      if minIndex == self.index:
        print '2 opponentDetected', minPosition
        return minPosition
      else:
        #print 'opponentPos', opponentPositions
        for positions in opponentPositions:
          #print 'pos, minPos', position, minPosition
          if not position == minPosition:
            print '3 opponentDetected', position
            return position
    return None
  
###### 'FLEE' BEHAVIOUR CODE ######

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
      minDistance = self.getMazeDistance(successorPos,self.center)
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