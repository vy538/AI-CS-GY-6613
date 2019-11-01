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

firstPenalty = 1
penalty = 1

class Node:
    def __init__(self,state,actions,score):
        self.state = state
        self.actions = actions
        self.score = score
    def __str__(self):
        str1 = str(self.score)+" : "+str(self.actions)
        return str1

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

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        print(legal)
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # print(scored)
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts

    def registerInitialState(self, state):
        self.lastAction = ""
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        def compareAns(t_node,res):
            if t_node.score < res.score:
                res = t_node
            elif t_node.score == res.score:
                if len(t_node.actions)<len(res.actions):
                    res = t_node
            return res


        def scoreCal(state,actions):
            ads = admissibleHeuristic(state)
            ans = ads + len(actions)
            return ans

        originalNode = Node(state,[],scoreCal(state,[]))
        # create node for original
        tempQueue = [originalNode]
        ans = Node(None,[],9999)
        
        while tempQueue:
            node = tempQueue[0]
            tempQueue = tempQueue[1:]

            if node.state.isWin():
                ans = compareAns(node,ans)
                break
            
            node_legal = node.state.getLegalPacmanActions()
            node_succesors = [(node.state.generatePacmanSuccessor(action),action) for action in node_legal]
            
            for suc in node_succesors:
                # end of the thread, compare parent to current ans
                if suc[0] == None:
                    # if this node have lower admiss value swape the answer
                    ans = compareAns(node,ans)
                else:
                    # build suc_node
                    suc_actions =  node.actions+[suc[1]]
                    suc_node = Node(suc[0],suc_actions,scoreCal(suc[0],suc_actions))
                    # if this node is win, return this node as ans, break while loop
                    if suc_node.state.isWin():
                        ans = compareAns(suc_node,ans)
                        break
                    # if this node is not lose, append this node to tempQueue
                    if not suc_node.state.isLose():
                        tempQueue.append(suc_node)

        # print("final ans",ans.score," actions ",ans.actions)
        # print("\n")
        if ans.actions == []:
            print "error"
            nowAction = Directions.STOP
        else:
            nowAction = ans.actions[0]

        self.lastAction = nowAction

        return nowAction


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.lastAction = ""
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        def compareAns(t_node,res):
            # print("compare",t_node.score,res.score)
            if t_node.score < res.score:
                res = t_node
            elif t_node.score == res.score:
                if len(t_node.actions)<len(res.actions):
                    res = t_node
            return res


        def scoreCal(state,actions):
            ads = admissibleHeuristic(state)
            ans = ads + len(actions)
            return ans

        originalNode = Node(state,[],scoreCal(state,[]))
        # create node for original
        tempQueue = [originalNode]
        ans = Node(None,[],9999)
        

        
        while tempQueue:
            node = tempQueue.pop()

            if node.state.isWin():
                # print("node is win state")
                ans = compareAns(node,ans)
                break
            
            node_legal = node.state.getLegalPacmanActions()
            node_succesors = [(node.state.generatePacmanSuccessor(action),action) for action in node_legal]
            
            for suc in node_succesors:
                suc_actions =  node.actions+[suc[1]]
                # end of the thread, compare parent to current ans
                if suc[0] == None:
                    # if this node have lower admiss value swape the answer
                    ans = compareAns(node,ans)
                else:
                    # build suc_node
                    suc_node = Node(suc[0],suc_actions,scoreCal(suc[0],suc_actions))
                    # if this node is win, return this node as ans, break while loop
                    if suc_node.state.isWin():
                        ans = compareAns(suc_node,ans)
                        break
                    # if this node is not lose, append this node to tempQueue
                    if not suc_node.state.isLose():
                        tempQueue.append(suc_node)

        # print("final ans",ans.score," actions ",ans.actions)
        # print("\n")
        if ans.actions == []:
            print "error"
            nowAction = Directions.STOP
        else:
            nowAction = ans.actions[0]
        self.lastAction = nowAction
        return nowAction


class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP

        def f_score(state,actions):
            g_value = len(actions)
            return admissibleHeuristic(state)+g_value

        def compareAns(t_node,res):
            if t_node.score < res.score:
                res = t_node
            elif t_node.score == res.score:
                if len(t_node.actions)<len(res.actions):
                    res = t_node
            return res

        def findNeighbor(originalNode,ans):
            c_legal = originalNode.state.getLegalPacmanActions()
            c_actions = originalNode.actions
            c_successors = [(originalNode.state.generatePacmanSuccessor(action),action) for action in c_legal]
            newNodes = []
            for pair in c_successors:
                t_actions = c_actions+[pair[1]]
                if pair[0] == None or len(t_actions)>maxDepth:
                    ans = compareAns(originalNode,ans)
                else:
                    t_score = f_score(pair[0],t_actions)
                    temp = Node(pair[0],t_actions,t_score)
                    newNodes.append(temp)
            return newNodes,ans

        def getScore(item):
            return item.score

        
        maxDepth = 8
        s_f_value = f_score(state,[])
        originalNode = Node(state,[],s_f_value)
        ans = Node(None,[],9999)

        openSet = [originalNode]
        closeSet = []

        while openSet:
            openSet.sort(key=getScore)
            node = openSet[0]
            if(node.state.isWin()):
                ans = compare(node,ans)
                break
            openSet = openSet[1:]
            closeSet.append(node)

            newNodes,ans = findNeighbor(node,ans)

            for n in newNodes:
                if n in closeSet:
                    continue
                if n not in openSet:
                    openSet.append(n)

        # print("final ans",ans.score," actions ",ans.actions)
        # print("\n")

        if ans.actions != []:
            nowAction = ans.actions[0]
        else:
            print "error"
            nowAction = Directions.STOP

        return nowAction





