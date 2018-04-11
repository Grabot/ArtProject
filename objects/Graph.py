import objects.Node as Node
import objects.Edge as Edge

class Graph():
    def __init__(self, nodes = [], edges = [], faces = []):
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

    def addNode(self, node):
    	self.nodes.append(node)

    def getConvexHullEdges(self):
    	return self.convexHullEdges


    def orientation(self, p1, p2, p3):
        orientation = (p2.getX() - p1.getX()) * (p3.getY() - p1.getY()) - (p3.getX() - p1.getX()) * (
        p2.getY() - p1.getY());
        return orientation


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
        for x in range(0, len(finalPoints)-1):
            edge = Edge.Edge(finalPoints[x], finalPoints[x+1])
            self.convexHullEdges.append(edge)
        # The final edge
        edge = Edge.Edge(finalPoints[-1], finalPoints[0])
        self.convexHullEdges.append(edge)