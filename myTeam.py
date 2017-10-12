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
    self.tooMuchFood = 0
    self.prevFoodState = self.getFoodYouAreDefending(gameState)
    self.opponentIndices = self.getOpponents(gameState)
    self.teamIndices = self.getTeam(gameState)
    self.teammateIndex = self.teamIndices.remove(self.index)
    

  def nextBehaviourState(self):

    if self.behaviourState == 'Start':
      if self.middleReached(gameState):
        self.behaviourState = 'Guard'
      elif self.opponentDetected(gameState):
        self.behaviourState = 'Defence'

    if self.behaviourState == 'Guard':
      #enemyDetected needs to return only if its the closest ghost to enemy, 
      #and return false if distance of one player to enemyPosition is 0
      if self.opponentDetected(gameState):
        self.behaviourState = 'Defence'

    elif self.behaviourState == 'Defence':
      if self.opponentIsDead(gameState, index):
        self.behaviourState = 'Offence'
      elif not opponentDetected(gameState):
        self.behaviourState = 'Guard'

    elif self.behaviourState == 'Offence':
      if self.isDead(gameState, index):
        self.resetFoodCount()
        self.behaviourState == 'Start'
      elif self.tooMuchFood(gameState, index):
        self.behaviourState == 'Flee'

    elif self.behaviourState == 'Flee':
      if self.middleReached(gameState, position):
        self.resetFoodCount()
        self.behaviourState = 'Defence'
      elif self.isDead(gameState, index):
        self.resetFoodCount()
        self.behaviourState = 'Start'

    else:
      print 'State not defined'

  
  def chooseAction(self, gameState):
    # check behaviourState value
    
    # if offensive:
      # call OffensiveBehaviour()
    # elif defensive:
      # call DefensiveBehaviour()
    # else:
      # call StartBehaviour()
      
    #### PLACEHOLDER CHOICES ####
    
    if self.behaviourState == 'Start':
      return self.chooseStartAction(gameState)

    elif self.behaviourState == 'Defence':
      return Directions.STOP

    elif self.behaviourState == 'Offence':
      return Directions.STOP

    elif self.behaviourState == 'Flee':
      return Directions.STOP

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
    
    
  ###### 'OFFENCE' BEHAVIOUR CODE ######
  
  def chooseOffensiveAction(self, gameState):
    # get a list of actions VIA MonteCarloSearch()
    
    # can return actions only and call evaluate here (more design consistent)
    # actions = MonteCarloSearch(gameState)
    # values = [self.evaluate(gameState, a) for a in actions]
    
    # OR can return actions and values (MonteCarlo design more flexible)
    # actions, values = MonteCarloSearch(gameState)
    
    # choose action with best value
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

  def MonteCarloSearch(self, gameState):
    # random searches to get list of actions
    # call evaluate on actions to get list of values
      # get offensive features/weights for each final state only (for now)
    # return actions, values (to chooseOffensiveAction)
    return 
  
  def evaluateOffensive(self, gameState, action):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getOffensiveFeatures(gameState, action)
    weights = self.getOffensiveWeights(gameState, action)
    return features * weights

  def getOffensiveFeatures(self, gameState, action):
    # distancetofood, foodremaining?, ghost?, capsule?/distancetocapsule?
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['featureName'] = self.getFeatureInfo(successor)

  def getOffensiveWeights(self, gameState, action):
    # what weights? check other implementations for a rough idea
    return {'featureName': weighting}
    
    
  ###### 'DEFENCE' BEHAVIOUR CODE ######

  def chooseDefensiveAction(self, gameState):
    # get a list of actions
    actions = gameState.getLegalActions(self.index)
    # get a list of values (call evaluate?) OR call evaluateDefensive
      # evaluate defensive features/weights
    values = [self.evaluate(gameState, a) for a in actions]
    # choose action with best value
    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
  
  def evaluateDefensive(self, gameState, action):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getDefensiveFeatures(gameState, action)
    weights = self.getDefensiveWeights(gameState, action)
    return features * weights

  def getDefensiveFeatures(self, gameState, action):
    # enemyagent, enemyagentdistance, scared? - maybe move to nextBehaviourState function, distancetocentre, reverse, STOP
    # tell it to hover somehow using reverse/STOP
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['featureName'] = self.getFeatureInfo(successor)

  def getDefensiveWeights(self, gameState, action):
    # what weights? check other implementations for a rough idea
    return {'featureName': weighting}

  def foodEatenByOpponent(self, gameState):
    foodEatenByOpponent = []
    for x in range(gameState.getWalls().width):
      for y in range(gameState.getWalls().height):
        if self.prevFoodState[x][y] == True and self.getFoodYouAreDefending(gameState)[x][y] == False:
          opponentEatenFood = ooponentEatenFood + [(x,y)]
    self.prevFoodState = self.getFoodYouAreDefending(gameState)
    return footEatenByOpponent

  def getOpponentPositions(self, gameState):
    opponentPositions = []
    for index in self.opponentIndices:
      if not gameState.getAgentPosition(index) == None:
        opponentPositions = opponentPositions + [gameState.getAgentPosition(index)]
    return opponentPositions

  def closestTeammember(self, gameState, position):
    minDistance = 99999
    for index in self.teamIndices:
      distance = self.getMazeDistance(gameState.getAgentPosition(index), position)
      if distance < minDistance:
        minDistance = distance
        minIndex = index
    return minIndex

  
  def opponentDetected(self,gameState):

    if len(self.getOpponentPositions(gameState)) > 0:
      None 


    foodEatenByOpponent = self.opponentEatenFood(gameState)

    if len(opponentEatenFood) > 0:
      for position in opponentEatenFood:
        None

        # check if you are the nearest teammate
        # update positions to chacee

    return
  
  
###### 'FLEE' BEHAVIOUR CODE ######

def chooseFleeAction(self, gameState):
  return
  #

def evaluateFlee(self, gameState, action):
  #
  return

def getFleeFeatures(self, gameState, action):
  # features are distancetocenter, nearbyghost?
  return

def getFleeWeights(self, gameState, action):
  #
  return

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

  

