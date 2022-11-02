import sys

class Robot:
    def __init__(self, fileName ):
        self.posX = -1
        self.posY = -1
        self.posZ = 0
        #File opening to assign map coordinate map
        self.coordinateMap = self.loadMap(fileName)

    def loadMap(self, fileName):
        rowCounter= 0
        columnCounter=0
        coordinateMap = []
        with open(fileName, "r") as file:
            info = file.readlines()
            firstRun =  True
            for line in info:
                line = line.strip()
                #Loading dimensions of the map
                if firstRun:
                   dimensions = line.split(",") 
                #coordinateMap[int(dimensions[0])][int(dimensions[1])]
                   print(dimensions[0], dimensions[1])
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
                    coordinateMap
        return coordinateMap