import sys
from StateNode import StateNode
from DeliveryState import DeliveryState


class Robot:
    def __init__(self, fileNameMap, fileNameDeliveries):
        self.posY = -1
        self.posX = -1
        self.posZ = 0
        self.maximumCost = 0

        # Border for future validations
        self.borderX = 0
        self.borderY = 0
        # File opening to assign map coordinate map
        lines = self.readMap(fileNameMap)
        self.coordinateMap = self.loadMap(lines)

        # File opening to create delivery list
        lines = self.readMap(fileNameDeliveries)
        tmpDeliveries = self.loadDeliveries(lines)

        # Root state node creation
        self.rootNode = StateNode(
            0, None, tmpDeliveries, None, self.posY, self.posX, self.posZ)

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
                self.maximumCost = int(line)
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
        loadposY = int((PosList[0])[1:])
        loadposX = int(PosList[1])
        # Skips the last parenthesis inside the splitted result
        loadPosZ = int((PosList[2])[:-1])
        
        #split coordinates
        PosList = line[3].split(",")
        # Skips the first parenthesis inside the splitted result
        dropposY = int((PosList[0])[1:])
        dropposX = int(PosList[1])
        # Skips the last parenthesis inside the splitted result
        dropPosZ = int((PosList[2])[:-1])
        return DeliveryState(loadDestination, loadposY, loadposX, loadPosZ, dropDestination, dropposY, dropposX, dropPosZ)

    def BreadthFirstSearch(self):
        if(self.isMoveValid("x",1)):
            print("valid move")
        else:
            print("not valid")
    # This validates if the move could be valid

    def isMoveValid(self, axis, value):
        # If the axis is X it checks if the move is valid by checking the border
        if (axis == "y"):
            if ((self.posY + value) < self.borderX and (self.posY + value) >= 0):
                #Condition to validate if the move has a Border, and obstacle, or is up on the shelf
                if  (self.coordinateMap[self.posY+value][self.posX] == "B" or
                    self.coordinateMap[self.posY+value][self.posX] == "X" or 
                    self.coordinateMap[self.posY+value][self.posX].isnumeric() or
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
            if ((self.posX + value) < self.borderY and (self.posX + value) >= 0):
                if  (self.coordinateMap[self.posY][self.posX+value] == "B" or
                    self.coordinateMap[self.posY][self.posX+value] == "X"): 
                    return False
                else:
                    #now, if it is valid, we need to check if the 
                    #robot is up on the shelf, if it is not, its just true
                    #due to all the conoditions met before
                    if(self.posZ > 0):
                        #If the robot is on the shelf, it can only move if it has a border,
                        #or a number on the north of its future position 
                        if  (self.coordinateMap[self.posY-1][self.posX+value].isnumeric() or
                            self.coordinateMap[self.posY-1][self.posX+value] == "B"):
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
            if  (self.coordinateMap[self.posY-1][self.posX] == "B" and  
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