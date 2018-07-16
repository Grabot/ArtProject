class HalfEdge:
    def __init__(self, node, face=None, adjacent_edge=None, next_edge=None):
        self.node = node  # vertex at the end of the half-edge
        self.face = face  # face the half-edge borders
        self.adjacent_edge = adjacent_edge  # oppositely oriented adjacent half-edge
        self.next_edge = next_edge  # next half-edge around the face
