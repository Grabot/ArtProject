from random import randint


class Face:
    def __init__(self, node1, node2, node3, edge=None):
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.edge = edge
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255), 1.0]
        # Initialize the voronoi node.
        self.voronoi_node = []
        self.voronoi_edges = []

    def set_voronoi_node(self, voronoi_node):
        self.voronoi_node = voronoi_node

    def get_voronoi_node(self):
        return self.voronoi_node

    def set_voronoi_edges(self, voronoi_edges):
        self.voronoi_edges = voronoi_edges

    def get_voronoi_edges(self):
        return self.voronoi_edges

    def append_voronoi_edges(self, voronoi_edges):
        self.voronoi_edges.append(voronoi_edges)

    def clear_voronoi_edges(self):
        self.voronoi_edges = []
