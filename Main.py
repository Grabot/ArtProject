import os
import math
from math import sqrt
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
        self.width = width
        self.height = height
        self.voronoiImage = VoronoiImage.VoronoiImage(imageName)

        # Mannually adding nodes and edges to a list. This will be automated later when the user clicks
        self.nodes = []
        self.edges = []
        self.convexHullEdges = []


    def orientation(self, p1, p2, p3):
    	orientation = (p2.getX() - p1.getX()) * (p3.getY() - p1.getY()) - (p3.getX() - p1.getX()) * (p2.getY() - p1.getY());
    	return orientation


    def gift_wrapping(self):
        if len(self.nodes) < 3:
        	# Not enough nodes for a convex hull calculation
        	return

        # We are going to find the left most node in the set, this node will always be in the convex hull.
        minX = self.width
        hullPoint = ""
        for n in self.nodes:
            if n.getX() < minX:
                hullPoint = n
                minX = n.getX()

        endPoint = ""
        finalPoints = []
        while finalPoints == [] or endPoint != finalPoints[0]:
        	finalPoints.append(hullPoint)
        	endPoint = self.nodes[0]

	        for index in range(1, len(self.nodes)):
	        	# We want to find the angle between the last found point (finalPoints[-1]), the currently selected endPoint and the node we're looping over.
	        	# If the angle is better between the last found point and the current point we're checking (n) we will put the endPoint on that node.
	        	if hullPoint == endPoint or self.orientation(finalPoints[-1], endPoint, self.nodes[index]) > 0:
	        		# The orientation is on the leftside.
	        		endPoint = self.nodes[index]

	        hullPoint = endPoint

	    # Set the edges for the convex hull
        self.convexHullEdges = []
        for x in range(0, len(finalPoints)):
        	edge = ""
        	if x == len(finalPoints)-1:
        		edge = Edge.Edge(finalPoints[x], finalPoints[0])
        	else:
        		edge = Edge.Edge(finalPoints[x], finalPoints[x+1])

        	self.convexHullEdges.append(edge)


    def main_loop(self):
        clock.set_fps_limit(30)
        nodeSize = 5

        while not self.has_exit:
            self.dispatch_events()
            self.clear()

            self.draw()

            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            # Draw the nodes with how you can give it a colour
            glColor4f(1, 0, 0, 1.0)
            for n in self.nodes:
                nodeX = n.getX()
                nodeY = n.getY()
                pyglet.graphics.draw(4, GL_QUADS, ('v2f', [
                    nodeX - nodeSize, nodeY - nodeSize,
                    nodeX - nodeSize, nodeY + nodeSize,
                    nodeX + nodeSize, nodeY + nodeSize,
                    nodeX + nodeSize, nodeY - nodeSize
                ]))
            # draw the edges
            for e in self.convexHullEdges:
                nodeFrom = e.getNodeFrom()
                nodeTo = e.getNodeTo()
                pyglet.graphics.draw(4, GL_LINES, (
                'v2f', (0, 0, 0, height, nodeFrom.getX(), nodeFrom.getY(), nodeTo.getX(), nodeTo.getY())))
            # Draw the voronoi polygons (numberOfPoints, GL_POLYGON, ('v2f', [all x,y coordinates]))
            # pyglet.graphics.draw(8, GL_POLYGON, ('v2f', [300,300, 300,400, 400,500, 500,500, 600,400, 600,300, 500,200, 400,200]))
            # White, so reset the colour
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
        nodeNew = Node.Node(x, y)
        self.nodes.append(nodeNew)
        self.gift_wrapping()


if __name__ == "__main__":
    imageName = "Oudegracht_Utrecht_2.png"
    imagePath = os.path.abspath(os.path.dirname(__file__))
    imagePath = os.path.join(imagePath, 'data')
    imagePath = os.path.join(imagePath, imageName)
    im = Image.open(imagePath)
    (width, height) = im.size

    window = MainWindow(width, height, imageName, "Voronoi art project")
    window.main_loop()
