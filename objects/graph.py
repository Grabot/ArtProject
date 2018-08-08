from random import shuffle

import numpy
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
        self.calculate_voronoi()

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

    def calculate_voronoi(self):
        self._voronoi_nodes = GraphLogic.calculate_voronoi_nodes(self._faces)
        self._voronoi_edges = GraphLogic.calculate_voronoi_edges(self._faces, self.nodes)
        GraphLogic.calculate_voronoi_faces(self.nodes)
