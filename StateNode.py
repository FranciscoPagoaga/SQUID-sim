from DeliveryState import DeliveryState
class StateNode:

    def __init__(self, cost, parent, deliveryStates, action, posX, posY, posZ):
        self.cost=cost
        self.parent=parent
        self.deliveryStates = deliveryStates
        self.childs = []
        self.action = action
        self.posX = posX
        self.posY = posY
        self.posZ = posZ