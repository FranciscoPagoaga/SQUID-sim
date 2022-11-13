class State:

    def __init__(self, posX, posY, posZ, deliveryState):
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.deliveryState = deliveryState

    def toString(self):
        toStringDeliveries = ""
        for delivery in self.deliveryState:
            toStringDeliveries = toStringDeliveries + delivery.toString()
        return f'x: {self.posX} y: {self.posY} z: {self.posZ} deliveries: {toStringDeliveries}'