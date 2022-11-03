import sys
from Robot import Robot

def main():
    fileNameMap = sys.argv[1]
    fileNameDeliveries = sys.argv[2]
    newMap = Robot(fileNameMap,fileNameDeliveries)
    print()

if __name__ == "__main__":
    main()