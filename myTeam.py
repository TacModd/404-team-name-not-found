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
  This function should return a list of two agents that will form the team, initialized using firstIndex and secondIndex as their agent index numbers.  isRed is True if the red team is being created, and will be False if the blue team is being created.

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

  # def __init__(self):
  #   self.behaviourState = 'Start'

  def registerInitialState(self, gameState):

    CaptureAgent.registerInitialState(self, gameState)
    self.behaviourState = 'Start'
    self.setCenter(gameState)

  def chooseAction(self,gameState):
    # check behaviourState value
    
    # if offensive:
      # call OffensiveBehaviour()
    # elif defensive:
      # call DefensiveBehaviour()
    # else:
      # call StartBehaviour()

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
  
  ''' probs devolve to separate functions '''
  """
  def evaluate():
    # get features
    # get weights
    # return features * weights
    # separate evaluate for each behaviour? or pass extra argument?
  """
    
    
  ###### 'START' BEHAVIOUR CODE ######
  
  def chooseStartAction(self, gameState):
    # get a list of actions
    # get a list of values (call evaluate?) OR call evaluateStart
      # start features/weights (defined in Top/Bottom class?)
    # choose action with best value
    
    # use greedyBFS to get to middle
      # one goes top, one goes bottom (see 'Top' and 'Bottom' classes)
    actions = gameState.getLegalActions(self.index)
    minDistance = 9999999999
    for action in actions:
      successor = self.getSuccessor(gameState, action)
      successorState = successor.getAgentState(self.index)
      successorPos = successorState.getPosition()
      if self.getMazeDistance(successorPos,self.center) < minDistance:
          bestAction = action
          minDistance = self.getMazeDistance(successorPos,self.center)
    return bestAction
      
  def evaluateStart(self, gameState, action):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getStartFeatures(gameState, action)
    weights = self.getStartWeights(gameState, action)
    return features * weights

    
    
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
  
  def evaluateOffensive(self, gameState, action):
    # same as base evaluate function really (see baselineTeam.py)
    features = self.getOffensiveFeatures(gameState, action)
    weights = self.getOffensiveWeights(gameState, action)
    return features * weights

  def getOffensiveFeatures(self, gameState, action):
    # distancetofood, foodeaten, numberfoodcarried, ghost?, capsule?
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['featureName'] = self.getFeatureInfo(successor)

  def getOffensiveWeights(self, gameState, action):
    # what weights?
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
    # enemyagent, enemyagentdistance, ghoststatus, distancetocentre
    # tell it to hover somehow
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['featureName'] = self.getFeatureInfo(successor)

  def getDefensiveWeights(self, gameState, action):
    # what weights?
    return {'featureName': weighting}

#########################################################################33
''' chooseAction function below can probs be deleted '''
"""
  def chooseAction(self, gameState):
    '''
    Picks among actions randomly.
    '''
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)
"""

class Top(DummyAgent):
  # go top somehow
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
    startPos = gameState.getInitialAgentPosition(self.index)
    #Find the closest position y-coordinate given the x-coordinate
    #minYPosition = min([self.getMazeDistance(startPos,(x,y)) for y in xrange(y,yMax-1)])
    minDistance = 99999999999
    for y in xrange(y,yMax):
      if not gameState.hasWall(x,y):
        if self.getMazeDistance(startPos,(x,y)) < minDistance:
          minY = y
          minDistance = self.getMazeDistance(startPos,(x,y))
    self.center = (x,minY)
    print self.center


    

class Bottom(DummyAgent):
  # go bottom somehow
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
    startPos = gameState.getInitialAgentPosition(self.index)
    #Find the closest position y-coordinate given the x-coordinate
    #minYPosition = min([self.getMazeDistance(startPos,(x,y)) for y in xrange(1,y-1)])
    minDistance = 99999999999
    for y in xrange(1,y-1):
      if not gameState.hasWall(x,y):
        if self.getMazeDistance(startPos,(x,y)) < minDistance:
          minY = y
          minDistance = self.getMazeDistance(startPos,(x,y))
    self.center = (x,minY)
    print self.center
    
  


