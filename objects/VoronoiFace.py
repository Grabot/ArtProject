from random import randint

class VoronoiFace:
    def __init__(self):
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255), 1.0]


    def getColour(self):
        return self.colour