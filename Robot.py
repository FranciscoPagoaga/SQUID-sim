import sys
from Node import Node
from DeliveryState import DeliveryState
from Problem import Problem

class Robot:
    def __init__(self, fileNameMap, fileNameDeliveries):
        self.posY = -1
        self.posX = -1
        self.posZ = 0
        self.maxCost = 0
        # Border for future validations
        self.borderX = 0
        self.borderY = 0
        
        # File opening to assign map coordinate map
        linesMap = self.readMap(fileNameMap)
        self.coordinateMap = self.loadMap(linesMap)

        # File opening to create delivery list
        linesDeliveries = self.readMap(fileNameDeliveries)
        tmpDeliveries = self.loadDeliveries(linesDeliveries)

        # Root state node creation
        self.rootNode = Node(0, None, tmpDeliveries, None, self.posX, self.posY, self.posZ)
        borders = linesMap[0].split(",")
        self.problem = Problem(self.rootNode.state, self.loadMap(linesMap), int(linesDeliveries[0]), int(borders[0]),int(borders[1]))

        # listaprueba = [self.rootNode]
        # print(self.isNotInFrontier(self.rootNode,listaprueba))

    def readMap(self, fileName):
        with open(fileName, "r") as file:
            info = file.readlines()
        return info

    def loadMap(self, info):
        rowCounter = 0
        columnCounter = 0
        coordinateMap = []
        firstRun = True
        for line in info:
            line = line.strip()
            # Loading dimensions of the map
            if firstRun:
                dimensions = line.split(",")
                self.borderY = int(dimensions[0])
                self.borderX = int(dimensions[1])
                firstRun = False
            else:
                # Fill map with its matrices
                row = []
                for char in list(line):
                    row.append(char)
                    # Searching for the 'R' to know the starting coordinate
                    if char == "R":
                        self.posY = int(rowCounter)
                        self.posX = int(columnCounter)
                    columnCounter += 1
                columnCounter = 0
                rowCounter += 1
                # Appends the whole row
                coordinateMap.append(row)
        return coordinateMap

    def loadDeliveries(self, info):
        isFirst = True
        deliveryList = []
        for line in info:
            line = line.strip()
            if isFirst:
                # Sets a maximum cost for later on searches
                self.maxCost = int(line)
                isFirst = False
            else:
                # Calls functino to return created object
                deliveryList.append(self.createDeliveryState(line))
        return deliveryList

    def createDeliveryState(self, line):
        # String management to extract the coordinates and types
        line = line.split("-")
        # Extracts the load and drop type
        loadDestination = line[0]
        dropDestination = line[2]
        # split the coordinates
        PosList = line[1].split(",")
        # Skips the first parenthesis inside the splitted result
        loadposX = int((PosList[0])[1:])
        loadposY = int(PosList[1])
        # Skips the last parenthesis inside the splitted result
        loadPosZ = int((PosList[2])[:-1])
        
        #split coordinates
        PosList = line[3].split(",")
        # Skips the first parenthesis inside the splitted result
        dropposX = int((PosList[0])[1:])
        dropposY = int(PosList[1])
        # Skips the last parenthesis inside the splitted result
        dropPosZ = int((PosList[2])[:-1])
        return DeliveryState(loadDestination, loadposX, loadposY, loadPosZ, dropDestination, dropposX, dropposY, dropPosZ)

    def BreadthFirstSearch(self):
        #Creates a node and assigns the rootnode
        node = self.rootNode
        #This are going to be our 2 most important tools, explored and frontier
        #with frontier we will know what next node we must explore
        #with explored we will know if a certain movement is already done
        frontier = []
        explored = set()
        frontier.append(node)
        f = open("states.txt", "a")
        cont = 1
        # f.write(node.state.toString() + "\n")
        while True:
            #if frontier gets to a point where its empty, bfs ends
            if(len(frontier) == 0):
                return explored

            #node now is a pointer that gets assigned the first position inside a queue
            node = frontier.pop(0)
            explored.add(node.state.toString())
            f.write(node.state.toString() + "\n")
            cont = cont + 1
            #We must validate if the path we are currently taken has already passed our max path cost
            #if it does, we stop searching in that way
            count = 0
            for childNode in self.problem.getActions(node):
                if(childNode.state.toString() not in explored and self.isNotInFrontier(childNode, frontier)):
                    if(node.state.toString() == "x: 7 y: 0 z: 0 deliveries: picked: False delivered: False picked: False delivered: False picked: False delivered: False picked: False delivered: False "):
                        print(childNode.state.toString())
                        frontier.append(childNode)
                    node.addChild(childNode)
                    frontier.append(childNode)
                    # explored.add(childNode.state.toString())

    # This validates if the move could be valid
    def isMoveValid(self, axis, value, node):
        # If the axis is X it checks if the move is valid by checking the border
        if (axis == "y"):
            if ((node.state.posY + value) < self.borderY and (node.state.posY + value) >= 0):
                #Condition to validate if the move has a Border, and obstacle, or is up on the shelf
                if  (self.coordinateMap[node.state.posY+value][node.state.posX] == "B" or
                    self.coordinateMap[node.state.posY+value][node.state.posX] == "X" or 
                    self.coordinateMap[node.state.posY+value][node.state.posX].isnumeric() or
                    self.posZ > 0):
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
                    if(self.posZ > 0):
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
            if  (self.coordinateMap[node.state.posY-1][self.posX] == "B" and  
                (self.posZ + value < self.getShelfLevels() and 
                self.posZ + value >0)):
                return True
            else:
                return False
                
    def getShelfLevels(self):
        #Gets how many levels the shelf has by cheking either y+1 and x+1 or x-1
        if(self.coordinateMap[self.posY-1][self.posX+1].isnumeric()):
            return int(self.coordinateMap[self.posY-1][self.posX+1])
        elif(self.coordinateMap[self.posY-1][self.posX-1].isnumeric()):
            return int(self.coordinateMap[self.posY-1][self.posX-1])
        else:
            return -1

    #returns a new DeliveryState if a change has been done 
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

    #returns if in that coordinate there is a pick up or a delivery and then 
    def isOnCoordinate(self, deliveryStates ,posX,posY,posZ):
        for delivery in deliveryStates:
            if  (delivery.picked == False):
                if(delivery.loadPosX == posX and delivery.loadPosY == posY and delivery.loadPosZ == posZ ):
                    return "load"
            elif (delivery.delivered == False):
                if(delivery.dropPosX == posX and delivery.dropPosY == posY and delivery.dropPosZ == posZ ):
                    return "put"
        return ""


    def leftDeliveries(self, deliveryStates):
        for delivery in deliveryStates:
            if(delivery.picked == False or delivery.picked == False ):
                return True

    def isNotInFrontier(self, node, frontier):
        for frontierNode in frontier:
            if(frontierNode.state.toString() == node.state.toString()):
                return False
        return True