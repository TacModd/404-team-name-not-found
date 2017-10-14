#https://github.com/rmit-s3492633-josh-caratelli/AI-2017-S1/blob/17ba9eba44e6b1566c2624dc367fbbfb11fc9481/contest/myTeam.py

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

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint

DEBUG_SEED = random.randint(1, 5)

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
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
  print "SEED: " + str(DEBUG_SEED) + "\n"
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """

  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

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

    foodLeft = len(self.getFood(gameState).asList())

    if foodLeft <= 2:
      bestDist = 9999
      for action in actions:
        successor = self.getSuccessor(gameState, action)
        pos2 = successor.getAgentPosition(self.index)
        dist = self.getMazeDistance(self.start,pos2)
        if dist < bestDist:
          bestAction = action
          bestDist = dist
      return bestAction

    return random.choice(bestActions)

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
    weights={
      'successorScore':1.0,
    }

    for key, value in weights.iteritems():
      weights[key] = value * DEBUG_SEED

    return weights

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  """
  def getFeatures(self, gameState, action):
    # Grabbing useful information
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    foodList = self.getFood(successor).asList()
    enemyDists = [successor.getAgentState(i).getPosition() for i in self.getOpponents(successor)]

    features['successorScore'] = -len(foodList)
    features['foodCollected'] = len(self.getFood(gameState).asList()) - len(foodList)
    myPos = successor.getAgentState(self.index).getPosition()

    # Compute distance to the nearest food
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    # Track enemy positions
    """
    features['enemyDist'] = 999
    if len(enemyDists) > 0:
        for enemy in enemyDists:
          if enemy is not None:
            minDistance = min(self.getMazeDistance(myPos, enemy))
        features['enemyDist'] = minDistance
    """
    return features

  def getWeights(self, gameState, action):
    weights={
      'successorScore': 100,
      'distanceToFood': -1,
      'enemyDist': 1,
      'foodCollected': 50
    }

    for key, value in weights.iteritems():
      weights[key] = value * DEBUG_SEED

    return weights

class DefensiveReflexAgent(ReflexCaptureAgent):
    """
    A reflex agent that keeps its side Pacman-free. Again,
    this is to give you an idea of what a defensive agent
    could be like.  It is not the best or only way to make
    such an agent.
    """
    def chooseAction(self, gameState):
        actions = gameState.getLegalActions(self.index)
        values = [self.evaluate(gameState,a) for a in actions]
        maxValue = max(values)
        bestActions = [a for a, v in zip(actions,values) if v == maxValue]
        return random.choice(bestActions)

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        myState = successor.getAgentState(self.index)
        myPos = myState.getPosition()
        initialPos = successor.getInitialAgentPosition(self.index)
        enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
        invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
        centreOfBoard = (gameState.getWalls().width/2, gameState.getWalls().height/2)


        # Computes distance to closest invader
        if len(invaders) > 0:
            dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
            features['invaderDistance'] = min(dists)



        # Calulating closest enemy if there are no invaders
        if len(invaders) == 0:
            actualEnemyDists = [self.getMazeDistance(myPos, a.getPosition()) for a in enemies if a.getPosition() != None]
            if actualEnemyDists:
                features['enemyDistance'] = min(actualEnemyDists)


        ### TESTING NOISY DISTANCES ###
        if not invaders:
            noisyEnemyDists = []
            noisyDistances = gameState.getAgentDistances()
            for index in self.getOpponents(gameState):
                noisyEnemyDists.append(noisyDistances[index])
                # print "enemy noisy dists: ", noisyEnemyDists
            features['noisyDistance'] = min(noisyEnemyDists)


        # Computes whether we're on defense (1) or offense (0)
        features['onDefense'] = 1
        if myState.isPacman:
             features['onDefense'] = 0

        # Computes number of current invaders we can see
        features['numInvaders'] = len(invaders)


        if action == Directions.STOP:
            features['stop'] = 1

        rev = Directions.REVERSE \
            [gameState.getAgentState(self.index).configuration.direction]
        if action == rev:
            features['reverse'] = 1

        # Compute if currently scared or not
        if myState.scaredTimer > 0:
            features['scared'] = myState.scaredTimer

        # Compute how much food you are defending
        # features['foodToDefend'] = len(self.getFoodYouAreDefending(gameState).asList())


        # If your teammate is also currently defending, stay away from them to cover larger area
        team = self.getTeam(gameState)
        for friend in team:
            if friend != self.index:
                teammate = friend
        friendlyState = successor.getAgentState(teammate)
        if not friendlyState.isPacman:
            friendPos = friendlyState.getPosition()
            distanceFromFriend = self.getMazeDistance(myPos, friendPos)
            features['friendDistance'] = distanceFromFriend


        # Stay away from starting position, encourage ghost to stay near border
        distanceFromStart = self.getMazeDistance(myPos, initialPos)
        features['startDistance'] = distanceFromStart


        # Favour staying in the centre of the board
        distanceFromCentre = self.getMazeDistance(myPos, centreOfBoard)
        features['centreDistance'] = distanceFromCentre

        return features

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        # print "features: ", features
        # print "weights: ", weights
        # print "action: ", action
        # print "features * weights: ", features*weights
        # print "\n"
        return features * weights

    def getWeights(self, gameState, action):
        weights={
            'numInvaders': -1000,
            'onDefense': 5000, # never cross over
            'invaderDistance': -1500, # go towards invaders (closest)
            'enemyDistance': -500, # go towards any enemy (closest)
            'noisyDistance': -400, # go towards probable location (closest)
            'stop': -100,
            'reverse': -2,
            'scared': -100,
            'startDistance': 10, # stay away from start
            'friendDistance': 10, # stay away from friend ##COULD BE IMPROVED##
            'centreDistance': -30 # go towards centre
        }

        for key, value in weights.iteritems():
            weights[key] = value * DEBUG_SEED

        return weights