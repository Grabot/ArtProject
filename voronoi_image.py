from os.path import abspath, dirname, join

from pyglet import image


# noinspection SpellCheckingInspection
class VoronoiImage:
    def __init__(self, imageName):
        directory = abspath(dirname(__file__))
        directory = join(directory, 'data')
        full_path = join(directory, imageName)
        self.image = image.load(full_path)
        self.x = 0
        self.y = 0
    
    def draw(self):
        self.image.blit(self.x, self.y)
