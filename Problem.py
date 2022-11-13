from Node import Node
from DeliveryState import DeliveryState
class Problem:
    def __init__(self, initalState, coordinateMap, maxCost, borderY, borderX):
        self.initialState = initalState
        self.coordinateMap = coordinateMap
        self.maxCost = maxCost
        self.borderY = borderY
        self.borderX = borderX
        
        rootNode = Node(0, None, self.initialState.deliveryState, None, 9, 1, 0)

    def getActions(self, node):
        returnedNodes = []
        if(node.cost < self.maxCost):
            #If it wants to pick an item, it checks if there is more than one pickable item,
            #if there is it iterates through a list
            for position in self.pickList(node):
                if(node.state.posZ>0 ):
                    #Creates a new delivery state item, due to problems with pointers and the queue
                    tmpDelivery = self.newDeliveryState(node.state.deliveryState)
                    #it assigns the position as true and creates the node
                    tmpDelivery[position].picked = True
                    tmpNode = Node(node.cost + 1.5, node, tmpDelivery, "V_PICK", node.state.posX, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
                else:
                    #Creates a new delivery state item, due to problems with pointers and the queue
                    tmpDelivery = self.newDeliveryState(node.state.deliveryState)
                    #it assigns the position as true and creates the node
                    tmpDelivery[position].picked = True
                    tmpNode = Node(node.cost + 0.5, node, tmpDelivery, "F_PICK", node.state.posX, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
            
            #checks if there can be a delivery done, and gives the position in the deliveryList
            deliverPos = self.deliverable(node)
            #if the funtion returns -1, it doesnt have a deliverable item
            if(deliverPos != -1):
                #if it does it creates, and check if it is on ground level or up on a shelf
                tmpDelivery = self.newDeliveryState(node.state.deliveryState)
                tmpDelivery[deliverPos].delivered = True
                if(node.state.posZ>0):
                    tmpNode = Node(node.cost + 2.5, node, tmpDelivery, "V_PUT", node.state.posX, node.state.posY, node.state.posZ)
                    returnedNodes.append(tmpNode)
                else:
                    tmpNode = Node(node.cost + 0.5, node, tmpDelivery, "F_PUT", node.state.posX, node.state.posY, node.state.posZ)
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
                if(self.isMoveValid("z",1,node)):
                    tmpNode = Node(node.cost + 4, node, node.state.deliveryState, "V_UP", node.state.posX, node.state.posY, node.state.posZ + 1)
                    returnedNodes.append(tmpNode)
                #Checks if a movement downwards is valid in that position
                if(self.isMoveValid("z",-1,node)):
                    tmpNode = Node(node.cost + 3, node, node.state.deliveryState, "V_DOWN", node.state.posX, node.state.posY, node.state.posZ - 1)
                    returnedNodes.append(tmpNode)
                
                
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
                (node.state.posZ + value <= self.getShelfLevels(node) and 
                node.state.posZ + value >= 0)):
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

    #Creates a new deliveryState to deal with reference errors
    def newDeliveryState(self, deliveryStates):
        deliveryResult = []
        for delivery in deliveryStates:
            loadDestination = delivery.loadDestination
            loadPosX = delivery.loadPosX
            loadPosY = delivery.loadPosY
            loadPosZ = delivery.loadPosZ
            dropDestination = delivery.dropDestination
            dropPosX = delivery.dropPosX
            dropPosY = delivery.dropPosY
            dropPosZ = delivery.dropPosZ
            picked = delivery.picked
            delivered = delivery.delivered
            tmpDelivery = DeliveryState(loadDestination, loadPosX, loadPosY, loadPosZ, dropDestination, dropPosX, dropPosY, dropPosZ, picked, delivered)
            deliveryResult.append(tmpDelivery)
        return deliveryResult

    #function to check if all deliveries have been done
    def goalTest(self, state):
        for deliveries in state.deliveryState:
            if(not deliveries.picked or not deliveries.delivered):
                return False
        return True

    #returns a list of numbers to check if theres more than one item
    #you can pick in that given coordinate
    def pickList(self, node):
        positionList = []
        counter = 0
        for deliveryState in node.state.deliveryState:
            if(deliveryState.picked == True and deliveryState.delivered == False):
                return []
            if(node.state.posZ > 0):
                if  (deliveryState.picked == False and 
                    node.state.posX == deliveryState.loadPosX and 
                    node.state.posY-1 == deliveryState.loadPosY and 
                    node.state.posZ == deliveryState.loadPosZ):
                    positionList.append(counter)
            else:    
                if  (deliveryState.picked == False and 
                    node.state.posX == deliveryState.loadPosX and 
                    node.state.posY == deliveryState.loadPosY and 
                    node.state.posZ == deliveryState.loadPosZ):
                    positionList.append(counter)
            counter = counter + 1
        return positionList
    
    #checks if we're in a coordinate to do a delivery and also
    #if we have that order picked to deliver
    def deliverable(self, node):
        counter = 0
        for deliveryState in node.state.deliveryState:
            #checks if its either on ground level or up on a shelf
            if(node.state.posZ >0):
                #checks if something is picked and hasnt been delivered in that coordinate
                #if its on a counter it has to check if it has a delivery position in front of him
                if  (deliveryState.picked == True and 
                    node.state.posX == deliveryState.dropPosX and 
                    node.state.posY-1 == deliveryState.dropPosY and 
                    node.state.posZ == deliveryState.dropPosZ and
                    deliveryState.delivered == False):
                    #returns the position in the list of deliveryStates to modify
                    return counter
            else:
                #checks if it is already picked and if the delivery hasnt been done
                #checks if a delivery can be done at that position
                if  (deliveryState.picked == True and 
                    node.state.posX == deliveryState.dropPosX and 
                    node.state.posY == deliveryState.dropPosY and 
                    node.state.posZ == deliveryState.dropPosZ and
                    deliveryState.delivered == False):
                    #returns the position in the list of deliveryStates to modify
                    return counter
            counter = counter + 1 
        return -1