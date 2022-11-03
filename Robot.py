import sys
from StateNode import StateNode
from DeliveryState import DeliveryState

class Robot:
    def __init__(self, fileNameMap, fileNameDeliveries ):
        self.posX = -1
        self.posY = -1
        self.posZ = 0
        self.maximumCost = 0
        #File opening to assign map coordinate map
        lines = self.readMap(fileNameMap)
        self.coordinateMap = self.loadMap(lines)

        #File opening to create delivery list
        lines = self.readMap(fileNameDeliveries)
        tmpDeliveries = self.loadDeliveries(lines)

        #Root state node creation
        self.rootNode = StateNode(0,None,tmpDeliveries)

    def readMap(self, fileName):
        with open(fileName, "r") as file:
            info = file.readlines()
        return info
    
    def loadMap(self, info):
        rowCounter= 0
        columnCounter=0
        coordinateMap = []
        firstRun =  True
        for line in info:
            line = line.strip()
            #Loading dimensions of the map
            if firstRun:
                dimensions = line.split(",") 
                firstRun=False
            else:
            #Fill map with its matrices
                row = []
                for char in list(line):
                    row.append(char)
                    #Searching for the 'R' to know the starting coordinate
                    if char == "R":
                        self.posX = rowCounter
                        self.posY = columnCounter
                    columnCounter+=1
                columnCounter=0
                rowCounter+=1
                #Appends the whole row
                coordinateMap.append(row)
        return coordinateMap

    def loadDeliveries(self, info):
        isFirst = True
        deliveryList = []
        for line in info:
            line = line.strip()
            if isFirst:
                #Sets a maximum cost for later on searches 
                self.maximumCost = int(line)
                isFirst = False
            else:
                #Calls functino to return created object
                deliveryList.append(self.createDeliveryState(line))
        return deliveryList 
    
    def createDeliveryState(self, line):
        #String management to extract the coordinates and types
        line = line.split("-") 
        #Extracts the load and drop type
        loadDestination= line[0]
        dropDestination = line[2]
        #split the coordinates
        PosList = line[1].split(",")
        #Skips the first parenthesis inside the splitted result
        loadPosX = int((PosList[0])[1:])
        loadPosY = int(PosList[1]) 
        #Skips the last parenthesis inside the splitted result                
        loadPosZ = int((PosList[2])[:-1])             
        PosList = line[3].split(",")
        #Skips the first parenthesis inside the splitted result                
        dropPosX = int((PosList[0])[1:])
        dropPosY = int(PosList[1]) 
        #Skips the last parenthesis inside the splitted result                
        dropPosZ = int((PosList[2])[:-1])
        return DeliveryState(loadDestination, loadPosX, loadPosY, loadPosZ, dropDestination, dropPosX, dropPosY, dropPosZ)