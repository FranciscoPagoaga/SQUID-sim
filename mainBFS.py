import sys
import time
from Robot import Robot

def main():
    fileNameMap = sys.argv[1]
    fileNameDeliveries = sys.argv[2]
    newRobot = Robot(fileNameMap,fileNameDeliveries)
    f = open("bfs.txt", "w")
    for move in newRobot.breadthFirstSearch():
        f.write(move + "\n")
    f.close()

if __name__ == "__main__":
    main()