import os
from pyglet import image


class VoronoiImage:
    def __init__(self, imageName):
        directory = os.path.abspath(os.path.dirname(__file__))
        directory = os.path.join(directory, 'data')
        full_path = os.path.join(directory, imageName)
        self.image = image.load(full_path)
        self.x = 0
        self.y = 0
    
    def draw(self):
        self.image.blit(self.x, self.y)
