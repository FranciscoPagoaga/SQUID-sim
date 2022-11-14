import sys
import time
from Node import Node
from DeliveryState import DeliveryState
from Problem import Problem
from  PriorityQueue import PriorityQueue

class Robot:
    def __init__(self, fileNameMap, fileNameDeliveries):
        self.posY = -1
        self.posX = -1
        self.posZ = 0
        self.maxCost = 0
        
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
        return DeliveryState(loadDestination, loadposX, loadposY, loadPosZ, dropDestination, dropposX, dropposY, dropPosZ, False, False)

    def breadthFirstSearch(self):
        start_time = time.time()
        #Creates a node and assigns the rootnode
        node = self.rootNode
        #This are going to be our 2 most important tools, explored and frontier
        #with frontier we will know what next node we must explore
        #with explored we will know if a certain movement is already done
        frontier = []
        explored = set()
        frontier.append(node)
        while True:
            #if frontier gets to a point where its empty, bfs ends
            if(len(frontier) == 0):
                print("No se encontro solucion")
                return []

            #node now is a pointer that gets assigned the first position inside a queue
            node = frontier.pop(0)
            explored.add(node.state.toString())
            #We must validate if the path we are currently taken has already passed our max path cost
            #if it does, we stop searching in that way
            for childNode in self.problem.getActions(node):
                if(childNode.state.toString() not in explored and self.isNotInFrontier(childNode, frontier)):
                    if(self.problem.goalTest(childNode.state)):
                        print("Tiempo transcurrido: " + str(time.time() - start_time) + " segundos")
                        print("Nodos explorados: " + str(len(explored)))
                        print("Nodos frontera: " + str(len(frontier)))
                        return self.solution(childNode)
                    node.addChild(childNode)
                    frontier.append(childNode)

    def uniformCostSearch(self):
        start_time = time.time()
        node = self.rootNode
        frontier = PriorityQueue()
        explored = set()
        frontier.insert(node)
        while True:
            if(frontier.isEmpty()):
                print("No se encontro solucion")
                return []
            
            node = frontier.delete()
            explored.add(node.state.toString())

            for childNode in self.problem.getActions(node):
                if(childNode.state.toString() not in explored and not frontier.isOnQueue(childNode)):
                    if(self.problem.goalTest(childNode.state)):
                        print("Tiempo transcurrido: " + str(time.time() - start_time) + " segundos")
                        print("Nodos explorados: " + str(len(explored)))
                        print("Nodos frontera: " + str(frontier.getSize()))
                        return self.solution(childNode)
                    node.addChild(childNode)
                    frontier.insert(childNode)
                elif(frontier.isOnQueue(childNode)):
                    frontier.swapNode(childNode)

    def isNotInFrontier(self, node, frontier):
        for frontierNode in frontier:
            if(frontierNode.state.toString() == node.state.toString()):
                return False
        return True

    def solution(self, node):
        solutionList = []
        while(node.parent != None):
            solutionList.append(node.action)
            node = node.parent
        solutionList.reverse()
        return solutionList