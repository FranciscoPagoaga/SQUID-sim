import sys
from Robot import Robot

def main():
    fileNameMap = sys.argv[1]
    fileNameDeliveries = sys.argv[2]
    newRobot = Robot(fileNameMap,fileNameDeliveries)
    f = open("statesSet.txt", "a")
    # for asd in newRobot.BreadthFirstSearch():
    #     f.write(asd + "\n")
        
    f.close()
    print()

if __name__ == "__main__":
    main()