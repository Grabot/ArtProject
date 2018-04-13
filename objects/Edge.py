class Edge:
    def __init__(self, nodeFrom, nodeTo):
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo

    def setNodeFrom(self, nodeFrom):
        self.nodeFrom = nodeFrom

    def getNodeFrom(self):
        return self.nodeFrom

    def setNodeTo(self, nodeTo):
        self.nodeTo = nodeTo

    def getNodeTo(self):
        return self.nodeTo
