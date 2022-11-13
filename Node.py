from DeliveryState import DeliveryState
from State import State
class Node:

    def __init__(self, cost, parent, deliveryStates, action, posX, posY, posZ):
        self.cost=cost
        self.parent=parent
        self.childs = []
        self.action = action
        self.state = State(posX, posY, posZ, deliveryStates)

    def addChild(self, node):
        self.childs.append(node)