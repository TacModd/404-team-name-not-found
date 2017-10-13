# https://github.com/Liuqian0501/pacman/blob/da59801062e2dbfa58cb1e80d12666fe3cb02230/contest/Kevin.py
# MyTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint
SIGHT_RANGE = 5
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

  def betterEvaluationFunction(self,gameState,length):
      """
        Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
        evaluation function (question 5).
    
        DESCRIPTION: <write something here so we know what you did>
      """
      "*** YOUR CODE HERE ***"
      if length != 1:
         features = self.getFeaturesSmart(gameState)
         weights = self.getWeightsSmart(gameState) 
      else :
        features = self.getFeaturesHungry(gameState)
        weights = self.getWeightsHungry(gameState) 
      return features * weights

          
  
  
  def value(self, state, agent, depth, alpha, beta, opponent): 
        length = len(opponent)
        
        agent = agent % length
        if opponent[agent]==self.index:
            agent = 0
            depth += 1

        if self.isTerminal(state, depth, opponent[agent],length):
            return self.betterEvaluationFunction(state,length)

        if opponent[agent]==self.index:
            return self.maxValue(state, agent, depth, alpha, beta,opponent)
        else:
            return self.minValue(state, agent, depth, alpha, beta,opponent)

  def minValue(self,state, agent, depth, alpha, beta,opponent):
        v = ("unknown", float("inf"))
        length = len(opponent)
        if self.isTerminal(state, depth, opponent[agent],length):
            return self.betterEvaluationFunction(state,length)

        for action in state.getLegalActions(opponent[agent]):

            
            Val = self.value(state.generateSuccessor(opponent[agent], action), agent + 1, depth, alpha, beta,opponent)
            if type(Val) is tuple:
                Val = Val[1] 

            NewVal = min(v[1], Val)

            if NewVal is not v[1]:
                v = (action, NewVal) 
            
            if v[1] <= alpha:
                return v
            
            beta = min(beta, v[1])

        return v
    
  def maxValue(self,state, agent, depth, alpha, beta,opponent):
        v = ("unknown", float("-inf"))
        length = len(opponent)
        if self.isTerminal(state, depth, opponent[agent],length):
            return self.betterEvaluationFunction(state,length)

        for action in state.getLegalActions(opponent[agent]):
#             if action == "Stop":
#                 continue
            
            Val = self.value(state.generateSuccessor(opponent[agent], action), agent + 1, depth, alpha, beta,opponent)
            if type(Val) is tuple:
                Val = Val[1] 

            NewVal = max(v[1], Val)

            if NewVal is not v[1]:
                v = (action, NewVal) 
            
            if v[1] >= beta:
                return v

            alpha = max(alpha, v[1])

        return v

  
  
  def isTerminal(self, state, depth, agent,length):
      if length ==1:
          return depth == 4 or state.isOver() 
      else :
          return depth == 4 or state.isOver() 


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

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
 

 
  
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    self.opponents=[]
    self.InvadePacman=[]
    
    for i in self.getOpponents(gameState):
        if not gameState.getAgentState(i).isPacman: 
            position =gameState.getAgentState(i).getPosition()
            if position != None:
                if util.manhattanDistance(position, gameState.getAgentPosition(self.index)) <= SIGHT_RANGE:
                    self.opponents.append(i)

        else:
            position =gameState.getAgentState(i).getPosition()
            if position != None:
                self.InvadePacman.append(i)
            
    self.opponents.insert(0,self.index)
    self.InvadePacman.insert(0,self.index)
    
    if gameState.getAgentState(self.index).isPacman: 
        action,_ = self.value(gameState, 0, 0, float("-inf"), float("inf"),self.opponents)

    else :
        action,_ = self.value(gameState, 0, 0, float("-inf"), float("inf"),self.InvadePacman)
    
    return action
    

        
  def getFeaturesHungry(self, gameState):
    

    # Compute distance to the nearest food in largest foodgroup
    enemyghost=[]
    enemyPacman = []
    teammate=[]
    for i in self.getOpponents(gameState):
                    if not gameState.getAgentState(i).isPacman:       
                            enemyghost.append(i)
                    else:
                        enemyPacman.append(i)
                        
    myState=gameState.getAgentState(self.index)
    myPos = myState.getPosition()
    foodList = self.getFood(gameState).asList()
    minDistanceToFoodGroup = min([self.getMazeDistance(myPos, food) for food in foodList])
    
    for i in self.getTeam(gameState):
                    if gameState.getAgentState(i).isPacman: 
                        if i!=self.index :     
                            teammate.append(i)
                   

    
    
    # Compute distance to the nearest food  in largest food group we are defending
    DefendingfoodList = self.getFoodYouAreDefending(gameState).asList()  
    minDistanceToDFoodGroup = min([self.getMazeDistance(myPos, food) for food in DefendingfoodList])
    
    
    #position of capsules
    capsules=self.getCapsules(gameState)
    owncapsules=self.getCapsulesYouAreDefending(gameState) 
 
    features = util.Counter()
    
    features['successorScore'] = self.getScore(gameState)
    
    
    #go eating at arriving
    if myState.isPacman:
        features['distanceToTarget'] = 0
        features['distanceToFoodGroup'] = minDistanceToFoodGroup
        if features['successorScore']<5:
            features['Fighting'] = 1

        else:
            features['Attacking'] = 1

    
    features['foodNum'] = len(foodList)  
    
    if not myState.isPacman:
        features['distanceToFoodGroup'] = 0
        
        #offensing through the weak side           
        if not self.red:
            features['distanceToTarget'] = self.getMazeDistance(myPos, (11.0,2.0))
        else :
            features['distanceToTarget'] = self.getMazeDistance(myPos, (19.0,13.0))
    
    features['DfoodNum'] = len(DefendingfoodList)    

    features['distanceToDFoodGroup'] = 0
  
    #whether eat capsule
    features['Capsule'] = 0

    #whether to play def
    features['onDefense'] = 0

    if not len(capsules) > 0:  
        features['Capsule'] = 1
        if len(enemyghost) == 0: 
            features['Capsule'] = -0.01
        else:
            for team in teammate:
                for i in enemyghost:
                    position = gameState.getAgentState(i).getPosition()
                    if gameState.getAgentState(i).getPosition() != None:
                        if util.manhattanDistance(position, gameState.getAgentPosition(team)) <= SIGHT_RANGE:        
                                features['Capsule'] = -1
        
        # If we are winning the game, keep eating dots if agent is pacman, def as a ghost, target will not change whening losing
        if self.getScore(gameState)>13:
            
            #if  reborned then play as def ghost
            if not myState.isPacman:
                features['onDefense'] = 1
                print "play Def"
                #if we still have own capsule, defence it
                if len(owncapsules)>0:
                     minDistance = min([self.getMazeDistance(myPos, capsule) for capsule in owncapsules])
                     features['distanceToTarget'] = minDistance
                else:
                    # find the group with the most food
                    features['distanceToDFoodGroup'] = minDistanceToDFoodGroup
    if gameState.isOver():
        features['over'] = 1
    
    return features    
  
  def getWeightsHungry(self, gameState):

        return {'successorScore': 300,'distanceToTarget':-3,'foodNum':-100,'distanceToFoodGroup':-2,'DfoodNum':100, 
                'distanceToDFoodGroup':-2,'Capsule':-5000,'Fighting':10000,'Attacking':200,'onDefense':10000,
                'over':100000}
  
  def getFeaturesSmart(self, gameState):
    
    
    enemyghostSaw=[]
    enemyPacman=[]
    
    for i in self.getOpponents(gameState):
        position = gameState.getAgentState(i).getPosition()
        if position != None:
                    if not gameState.getAgentState(i).isPacman:
                        if util.manhattanDistance(position, gameState.getAgentPosition(self.index)) <= SIGHT_RANGE:         
                            enemyghostSaw.append(i)
                    else:
                        enemyPacman.append(i)
    
    
    
    # Compute distance to the nearest food in largest foodgroup
    myState=gameState.getAgentState(self.index)
    myPos = myState.getPosition()
    foodList = self.getFood(gameState).asList()
    minDistanceToFoodGroup = min([self.getMazeDistance(myPos, food) for food in foodList])
    
    
    # Compute distance to the nearest food  in largest food group we are defending
    DefendingfoodList = self.getFoodYouAreDefending(gameState).asList()       
    minDistanceToDFoodGroup = min([self.getMazeDistance(myPos, food) for food in DefendingfoodList])
    
    
    #position of capsules
    capsules=self.getCapsules(gameState)
    owncapsules=self.getCapsulesYouAreDefending(gameState)   

      
    features = util.Counter()

    features['successorScore'] = self.getScore(gameState)


    # Compute distance to the nearest food
    features['foodNum'] = len(foodList)
    features['distanceToFoodGroup'] = minDistanceToFoodGroup

    
    # Compute distance to the nearest Enemy
    EnemyGhostPositionList = []
    EatableEnemyPositionList = []
    EnemyPacmanPositionList = []
    
   
    for i in enemyghostSaw:
        position = gameState.getAgentState(i).getPosition()
        if gameState.getAgentState(i).scaredTimer > 0:  
            EatableEnemyPositionList.append(position)
        else:
            EnemyGhostPositionList.append(position )


            
    for i in enemyPacman:
        position = gameState.getAgentState(i).getPosition()
        if gameState.getAgentState(i).getPosition() != None:
                EnemyPacmanPositionList.append(position )
    
       
    if myState.isPacman:
        features['HeroAlive'] = 1
    else:
        features['HeroAlive'] = 0
    
    features['PacmanAlive']=len(enemyPacman)
    
    
    

    if len(EnemyGhostPositionList) > 0: 
        minDistance = min([self.getMazeDistance(myPos, pos) for pos in EnemyGhostPositionList])
        features['distanceToEnemyGhost'] = minDistance 
    
     
    if len(EatableEnemyPositionList) > 0: 
        minDistance1 = min([self.getMazeDistance(myPos, pos) for pos in EatableEnemyPositionList])
        features['distanceToEatableEnemy'] = minDistance1 

    

    
    if len(EnemyPacmanPositionList) > 0:
        minDistance2 = min([self.getMazeDistance(myPos, pos) for pos in EnemyPacmanPositionList])
        features['distanceToPacmanEnemy'] =minDistance2
        
    
    
    
    features['distanceToHome'] = 0
    if myState.isPacman: 
        features['onDefense'] = 0
       
        #If capsules left , eat it    
        if len(capsules) > 0: 
            minDistance = min([self.getMazeDistance(myPos, capsule) for capsule in capsules])
            features['distanceToCapsule'] = minDistance
        else:
            features['EatCapsule'] = 1
            if self.getScore(gameState)>0:
                #if we are winning 
                features['distanceToHome'] = minDistanceToDFoodGroup
    else:
        if features['PacmanAlive'] > 0 :

                if self.getScore(gameState) > 13:
                    features['onDefense'] = 1
                    features['distanceToFoodGroup'] = 0
                    
                    
    if gameState.isOver():
        features['over'] = 1
                      
    return features

  def getWeightsSmart(self, gameState):
    return {'successorScore': 300,'foodNum': -100, 'distanceToFoodGroup': -2,'HeroAlive':3000, 'PacmanAlive':-300, 
            'distanceToEnemyGhost':2,'distanceToEatableEnemy':-3,'distanceToPacmanEnemy':-200,
            'distanceToHome': -2, 'EatCapsule':5000, 'distanceToCapsule':-200,'onDefense':10000,'over':100000}



class DefensiveReflexAgent(OffensiveReflexAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """


  def getFeaturesHungry(self, gameState):
    

    # Compute distance to the nearest food in largest foodgroup
    enemyghost=[]
    enemyPacman = []
    teammate=[]
    for i in self.getOpponents(gameState):
                    if not gameState.getAgentState(i).isPacman:       
                            enemyghost.append(i)
                    else:
                        enemyPacman.append(i)
                        
    myState=gameState.getAgentState(self.index)
    myPos = myState.getPosition()
    foodList = self.getFood(gameState).asList()
    food = foodList[len(foodList)-1]
    minDistanceToFoodGroup = self.getMazeDistance(myPos, food) 
    
    for i in self.getTeam(gameState):
                    if gameState.getAgentState(i).isPacman: 
                        if i!=self.index :     
                            teammate.append(i)
                   

    
    
    # Compute distance to the nearest food  in largest food group we are defending
    DefendingfoodList = self.getFoodYouAreDefending(gameState).asList()  
    minDistanceToDFoodGroup = min([self.getMazeDistance(myPos, food) for food in DefendingfoodList])
    
    
    #position of capsules
    capsules=self.getCapsules(gameState)
    owncapsules=self.getCapsulesYouAreDefending(gameState) 
 
    features = util.Counter()
    
    features['successorScore'] = self.getScore(gameState)
    
    
    #go eating at arriving
    if myState.isPacman:
        features['distanceToTarget'] = 0
        features['distanceToFoodGroup'] = minDistanceToFoodGroup
        if features['successorScore']<7:
            features['Fighting'] = 1

        else:
            features['Attacking'] = 1

    
    features['foodNum'] = len(foodList)  
    
    if not myState.isPacman:
        features['distanceToFoodGroup'] = 0
        
        #offensing through the weak side           
        if not self.red:
            features['distanceToTarget'] = self.getMazeDistance(myPos, (11.0,13.0))
        else :
            features['distanceToTarget'] = self.getMazeDistance(myPos, (19.0,2.0))
    
    features['DfoodNum'] = len(DefendingfoodList)    

    features['distanceToDFoodGroup'] = 0
  
    #whether eat capsule
    features['Capsule'] = 0

    #whether to play def
    features['onDefense'] = 0


    if not len(capsules) > 0:  
        features['Capsule'] = 1
        if len(enemyghost) == 0: 
            features['Capsule'] = -0.01
        else:
            for team in teammate:
                for i in enemyghost:
                    position = gameState.getAgentState(i).getPosition()
                    if gameState.getAgentState(i).getPosition() != None:
                        if util.manhattanDistance(position, gameState.getAgentPosition(team)) <= SIGHT_RANGE:        
                                features['Capsule'] = -1
                                
        if self.getScore(gameState)>13:
            
            #if  reborned then play as def ghost
            if not myState.isPacman:
                features['onDefense'] = 1
              
                #if we still have own capsule, defence it
                if len(owncapsules)>0:
                     minDistance = min([self.getMazeDistance(myPos, capsule) for capsule in owncapsules])
                     features['distanceToTarget'] = minDistance
                else:
                    # find the group with the most food
                    features['distanceToDFoodGroup'] = minDistanceToDFoodGroup

    return features