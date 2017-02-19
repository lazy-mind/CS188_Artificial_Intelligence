# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()
    
    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #TODO: project 3 value iteration should complete this method
        
        #how do we run value iteration?
        # we need to update value for each state , in this function , it is just value
        # and after computing them we should have the true value
        # we don't need to consider the converge thing from now yet, because we will assign iteration rounds
        
        """
        here's how we want to do this:
        0 round: all value become 0
        for each round: do the evaluation function:
        keep doing it for the required rounds until we get vk
        (iteration)
        call computeQvalue function
        call getactions function
        """
        #print self.mdp.getStates()
        #print self.values
        for states in self.mdp.getStates():
            self.values[states]=0
                #if self.mdp.isTerminal(states):
                #print "yes"
                #print self.values
        
        
        while self.iterations>=1:
            save=self.values.copy()
            for states in self.mdp.getStates():
                summary=[0]
                for actions in self.mdp.getPossibleActions(states):
                    temp=self.mdp.getTransitionStatesAndProbs(states,actions)
                    sum=0
                    for t in temp:
                        sum+=t[1]*(self.mdp.getReward(states,actions,t[0])+(self.discount)*(save[t[0]]))
                    #print self.mdp.getReward(states,actions,t[0])
                    summary.append(sum)
                summary=summary[1:]
                final=0
                if(len(summary)>=1):
                    final=max(summary)
                else:
                    final=0
                self.values[states]=final
            self.iterations=self.iterations-1

        #print self.values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
                #TODO: project 3 value iteration should complete this method
        
        #first we assign all value to be 0
        #then we do 1 value iteration
        """
        here is how iteration works:
        1. for each position in the state (no matter of the priority)
        2. find out all legal action
        3. for each legal action, assign value
        4. as: (probability)*((reward)+discount*(childrenstate's value))
        5. be careful about summaration of different child states in that case
        6. here we get the action, and we get the value
        """
        #if the question was asking us to compute Q from value, it means we first have a complete value, and do Q calculation once, that is enough
        
        temp=self.mdp.getTransitionStatesAndProbs(state,action)
        sum=0
        for t in temp:
            sum+=t[1]*(self.mdp.getReward(state,action,t[0])+(self.discount)*(self.values[t[0]]))
        return sum

        util.raiseNotDefined()


    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # TODO: project 3 value iteration should complete this method
        # this method use the result of the computeQvalueFromValues.
        # that is: we have our Q value for each state now
        # and we choose the biggest Q value all the time will be fine
        summary=[(-10000,'exit')]
        for actions in self.mdp.getPossibleActions(state):
            temp=self.mdp.getTransitionStatesAndProbs(state,actions)
            sum=0
            for t in temp:
                sum+=t[1]*(self.mdp.getReward(state,actions,t[0])+(self.discount)*(self.values[t[0]]))
            summary.append((sum,actions))
        summary=summary[1:]
        final=[-10000,'exit']
        for each in summary:
            if final[0]<=each[0]:
                final=each
        return final[1]
        
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #TODO: project 3 value iteration should complete this method
        
        #how do we run value iteration?
        # we need to update value for each state , in this function , it is just value
        # and after computing them we should have the true value
        # we don't need to consider the converge thing from now yet, because we will assign iteration rounds
        
        """
            here's how we want to do this:
            0 round: all value become 0
            for each round: do the evaluation function:
            keep doing it for the required rounds until we get vk
            (iteration)
            call computeQvalue function
            call getactions function
            """
        #print self.mdp.getStates()
        #print self.values
        for states in self.mdp.getStates():
            self.values[states]=0
        #if self.mdp.isTerminal(states):
        #print "yes"
        #print self.values
        
        copy=self.mdp.getStates()
        
        while self.iterations>=1:
            #save=self.values.copy()
            states=copy[0]
            #print states
            summary=[0]
            for actions in self.mdp.getPossibleActions(states):
                temp=self.mdp.getTransitionStatesAndProbs(states,actions)
                sum=0
                for t in temp:
                    sum+=t[1]*(self.mdp.getReward(states,actions,t[0])+(self.discount)*(self.values[t[0]]))
                    #print self.mdp.getReward(states,actions,t[0])
                summary.append(sum)
            summary=summary[1:]
            final=0
            if(len(summary)>=1):
                final=max(summary)
            else:
                final=0
            self.values[states]=final
            self.iterations=self.iterations-1
            copy=copy[1:]
            if (len(copy)==0):
                copy=self.mdp.getStates()

        #print self.values

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE***"
        #compute predecessors of all states (we use the policy: we stand at the position now, and take actions, see where can i go, that's my predecessors)
        #the predecessor will be a set that prevent duplicate
        statelist=self.mdp.getStates()
        #print "print state list: ",statelist
        #print self.values[statelist[0]]
        #print self.values[0:]
        
        
        predecessors=[]
        aelement=[]
        element=set(aelement)
        for eachone in statelist:   # compute predecessor for each state
            for each in statelist:  # for eachstate, find out its predecessor by checking one by one
                actionlist=self.mdp.getPossibleActions(each)    # get action
                for a in actionlist:
                    possible=self.mdp.getTransitionStatesAndProbs(each,a)   # see where it leads
                    for p in possible:
                        if p[0] == eachone and p[1]!=0: # it is predecessor with nonzero probability
                            element.add(each)   #add to the element list
                            break
            predecessors.append((eachone,element))   #for each state we have a list, consisting set of the possible predecessor
            element=set(aelement)
    
        #print "          "
        #print "          "
        #num=0
        #for p in predecessors:
        #   print "state ",num," 's predecessor:"
        #   print p
        #   num=num+1
        

        #initialize an empty priority queue (should be easy)
        priorityqueue=util.PriorityQueue()

        #for each non-terminal state: (in order: getStates)
        # diff= current value of s(self.value) - Q(the highest)    absolute value
        # don't update s
        # push s in queue with priority -diff
        for each in statelist:
            if each!='TERMINAL_STATE':
                temp=[]
                for a in self.mdp.getPossibleActions(each):
                    temper=self.mdp.getTransitionStatesAndProbs(each,a)
                    sum=0
                    for t in temper:
                        sum+=t[1]*(self.mdp.getReward(each,a,t[0])+(self.discount)*(self.values[t[0]]))
                    temp.append(sum)
                if (len(temp))>0:
                    maximum=max(temp)
                else:
                    maximum=0
                sub=self.values[each]
                diff=sub-maximum
                if diff<0:
                    priorityqueue.update(each,diff)
                else:
                    priorityqueue.update(each,-diff)

        # Do the iteration: (-1)
        """
        empty --> terminate
        
        pop , update s value(not terminal)
        for presuccessor of s
            diff= q - Q(biggest)
            if diff> beta(the value now)
                push p in queue with -diff
        """

        while self.iterations>=1:
            if priorityqueue.isEmpty():
                break
            s=priorityqueue.pop()
            #s=priorityqueue.pop()
            #print " "
            #print "here is s:",s
            temp=[]
            for a in self.mdp.getPossibleActions(s):
                temper=self.mdp.getTransitionStatesAndProbs(s,a)
                sum=0
                for t in temper:
                    sum+=t[1]*(self.mdp.getReward(s,a,t[0])+(self.discount)*(self.values[t[0]]))
                temp.append(sum)
            if (len(temp))>0:
                maximum=max(temp)
            else:
                maximum=0
            if s!='TERMINAL_STATE':
                self.values[s]=maximum

            for p in predecessors:
                if p[0]==s:
                    for each in p[1]:
                        temp=[]
                        for a in self.mdp.getPossibleActions(each):
                            temper=self.mdp.getTransitionStatesAndProbs(each,a)
                            sum=0
                            for t in temper:
                                sum+=t[1]*(self.mdp.getReward(each,a,t[0])+(self.discount)*(self.values[t[0]]))
                            temp.append(sum)
                        if (len(temp))>0:
                            maximum=max(temp)
                        else:
                            maximum=0
                        sub=self.values[each]
                        diff=sub-maximum
                        if diff<0:
                            diff=-diff
                        if (diff>self.theta):
                            priorityqueue.update(each,-diff)
            self.iterations=self.iterations-1















