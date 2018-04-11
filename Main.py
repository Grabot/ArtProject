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
import objects.Face as Face
import objects.Graph as Graph


class MainWindow(window.Window):
    def __init__(self, width, height, imageName, name):
        window.Window.__init__(self, width, height, name)
        self.width = width
        self.height = height
        self.voronoiImage = VoronoiImage.VoronoiImage(imageName)

        # Mannually add 4 nodes with triangulation edges far outside the sight to make it easy to make the delaunay and voronoi calculations.
        nodes = []
        nodes.append(Node.Node(-99999999, -99999999))
        nodes.append(Node.Node(99999999, -99999999))
        nodes.append(Node.Node(0, 99999999))

        edges = []
        edges.append(Edge.Edge(nodes[0], nodes[1]))
        edges.append(Edge.Edge(nodes[1], nodes[2]))
        edges.append(Edge.Edge(nodes[2], nodes[0]))

        faces = []
        faces.append(Face.Face(nodes[0], nodes[1], nodes[2]))
        self.graph = Graph.Graph(nodes, edges, faces)
        # The graph doesn't have any nodes or edges yet.


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
            for n in self.graph.getNodes():
                nodeX = n.getX()
                nodeY = n.getY()
                pyglet.graphics.draw(4, GL_QUADS, ('v2f', [
                    nodeX - nodeSize, nodeY - nodeSize,
                    nodeX - nodeSize, nodeY + nodeSize,
                    nodeX + nodeSize, nodeY + nodeSize,
                    nodeX + nodeSize, nodeY - nodeSize
                ]))
            # draw the edges
            glColor4f(0, 1, 0, 1.0)
            for e in self.graph.getEdges():
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
