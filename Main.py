import os
import math
from math import sqrt, cos, sin, pi
from pyglet import window
from pyglet import clock
from pyglet.gl import *
from PIL import Image
import VoronoiImage as VoronoiImage
import objects.Node as Node
import objects.HalfEdge as HalfEdge
import objects.Face as Face
import objects.Graph as Graph


class MainWindow(window.Window):
	def __init__(self, width, height, imageName, name):
		window.Window.__init__(self, width, height, name)
		self.width = width
		self.height = height
		self.voronoiImage = VoronoiImage.VoronoiImage(imageName)

		# Mannually add 4 nodes with triangulation edges far outside the sight to make it easy to make the delaunay and voronoi calculations.
		node1 = Node.Node(-99999999, -99999999)
		node2 = Node.Node(99999999, -99999999)
		node3 = Node.Node(0, 99999999)
		# We'll also initialize a point in the field (not 0, 0 since that's the bottom left corner)
		node4 = Node.Node(600, 400)

		face1 = Face.Face(node1, node2, node4)
		face2 = Face.Face(node2, node3, node4)
		face3 = Face.Face(node3, node1, node4)

		halfEdge1 = HalfEdge.HalfEdge(node1, face1)
		halfEdge2 = HalfEdge.HalfEdge(node2, face1)
		halfEdge3 = HalfEdge.HalfEdge(node4, face1)
		halfEdge4 = HalfEdge.HalfEdge(node2, face2)
		halfEdge5 = HalfEdge.HalfEdge(node3, face2)
		halfEdge6 = HalfEdge.HalfEdge(node4, face2)
		halfEdge7 = HalfEdge.HalfEdge(node3, face3)
		halfEdge8 = HalfEdge.HalfEdge(node1, face3)
		halfEdge9 = HalfEdge.HalfEdge(node4, face3)

		nodes = []
		nodes.append(node1)
		nodes.append(node2)
		nodes.append(node3)
		nodes.append(node4)
		faces = []
		faces.append(face1)
		faces.append(face2)
		faces.append(face3)
		halfEdges = []
		halfEdges.append(halfEdge1)
		halfEdges.append(halfEdge2)
		halfEdges.append(halfEdge3)
		halfEdges.append(halfEdge4)
		halfEdges.append(halfEdge5)
		halfEdges.append(halfEdge6)
		halfEdges.append(halfEdge7)
		halfEdges.append(halfEdge8)
		halfEdges.append(halfEdge9)

		halfEdge1.setAdjacentEdge(halfEdge9)
		halfEdge1.setNextEdge(halfEdge2)
		# It is possible that there isn't a adjacent Edge. This is the case for the outer edges.
		halfEdge2.setNextEdge(halfEdge3)
		halfEdge3.setAdjacentEdge(halfEdge4)
		halfEdge3.setNextEdge(halfEdge1)
		halfEdge4.setAdjacentEdge(halfEdge3)
		halfEdge4.setNextEdge(halfEdge5)
		halfEdge5.setNextEdge(halfEdge6)
		halfEdge6.setAdjacentEdge(halfEdge7)
		halfEdge6.setNextEdge(halfEdge4)
		halfEdge7.setAdjacentEdge(halfEdge8)
		halfEdge7.setNextEdge(halfEdge6)
		halfEdge8.setNextEdge(halfEdge9)
		halfEdge9.setAdjacentEdge(halfEdge1)
		halfEdge9.setNextEdge(halfEdge7)
		self.graph = Graph.Graph(nodes, halfEdges, faces)
		# The graph doesn't have any nodes or edges yet.


	def main_loop(self):
		clock.set_fps_limit(30)
		nodeSize = 5

		while not self.has_exit:
			self.dispatch_events()
			self.clear()

			# White, so reset the colour
			glColor4f(1, 1, 1, 1)
			self.draw()

			gl.glEnable(gl.GL_BLEND)
			gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
			# Draw the nodes with how you can give it a colour
			glColor4f(1, 0, 0, 1.0)
			for n in self.graph.getNodes():
				nodeX = n.getX()
				nodeY = n.getY()
				pyglet.graphics.draw(4, GL_QUADS, ('v2f', [
					nodeX - nodeSize, nodeY - nodeSize,
					nodeX - nodeSize, nodeY + nodeSize,
					nodeX + nodeSize, nodeY + nodeSize,
					nodeX + nodeSize, nodeY - nodeSize
				]))
			# draw the edges using the half edge data structure
			glColor4f(0, 1, 0, 1.0)
			for e in self.graph.getEdges():
				adjacentEdge = e.getAdjacentEdge()
				# It is possible that there is no adjacent edge, this is the case for the outer edges, we don't need to draw them.
				if adjacentEdge != None:
					nodeFrom = e.getAdjacentEdge().getNode()
					nodeTo = e.getNode()
					pyglet.graphics.draw(4, GL_LINES, (
						'v2f', (0, 0, 0, height, nodeFrom.getX(), nodeFrom.getY(), nodeTo.getX(), nodeTo.getY())))

			# Draw the voronoi polygons (numberOfPoints, GL_POLYGON, ('v2f', [all x,y coordinates]))
			# pyglet.graphics.draw(8, GL_POLYGON, ('v2f', [300,300, 300,400, 400,500, 500,500, 600,400, 600,300, 500,200, 400,200]))

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
		nodeNew = Node.Node(x, y)
		self.graph.addNode(nodeNew)


if __name__ == "__main__":
	imageName = "Oudegracht_Utrecht_2.png"
	imagePath = os.path.abspath(os.path.dirname(__file__))
	imagePath = os.path.join(imagePath, 'data')
	imagePath = os.path.join(imagePath, imageName)
	im = Image.open(imagePath)
	(width, height) = im.size

	window = MainWindow(width, height, imageName, "Voronoi art project")
	window.main_loop()
