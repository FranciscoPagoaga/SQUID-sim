class DeliveryState:
    def __init__(self, loadDestination, loadPosX, loadPosY, loadPosZ,dropDestination, dropPosX,dropPosY,dropPosZ,picked,delivered):
        self.loadDestination = loadDestination
        self.loadPosX = loadPosX
        self.loadPosY = loadPosY
        self.loadPosZ = loadPosZ
        self.picked = picked
        self.dropDestination = dropDestination
        self.dropPosX = dropPosX
        self.dropPosY = dropPosY
        self.dropPosZ = dropPosZ
        self.delivered = delivered

    def toString(self):
        return f'picked: {self.picked} delivered: {self.delivered} '        

    