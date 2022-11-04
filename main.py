import sys
from Robot import Robot

def main():
    fileNameMap = sys.argv[1]
    fileNameDeliveries = sys.argv[2]
    newRobot = Robot(fileNameMap,fileNameDeliveries)
    newRobot.BreadthFirstSearch()
    print()

if __name__ == "__main__":
    main()