#https://github.com/calrhino/CaptureThePacMan/blob/c91d91e4d43259eb46966bee0876d98f5e443064/myTeam.py
# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
from capture import GameState
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveAgent', second = 'DefensiveAgent'):
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
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    actions = gameState.getLegalActions(self.index)

    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)
    # tried to implement expectmax but couldn't
    # newvalue = float('-Infinity')                 #assign the newvalue to negative infinity
    # treeDepth = 1
    # for a in gameState.getLegalActions(self.index):           # for the actions in the gameState legal actions
    #   succ = self.getSuccessor(gameState,a)
    #   oldvalue = newvalue                           # assign the old value to the new value
    #   newvalue = max(newvalue, self.expectValue(succ, treeDepth)) #new value will be the max of new value and the 
    #                                               #minValue with gameState successor, treeDepth and 1 ghost
    #   if newvalue > oldvalue: # if the new value is bigger than the old value to make sure it is a good and legal action
    #     action = a             #have to do this to find the max of an action in a loop

    # return action #returns the action

  #tried to implement
  def maxValueExpect(gameState, treeDepth):
       # terminal state
      if treeDepth == 0:
        return self.evaluate(gameState,Directions.STOP)     #returns the heuristic value of the node

      value = float("-Infinity")
      for a in gameState.getLegalActions(self.index):          #for actions in the legal actions of pacman
        succ = self.getSuccessor(0,a)
        bestActions = max(value, self.expectValue(succ, treeDepth, 1)) #find the max of value and expectValue with its succ, treeDepth, and a ghost

      return bestActions

    # agent will no longer take min over all ghost actions, but the expectation according to your agent's model of how the ghosts act
  def expectValue(gameState, treeDepth, ghost):
      if treeDepth == 0:
        return self.evaluate(gameState,Directions.STOP)     #returns the heuristic value of the node, which is evaluationFunction

      value = float('Infinity')
      totalAgents = gameState.getNumAgents()-1      #assign total Agents to num of ghosts by gameState.getNumAgents -1
      ghostMoves = gameState.getLegalActions(self.index)
      ghostMovesNum = len(ghostMoves)          #this helps to determine how the ghost will act by getting the int of ghostMoves
      
      for a in ghostMoves:                     #for the actions in the legal actions of the ghosts 
        if self.index == totalAgents:               #if the ghost is equal to the total agents, then find the min of value and maxValue
          succ = gameState.generateSuccessor(self.index,a)
          value = min(value, maxValueExpect(succ, treeDepth-1)) # the minus one prevent the exceeding the maximum recursion depth 
        else:
          succ = gameState.generateSuccessor(self.index,a)    #if it is not equal, then add one to the ghost and run expectValue again
          value = min(value, expectValue(succ, treeDepth, self.index+1)) 
      
      return (value+ghostMovesNum)      #the value which is expectation of the min + the ghostMovesNum, which how the ghost may act.

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor) #compute the score from the successor state
    myPos = successor.getAgentState(self.index).getPosition()

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    #get the enemies and its state
    enemies = [successor.getAgentState(e) for e in self.getOpponents(successor)]
    
    #find the ghost in the enemies
    ghosts = [ghost for ghost in enemies if ghost.isPacman and ghost.getPosition() != None]
    #find the invaders in the rank of the enemies
    invaders = [invader for invader in enemies if invader.isPacman and invader.getPosition() != None]
    
    #find the enemies position and try to avoid them
    invaderLength = len(invaders)
    if invaderLength == 0:
      #find the ghosts position
      for g in ghosts:
        ghostPos = [g.getPosition()]
      
    else:
      #find the invaders position
      for i in invaders:
        invadePos = [i.getPosition()]

    # find the invader if it is near the offensive pacman. It seems to trap but not kill
    if invaderLength!= 0 and not successor.getAgentState(self.index).isPacman:
        #see the invader position
        for invadePacman in invadePos:
          maze = self.getMazeDistance
          distanceToPacman = min([maze(myPos, invadePacman)])
          #trap the pacman
        if distanceToPacman <= 1:
            features['trapInvader'] = distanceToPacman
    
    return features

  def getWeights(self, gameState, action):
    return {'trapInvader': 80,'successorScore': 100, 'distanceToFood': -1}

class DefensiveAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()
    foodList = self.getFood(successor).asList() #tries to guard the food area

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # Computes distance to invaders we can see
    # get the enemies position
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    #find the invaders
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    
    features['numInvaders'] = len(invaders)
    #if there are invaders in our side
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)
    
    #invade pacman but doesnt
    ghosts = [ghost for ghost in enemies if ghost.isPacman and ghost.getPosition() != None]
    #find the invaders in the rank of the enemies
    # invaders = [invader for invader in enemies if invader.isPacman and invader.getPosition() != None]
    
    # #find the enemies position and try to avoid them
    # invaderLength = len(invaders)
    # if invaderLength == 0:
    #   #find the ghosts position
    #   for g in ghosts:
    #     ghostPos = [g.getPosition()]
      
    # else:
    #   #find the invaders position
    #   for i in invaders:
    #     invadePos = [i.getPosition()]

    # # find the invader if it is near the offensive pacman. It seems to trap but not kill
    # if invaderLength!= 0:
    #     for invadePacman in invadePos:
    #       maze = self.getMazeDistance
    #       distanceToPacman = min([maze(myPos, invadePacman)])
    #     if distanceToPacman <= 1:
    #         features['stopInvader'] = distanceToPacman
    

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': -10, 'stop': -100, 'reverse': -2}