from random import shuffle

import numpy
import math
from objects.node import Node
from objects.edge import Edge
import objects.graph_logic as GraphLogic


class Graph:
    def __init__(self, nodes=None, edges=None, faces=None):
        self.nodes = nodes or []
        self.edges = edges or []
        # Starting with _ is the Python way to mark this field as private.
        # This happens because external code should use the randomized get_faces() method.
        self._faces = faces or []
        self._voronoi_nodes = []
        self._voronoi_edges = []
        self._voronoi_faces = []
    
    def get_faces(self):
        shuffle(self._faces)
        return self._faces

    def get_voronoi_nodes(self):
        shuffle(self._voronoi_nodes)
        return self._voronoi_nodes

    def get_voronoi_edges(self):
        shuffle(self._voronoi_edges)
        return self._voronoi_edges

    def check_can_flip_edge(self, e):
        # First a simple check if we can flip the edge.
        if e.adjacent_edge == None:
            return False
        return True

    def flip_edge(self, e):
        # First a simple check if we can flip the edge.
        [e1, e2, new_face1, new_face2, e1_1, e2_1] = GraphLogic.flip_edge(e)
        
        # Add the new faces and also remove the old ones.
        self.edges.remove(e1)
        self.edges.remove(e2)
        
        self._faces.remove(e1.face)
        self._faces.remove(e2.face)
        
        self._faces.append(new_face1)
        self._faces.append(new_face2)
        
        # Do the same with the new edges.
        self.edges.append(e1_1)
        self.edges.append(e2_1)
        
        print("flipping the flippin edge")
        return [e1_1, e2_1]
    
    def manually_flip_edge(self, edge):
        for e in self.edges:
            if e == edge:
                return self.flip_edge(e)[0]
    
    """
    Returns True is D lies in the circumcircle of ABC
    This is done by determining the determinant of a matrix.
    """
    def is_in_circle(self, A, B, C, D):
        M = [[A.x, A.y, (pow(A.x, 2) + pow(A.y, 2)), 1],
             [B.x, B.y, (pow(B.x, 2) + pow(B.y, 2)), 1],
             [C.x, C.y, (pow(C.x, 2) + pow(C.y, 2)), 1],
             [D.x, D.y, (pow(D.x, 2) + pow(D.y, 2)), 1]]
        det_result = numpy.linalg.det(M)
        return det_result > 0
    
    def is_valid_edge(self, triangleNode1, triangleNode2, triangleNode3, node):
        return not self.is_in_circle(triangleNode1, triangleNode2, triangleNode3, node)
    
    def check_flip_edge(self, flip_edges):
        print("flipping edges")
        while flip_edges:
            edge = flip_edges.pop()
            
            # It is possible that the edge has since been removed.
            if edge in self.edges:
                if edge.adjacent_edge != None:
                    adjacentEdge = edge.adjacent_edge
                    A = adjacentEdge.node
                    B = adjacentEdge.next_edge.node
                    C = adjacentEdge.next_edge.next_edge.node

                    # The node can change, we can always find which node to compare using the edge.
                    D = edge.next_edge.node

                    # Check the determinant of the point compared to the triangle
                    if not self.is_valid_edge(A, B, C, D):
                        # Check if we can flip the edge
                        if self.check_can_flip_edge(edge):
                            print("edge is not valid, flip it!")
                            [e1_1, e2_1] = self.flip_edge(edge)
                            # check the other edges now, except if it is an outer edge
                            flip_edges.append(e1_1.next_edge)
                            flip_edges.append(e1_1.next_edge.next_edge)
                            flip_edges.append(e2_1.next_edge)
                            flip_edges.append(e2_1.next_edge.next_edge)

    
    def is_in_face(self, p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, node_x, node_y):
        Area = 0.5 * (-p1_y * p2_x + p0_y * (-p1_x + p2_x) + p0_x * (
                p1_y - p2_y) + p1_x * p2_y)
        
        s = 1 / (2 * Area) * (p0_y * p2_x - p0_x * p2_y + (p2_y - p0_y) * node_x + (
                p0_x - p2_x) * node_y)
        t = 1 / (2 * Area) * (p0_x * p1_y - p0_y * p1_x + (p0_y - p1_y) * node_x + (
                p1_x - p0_x) * node_y)
        
        return s > 0 and t > 0 and 1 - s - t > 0
    
    def add_node(self, node):
        print("add node")
        # We have added a node, so we want to find out which face it is in and connect it with edges
        for f in self._faces:
            if self.is_in_face(f.node1.x, f.node1.y, f.node2.x, f.node2.y, f.node3.x, f.node3.y, node.x, node.y):
                [
                    face1, face2, face3,
                    edge1_1, edge1_2, edge2_1, edge2_2, edge3_1, edge3_2,
                    edge1, edge2, edge3
                ] = GraphLogic.add_node(f, node)
                
                self._faces.append(face1)
                self._faces.append(face2)
                self._faces.append(face3)
                
                # We don't have to remove edges, only add the newly created ones.
                self.edges.append(edge1_1)
                self.edges.append(edge1_2)
                self.edges.append(edge2_1)
                self.edges.append(edge2_2)
                self.edges.append(edge3_1)
                self.edges.append(edge3_2)
                
                # The original face is now replaced with 3 new ones, so we will remove the original
                self._faces.remove(f)
                
                # We want to check whether or not the edges are valid Delaunay, we will do that by comparing
                # the new node with the 3 triangle nodes of the adjacent face.
                edge_flip_checks = [edge1, edge2, edge3, edge1_1, edge1_2, edge2_1, edge2_2, edge3_1, edge3_2]
                self.check_flip_edge(edge_flip_checks)
        
        self.nodes.append(node)
        self.calculate_voronoi_nodes()
        self.calculate_voronoi_edges()
        self.calculate_voronoi_faces()
    
    def orientation(self, p1, p2, p3):
        return (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)

    def find_check_face(self, x, y):
        for f in self._faces:
            if self.is_in_face(f.node1.x, f.node1.y, f.node2.x, f.node2.y, f.node3.x, f.node3.y, x, y):
                return f

    def test_edge(self, the_edge):
        # It is possible that the edge has since been removed.
        if the_edge in self.edges:
            if the_edge.adjacent_edge != None:
                adjacentEdge = the_edge.adjacent_edge

                # My guess is that the problem is that the points are not correctly ordered.
                # We want it to not have crossing lines, we made a simple test based on lines crossing
                # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect#9997374
                A = adjacentEdge.node
                B = adjacentEdge.next_edge.node
                C = adjacentEdge.next_edge.next_edge.node

                D = the_edge.next_edge.node

                print("Ax:", A.x, "Ay:", A.y)
                print("Bx:", B.x, "By:", B.y)
                print("Cx:", C.x, "Cy:", C.y)
                print("Dx:", D.x, "Dy:", D.y)

                # Check the determinant of the point compared to the triangle
                if not self.is_valid_edge(A, B, C, D):
                    # Check if we can flip the edge
                    if self.check_can_flip_edge(the_edge):
                        return True
        return False

    def get_slope(self, p1, p2):
        slope = (p1.y - p2.y) / (p1.x - p2.x)
        return slope

    def get_intersection(self, line1, line2):
        slope1, slope2 = line1[0], line2[0]
        yint1, yint2 = line1[1], line2[1]
        matA = numpy.matrix([[(slope1 * -1), 1], [(slope2 * -1), 1]])
        matB = numpy.matrix([[yint1], [yint2]])
        invA = matA.getI()
        resultant = invA * matB
        return Node(resultant[0, 0], resultant[1, 0])

    def get_midpoint(self, p1, p2):
        midNode = Node(((p1.x + p2.x) / 2), ((p1.y + p2.y) / 2))
        return midNode

    def perp_slope(self, slope):
        # takes slope and returns the slope of a line perpendicular to it
        if slope == 0:
            slope += 0.00000000000001
        return (slope * -1) ** -1

    def line_from_slope(self, slope, point):
        return [slope, (slope * (-1 * point.x)) + point.y]

    def calculate_voronoi_nodes(self):
        print("calculate_voronoi nodes")
        self._voronoi_nodes = []
        for f in self._faces:
            # We need to get the circumcenter of all the faces and that will be the nodes of the voronoi.

            mid1 = self.get_midpoint(f.node1, f.node2)
            mid2 = self.get_midpoint(f.node2, f.node3)
            line1 = self.get_slope(f.node1, f.node2)
            line2 = self.get_slope(f.node2, f.node3)
            perp1 = self.perp_slope(line1)
            perp2 = self.perp_slope(line2)
            perpbi1 = self.line_from_slope(perp1, mid1)
            perpbi2 = self.line_from_slope(perp2, mid2)
            circumcent = self.get_intersection(perpbi1, perpbi2)

            self._voronoi_nodes.append(circumcent)
            f.set_voronoi_node(circumcent)

    def calculate_voronoi_edges(self):
        print("calculate voronoi edges")

        # first clear all the edges because we are going to re-calculate them
        self._voronoi_edges = []
        for f in self._faces:
            f.clear_voronoi_edges()

        for n in self.nodes:
            n.clear_voronoi_edges()

        for f in self._faces:
            # We will connect all the voronoi nodes with the 3 adjacent voronoi nodes in the faces of it's corresponding face.
            face_edge1 = f.edge
            face_edge2 = face_edge1.next_edge
            face_edge3 = face_edge1.next_edge.next_edge

            face1 = None
            face2 = None
            face3 = None
            if face_edge1.adjacent_edge != None:
                face1 = face_edge1.adjacent_edge.face

            if face_edge2.adjacent_edge != None:
                face2 = face_edge2.adjacent_edge.face

            if face_edge3.adjacent_edge != None:
                face3 = face_edge3.adjacent_edge.face

            voronoi_edges = []
            # We now have the current face and all it's adjacent faces.
            # We have already calculated the voronoi nodes for these faces, so we can connect them
            if face1 != None:
                edge = Edge(f.get_voronoi_node(), face1.get_voronoi_node())
                voronoi_edges.append(edge)
                self._voronoi_edges.append(edge)

                if f.node1 == face1.node1 or f.node1 == face1.node2 or f.node1 == face1.node3:
                    f.node1.add_voronoi_edge(edge)

                if f.node2 == face1.node1 or f.node2 == face1.node2 or f.node2 == face1.node3:
                    f.node2.add_voronoi_edge(edge)

                if f.node3 == face1.node1 or f.node3 == face1.node2 or f.node3 == face1.node3:
                    f.node3.add_voronoi_edge(edge)


            if face2 != None:
                edge = Edge(f.get_voronoi_node(), face2.get_voronoi_node())
                voronoi_edges.append(edge)
                self._voronoi_edges.append(edge)

                if f.node1 == face2.node1 or f.node1 == face2.node2 or f.node1 == face2.node3:
                    f.node1.add_voronoi_edge(edge)

                if f.node2 == face2.node1 or f.node2 == face2.node2 or f.node2 == face2.node3:
                    f.node2.add_voronoi_edge(edge)

                if f.node3 == face2.node1 or f.node3 == face2.node2 or f.node3 == face2.node3:
                    f.node3.add_voronoi_edge(edge)

            if face3 != None:
                edge = Edge(f.get_voronoi_node(), face3.get_voronoi_node())
                voronoi_edges.append(edge)
                self._voronoi_edges.append(edge)

                if f.node1 == face3.node1 or f.node1 == face3.node2 or f.node1 == face3.node3:
                    f.node1.add_voronoi_edge(edge)

                if f.node2 == face3.node1 or f.node2 == face3.node2 or f.node2 == face3.node3:
                    f.node2.add_voronoi_edge(edge)

                if f.node3 == face3.node1 or f.node3 == face3.node2 or f.node3 == face3.node3:
                    f.node3.add_voronoi_edge(edge)


    def calculate_voronoi_faces(self):
        print("calculating voronoi faces")
        for n in self.nodes:
            test = ""
