from os.path import abspath, dirname, join

from PIL import Image
from pyglet import clock
from pyglet import window
from pyglet.gl import glColor4f, gl, GL_POLYGON, GL_QUADS, GL_LINES
from pyglet.graphics import draw

from objects.face import Face
from objects.graph import Graph
from objects.half_edge import HalfEdge
from objects.node import Node
from voronoi_image import VoronoiImage
from random import randint

class MainWindow(window.Window):
    def __init__(self, width, height, image_name, name):
        window.Window.__init__(self, width, height, name)
        self.show_edge = False
        self.width = width
        self.height = height
        self.voronoi_image = VoronoiImage(image_name)

        # Manually add 3 nodes with triangulation edges far outside the sight.
        node1 = Node(-9999999, -9999999)
        node2 = Node(9999999, -9999999)
        node3 = Node(0, 9999999)

        face1 = Face(node1, node2, node3)

        half_edge1 = HalfEdge(node1, face1)
        half_edge2 = HalfEdge(node2, face1)
        half_edge3 = HalfEdge(node3, face1)

        # It is possible that there isn't a adjacent Edge. This is the case for the outer edges.
        half_edge1.next_edge = half_edge2
        half_edge2.next_edge = half_edge3
        half_edge3.next_edge = half_edge1

        face1.edge = half_edge1

        nodes = []
        nodes.append(node1)
        nodes.append(node2)
        nodes.append(node3)
        faces = []
        faces.append(face1)
        half_edges = []
        half_edges.append(half_edge1)
        half_edges.append(half_edge2)
        half_edges.append(half_edge3)

        # We will select a sorta random edge that is not on the outside.
        self.the_edge_to_show = half_edges[2]
        self.show_face = False
        self.show_all_faces = False
        self.show_voronoi_faces = False
        self.show_next_edge = False
        self.should_get_adjacent_edge = False
        self.flip_edge = False
        self.amountOfNodes = 200
        self.show_test_face = False
        self.test_selected_edge = False
        
        self.graph = Graph(nodes, half_edges, faces)
        self.graph.calculate_voronoi()

        self.check_face = self.graph.find_check_face(0, 0)
    
    def main_loop(self):
        clock.set_fps_limit(30)
        nodeSize = 5
        
        timer = 0
        while not self.has_exit:
            self.dispatch_events()
            self.clear()
            
            timer += 1

            # if timer % 5 == 0:
            #     x = randint(0, width)
            #     y = randint(0, height)
            #     self.addNode(x, y)


            if self.show_next_edge:
                self.show_next_edge = False
                self.the_edge_to_show = self.the_edge_to_show.next_edge
            if self.should_get_adjacent_edge:
                self.should_get_adjacent_edge = False
                if self.the_edge_to_show.adjacent_edge is not None:
                    self.the_edge_to_show = self.the_edge_to_show.adjacent_edge
            
            if self.flip_edge:
                temp = self.graph.manually_flip_edge(self.the_edge_to_show)
                if temp != None:
                    self.the_edge_to_show = temp
                self.flip_edge = False
                print("flipping edge :)")
            
            # White, so reset the colour
            glColor4f(1, 1, 1, 1)
            gl.glLineWidth(1)
            self.draw()
            
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

            if not self.show_voronoi_faces:

                if self.show_all_faces:

                    for f in self.graph.get_faces():
                        colour = f.colour
                        glColor4f(colour[0] / 256, colour[1] / 256, colour[2] / 256, colour[3])
                        n1 = f.node1
                        n2 = f.node2
                        n3 = f.node3
                        draw(3, GL_POLYGON,
                             ('v2f', [n1.x, n1.y, n2.x, n2.y, n3.x, n3.y]))

                # Draw the nodes with how you can give it a colour
                glColor4f(1, 0, 0, 1.0)
                for n in self.graph.nodes:
                    nodeX = n.x
                    nodeY = n.y
                    draw(4, GL_QUADS, ('v2f', [
                        nodeX - nodeSize, nodeY - nodeSize,
                        nodeX - nodeSize, nodeY + nodeSize,
                        nodeX + nodeSize, nodeY + nodeSize,
                        nodeX + nodeSize, nodeY - nodeSize
                    ]))
                # draw the edges using the half edge data structure
                glColor4f(0, 1, 0, 1.0)
                for e in self.graph.edges:
                    adjacentEdge = e.adjacent_edge
                    # It is possible that there is no adjacent edge, this is the case for the outer edges, we don't need to draw them.
                    if adjacentEdge != None:
                        nodeFrom = e.adjacent_edge.node
                        nodeTo = e.node
                        draw(4, GL_LINES, (
                            'v2f', (0, 0, 0, height, nodeFrom.x, nodeFrom.y, nodeTo.x, nodeTo.y)))

                if self.show_edge:
                    # Some visual debugging, show the edge as thicker and blue and draw the face.
                    gl.glLineWidth(5)
                    glColor4f(0, 0, 1, 1.0)
                    adjacentEdge = self.the_edge_to_show.adjacent_edge
                    if adjacentEdge != None:
                        nodeFrom = self.the_edge_to_show.adjacent_edge.node
                        nodeTo = self.the_edge_to_show.node
                        # print("edge name is " + self.showEdge)
                        draw(4, GL_LINES, (
                            'v2f', (0, 0, 0, height, nodeFrom.x, nodeFrom.y, nodeTo.x, nodeTo.y)))

                    if self.show_face:
                        current_face = self.the_edge_to_show.face
                        n1 = current_face.node1
                        n2 = current_face.node2
                        n3 = current_face.node3
                        draw(3, GL_POLYGON,
                                             ('v2f', [n1.x, n1.y, n2.x, n2.y, n3.x, n3.y]))
                    if self.test_selected_edge:
                        self.test_selected_edge = False
                        print("test the edge:", self.graph.test_edge(self.the_edge_to_show))


                # draw the clicked face (for testing if the face finder is correct)
                if self.show_test_face:
                    glColor4f(0, 0, 0, 1.0)
                    n1 = self.check_face.node1
                    n2 = self.check_face.node2
                    n3 = self.check_face.node3
                    draw(3, GL_POLYGON,
                         ('v2f', [n1.x, n1.y, n2.x, n2.y, n3.x, n3.y]))

            else:
                print("Hello world")
                # Draw the voronoi polygons (numberOfPoints, GL_POLYGON, ('v2f', [all x,y coordinates]))
                # draw(8, GL_POLYGON, ('v2f', [300,300, 300,400, 400,500, 500,500, 600,400, 600,300, 500,200, 400,200]))
            
            glColor4f(0, 0, 0, 1.0)
            clock.tick()
            self.flip()
    
    def draw(self):
        self.voronoi_image.draw()

    def check_face_function(self, x, y):
        print("check face")
        self.check_face = self.graph.find_check_face(x, y)

    # Event handlers
    def on_mouse_motion(self, x, y, dx, dy):
        pass
    
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        pass
    
    def on_mouse_release(self, x, y, button, modifiers):
        self.addNode(x, y)

    def addNode(self, x, y):
        print("node added at x:", x, "y:", y)
        nodeNew = Node(x, y)
        self.graph.add_node(nodeNew)

    def on_key_press(self, symbol, modifiers):
        print("symbol", str(symbol))
        if symbol == 97:
            # key press A
            pressedA = True
        elif symbol == 65307:
            # escape key is pressed
            exit()
        elif symbol == 98:   # b
            self.show_edge = True
        elif symbol == 118:  # v
            self.show_edge = False
        elif symbol == 110:  # n
            self.show_next_edge = True
        elif symbol == 102:  # f
            self.show_face = True
        elif symbol == 103:  # g
            self.show_face = False
        elif symbol == 116:  # t
            self.should_get_adjacent_edge = True
        elif symbol == 112:  # p
            self.flip_edge = True
        elif symbol == 122:  # z
            self.show_all_faces = True
        elif symbol == 120:  # x
            self.show_all_faces = False
        elif symbol == 119:  # w
            self.show_voronoi_faces = True
        elif symbol == 101:  # e
            self.show_voronoi_faces = False
        elif symbol == 113:  # q
            self.show_test_face = True
        elif symbol == 49:   #1
            self.test_selected_edge = True
    
    def on_key_release(self, symbol, modifiers):
        pass


if __name__ == "__main__":
    image_name = "Oudegracht_Utrecht_2.png"
    image_path = abspath(dirname(__file__))
    image_path = join(image_path, 'data')
    image_path = join(image_path, image_name)
    im = Image.open(image_path)
    (width, height) = im.size
    
    window = MainWindow(width, height, image_name, "Voronoi art project")
    window.main_loop()
