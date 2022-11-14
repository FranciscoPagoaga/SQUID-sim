import sys
import time
from Robot import Robot

def main():
    fileNameMap = sys.argv[1]
    fileNameDeliveries = sys.argv[2]
    newRobot = Robot(fileNameMap,fileNameDeliveries)
    f = open("ucs.txt", "w")
    for move in newRobot.uniformCostSearch():
        f.write(move + "\n")

if __name__ == "__main__":
    main()