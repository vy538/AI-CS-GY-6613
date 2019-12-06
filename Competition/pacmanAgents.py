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
import random
import math

def admissibleHeuristic(state,orgState):
    if state.isLose():
        return 10000.0;
    # print("food number",state.getNumFood(),"cap number",len(state.getCapsules()))
    ans = len(state.getCapsules())*10
    print("getCapsules pan", ans)
    gain = state.getScore() - orgState.getScore()
    print("gain pan",gain)
    ans -= gain
    pos = state.getPacmanPosition()
    if pos in exploredMap:
    	temp =  exploredMap[pos]*25
        print("visited pan",temp)
    	ans += temp
    return ans

exploredMap = {}

class Node:
    def __init__(self,state,actions,score):
        self.state = state
        self.actions = actions
        self.score = score
    def __str__(self):
        str1 = str(self.score)+" : "+str(self.actions)
        return str1

class CompetitionAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
    	self.maxDepth = 8
    	exploredMap = {}
        return;

    def f_score(self, state, actions, orgState):
    	g_value = pow(1.1,len(actions))
        print("g_value",g_value)
        ans = g_value + admissibleHeuristic(state,orgState)
        print("ans",ans)
        print "\n"
    	return ans

    def compareAns(self, t_node, res):
    	if t_node.score < res.score:
            res = t_node
        elif t_node.score == res.score:
            if len(t_node.actions)<len(res.actions):
                res = t_node
        return res

    def findNeighbor(self,originalNode,ans):
        c_legal = originalNode.state.getLegalPacmanActions()
        c_actions = originalNode.actions
        c_successors = [(originalNode.state.generatePacmanSuccessor(action),action) for action in c_legal]
        newNodes = []
        for pair in c_successors:
            t_actions = c_actions+[pair[1]]
            if pair[0] == None or len(t_actions) > self.maxDepth:
                ans = self.compareAns(originalNode,ans)
            else:
                t_score = self.f_score(pair[0],t_actions,self.state)
                temp = Node(pair[0],t_actions,t_score)
                newNodes.append(temp)
        return newNodes,ans

    def storedPosition(self,position):
    	if position in exploredMap:
    		exploredMap[position] += 1
    	else:
    		exploredMap[position] = 1
    	return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write your algorithm Algorithm instead of returning Directions.STOP
        def getScore(item):
            return item.score

        self.state = state
        self.storedPosition(state.getPacmanPosition())
        s_f_value = self.f_score(state,[],state)
        originalNode = Node(state,[],s_f_value)
        ans = Node(None,[],9999)

        openSet = [originalNode]
        closeSet = []

        while openSet:
            openSet.sort(key=getScore)
            node = openSet[0]
            if(node.state.isWin()):
                ans = self.compareAns(node,ans)
                break
            openSet = openSet[1:]
            closeSet.append(node)

            newNodes,ans = self.findNeighbor(node,ans)

            for n in newNodes:
                if n in closeSet:
                    continue
                if n not in openSet:
                    openSet.append(n)

        if ans.actions != []:
            nowAction = ans.actions[0]
        else:
            print "error"
            nowAction = Directions.STOP

        return nowAction



