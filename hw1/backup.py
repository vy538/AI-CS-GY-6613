
        def getOpposite(action):
            if action == "North":
                return "South"
            if action == "South":
                return "North"
            if action == "West":
                return "East"
            if action == "East":
                return "West"
            return None

        def checkDuplicate(a1,a2):
            if a1 == getOpposite(a2):
                return penalty
            return 0

        def actionsScore(actions):
            ans = 0
            if actions:
                duplicate = []
                if self.lastAction == getOpposite(actions[0]):
                    ans += firstPenalty
                for i in range(0,len(actions),2):
                    if i+1 < len(actions):
                        ans += checkDuplicate(actions[i],actions[i+1])
                # print("actions score",ans)
            return ans