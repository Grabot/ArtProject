import objects.Node as Node
import objects.Edge as Edge
import objects.HalfEdge as HalfEdge
import objects.Face as Face
import numpy

class Graph:
	def __init__(self, nodes=[], edges=[], faces=[]):
		self.nodes = nodes
		self.edges = edges
		self.faces = faces
		# Now we won't use it anymore, but it is nice that it works and it is nice to have.
		self.convexHullEdges = []

	def setNodes(self, nodes):
		self.nodes = nodes

	def getNodes(self):
		return self.nodes

	def setEdges(self, edges):
		self.edges = edges

	def getEdges(self):
		return self.edges

	def setFaces(self, faces):
		self.faces = faces

	def getFaces(self):
		return self.faces


	def flipEdge(self, e):
		# First a simple check if we can flip the edge.
		if e.getAdjacentEdge() == None:
			return
		# First we find the 2 faces that the edge has.
		e1 = e
		e2 = e.getAdjacentEdge()
		face1 = e1.getFace()
		face2 = e2.getFace()
		node1 = e1.getNextEdge().getNode()
		node2 = e2.getNextEdge().getNode()

		# Create the new Half Edge.
		e1_1 = HalfEdge.HalfEdge(node1)
		e2_1 = HalfEdge.HalfEdge(node2)

		e1_1.setAdjacentEdge(e2_1)
		e2_1.setAdjacentEdge(e1_1)

		# Set the correct next edges.
		e1_1.setNextEdge(e1.getNextEdge().getNextEdge())
		e2_1.setNextEdge(e2.getNextEdge().getNextEdge())

		# The new next edge here used to be on the corner, so it's easier to take it from the other side
		e1_1.getNextEdge().setNextEdge(e2.getNextEdge())
		e2_1.getNextEdge().setNextEdge(e1.getNextEdge())

		e1_1.getNextEdge().getNextEdge().setNextEdge(e1_1)
		e2_1.getNextEdge().getNextEdge().setNextEdge(e2_1)

		# Create the new faces.
		node1Face1 = e1_1.getNode()
		node2Face1 = e1_1.getNextEdge().getNode()
		node3Face1 = e1_1.getNextEdge().getNextEdge().getNode()
		newFace1 = Face.Face(node1Face1, node2Face1, node3Face1, e1_1)

		# Create face 2
		node1Face2 = e2_1.getNode()
		node2Face2 = e2_1.getNextEdge().getNode()
		node3Face2 = e2_1.getNextEdge().getNextEdge().getNode()
		newFace2 = Face.Face(node1Face2, node2Face2, node3Face2, e2_1)

		e1_1.setFace(newFace1)
		e2_1.setFace(newFace2)

		# Add the new faces and also remove the old ones.
		self.faces.append(newFace1)
		self.faces.append(newFace2)

		self.faces.remove(face1)
		self.faces.remove(face2)

		# Do the same with the new edges.
		self.edges.append(e1_1)
		self.edges.append(e2_1)

		self.edges.remove(e1)
		self.edges.remove(e2)
		print("flipping the flippin edge")
		return e1_1


	def manuallyFlipEdge(self, edgeToFlip):
		for e in self.edges:
			if e == edgeToFlip:
				print("flipping the flippin edge")
				return self.flipEdge(e)


	def inCircle(self, A, B, C, D):
		# returns True is D lies in the circumcircle of ABC
		# This is done by determining the determinant of a matrix.
		M = [[A.getX(), A.getY(), (pow(A.getX(), 2) + pow(A.getY(), 2)), 1],
			 [B.getX(), B.getY(), (pow(B.getX(), 2) + pow(B.getY(), 2)), 1],
			 [C.getX(), C.getY(), (pow(C.getX(), 2) + pow(C.getY(), 2)), 1],
			 [D.getX(), D.getY(), (pow(D.getX(), 2) + pow(D.getY(), 2)), 1]]
		return numpy.linalg.det(M) > 0

	def validEdge(self, triangleNode1, triangleNode2, triangleNode3, node):
		return not self.inCircle(triangleNode1, triangleNode2, triangleNode3, node)


	def checkFlipEdge(self, edge, node):		
		if edge.getAdjacentEdge() != None:
			adjacentEdge = edge.getAdjacentEdge()
			otherFaceNode1 = adjacentEdge.getNode()
			otherFaceNode2 = adjacentEdge.getNextEdge().getNode()
			otherFaceNode3 = adjacentEdge.getNextEdge().getNextEdge().getNode()
			if not self.validEdge(otherFaceNode1, otherFaceNode2, otherFaceNode3, node):
				print("edge is not valid, flip it!")
				newEdge = self.flipEdge(edge)

				# TODO, you should add the other edges
				self.checkFlipEdge(newEdge, node)
			else:
				return False


	def inFace(self, p0, p1, p2, node):
		Area = 0.5 * (-p1.getY() * p2.getX() + p0.getY() * (-p1.getX() + p2.getX()) + p0.getX() * (
			p1.getY() - p2.getY()) + p1.getX() * p2.getY())

		s = 1 / (2 * Area) * (p0.getY() * p2.getX() - p0.getX() * p2.getY() + (p2.getY() - p0.getY()) * node.getX() + (
			p0.getX() - p2.getX()) * node.getY())
		t = 1 / (2 * Area) * (p0.getX() * p1.getY() - p0.getY() * p1.getX() + (p0.getY() - p1.getY()) * node.getX() + (
			p1.getX() - p0.getX()) * node.getY())

		return s > 0 and t > 0 and 1 - s - t > 0

	def addNode(self, node):
		# We have added a node, so we want to find out which face it is in and connect it with edges
		for f in self.faces:
			if self.inFace(f.getNode1(), f.getNode2(), f.getNode3(), node):
				# The 3 edges of the face that is chosen.
				edge1 = f.getEdge()
				edge2 = edge1.getNextEdge()
				edge3 = edge2.getNextEdge()

				# Create 3 new edges. and we need to fix the other half edges to get the correct "next edge"
				edge1_1 = HalfEdge.HalfEdge(node)
				edge1_2 = HalfEdge.HalfEdge(f.getNode1())

				edge2_1 = HalfEdge.HalfEdge(node)
				edge2_2 = HalfEdge.HalfEdge(f.getNode2())

				edge3_1 = HalfEdge.HalfEdge(node)
				edge3_2 = HalfEdge.HalfEdge(f.getNode3())

				# Set the new and correct "next edge" for all new half edges and the 3 half edges of the face.
				edge1.setNextEdge(edge1_1)
				edge1_1.setNextEdge(edge3_2)
				edge3_2.setNextEdge(edge1)

				edge2.setNextEdge(edge2_1)
				edge2_1.setNextEdge(edge1_2)
				edge1_2.setNextEdge(edge2)

				edge3.setNextEdge(edge3_1)
				edge3_1.setNextEdge(edge2_2)
				edge2_2.setNextEdge(edge3)

				# Set the new and correct adjacent edges. These stay the same for the original 3 face edges, but should be set for the newly created edges.
				edge1_1.setAdjacentEdge(edge1_2)
				edge1_2.setAdjacentEdge(edge1_1)
				edge2_1.setAdjacentEdge(edge2_2)
				edge2_2.setAdjacentEdge(edge2_1)
				edge3_1.setAdjacentEdge(edge3_2)
				edge3_2.setAdjacentEdge(edge3_1)

				# We will add the 3 newly created faces. with a half edge for each face. and set the faces on the half edges
				# Create face 1
				node1Face1 = edge1_1.getNode()
				node2Face1 = edge1_1.getNextEdge().getNode()
				node3Face1 = edge1_1.getNextEdge().getNextEdge().getNode()
				face1 = Face.Face(node1Face1, node2Face1, node3Face1, edge1_1)

				# Create face 2
				node1Face2 = edge2_1.getNode()
				node2Face2 = edge2_1.getNextEdge().getNode()
				node3Face2 = edge2_1.getNextEdge().getNextEdge().getNode()
				face2 = Face.Face(node1Face2, node2Face2, node3Face2, edge2_1)

				node1Face3 = edge3_1.getNode()
				node2Face3 = edge3_1.getNextEdge().getNode()
				node3Face3 = edge3_1.getNextEdge().getNextEdge().getNode()
				face3 = Face.Face(node1Face3, node2Face3, node3Face3, edge3_1)

				edge1_1.setFace(face1)
				edge1_2.setFace(face2)
				edge2_1.setFace(face2)
				edge2_2.setFace(face3)
				edge3_1.setFace(face3)
				edge3_2.setFace(face1)
				edge1.setFace(face1)
				edge2.setFace(face2)
				edge3.setFace(face3)

				self.faces.append(face1)
				self.faces.append(face2)
				self.faces.append(face3)

				# We don't have to remove edges, only add the newly created ones.
				self.edges.append(edge1_1)
				self.edges.append(edge1_2)
				self.edges.append(edge2_1)
				self.edges.append(edge2_2)
				self.edges.append(edge3_1)
				self.edges.append(edge3_2)

				# The original face is now replaced with 3 new ones, so we will remove the original
				self.faces.remove(f)

				# We want to check whether or not the edges are valid delaunay, we will do that by comparing
				# the new node with the 3 triangle nodes of the adjacent face.
				flip1 = self.checkFlipEdge(edge1, node)
				flip2 = True
				if not flip1:
					flip2 = self.checkFlipEdge(edge2, node)
				if not flip1 or not flip2:
					self.checkFlipEdge(edge3, node)



		self.nodes.append(node)


	def getConvexHullEdges(self):
		return self.convexHullEdges

	def orientation(self, p1, p2, p3):
		return (p2.getX() - p1.getX()) * (p3.getY() - p1.getY()) - (p3.getX() - p1.getX()) * (p2.getY() - p1.getY())

	def gift_wrapping(self):
		if len(self.nodes) < 3:
			# Not enough nodes for a convex hull calculation
			return

		# We are going to find the left most node in the set, this node will always be in the convex hull.
		minX = 9999999
		hullPoint = ""
		for n in self.nodes:
			if n.getX() < minX:
				hullPoint = n
				minX = n.getX()

		endPoint = ""
		finalPoints = []
		while finalPoints == [] or endPoint != finalPoints[0]:
			finalPoints.append(hullPoint)
			endPoint = self.nodes[0]

			for index in range(1, len(self.nodes)):
				# We want to find the angle between the last found point (finalPoints[-1]), the currently selected endPoint and the node we're looping over.
				# If the angle is better between the last found point and the current point we're checking (n) we will put the endPoint on that node.
				if hullPoint == endPoint or self.orientation(finalPoints[-1], endPoint, self.nodes[index]) > 0:
					# The orientation is on the leftside.
					endPoint = self.nodes[index]

			hullPoint = endPoint

		# Set the edges for the convex hull
		self.convexHullEdges = []
		for x in range(0, len(finalPoints) - 1):
			edge = Edge.Edge(finalPoints[x], finalPoints[x + 1])
			self.convexHullEdges.append(edge)
		# The final edge
		edge = Edge.Edge(finalPoints[-1], finalPoints[0])
		self.convexHullEdges.append(edge)
