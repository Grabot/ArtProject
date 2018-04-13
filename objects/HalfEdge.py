
class HalfEdge():
    def __init__(self, node, edge, nextEdge, face):
        self.node = node 			# vertex at the end of the half-edge
        self.edge = edge 			# oppositely oriented adjacent half-edge 
        self.nextEdge = nextEdge 	# next half-edge around the face
        self.face = face 			# face the half-edge borders
