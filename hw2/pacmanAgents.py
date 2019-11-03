# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
from heuristics import *
import random
import math




class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        print("\n")
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
            print(self.actionList[i])
        tempState = state;
        for i in range(0,len(self.actionList)):
            print("what action now? ",self.actionList[i])
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                print("isWin?",tempState.isWin())
                print("isLose?",tempState.isLose())
                break;
        # returns random action from all the valide actions
        print("actions: ",self.actionList[0])
        return self.actionList[0];

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,5):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Hill Climber Algorithm instead of returning Directions.STOP

        def updateActionList():
            for i in range(0,len(self.actionList)):
                randNow = random.randint(0,1)
                if randNow == 0:
                    self.actionList[i] = possible[random.randint(0,len(possible)-1)]
            return

        def generateActionsTempState(temp):
            for i in range(0,len(self.actionList)):
                if temp.isWin() + temp.isLose() == 0:
                    temp = temp.generatePacmanSuccessor(self.actionList[i])
                else:
                    return temp
                if temp == None:
                    self.keepContinue = False
                    return temp
            return temp

        def stateScoreEvaluation(temp):
            if not self.keepContinue:
                return
            nowScore = gameEvaluation(state,temp)
            # print nowScore
            if nowScore > self.bestSeq["score"]:
                self.bestSeq["actions"] = self.actionList[:]
                self.bestSeq["score"] = nowScore
            else:
                self.actionList = self.bestSeq["actions"][:]
            # print("current bestSeq:",self.bestSeq)
            return

        self.bestSeq = {"actions":[],"score":0};
        possible = state.getAllPossibleActions();

        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)]

        self.bestSeq["actions"] = self.actionList[:]
        self.keepContinue = True
        while self.keepContinue :
            tempState = state
            tempState = generateActionsTempState(tempState)
            stateScoreEvaluation(tempState)
            updateActionList()
        return self.bestSeq["actions"][0]

class Chrome:
    _COUNTER = 0
    def __init__(self,actionList,score=None,root = False):
        if root:
            Chrome._COUNTER = 0
        self.actionList = actionList[:]
        self.score = -999
        self.rank = -1
        self.id = Chrome._COUNTER
        Chrome._COUNTER += 1
        # print(self)

    def __str__(self):
        str1 = str(self.id)+"\tactionList: "+str(self.actionList)+"\n\tscore: "+str(self.score)+"\n\trank: "+str(self.rank)
        return str1

class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP

        def initPopulation():
            pop = []
            for i in range(0,8):
                acts = []
                for j in range(0,5):
                    acts.append(self.possible[random.randint(0,len(self.possible)-1)])
                newUnit = Chrome(acts)
                pop.append(newUnit)
            return pop

        def updateFitness(pop):
            for i in range(0,8):
                unit = pop[i]
                acts = unit.actionList
                tempState = state
                for j in range(0,5):
                    if tempState.isWin() + tempState.isLose() == 0:
                        tempState = tempState.generatePacmanSuccessor(acts[j])
                    else:
                        break
                    if tempState == None:
                        self.keepContinue = False
                        return pop     
                score = gameEvaluation(state,tempState)
                pop[i].score = score

            return pop

        def getUnitScore(unit):
            return unit.score

        def parentSelection(pop):
            # print "in parent selection"
            weightedPool = []
            highestRank = max([p.rank for p in pop])
            for p in pop:
                j = highestRank - p.rank + 1
                while j > 0:
                    weightedPool.append(p)
                    j -= 1
            parent1 = weightedPool[random.randint(0,len(weightedPool)-1)]
            parent2 = weightedPool[random.randint(0,len(weightedPool)-1)]
            parents = [parent1,parent2]
            return parents

        def crossover(parents):
            result = parents
            rand1 = random.randint(1,10)
            if rand1 > 7:
                return result
            else:
                for i in range(0,2):
                    tempActions = parents[0].actionList[:]
                    for j in range(0,5):
                        rand2 = random.randint(1,10)%2
                        tempActions[j] = parents[rand2].actionList[j]
                    result[i] = Chrome(tempActions)
            return result

        def multation(pop):
            if not self.keepContinue:
                return pop
            for p in pop:
                rand = random.randint(1,10)
                if rand == 1:
                    # print "mutate!"
                    p_act = p.actionList[:]
                    randomP = random.randint(0,len(p_act)-1)
                    newAct = None
                    while True:
                        newAct = self.possible[random.randint(0,len(self.possible)-1)]
                        if newAct != p_act[randomP]:
                            break
                    p_act[randomP] = newAct
                    p.actionList = p_act[:]
            return pop

        def generateNewPopulation(pop):
            if not self.keepContinue:
                return pop
            newPop = []
            while len(newPop)<8:
                parents = parentSelection(population)
                results = crossover(parents)
                for indi in results:
                    newPop.append(indi)
            return newPop

        def updateCurrentBest(pop):
            if not self.keepContinue:
                return pop
            pop.sort(key=getUnitScore,reverse=True)
            self.bestSeq = pop[0]
            return pop

        def giveRank(pop):
            if not self.keepContinue:
                return pop
            c_rank = c_score = 0
            for p in pop:
                if p.score != c_score:
                    c_score = p.score
                    c_rank += 1 
                p.rank = c_rank
            return pop


        # print "\n----------------------------new Step----------------------------"
        self.possible = state.getAllPossibleActions()
        self.bestSeq = Chrome([],-1,True)
        population = initPopulation()
        self.keepContinue = True

        while self.keepContinue:
            population = updateFitness(population)
            population = updateCurrentBest(population)
            population = giveRank(population)
            population = generateNewPopulation(population)
            population = multation(population)

        ansSeq = self.bestSeq.actionList
        return ansSeq[0]

class Node:
    _COUNTER = 0

    def __init__(self,root=False,actionList=[],parent=None):
        if root:
            Node._COUNTER = 0
        self.actionList = actionList
        self.children = {}
        self.parent = parent
        self.totalReward = 0
        self.visited = 1
        self.id = Node._COUNTER
        Node._COUNTER += 1
        # print "created "+str(self)

    def __str__(self):
        str1 = "\n\tID: "+ str(self.id)
        str1 += "\t\tact: "+str(self.actionList)
        str1 += "\n\t\t\tscore: "+str(self.totalReward/self.visited)
        if self.parent != None:
            str1 += "\n\t\t\tparentID: "+str(self.parent.id)
        if len(self.children) > 0:
            for child in self.children:
                str1+= "\n\t\t\tchild key: "+str(child)+"\tchildID: "+str(self.children[child].id)
        return str1

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        # self.run = False
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        def isTerminalState(_state):
            # print "in isTerminalState"
            return _state.isLose() + _state.isWin() != 0

        def getNodeState(tempState,act):
            # print "in getNodeState"
            tempState = tempState.generatePacmanSuccessor(act)
            if tempState == None:
                self.keepContinue = False
            return tempState

        def getNodeStateByNode(node):
            # print "in getNodeStateByNode"
            tempState = state
            i = 0
            while i < len(node.actionList) and self.keepContinue:
                if isTerminalState(tempState):
                    break
                tempState = getNodeState(tempState,node.actionList[i])
                i += 1
            return tempState

        def createNewChild(node,tempState,act):
            # print "in createNewChild"
            newNode = None
            tempState = getNodeState(tempState,act)
            newActionList = node.actionList[:]+ [act]
            newNode = Node(False,newActionList,node)
            node.children[act] = newNode  
            return newNode,tempState

        def expendTree(node,tempState):
            # print "in expendTree"
            legalActions = tempState.getLegalPacmanActions()
            newNode = None
            i = 0
            while i < len(legalActions) and self.keepContinue:
                act = legalActions[i]
                if act not in node.children:
                    newNode,tempState = createNewChild(node,tempState,act)
                    break
                i += 1
            if len(node.children) == len(legalActions):
                self.expended.append(node)
            return newNode,tempState

        def treePolicy(node):
            # print "in treePolicy"
            tempState = getNodeStateByNode(node)
            while self.keepContinue and not isTerminalState(tempState):
                if node not in self.expended:
                    return expendTree(node,tempState)
                else:
                    node = bestChild(node,1)
                    tempState = getNodeStateByNode(node)
            return node,tempState

        def defaultPolicy(tempState):
            # print "in default Policy"
            if not self.keepContinue:
                return -1

            thisNodeTempState = tempState
            i = 0
            while i<5:
                if isTerminalState(tempState):
                    break
                legalActions = tempState.getLegalPacmanActions()
                tempState = getNodeState(tempState,legalActions[random.randint(0,len(legalActions)-1)])
                if not self.keepContinue:
                    return -1
                i+=1
            reward = gameEvaluation(thisNodeTempState,tempState)
            return reward

        def backUp(node,reward):
            # print "in back up"
            if not self.keepContinue:
                return

            while node != None:
                node.visited += 1
                node.totalReward += reward
                # print "update"+str(node)
                node = node.parent
            return

        def UCB(node,parentNode,c):
            # print "in UCB"
            part1 = node.totalReward/node.visited
            part2 = c*math.sqrt(2*math.log(parentNode.visited)/node.visited)
            return part1 + part2
        
        def bestChild(node,c):
            # print "in best child"
            currentBest = {"child":None,"score":-999}
            for child in node.children:
                tempScore = UCB(node.children[child],node,c)
                if tempScore > currentBest["score"]:
                    currentBest["child"] = node.children[child]
                    currentBest["score"] = tempScore
            return currentBest["child"]
        
        def getAns(root):
            ans = None
            mostVisitedTime = -1
            for child in root.children:
                c_child = root.children[child]
                if c_child.visited > mostVisitedTime:
                    ans = c_child
                    mostVisitedTime = c_child.visited
                elif c_child.visited == mostVisitedTime and random.randint(0,1) == 1:
                    ans = c_child
            return ans

        def debuggingPrintTree(node):
            print node
            for child in node.children:
                childNode = node.children[child]
                debuggingPrintTree(childNode)
            return
        
        root = Node(True) #create root node
        self.expended = []
        self.keepContinue = True

        while self.keepContinue:
            newNode,newNodeState = treePolicy(root)
            reward = defaultPolicy(newNodeState)
            backUp(newNode,reward)

        ansNode = getAns(root)
        ansAction = ansNode.actionList[0]
        return ansAction












