import os
from pyglet import window
from pyglet import clock
from pyglet import image
from pyglet.gl import *
from PIL import Image


class MainWindow(window.Window):

	def __init__(self, width, height, imageName, name):
		window.Window.__init__(self, width, height, name)
		self.set_mouse_visible(False)
		self.voronoiImage = VoronoiImage(imageName)

	def main_loop(self):
		clock.set_fps_limit(30)

		while not self.has_exit:
			self.dispatch_events()
			self.clear()

			self.draw()

			gl.glEnable(gl.GL_BLEND)
			gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
			# draw the nodes with how you can give it a colour
			glColor4f(1, 0, 0, 1.0)
			pyglet.graphics.draw(4, GL_QUADS, ('v2f', [250,250, 250,260, 260,260, 260,250]))
			# draw the edges
			pyglet.graphics.draw(4, GL_LINES, ('v2f', (0, 0, 0, height, width / 2, height, width / 2, 0)))
			# draw the voronoi polygons (numberOfPoints, GL_POLYGON, ('v2f', [all x,y coordinates]))
			pyglet.graphics.draw(8, GL_POLYGON, ('v2f', [300,300, 300,400, 400,500, 500,500, 600,400, 600,300, 500,200, 400,200]))
			# white, so reset the colour
			glColor4f(1, 1, 1, 1)

			clock.tick()
			self.flip()


	def draw(self):
		self.voronoiImage.draw()


class VoronoiImage():

	def __init__(self, imageName):
		directory = os.path.abspath(os.path.dirname(__file__))
		directory = os.path.join(directory, 'data')
		full_path = os.path.join(directory, imageName)
		self.image = image.load(full_path)
		self.x = 0
		self.y = 0

	def draw(self):
		self.image.blit(self.x, self.y)


if __name__ == "__main__":
	imageName = "Oudegracht_Utrecht_2.png"
	directory = os.path.abspath(os.path.dirname(__file__))
	directory = os.path.join(directory, 'data')
	im = Image.open(directory + "\\" + imageName)
	(width, height) = im.size

	window = MainWindow(width, height, imageName, "Voronoi art project")
	window.main_loop()
