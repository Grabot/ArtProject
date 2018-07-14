from random import randint


class Face:
    def __init__(self, node1, node2, node3, edge=None):
        self.node1 = node1
        self.node2 = node2
        self.node3 = node3
        self.edge = edge
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255), 1.0]
