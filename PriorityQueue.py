class PriorityQueue:
    def __init__(self):
        self.queue = []
    
    def isEmpty(self):
        return len(self.queue) == 0

    def insert(self,node):
        self.queue.append(node)

    def delete(self):
        try:
            min_val = 0
            for i in range(len(self.queue)):
                if self.getCost(self.queue[i]) < self.getCost(self.queue[min_val]):
                    min_val = i
            node = self.queue.pop(min_val)
            return node
        except IndexError:
            print()
            exit()

    def getCost(self, node):
        if(node.action == "F_EAST" or node.action == "F_WEST" or node.action == "F_NORTH" or node.action == "F_SOUTH"):
            return 1
        elif(node.action == "V_EAST" or node.action == "V_WEST"):
            return 2
        elif(node.action == "F_PUT" or node.action == "F_PICK"):
            return 0.5
        elif(node.action == "V_UP"):
            return 4
        elif(node.action == "V_DOWN"):
            return 3
        elif(node.action == "V_PICK"):
            return 1.5
        elif(node.action == "V_PUT"):
            return 2.5
        else:
            return 0
        
    def isOnQueue(self,node):
        for frontierNode in self.queue:
            if(node.state.toString() == frontierNode.state.toString()):
                return True
        return False

    def swapNode(self, node):
        count = 0
        for frontierNode in self.queue:
            if(node.state.toString() == frontierNode.state.toString() and frontierNode.cost > node.cost):
                self.queue[count] = node
            count = count + 1

    def getSize(self):
        return len(self.queue)