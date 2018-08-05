class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.voronoi_edges = []

    def get_voronoi_edges(self):
        return self.voronoi_edges

    def add_voronoi_edge(self, edge):
        self.voronoi_edges.append(edge)

    def set_voronoi_edges(self, voronoi_edges):
        self.voronoi_edges = voronoi_edges

    def clear_voronoi_edges(self):
        self.voronoi_edges = []
