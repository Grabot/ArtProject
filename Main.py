import os
from pyglet import window
from pyglet import clock
from pyglet.gl import *
from PIL import Image
import VoronoiImage as VoronoiImage
import objects.Node as Node
import objects.Edge as Edge


class MainWindow(window.Window):

	def __init__(self, width, height, imageName, name):
		window.Window.__init__(self, width, height, name)
		self.voronoiImage = VoronoiImage.VoronoiImage(imageName)
		self.node1 = Node.Node("node1", 300, 300)
		self.node2 = Node.Node("node2", 400, 400)
		self.edge1 = Edge.Edge("edge1", self.node1, self.node2)

		# mannually adding nodes and edges to a list. This will be automated later when the user clicks
		self.nodes = []
		self.nodes.append(self.node1)
		self.nodes.append(self.node2)

		self.edges = []
		self.edges.append(self.edge1)


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
			for n in self.nodes:
				nodeX = n.getX()
				nodeY = n.getY()
				pyglet.graphics.draw(4, GL_QUADS, ('v2f', [nodeX-5,nodeY-5, nodeX-5,nodeY+5, nodeX+5,nodeY+5, nodeX+5,nodeY-5]))
			# draw the edges
			for e in self.edges:
				nodeFrom = e.getNodeFrom()
				nodeTo = e.getNodeTo()
				pyglet.graphics.draw(4, GL_LINES, ('v2f', (0, 0, 0, height, nodeFrom.getX(), nodeFrom.getY(), nodeTo.getX(), nodeTo.getY())))
			# draw the voronoi polygons (numberOfPoints, GL_POLYGON, ('v2f', [all x,y coordinates]))
			# pyglet.graphics.draw(8, GL_POLYGON, ('v2f', [300,300, 300,400, 400,500, 500,500, 600,400, 600,300, 500,200, 400,200]))
			# white, so reset the colour
			glColor4f(1, 1, 1, 1)

			clock.tick()
			self.flip()

	def draw(self):
		self.voronoiImage.draw()

	# Event handlers
	def on_mouse_motion(self, x, y, dx, dy):
		pass

	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		pass

	def on_mouse_press(self, x, y, button, modifiers):
		pass

	def on_mouse_release(self, x, y, button, modifiers):
		pass


if __name__ == "__main__":
	imageName = "Oudegracht_Utrecht_2.png"
	imagePath = os.path.abspath(os.path.dirname(__file__))
	imagePath = os.path.join(imagePath, 'data')
	imagePath = os.path.join(imagePath, imageName)
	im = Image.open(imagePath)
	(width, height) = im.size

	window = MainWindow(width, height, imageName, "Voronoi art project")
	window.main_loop()
