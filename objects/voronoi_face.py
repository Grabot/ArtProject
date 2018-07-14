from random import randint


class VoronoiFace:
    def __init__(self, nodes=None):
        self.nodes = nodes or []
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255), 1.0]
