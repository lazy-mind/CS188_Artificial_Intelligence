# factorOperations.py
# -------------------
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


from bayesNet import Factor
import operator as op
import util

def joinFactorsByVariableWithCallTracking(callTrackingList=None):


    def joinFactorsByVariable(factors, joinVariable):
        """
        Input factors is a list of factors.
        Input joinVariable is the variable to join on.

        This function performs a check that the variable that is being joined on 
        appears as an unconditioned variable in only one of the input factors.

        Then, it calls your joinFactors on all of the factors in factors that 
        contain that variable.

        Returns a tuple of 
        (factors not joined, resulting factor from joinFactors)
        """

        if not (callTrackingList is None):
            callTrackingList.append(('join', joinVariable))

        currentFactorsToJoin =    [factor for factor in factors if joinVariable in factor.variablesSet()]
        currentFactorsNotToJoin = [factor for factor in factors if joinVariable not in factor.variablesSet()]

        # typecheck portion
        numVariableOnLeft = len([factor for factor in currentFactorsToJoin if joinVariable in factor.unconditionedVariables()])
        if numVariableOnLeft > 1:
            print "Factor failed joinFactorsByVariable typecheck: ", factor
            raise ValueError, ("The joinBy variable can only appear in one factor as an \nunconditioned variable. \n" +  
                               "joinVariable: " + str(joinVariable) + "\n" +
                               ", ".join(map(str, [factor.unconditionedVariables() for factor in currentFactorsToJoin])))
        
        joinedFactor = joinFactors(currentFactorsToJoin)
        return currentFactorsNotToJoin, joinedFactor

    return joinFactorsByVariable

joinFactorsByVariable = joinFactorsByVariableWithCallTracking()


def joinFactors(factors):
    """
    Question 3: Your join implementation 

    Input factors is a list of factors.  
    
    You should calculate the set of unconditioned variables and conditioned 
    variables for the join of those factors.

    Return a new factor that has those variables and whose probability entries 
    are product of the corresponding rows of the input factors.

    You may assume that the variableDomainsDict for all the input 
    factors are the same, since they come from the same BayesNet.

    joinFactors will only allow unconditionedVariables to appear in 
    one input factor (so their join is well defined).

    Hint: Factor methods that take an assignmentDict as input 
    (such as getProbability and setProbability) can handle 
    assignmentDicts that assign more variables than are in that factor.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    """
    for f in factors:
        print
        print f
        print "SUCCESS 1 \n",f.getAllPossibleAssignmentDicts()
        print "SUCCESS 2 \n",f.unconditionedVariables()
        print "SUCCESS 3 \n",f.conditionedVariables()
        print "SUCCESS 4 \n",f.variableDomainsDict()
        #dic={'D':'wet','W':'sun'}
        #print "SUCCESS 2 \n",f.getProbability(dic)
        print
        print "~~~~~~~~~~~END~~~~~~~~~~"
    """
    
    #before we get started, let's rethink how the jointFactors work
    #basically we have all the CPT tables, maybe not a complete table
    #we first clarify what we Query, Evidence, Hidden
    #the goal is to joint and eliminate all the hidden
    #finally joint all Query and Evidence to get a joint distribution
    #the joint distribution multiply the evidence will give us sth. to normalizedff
    
    # factors---->joint util f(want,want,want,want,)------> normalized to get
    
    """
        what we want to do:
        1.get each factors
        2.get different variables and get a new factor  (use conditioned & unconditioned)
        3.do the multiplication correspondingly  (use getporbability and variableDomainsDict)
    """

    setsOfUnconditioned = [set(factor.unconditionedVariables()) for factor in factors]
    if len(factors) > 1:
        intersect = reduce(lambda x, y: x & y, setsOfUnconditioned)
        if len(intersect) > 0:
            print "Factor failed joinFactors typecheck: ", factor
            raise ValueError, ("unconditionedVariables can only appear in one factor. \n"
                    + "unconditionedVariables: " + str(intersect) +
                    "\nappear in more than one input factor.\n" + 
                    "Input factors: \n" +
                    "\n".join(map(str, factors)))

    #the following lines help us to get the correct joint presentation
    unconditionedVariablesListh=[]
    conditionedVariablesListh=[]
    unconditionedVariablesList=set(unconditionedVariablesListh)
    conditionedVariablesList=set(conditionedVariablesListh)
    domainDict={}
    for f in factors:
        print f
        unconditionedVariablesList=f.unconditionedVariables()|unconditionedVariablesList
        conditionedVariablesList=f.conditionedVariables()|conditionedVariablesList
        domainDict=f.variableDomainsDict()
        #print "SUCCESS 1 \n",f.getAllPossibleAssignmentDicts()
    conditionedVariablesList=conditionedVariablesList-unconditionedVariablesList
    newfactorCPT  = Factor(unconditionedVariablesList, conditionedVariablesList, domainDict)

    #we want to assign proper value to teh presentation now
    #conditionedVariablesListh=list(conditionedVariablesList)
    possibleAssignmentDictsList=newfactorCPT.getAllPossibleAssignmentDicts()
    computevalue=0
    for a in possibleAssignmentDictsList:
        #aitem=a.items()
        p=1
        for f in factors:
            eachAssignment=f.getAllPossibleAssignmentDicts()
            for e in eachAssignment:
                condition=0
                eitems=e.items()
                for eache in eitems:
                    if a[eache[0]]==eache[1]:
                        condition=1
                    else:
                        condition=0
                        break
                if condition==1:
                    p=p*f.getProbability(e)
                    break

        newfactorCPT.setProbability(a,p)

    return newfactorCPT
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()


def eliminateWithCallTracking(callTrackingList=None):

    def eliminate(factor, eliminationVariable):
        """
        Question 4: Your eliminate implementation 

        Input factor is a single factor.
        Input eliminationVariable is the variable to eliminate from factor.
        eliminationVariable must be an unconditioned variable in factor.
        
        You should calculate the set of unconditioned variables and conditioned 
        variables for the factor obtained by eliminating the variable
        eliminationVariable.

        Return a new factor where all of the rows mentioning
        eliminationVariable are summed with rows that match
        assignments on the other variables.

        Useful functions:
        Factor.getAllPossibleAssignmentDicts
        Factor.getProbability
        Factor.setProbability
        Factor.unconditionedVariables
        Factor.conditionedVariables
        Factor.variableDomainsDict
        """
        # autograder tracking -- don't remove
        if not (callTrackingList is None):
            callTrackingList.append(('eliminate', eliminationVariable))

        # typecheck portion
        if eliminationVariable not in factor.unconditionedVariables():
            print "Factor failed eliminate typecheck: ", factor
            raise ValueError, ("Elimination variable is not an unconditioned variable " \
                            + "in this factor\n" + 
                            "eliminationVariable: " + str(eliminationVariable) + \
                            "\nunconditionedVariables:" + str(factor.unconditionedVariables()))
        
        if len(factor.unconditionedVariables()) == 1:
            print "Factor failed eliminate typecheck: ", factor
            raise ValueError, ("Factor has only one unconditioned variable, so you " \
                    + "can't eliminate \nthat variable.\n" + \
                    "eliminationVariable:" + str(eliminationVariable) + "\n" +\
                    "unconditionedVariables: " + str(factor.unconditionedVariables()))

        "*** YOUR CODE HERE ***"
    
        """
            we find what cna we do with this function
            the previous part handle the exception cases pretty well for us
            we need to do the elimination procedure below, and the method can look in the joint
            1. we need to construct a new CPT , while remainning the CPT of the original
            2. from the original CPT , we do a loop , to find out all the eliminated variable
            3. plus all the probability
            4. return the new CPT
        """
        tempset=factor.unconditionedVariables()
        tempset.remove(eliminationVariable)
        unconditionedVariablesList=list(tempset)
        conditionedVariablesList=list(factor.conditionedVariables())
        domainDict=factor.variableDomainsDict()
    
        newCPT=Factor(unconditionedVariablesList, conditionedVariablesList, domainDict)
        
        #so far so good
        possibleAssignmentDictsList=factor.getAllPossibleAssignmentDicts()
        newpossibleAssignmentDictsList=newCPT.getAllPossibleAssignmentDicts()
        
        print newpossibleAssignmentDictsList[0]
        
        for a in newpossibleAssignmentDictsList:
            p=0
            condition=0
            for b in possibleAssignmentDictsList:
                keylist=a.keys()
                #print "keylist"
                #print keylist
                for k in keylist:
                    if a[k]==b[k]:
                        condition=1
                    else:
                        condition=0
                        break
                if condition==1:
                    p=p+factor.getProbability(b)
            newCPT.setProbability(a,p)
           

        """
        if len(possibleAssignmentDictsList)==len(newpossibleAssignmentDictsList):
            print
            print 1
            print
        else:
            print "not"
        """
        
        """
        possibleAssignmentDictsList=factor.getAllPossibleAssignmentDicts()
        computevalue=0
        for a in possibleAssignmentDictsList:
            #aitem=a.items()
            p=0
            for f in factors:
                eachAssignment=f.getAllPossibleAssignmentDicts()
                for e in eachAssignment:
                    condition=0
                    eitems=e.items()
                    for eache in eitems:
                        if a[eache[0]]==eache[1]:
                            condition=1
                        else:
                            condition=0
                            break
                    if condition==1:
                        p=p*f.getProbability(e)
                        break
            newfactorCPT.setProbability(a,p)
        """
        
        
        return newCPT

    
        #util.raiseNotDefined()

    return eliminate

eliminate = eliminateWithCallTracking()


def normalize(factor):
    """
    Question 5: Your normalize implementation 

    Input factor is a single factor.

    The set of conditioned variables for the normalized factor consists 
    of the input factor's conditioned variables as well as any of the 
    input factor's unconditioned variables with exactly one entry in their 
    domain. 
    Since there is only one entry in that variable's domain, we
    can either assume it was assigned as evidence to have only one variable 
    in its domain, or it only had one entry in its domain to begin with.
    
    This blurs the distinction between evidence assignments and variables
    with single value domains, but that is alright since we have to assign 
    variables that only have one value in their domain to that single value.

    Return a new factor where the sum of the all the probabilities in the table is 1.
    This should be a new factor, not a modification of this factor in place.

    If the sum of probabilities in the input factor is 0,
    you should return None.

    This is intended to be used at the end of a probabilistic inference query.
    Because of this, all variables that have more than one element in their 
    domain are assumed to be unconditioned.
    There are more general implementations of normalize, but we will only 
    implement this version.

    Useful functions:
    Factor.getAllPossibleAssignmentDicts
    Factor.getProbability
    Factor.setProbability
    Factor.unconditionedVariables
    Factor.conditionedVariables
    Factor.variableDomainsDict
    """

    # typecheck portion
    variableDomainsDict = factor.variableDomainsDict()
    for conditionedVariable in factor.conditionedVariables():
        if len(variableDomainsDict[conditionedVariable]) > 1:
            print "Factor failed normalize typecheck: ", factor
            raise ValueError, ("The factor to be normalized must have only one " + \
                            "assignment of the \n" + "conditional variables, " + \
                            "so that total probability will sum to 1\n" + 
                            str(factor))

    "*** YOUR CODE HERE ***"

    """
        here is what we  will do in the normalized function
        1. we create a new CPT, with unconditioned and conditioned and same variabledomaindict
        2. we use the old CPT , get the sum of all probability
        3. we use the old CPT , the probability divide the sum , give this value to the new one
    """
    domainDict=factor.variableDomainsDict()

    untempsetcopy=factor.unconditionedVariables()
    tempset=factor.conditionedVariables()
    untempseth=[]
    untempset=set(untempseth)
    
    for u in untempsetcopy:
        if len(domainDict[u])==1:
            tempset.add(u)
        else:
            untempset.add(u)

    unconditionedVariablesList=list(untempset)
    conditionedVariablesList=list(tempset)

    #print domainDict
    
    newCPT=Factor(unconditionedVariablesList,conditionedVariablesList,domainDict)

    #so far we construct the correct CPT form
    #next step is purely calculate
    sum=0
    for a in factor.getAllPossibleAssignmentDicts():
        sum=sum+factor.getProbability(a)
    print sum
    for a in newCPT.getAllPossibleAssignmentDicts():
        pro=factor.getProbability(a)
        newCPT.setProbability(a,pro/sum)



    return newCPT




    #    util.raiseNotDefined()

