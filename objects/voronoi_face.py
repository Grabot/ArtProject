from random import randint


# noinspection SpellCheckingInspection
class VoronoiFace:
    def __init__(self):
        self.nodes = []
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255), 1.0]

    def add_node(self, node):
        self.nodes.append(node)

    def contains(self, node):
        return node in self.nodes

    def clear_nodes(self):
        self.nodes = []

    def get_nodes(self):
        return self.nodes
