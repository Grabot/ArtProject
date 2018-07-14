from random import shuffle

import numpy

import objects.graph_logic as GraphLogic


class Graph:
    def __init__(self, nodes=None, edges=None, faces=None):
        self.nodes = nodes or []
        self.edges = edges or []
        self._faces = faces or []
    
    def get_faces(self):
        shuffle(self._faces)
        return self._faces
    
    def flip_edge(self, e):
        # First a simple check if we can flip the edge.
        if e.getAdjacentEdge() == None:
            return
        [e1, e2, newFace1, newFace2, e1_1, e2_1] = GraphLogic.flipEdge(e)
        
        # Add the new faces and also remove the old ones.
        self.edges.remove(e1)
        self.edges.remove(e2)
        
        self._faces.remove(e1.face)
        self._faces.remove(e2.face)
        
        self._faces.append(newFace1)
        self._faces.append(newFace2)
        
        # Do the same with the new edges.
        self.edges.append(e1_1)
        self.edges.append(e2_1)
        
        print("flipping the flippin edge")
        return [e1_1, e2_1]
    
    def manuallyFlipEdge(self, edgeToFlip):
        for e in self.edges:
            if e == edgeToFlip:
                return self.flip_edge(e)[0]
    
    def inCircle(self, A, B, C, D):
        # returns True is D lies in the circumcircle of ABC
        # This is done by determining the determinant of a matrix.
        M = [[A.getX(), A.getY(), (pow(A.getX(), 2) + pow(A.getY(), 2)), 1],
             [B.getX(), B.getY(), (pow(B.getX(), 2) + pow(B.getY(), 2)), 1],
             [C.getX(), C.getY(), (pow(C.getX(), 2) + pow(C.getY(), 2)), 1],
             [D.getX(), D.getY(), (pow(D.getX(), 2) + pow(D.getY(), 2)), 1]]
        return numpy.linalg.det(M) > 0
    
    def validEdge(self, triangleNode1, triangleNode2, triangleNode3, node):
        return not self.inCircle(triangleNode1, triangleNode2, triangleNode3, node)
    
    def checkFlipEdge(self, flipEdges, node):
        
        print("flipping edges")
        while flipEdges:
            edge = flipEdges.pop()
            
            # It is possible that the edge has since been removed.
            if edge in self.edges:
                if edge.getAdjacentEdge() != None:
                    adjacentEdge = edge.getAdjacentEdge()
                    otherFaceNode1 = adjacentEdge.node
                    otherFaceNode2 = adjacentEdge.getNextEdge().node
                    otherFaceNode3 = adjacentEdge.getNextEdge().getNextEdge().node
                    if not self.validEdge(otherFaceNode1, otherFaceNode2, otherFaceNode3, node):
                        print("edge is not valid, flip it!")
                        [e1_1, e2_1] = self.flip_edge(edge)
                        flipEdges.append(e1_1.getNextEdge())
                        flipEdges.append(e1_1.getNextEdge().getNextEdge())
                        flipEdges.append(e2_1.getNextEdge())
                        flipEdges.append(e2_1.getNextEdge().getNextEdge())
    
    def inFace(self, p0, p1, p2, node):
        Area = 0.5 * (-p1.getY() * p2.getX() + p0.getY() * (-p1.getX() + p2.getX()) + p0.getX() * (
                p1.getY() - p2.getY()) + p1.getX() * p2.getY())
        
        s = 1 / (2 * Area) * (p0.getY() * p2.getX() - p0.getX() * p2.getY() + (p2.getY() - p0.getY()) * node.getX() + (
                p0.getX() - p2.getX()) * node.getY())
        t = 1 / (2 * Area) * (p0.getX() * p1.getY() - p0.getY() * p1.getX() + (p0.getY() - p1.getY()) * node.getX() + (
                p1.getX() - p0.getX()) * node.getY())
        
        return s > 0 and t > 0 and 1 - s - t > 0
    
    def addNode(self, node):
        print("add node")
        # We have added a node, so we want to find out which face it is in and connect it with edges
        for f in self._faces:
            if self.inFace(f.node1, f.node2, f.node3, node):
                [
                    face1, face2, face3,
                    edge1_1, edge1_2, edge2_1, edge2_2, edge3_1, edge3_2,
                    edge1, edge2, edge3
                ] = GraphLogic.addNode(f, node)
                
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
                
                # We want to check whether or not the edges are valid delaunay, we will do that by comparing
                # the new node with the 3 triangle nodes of the adjacent face.
                edgeFlipChecks = [edge1, edge2, edge3]
                self.checkFlipEdge(edgeFlipChecks, node)
        
        self.nodes.append(node)
        self.calculateVoronoi()
    
    def orientation(self, p1, p2, p3):
        return (p2.getX() - p1.getX()) * (p3.getY() - p1.getY()) - (p3.getX() - p1.getX()) * (p2.getY() - p1.getY())
    
    def calculateVoronoi(self):
        print("calculateVoronoi")
