
class HalfEdge():
	def __init__(self, node, face, adjacentEdge=None, nextEdge=None):
		self.node = node 					# vertex at the end of the half-edge
		self.face = face 					# face the half-edge borders
		self.adjacentEdge = adjacentEdge 	# oppositely oriented adjacent half-edge 
		self.nextEdge = nextEdge 			# next half-edge around the face

	def getNode(self):
		return self.node

	def setNode(self, node):
		self.node = node

	def getFace(self):
		return self.face

	def setFace(self, face):
		self.face = face

	def getAdjacentEdge(self):
		return self.adjacentEdge

	def setAdjacentEdge(self, adjacentEdge):
		self.adjacentEdge = adjacentEdge

	def getNextEdge(self):
		return self.nextEdge

	def setNextEdge(self, nextEdge):
		self.nextEdge = nextEdge