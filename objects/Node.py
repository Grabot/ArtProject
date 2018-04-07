class Node():
    def __init__(self, x, y, nodeIndex):
        self.x = x
        self.y = y
        self.nodeIndex = nodeIndex

    def setX(self, x):
        self.x = x

    def getX(self):
        return self.x

    def setY(self, y):
        self.y = y

    def getY(self):
        return self.y

    def getNodeIndex(self):
        return self.nodeIndex
