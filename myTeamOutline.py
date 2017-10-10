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
               first = 'DummyAgent', second = 'DummyAgent'):
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

  def tempChooseAction():
    # get a list of actions
    # get a list of values (call evaluate?)
    # choose action with best value

  def evaluate():
    # get features
    # get weights
    # return features * weights

  def getSuccessor():
    #
  
  def FigureOutBehaviour():
    # figure out behaviour
      # 'start' behaviour until middle reached (stack ends?)
      # defensive default (BOTH) once 'start' phase ends
      # if enemy pacman eaten BOTH switch to offensive
      # check value

    # if offensive:
      # call OffensiveBehaviour()
    # elif defensive:
      # call DefensiveBehaviour()
    # else:
      # call StartBehaviour()

  def StartBehaviour():
    # use greedyBFS to get to middle
      # one goes top, one goes bottom (see 'Top' and 'Bottom' classes)

  def getStartFeatures():
    #

  def getStartWeights():
    #
    
  def OffensiveBehaviour():
    # call MonteCarlo algorithm to get final state scores
    # call evaluate on returned list of final scores?
    # return best score to chooseAction()?

  def MonteCarloSearch():
    # random searches
    # get offensive features/weights for each final state only (for now)

  def getOffensiveFeatures():
    # distancetofood, foodeaten, numberfoodcarried, ghost?, capsule?

  def getOffensiveWeights():
    # what weights?

  def DefensiveBehaviour():
    # get defensive features/weights
    # return scores to chooseAction()

  def getDefensiveFeatures():
    # enemyagent, enemyagentdistance, ghoststatus, distancetocentre
    # tell it to hover somehow

  def getDefensiveWeights():
    # what weights?


    

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """
    actions = gameState.getLegalActions(self.index)

    '''
    You should change this in your own agent.
    '''

    return random.choice(actions)

class Top(DummyAgent):
  # go top somehow

class Bottom(DummyAgent):
  # go bottom somehow

