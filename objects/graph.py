from random import shuffle

import numpy
import time
import objects.graph_logic as GraphLogic


class Graph:
    def __init__(self, nodes=None, edges=None, faces=None):
        self.nodes = nodes or []
        self.edges = edges or []
        # Starting with _ is the Python way to mark this field as private.
        # This happens because external code should use the randomized get_faces() method.
        self._faces = faces or []
    
    def get_faces(self):
        shuffle(self._faces)
        return self._faces

    def check_can_flip_edge(self, e):
        # First a simple check if we can flip the edge.
        if e.adjacent_edge == None:
            return False
        # Then another, more difficult check, to see if the edge can be flipped or if it is out of the flip bounds
        # We do this by checking if the 2 faces combined are convex, if not the edge cannot be flipped.
        edge1 = e
        edge2 = e.adjacent_edge
        node1 = edge1.next_edge.node
        node2 = edge1.next_edge.next_edge.node
        node3 = edge2.next_edge.node
        node4 = edge2.next_edge.next_edge.node
        triangle_ABC = (node1.y - node2.y) * node3.x + (node2.x - node1.x) * node3.y + (
                    node1.x * node2.y - node2.x * node1.y)
        triangle_ABD = (node1.y - node2.y) * node4.x + (node2.x - node1.x) * node4.y + (
                    node1.x * node2.y - node2.x * node1.y)
        triangle_BCD = (node2.y - node3.y) * node4.x + (node3.x - node2.x) * node4.y + (
                    node2.x * node3.y - node3.x * node2.y)
        triangle_CAD = (node3.y - node1.y) * node4.x + (node1.x - node3.x) * node4.y + (
                    node3.x * node1.y - node1.x * node3.y)

        if triangle_ABC < 0:
            triangle_ABC = triangle_ABC * -1
            triangle_ABD = triangle_ABD * -1
            triangle_BCD = triangle_BCD * -1
            triangle_CAD = triangle_CAD * -1

        # not sure if it's correct, but taken from this.
        # https://stackoverflow.com/questions/2122305/convex-hull-of-4-points
        if triangle_ABC > 0 and triangle_ABD > 0 and triangle_BCD > 0 and triangle_CAD > 0:
            return False
        if triangle_ABC > 0 and triangle_ABD > 0 and triangle_BCD < 0 and triangle_CAD < 0:
            return False
        if triangle_ABC > 0 and triangle_ABD < 0 and triangle_BCD > 0 and triangle_CAD < 0:
            return False
        if triangle_ABC > 0 and triangle_ABD < 0 and triangle_BCD < 0 and triangle_CAD > 0:
            return False

        return True


    def flip_edge(self, e):
        # First a simple check if we can flip the edge.
        if e.adjacent_edge == None:
            return
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
    
    def check_flip_edge(self, flip_edges, node):
        print("flipping edges")
        while flip_edges:
            edge = flip_edges.pop()
            
            # It is possible that the edge has since been removed.
            if edge in self.edges:
                if edge.adjacent_edge != None:
                    adjacentEdge = edge.adjacent_edge
                    otherFaceNode1 = adjacentEdge.node
                    otherFaceNode2 = adjacentEdge.next_edge.node
                    otherFaceNode3 = adjacentEdge.next_edge.next_edge.node
                    # Check the determinant of the point compared to the triangle
                    if not self.is_valid_edge(otherFaceNode1, otherFaceNode2, otherFaceNode3, node):
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
                edge_flip_checks = [edge1, edge2, edge3]
                self.check_flip_edge(edge_flip_checks, node)
        
        self.nodes.append(node)
        self.calculate_voronoi()
    
    def orientation(self, p1, p2, p3):
        return (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)
    
    def calculate_voronoi(self):
        print("calculate_voronoi")

    def find_check_face(self, x, y):
        for f in self._faces:
            if self.is_in_face(f.node1.x, f.node1.y, f.node2.x, f.node2.y, f.node3.x, f.node3.y, x, y):
                return f
