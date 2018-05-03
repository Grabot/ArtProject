from random import randint

class Face:
    def __init__(self, node1, node2, node3, edge = None):
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.edge = edge
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255), 1.0]

    def setNode1(self, node1):
        self.node1 = node1

    def getNode1(self):
        return self.node1

    def setNode2(self, node2):
        self.node2 = node2

    def getNode2(self):
        return self.node2

    def setNode3(self, node3):
        self.node3 = node3

    def getNode3(self):
        return self.node3

    def setEdge(self, edge):
        self.edge = edge

    def getEdge(self):
        return self.edge

    def getColour(self):
        return self.colour