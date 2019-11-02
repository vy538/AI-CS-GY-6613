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
        # self.ans = []
        # self.visitedQueue = []
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        ans = []
        
        originalNode = self.nodeBuilder(state,[],admissibleHeuristic(state))
        # create node for original
        tempQueue = [originalNode]
        tempVisitedQueue = []
        while (tempQueue != []):
            # print(tempQueue)
            tempNode = tempQueue[0]
            tempQueue = tempQueue[1:]

            c_state = tempNode["state"]
            c_actions = tempNode["actions"]

            
            c_legal = c_state.getLegalPacmanActions()
            successors = [(c_state.generatePacmanSuccessor(action),action) for action in c_legal]

            for successor in successors:
                suc_state = successor[0]
                if(suc_state == None):
                    if(tempNode not in ans):
                        ans.append(tempNode)
                    break
                node_suc = self.nodeBuilder(suc_state, c_actions+[successor[1]],admissibleHeuristic(suc_state))
                if(suc_state.isWin()):
                    ans = node_suc
                if(node_suc not in tempVisitedQueue):
                    tempQueue.append(node_suc)
                    tempVisitedQueue.append(node_suc)
        
        
        bestNodes = self.getLowestNode(ans)
        bestActions = bestNodes["actions"]
        nowAction = bestActions[0]
        
        return nowAction

    def getLowestNode(self,t_queue):
        temp_low = t_queue[0]
        for item in t_queue:
            if(item["score"]<temp_low["score"]):
                temp_low = item
        return temp_low

    def nodeBuilder(self,state,actions,score):
        temp ={
            "state":state,
            "actions":actions,
            "score":score
        }
        return temp



class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):

        self.ans = []
        self.currentPosition = (0,0)
        self.visitedQueue = []
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        
        self.ans = []
        tempQueue = [(state,self.currentPosition,[])] #root init
        if(self.currentPosition not in self.visitedQueue):
            self.visitedQueue.append(self.currentPosition)
        
        tempVisitedQueue = [] 
        
        while(tempQueue != []):
            
            c_state,c_pos,c_actions = tempQueue.pop()
            
            c_legal = c_state.getLegalPacmanActions()
            successors = [(c_state.generatePacmanSuccessor(action),action) for action in c_legal]
            
            for suc in successors:
                suc_state = suc[0]
                suc_dir = suc[1]
                suc_pos = self.getPosition(c_pos,suc_dir)
                
                if(suc_pos not in tempVisitedQueue and suc_state is not None): 
                    if not suc_state.isLose():
                        if suc_pos not in self.visitedQueue:
                            # print("add ans:",[c_actions + [suc_dir]])
                            self.ans += [c_actions + [suc_dir]]
                        tempQueue.append((suc_state, suc_pos, c_actions + [suc_dir]))
                        tempVisitedQueue.append(suc_pos)
                
        
        lenAns = [(len(directions),directions) for directions in self.ans]
        bestScore = min(lenAns)[0]
        bestActions = [pair[1] for pair in lenAns if pair[0] == bestScore]
        self.ans = bestActions[0]
        nowAction = self.ans[0]
        self.currentPosition = self.getPosition(self.currentPosition,nowAction)
        return nowAction

    def getPosition(self,orginal,action):
        ans = (0,0)
        if(action == 'North'):
            ans = (orginal[0],orginal[1]+1)
        if(action == 'South'):
            ans = (orginal[0],orginal[1]-1)
        if(action == 'East'):
            ans = (orginal[0]+1,orginal[1])
        if(action == 'West'):
            ans = (orginal[0]-1,orginal[1])
        return ans 

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):

        self.currentPosition = (0,0)
        s_pos = self.currentPosition
        s_f_value = self.totalNumber(state,s_pos)
        rootNode = self.nodeBuilder(state,s_pos,s_f_value,[])
        self.actucalVisitedNodes = [s_pos] 
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        print("\n")
        print("currentPosition",self.currentPosition)
        # print(self.actucalVisitedNodes)
        ans = tempAns = []
        s_pos = self.currentPosition
        s_f_value = self.totalNumber(state,s_pos)
        originalNode = self.nodeBuilder(state,s_pos,s_f_value,[])
        
        openSet = [originalNode]
        closeSet = []

        while (openSet != []):
            # self.debbuger("openSet: ",openSet)
            # self.debbuger("closeSet: ",closeSet)

            node = self.getLowestNode(openSet)
            
            if(node["pos"] not in self.actucalVisitedNodes):
                ans = node
                break
            
            openSet.remove(node)
            closeSet.append(node)
            
            newNodes = self.findNeighbor(node)

            for node in newNodes:
                if self.findIfThisNodeInThisSet(closeSet,node):
                    continue
                if not self.findIfThisNodeInThisSet(openSet,node):
                    # print("appending",node["pos"])
                    openSet.append(node)
        
        print("ans",ans)
        if(ans["pos"] not in self.actucalVisitedNodes):
            self.actucalVisitedNodes.append(ans["pos"])
        nowAction = ans["actions"][0]
        self.currentPosition = self.getPosition(self.currentPosition,nowAction)
        # print("nowAction",nowAction)

        return nowAction


    def findIfThisNodeInThisSet(self,t_set,node):
        for item in t_set:
            if item["pos"] == node["pos"]:
                return True
        return False

    def debbuger(self,t_name,t_queue):
        str1 = t_name
        for item in t_queue:
            str1 += str(item["pos"])
            str1 +=", "
        print(str1)

    def findNeighbor(self,originalNode):
        c_legal = originalNode["state"].getLegalPacmanActions()
        c_pos = originalNode["pos"]
        c_actions = originalNode["actions"]
        c_successors = [(originalNode["state"].generatePacmanSuccessor(action),self.getPosition(c_pos,action),action) for action in c_legal]
        c_successors = [pair for pair in c_successors if pair[0]!= None and not pair[0].isLose()]
        newNodes = []
        for pair in c_successors:
            t_score = self.totalNumber(pair[0],pair[1])
            t_actions = c_actions+[pair[2]]
            temp = self.nodeBuilder(pair[0],pair[1],t_score,t_actions)
            newNodes.append(temp)
        return newNodes

    def nodeBuilder(self,state,position,f_value,actions):
        # print("inside nodeBuilder:",state,position,f_value,actions)
        temp = {
            "state":state,
            "pos": position,
            "f_value": f_value,
            "actions": actions
        }
        return temp

    def getLowestNode(self,t_queue):
        bestScore = min(t_queue)["f_value"]
        # print(bestScore)
        bestNodes = [pair for pair in t_queue if pair["f_value"] == bestScore]
        # print(bestNodes)
        ans = bestNodes[0]
        return ans

    def totalNumber(self,state,pos):
        original = self.currentPosition
        g_value = abs(original[0] - pos[0]) + abs(original[1] - pos[1])
        return admissibleHeuristic(state)+g_value

    def getPosition(self,orginal,action):
        ans = (0,0)
        if(action == 'North'):
            ans = (orginal[0],orginal[1]+1)
        if(action == 'South'):
            ans = (orginal[0],orginal[1]-1)
        if(action == 'East'):
            ans = (orginal[0]+1,orginal[1])
        if(action == 'West'):
            ans = (orginal[0]-1,orginal[1])
        return ans 
