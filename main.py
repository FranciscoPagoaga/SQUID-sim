import sys
from Robot import Robot

def main():
    fileName = sys.argv[1]
    newMap = Robot(fileName)
    print()

if __name__ == "__main__":
    main()