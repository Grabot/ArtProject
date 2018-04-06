
class Edge():

    def __init__(self, name, nodeFrom, nodeTo):
        self.name = name
        self.nodeFrom = nodeFrom
        self.nodeTo = nodeTo

    def getName(self):
        return self.name

    def setNodeFrom(self, nodeFrom):
    	self.nodeFrom = nodeFrom

    def getNodeFrom(self):
    	return self.nodeFrom

    def setNodeTo(self, nodeTo):
    	self.nodeTo = nodeTo

    def getNodeTo(self):
    	return self.nodeTo