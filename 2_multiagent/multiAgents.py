# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #print bestScore
        #print legalMoves
        return legalMoves[chosenIndex]
        "Add more of your code here if you want to"

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #here we difine how the agent work if it was too closed to the ghost
        newGhostPos=successorGameState.getGhostPosition(1)
        x,y=newPos
        safeDis= manhattanDistance(newGhostPos,newPos)+1
        safeInt=int(safeDis)
        if safeInt<=3:
            return safeInt

        #here in other cases,we define how the agent act if the ghost is far away
        #we may use a search to find out where are the nearst dot and go eat it, basically a greedy algorithm
        #therefore we need to know where the nearest dot is , and maybe give extra credit to the power pellet
        else:
            dotlist=newFood.asList()  #with this code we have a list of the now exsiting dot
            if len(dotlist)>=1:
                oldPos= currentGameState.getPacmanPosition()  # current position(not after action)
                dotDistance=[manhattanDistance(oldPos,eachdot) for eachdot in dotlist] #(a list of all distance)
                shortestone=min(dotDistance) #find the shortest one
                bestIndex=[index for index in range(len(dotlist)) if manhattanDistance(dotlist[index],oldPos)==shortestone] #find the shortest ones's index collection
                chosenIndex = random.choice(bestIndex) # make a random choice
                if (manhattanDistance(newPos,dotlist[chosenIndex])<shortestone):
                    return 100
                if (manhattanDistance(newPos,dotlist[chosenIndex])>shortestone):
                    return 0
                if (manhattanDistance(newPos,dotlist[chosenIndex])==shortestone):
                    return -5
            else:
                return 5

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        
        #here we want to implement a more general mini-max tree search
        """
            According to the lecture notes, things we have to do to implement:
            1. Do the min-value function and the max-value function
            2. Do the main function that calls the two functions repeatedly
            3. Just follow the psesudcode
        """
        
        requireDepth=self.depth
        # evaluate=self.evaluationFunction
        agentNumber=gameState.getNumAgents  # how many agent are there, -1 will give the number of ghost
        legalAction=gameState.getLegalActions(0)
        #generateSuccessor(index,action)
        # isWin and isLose
        
        currentDepth=0
        
        def max_value(state,exploredDepth):
            v=-999999999
            exploredDepth=exploredDepth+1
            if (exploredDepth==self.depth or state.isLose() or state.isWin()) :
                return self.evaluationFunction(state)
            
            else :
                for action in state.getLegalActions(0):
                    #for successor in state.generateSuccessor(0,action):
                    v=max(v,min_value(state.generateSuccessor(0,action),1,exploredDepth))
            return v
    
    
        def min_value(state,agentIndexNum,exploredDepth):
            v=999999999
            if(state.isWin() or state.isLose()):
                return self.evaluationFunction(state)
            
            else:
                for action in state.getLegalActions(agentIndexNum):
                    if (agentIndexNum==state.getNumAgents()-1):
                        v=min(v,max_value(state.generateSuccessor(agentIndexNum,action),exploredDepth))
                    else:
                        #agentIndexNum=agentIndexNum+1
                        v=min(v,min_value(state.generateSuccessor(agentIndexNum,action),(agentIndexNum+1),exploredDepth))
                return v


        """
        def value(state):
            if state.isWin==1 or state.isLose==1:
                return [];
            if agentIndex==0:
                for action in legalAction:
                    return max-value(state,action)
            if agentIndex!=0:
                return min-value(state)
        """
        v=-999999999
        actiontotake='East'
        actionSequence=[]
        for action in gameState.getLegalActions(0):
            #            for successor in gameState.generateSuccessor(0,action):
            bigger=min_value(gameState.generateSuccessor(0,action),1,0)
            if bigger>v:
                v=bigger
                actiontotake=action
        return actiontotake


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        
        """
            According to to pseudocode,
            the basic framework of alpha-beta is similar to the mini-max(actually it is just an improvement from mini-max)
            so we copy the mini-max code here first
            and the keys are:
            1. how to terminate the process once we have found out that it fits the pruning condition
                (already shown in the pseudocode)
                to do this we have to find out what alpha and beta's initial value is
                the alpha means the best agent can get
                the beta means the best ghost can get
                so alpha should be really big
                and beta should be really small
                
                here comes the question
                whether the alpha\beta bigger\smaller than the v we initially set?
                
                
            2. how to choose randomly between tie-option
                (random.choice()????)
            
        """
        """

        def max_value(state, alpha, beta, currentDepth):
            currentDepth = currentDepth + 1
            if state.isWin() or state.isLose() or currentDepth == self.depth:
                return self.evaluationFunction(state)
            v = float('-Inf')
            for pAction in state.getLegalActions(0):
                v = max(v, min_value(state.generateSuccessor(0, pAction), alpha, beta, currentDepth, 1))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, currentDepth, ghostNum):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            v = float('Inf')
            for pAction in state.getLegalActions(ghostNum):
                if ghostNum == gameState.getNumAgents() - 1:
                    v = min(v, max_value(state.generateSuccessor(ghostNum, pAction), alpha, beta, currentDepth))
                else:
                    v = min(v, min_value(state.generateSuccessor(ghostNum, pAction), alpha, beta, currentDepth, ghostNum + 1))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v

        # Body of alpha beta starts here: #
        pacmanActions = gameState.getLegalActions(0)
        maximum = float('-Inf')
        alpha = float(0)
        beta = float('Inf')
        maxAction = ''
        for action in pacmanActions:
            currentDepth = 0
            currentMax = min_value(gameState.generateSuccessor(0, action), alpha, beta, currentDepth, 1)
            if currentMax > maximum:
                maximum = currentMax
                maxAction = action
        return maxAction

        """
        #just a reminder to myself, we don't need to take a,b as a list to change its value all the time
        #each state and mini agent has their own one , so it is okay to use integer
        #otherwise, we will miss some main node
        #and in the main function, we must update the alpha value , otherwise we might give extra node to expand
        #finally we should be care about the equivalent case, in such problem , equivalent won't cause pruning
        

        currentDepth=0
        a=-100000
        b=100000
        
        def max_value(state,exploredDepth,a,b):
            v=-999999999
            exploredDepth=exploredDepth+1
            if (exploredDepth==self.depth or state.isLose() or state.isWin()) :
                return self.evaluationFunction(state)
            
            else :
                for action in state.getLegalActions(0):
                    #for successor in state.generateSuccessor(0,action):
                    v=max(v,min_value(state.generateSuccessor(0,action),1,exploredDepth,a,b))
                    if v>b : #the equal case is for the requirement, we need to choose randomly between tie-condition
                        return v
                    a=max(a,v)
                    #from here we know a should be a small number that let v comes out
                return v
        
        
        def min_value(state,agentIndexNum,exploredDepth,a,b):
            v=999999999
            # exploredDepth=exploredDepth+1
            if(state.isWin() or state.isLose()):
                return self.evaluationFunction(state)
            
            else:
                for action in state.getLegalActions(agentIndexNum):
                    if (agentIndexNum==state.getNumAgents()-1):
                        v=min(v,max_value(state.generateSuccessor(agentIndexNum,action),exploredDepth,a,b))
                    else:
                        #agentIndexNum=agentIndexNum+1
                        v=min(v,min_value(state.generateSuccessor(agentIndexNum,action),(agentIndexNum+1),exploredDepth,a,b))
                    if (v<a):
                        return v
                    b=min(b,v)
                return v
        
        
        val=-999999999
        actiontotake=Directions.STOP
        actionSequence=[]
        for action in gameState.getLegalActions(0):
            #            for successor in gameState.generateSuccessor(0,action):
            bigger=min_value(gameState.generateSuccessor(0,action),1,0,a,b)
            if bigger>val:
                val=bigger
                actiontotake=action
            a=max(a,val)
            
        return actiontotake

      

        """
            def value(state):
            if state.isWin==1 or state.isLose==1:
            return [];
            if agentIndex==0:
            for action in legalAction:
            return max-value(state,action)
            if agentIndex!=0:
            return min-value(state)
        """
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        #the expected max is basically like the minimax , but when calculate the minimax, we do the expected value
        #since the same probability, we can just divided by the number of children
        currentDepth=0
        
        def max_value(state,exploredDepth):
            v=-999999999
            exploredDepth=exploredDepth+1
            if (exploredDepth==self.depth or state.isLose() or state.isWin()) :
                return self.evaluationFunction(state)
            
            else :
                times=0
                for action in state.getLegalActions(0):
                    #for successor in state.generateSuccessor(0,action):
                    v=max(v,min_value(state.generateSuccessor(0,action),1,exploredDepth))
            return v
        #the max is same as before
        
        
        def min_value(state,agentIndexNum,exploredDepth):
            v=0
            float(v)
            store=v
            if(state.isWin() or state.isLose()):
                return self.evaluationFunction(state)
            
            
            else:
                for action in state.getLegalActions(agentIndexNum):
                    if (agentIndexNum==state.getNumAgents()-1):
                        length=(float)(len(state.getLegalActions(agentIndexNum)))
                        v+=max_value(state.generateSuccessor(agentIndexNum,action),exploredDepth)/length #here we do the calculation
                    else:
                        #agentIndexNum=agentIndexNum+1
                        length=(float)(len(state.getLegalActions(agentIndexNum)))
                        v+=(min_value(state.generateSuccessor(agentIndexNum,action),(agentIndexNum+1),exploredDepth))/length
                    v=v-store
                        #print v
                return v
        
        
        """
            def value(state):
            if state.isWin==1 or state.isLose==1:
            return [];
            if agentIndex==0:
            for action in legalAction:
            return max-value(state,action)
            if agentIndex!=0:
            return min-value(state)
            """
        v=-999999999
        actiontotake='East'
        actionSequence=[]
        for action in gameState.getLegalActions(0):
            #            for successor in gameState.generateSuccessor(0,action):
            bigger=min_value(gameState.generateSuccessor(0,action),1,0)
            if bigger>v:
                v=bigger
                actiontotake=action
        return actiontotake




def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    
    Here we want to value the different state:
    1. Less Food Left is Better: we can test length of food list in different states, the length determine the award 1 (linear relationship)
    2. Far away from the ghost, the better (we can make the pacman walk to food if the ghost is far away, if it is too near, we use search algorithm to avoid)
    3. Winning is the most important thing, give 100000000000 points for winning
    4. Each step comes with a cost like 1
    5. Chase for the pellet, if the ghost is near, or our agent itself is near to the pellet( manhanttan distance less than 10)
    6. if the ghost is scared, record the scared time and the remaining unscared ghost, make the optimal search we can
    7. the limited depth will be at 7 moves
    
    """
    "*** YOUR CODE HERE ***"
    
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    dotlist=newFood.asList()
    
    
    # because we are valueing the state, we don't need to involve the acitons that are leagl
    
    #credit for scaring
    total_scare=0
    for eachone in newScaredTimes:
        total_scare+=eachone
    
    
    
    #food chasing
    credit_for_food_left=0
    if (len(dotlist)>=1):
        credit_for_food_left=1000-(len(dotlist))*5


    #ghost avoiding
    credit_for_away_from_ghost=0
    numberOfAgent=currentGameState.getNumAgents()
    newGhostPos=[]
    ghostDistance=[]
    
    whichagent=1
    while whichagent<=numberOfAgent-1:
        newGhostPos.append(currentGameState.getGhostPosition(whichagent))
        whichagent=whichagent+1
    whichagent=1
    while whichagent<=numberOfAgent-1:
        ghostDistance.append(manhattanDistance(newGhostPos[whichagent-1],newPos))
        whichagent=whichagent+1
    shortestone=min(ghostDistance)
    
    if(shortestone<=7):
        credit_for_away_from_ghost=(shortestone)*5
    else:
        credit_for_away_from_ghost=100

    safe_credit=0
    dangerous_distance=0
    dangerous_distance=shortestone
    if(dangerous_distance<=3):
        safe_credit=-100

    #win chasing
    credit_for_win=0
    if (currentGameState.isWin()==1):
        credit_for_win=1

    credit_for_loose=0
    if (currentGameState.isLose()==1):
        credit_for_loose=-1

    #capsule chasing
    CapsulePos=currentGameState.getCapsules()
    length=len(CapsulePos)
    length=length-1
    capsuleDistance=[]
    while length>=0:
        capsuleDistance.append(manhattanDistance(CapsulePos[length],newPos))
        length=length-1
    if(len(capsuleDistance)>=1):
        shortestCapsule=min(capsuleDistance)
    else:
        shortestCapsule=0

    credit_for_eat=0
    credit_for_chasing_pellet=0
    if shortestCapsule>0 :
        credit_for_chasing_pellet=(-shortestCapsule)*100
        credit_for_eat=-(len(CapsulePos))*100
    else:
        credit_for_eat=1000


    credit_for_scare=0
    if(len(CapsulePos)==2):
        credit_for_scare=0
    if(len(CapsulePos)==1):
        credit_for_scare=1000
    if(len(CapsulePos)==0):
        credit_for_scare=10000

    #near dot chasing
    lengthtwo=len(dotlist)
    lengthtwo=lengthtwo-1
    dotDistance=[]
    while lengthtwo>=0:
        dotDistance.append(manhattanDistance(dotlist[lengthtwo],newPos))
        lengthtwo=lengthtwo-1
    if(len(dotDistance)>=1):
        shortestdot=min(dotDistance)
    else:
        shortestdot=1
    float(shortestdot)
    credit_for_dot=(1/shortestdot+1)*100



    #Direction Preference
    Left_heuristic=0
    x,y=newPos
    Left_heuristic=x
    Top_heuristic=y

    choose=[1,2]
    
        # print shortestCapsule


    if(shortestone>=10):
        credit_overall=(credit_for_away_from_ghost)*1+(credit_for_food_left)+(credit_for_win)*10000000+(credit_for_loose)*10000+credit_for_dot+Left_heuristic*3+Top_heuristic*3+credit_for_eat+ currentGameState.getScore()+credit_for_chasing_pellet+credit_for_scare
    else:
        credit_overall=(credit_for_away_from_ghost)*1000+(credit_for_food_left)+(credit_for_win)*10000000+(credit_for_loose)*10000+credit_for_dot+Left_heuristic*3+Top_heuristic*3+credit_for_eat+credit_for_chasing_pellet+credit_for_scare
    return credit_overall

# Abbreviation
better = betterEvaluationFunction

