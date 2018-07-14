from random import randint


class VoronoiFace:
    def __init__(self, nodes=None):
        self.nodes = nodes or []
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255), 1.0]
    
    def getColour(self):
        return self.colour
    
    def setNodes(self, nodes):
        self.nodes = nodes
    
    def getNodes(self):
        return self.nodes
