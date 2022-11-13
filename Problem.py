from Node import Node

class Problem:
    def __init__(self, initalState, coordinateMap, maxCost, borderY, borderX):
        self.initialState = initalState
        self.coordinateMap = coordinateMap
        self.maxCost = maxCost
        self.borderY = borderY
        self.borderX = borderX
        
        rootNode = Node(0, None, self.initialState.deliveryState, None, 9, 1, 0)

        # for node in self.getActions(rootNode):
        #     print(node.state.toString())

    def getActions(self, node):
        returnedNodes = []
        if(node.cost < self.maxCost):
            deliveryType = self.isOnCoordinate(node.state.deliveryState,node.state.posX, node.state.posY, node.state.posZ) 
            if(deliveryType != ""):
                if(node.state.posZ>0 and deliveryType == "load" and self.isLoadable(node.state.deliveryState)):
                    updatedDeliveries = self.searchDeliveryOcurrence(node.state.deliveryState, node.state.posX, node.state.posY, node.state.posZ)
                    tmpNode = Node(node.cost + 1.5, node, updatedDeliveries, "V_PICK", node.state.posX, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
                elif(node.state.posZ>0 and deliveryType == "put"):
                    updatedDeliveries = self.searchDeliveryOcurrence(node.state.deliveryState, node.state.posX, node.state.posY, node.state.posZ)
                    tmpNode = Node(node.cost + 2.5, node, updatedDeliveries, "V_PUT", node.state.posX, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
                elif(node.state.posZ == 0 and deliveryType == "load" and self.isLoadable(node.state.deliveryState)):
                    updatedDeliveries = self.searchDeliveryOcurrence(node.state.deliveryState, node.state.posX, node.state.posY, node.state.posZ)
                    tmpNode = Node(node.cost + 0.5, node, updatedDeliveries, "F_PICK", node.state.posX, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
                elif(node.state.posZ == 0 and deliveryType == "put"):
                    updatedDeliveries = self.searchDeliveryOcurrence(node.state.deliveryState, node.state.posX, node.state.posY, node.state.posZ)                        
                    tmpNode = Node(node.cost + 0.5, node, updatedDeliveries, "F_PUT", node.state.posX, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
                        
            #validation to see if a movement to the west could be valid
            if(self.isMoveValid("y",1,node)):
                tmpNode = Node(node.cost + 1, node, node.state.deliveryState, "F_SOUTH", node.state.posX, node.state.posY + 1, node.state.posZ)
                returnedNodes.append(tmpNode)

            #validation to see if a movement to the west could be valid
            if(self.isMoveValid("y",-1,node)):
                tmpNode = Node(node.cost + 1, node, node.state.deliveryState, "F_NORTH", node.state.posX, node.state.posY - 1, node.state.posZ)
                returnedNodes.append(tmpNode)

            #validation to see if a movement to the west could be valid
            if(self.isMoveValid("x",1,node)):
                if(node.state.posZ > 0):
                    tmpNode =Node(node.cost + 2, node, node.state.deliveryState, "V_EAST", node.state.posX + 1, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
                else:
                    tmpNode = Node(node.cost + 1, node, node.state.deliveryState, "F_EAST", node.state.posX + 1, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)

            #validation to see if a movement to the west could be valid
            if(self.isMoveValid("x",-1,node)):
                #We must check if it is a movement to the west up on a shelf or on ground level
                if(node.state.posZ > 0):
                    #if it is up on the shelf the cost differs and is more expensive
                    tmpNode = Node(node.cost + 2, node, node.state.deliveryState, "V_WEST", node.state.posX - 1, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
                else:
                    #if it is on ground level the cost differs and is cheaper
                    tmpNode = Node(node.cost + 1, node, node.state.deliveryState, "F_WEST", node.state.posX - 1, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)

                #Checks if a movement upwards is valid in that position
                # if(self.isMoveValid("z",1,node)):
                #     tmpNode = Node(node.cost + 4, node, node.state.deliveryState, "V_UP", node.state.posX, node.state.posY, node.state.posZ + 1)
                #     returnedNodes.append(tmpNode)
                # #Checks if a movement downwards is valid in that position
                # if(self.isMoveValid("z",-1,node)):
                #     tmpNode = Node(node.cost + 3, node, node.state.deliveryState, "V_DOWN", node.state.posX, node.state.posY, node.state.posZ - 1)
                #     returnedNodes.append(tmpNode)
                
                
        return returnedNodes

    # This validates if the move could be valid
    def isMoveValid(self, axis, value, node):
        # If the axis is X it checks if the move is valid by checking the border
        if (axis == "y"):
            if ((node.state.posY + value) < self.borderY and (node.state.posY + value) >= 0):
                #Condition to validate if the move has a Border, and obstacle, or is up on the shelf
                if  (self.coordinateMap[node.state.posY+value][node.state.posX] == "B" or
                    self.coordinateMap[node.state.posY+value][node.state.posX] == "X" or 
                    self.coordinateMap[node.state.posY+value][node.state.posX].isnumeric() or
                    node.state.posZ > 0):
                    return False
                else:
                    return True
            else:
                return False
        elif (axis == "x"):
            #This gets a little convoluted but hang on.
            #If on posX value is out of bounds, or it moves 
            #to a position with a border or obstacle, its false
            if ((node.state.posX + value) < self.borderX and (node.state.posX + value) >= 0):
                if  (self.coordinateMap[node.state.posY][node.state.posX+value] == "B" or
                    self.coordinateMap[node.state.posY][node.state.posX+value] == "X"): 
                    return False
                else:
                    #now, if it is valid, we need to check if the 
                    #robot is up on the shelf, if it is not, its just true
                    #due to all the conoditions met before
                    if(node.state.posZ > 0):
                        #If the robot is on the shelf, it can only move if it has a border,
                        #or a number on the north of its future position 
                        if  (self.coordinateMap[node.state.posY-1][node.state.posX+value].isnumeric() or
                            self.coordinateMap[node.state.posY-1][node.state.posX+value] == "B"):
                            return True
                        else:
                            return False
                    else:

                        return True
            else:
                return False
        elif (axis == "z"):
            #Z axis is simpler, just check if there is a Border on its north
            #you must also check if the movement upwards is still on the range
            #of the shelf, or it is going below zero level
            if  (self.coordinateMap[node.state.posY-1][node.state.posX] == "B" and  
                (node.state.posZ + value < self.getShelfLevels(node) and 
                node.state.posZ + value >0)):
                return True
            else:
                return False

    def getShelfLevels(self,node):
        #Gets how many levels the shelf has by cheking either y+1 and x+1 or x-1
        if(self.coordinateMap[node.state.posY-1][node.state.posX+1].isnumeric()):
            return int(self.coordinateMap[node.state.posY-1][node.state.posX+1])
        elif(self.coordinateMap[node.state.posY-1][node.state.posX-1].isnumeric()):
            return int(self.coordinateMap[node.state.posY-1][node.state.posX-1])
        else:
            return -1

    def isOnCoordinate(self, deliveryStates ,posX,posY,posZ):
        for delivery in deliveryStates:
            if  (delivery.picked == False):
                if(delivery.loadPosX == posX and delivery.loadPosY == posY and delivery.loadPosZ == posZ ):
                    return "load"
            elif (delivery.delivered == False):
                if(delivery.dropPosX == posX and delivery.dropPosY == posY and delivery.dropPosZ == posZ ):
                    return "put"
        return ""

    def searchDeliveryOcurrence(self, deliveryStates, posX, posY, posZ):
        deliveryResult = []
        flag = 0
        for delivery in deliveryStates:
            if(delivery.picked == False):
                if  (delivery.loadPosX == posX and 
                    delivery.loadPosY == posY and
                    delivery.loadPosZ == posZ and
                    flag == 0):
                    delivery.picked = True
                    flag = flag  + 1
            elif(delivery.delivered == False):
                if  (delivery.dropPosX == posX and
                    delivery.dropPosY == posY and
                    delivery.dropPosZ == posZ and
                    flag == 0):
                    delivery.delivered = True
                    flag = flag + 1
            deliveryResult.append(delivery)
        return deliveryResult

    def isLoadable(self, deliveryStates):
        for delivery in deliveryStates:
            if(delivery.picked == True and delivery.picked == False):
                return False
        return True
    # def actions(self, state):
