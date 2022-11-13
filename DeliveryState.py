class DeliveryState:
    def __init__(self, loadDestination, loadPosX, loadPosY, loadPosZ,dropDestination, dropPosX,dropPosY,dropPosZ):
        self.loadDestination = loadDestination
        self.loadPosX = loadPosX
        self.loadPosY = loadPosY
        self.loadPosZ = loadPosZ
        self.picked = False
        self.dropDestination = dropDestination
        self.dropPosX = dropPosX
        self.dropPosY = dropPosY
        self.dropPosZ = dropPosZ
        self.delivered = False
        # print(f"X: {self.dropPosX}, Y: {self.dropPosY}")

    def toString(self):
        return f'picked: {self.picked} delivered: {self.delivered} '        

    