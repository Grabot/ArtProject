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
from random import randint


class MainWindow(window.Window):
    def __init__(self, width, height, imageName, name):
        window.Window.__init__(self, width, height, name)
        self.showEdge = False
        self.width = width
        self.height = height
        self.voronoiImage = VoronoiImage.VoronoiImage(imageName)

        # Mannually add 4 nodes with triangulation edges far outside the sight to make it easy to make the delaunay and voronoi calculations.
        node1 = Node.Node(-9999999, -9999999)
        node2 = Node.Node(9999999, -9999999)
        node3 = Node.Node(0, 9999999)

        face1 = Face.Face(node1, node2, node3)

        halfEdge1 = HalfEdge.HalfEdge(node1, face1)
        halfEdge2 = HalfEdge.HalfEdge(node2, face1)
        halfEdge3 = HalfEdge.HalfEdge(node3, face1)

        # It is possible that there isn't a adjacent Edge. This is the case for the outer edges.
        halfEdge1.setNextEdge(halfEdge2)
        halfEdge2.setNextEdge(halfEdge3)
        halfEdge3.setNextEdge(halfEdge1)

        face1.setEdge(halfEdge1)

        nodes = []
        nodes.append(node1)
        nodes.append(node2)
        nodes.append(node3)
        faces = []
        faces.append(face1)
        halfEdges = []
        halfEdges.append(halfEdge1)
        halfEdges.append(halfEdge2)
        halfEdges.append(halfEdge3)

        # We will select a sorta random edge that is not on the outside.
        self.theEdgeToShow = halfEdges[2]
        self.showFace = False
        self.showAllFaces = False
        self.showVoronoiFaces = False
        self.showNextEdge = False
        self.getAdjacentEdge = False
        self.flipEdge = False
        self.amountOfNodes = 200

        self.graph = Graph.Graph(nodes, halfEdges, faces)

    def main_loop(self):
        clock.set_fps_limit(30)
        nodeSize = 5

        timer = 0
        while not self.has_exit:
            self.dispatch_events()
            self.clear()

            timer += 1
            if timer == 20:
                nodeX = 737
                nodeY = 702
                nodeNew = Node.Node(nodeX, nodeY)
                self.graph.addNode(nodeNew)

            if timer == 50:
                nodeX = 190
                nodeY = 210
                nodeNew = Node.Node(nodeX, nodeY)
                self.graph.addNode(nodeNew)

            if self.showNextEdge:
                self.showNextEdge = False
                self.theEdgeToShow = self.theEdgeToShow.getNextEdge()
            if self.getAdjacentEdge:
                self.getAdjacentEdge = False
                if self.theEdgeToShow.getAdjacentEdge() is not None:
                    self.theEdgeToShow = self.theEdgeToShow.getAdjacentEdge()

            if self.flipEdge:
                temp = self.graph.manuallyFlipEdge(self.theEdgeToShow)
                if temp != None:
                    self.theEdgeToShow = temp
                self.flipEdge = False
                print("flipping edge :)")

            # White, so reset the colour
            glColor4f(1, 1, 1, 1)
            gl.glLineWidth(1)
            self.draw()

            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            # Draw the nodes with how you can give it a colour

            if self.showAllFaces:

                for f in self.graph.getFaces():
                    colour = f.getColour()
                    glColor4f(colour[0] / 256, colour[1] / 256, colour[2] / 256, colour[3])
                    n1 = f.getNode1()
                    n2 = f.getNode2()
                    n3 = f.getNode3()
                    pyglet.graphics.draw(3, GL_POLYGON,
                                         ('v2f', [n1.getX(), n1.getY(), n2.getX(), n2.getY(), n3.getX(), n3.getY()]))

            if self.showVoronoiFaces:
                print("show Voronoi faces")

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

            if self.showEdge:
                # Some visual debugging, show the edge as thicker and blue and draw the face.
                gl.glLineWidth(5)
                glColor4f(0, 0, 1, 1.0)
                adjacentEdge = self.theEdgeToShow.getAdjacentEdge()
                if adjacentEdge != None:
                    nodeFrom = self.theEdgeToShow.getAdjacentEdge().getNode()
                    nodeTo = self.theEdgeToShow.getNode()
                    # print("edge name is " + self.showEdge)
                    pyglet.graphics.draw(4, GL_LINES, (
                        'v2f', (0, 0, 0, height, nodeFrom.getX(), nodeFrom.getY(), nodeTo.getX(), nodeTo.getY())))

                if self.showFace:
                    theFace = self.theEdgeToShow.getFace()
                    n1 = theFace.getNode1()
                    n2 = theFace.getNode2()
                    n3 = theFace.getNode3()
                    pyglet.graphics.draw(3, GL_POLYGON,
                                         ('v2f', [n1.getX(), n1.getY(), n2.getX(), n2.getY(), n3.getX(), n3.getY()]))

            # Draw the voronoi polygons (numberOfPoints, GL_POLYGON, ('v2f', [all x,y coordinates]))
            # pyglet.graphics.draw(8, GL_POLYGON, ('v2f', [300,300, 300,400, 400,500, 500,500, 600,400, 600,300, 500,200, 400,200]))

            glColor4f(0, 0, 0, 1.0)
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
        print("node added at x:", x, "y:", y)
        nodeNew = Node.Node(x, y)
        self.graph.addNode(nodeNew)

    def on_key_press(self, symbol, modifiers):
        print("symbol", str(symbol))
        if symbol == 97:
            # key press A
            print("a pressed")
            pressedA = True
        elif symbol == 65307:
            # escape key is pressed
            exit()
        elif symbol == 98:
            self.showEdge = True
        elif symbol == 118:
            self.showEdge = False
        elif symbol == 110:
            self.showNextEdge = True
        elif symbol == 102:
            self.showFace = True
        elif symbol == 103:
            self.showFace = False
        elif symbol == 116:
            self.getAdjacentEdge = True
        elif symbol == 112:
            self.flipEdge = True
        elif symbol == 122:
            self.showAllFaces = True
        elif symbol == 120:
            self.showAllFaces = False
        elif symbol == 119:
            self.showVoronoiFaces = True
        elif symbol == 101:
            self.showVoronoiFaces = False

    def on_key_release(self, symbol, modifiers):
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
