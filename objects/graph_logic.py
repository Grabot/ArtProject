import objects.face as Face
import objects.half_edge as HalfEdge


def addNode(f, node):
    print("Hello World")
    # The 3 edges of the face that is chosen.
    edge1 = f.edge
    edge2 = edge1.next_edge
    edge3 = edge2.next_edge
    
    # Create 3 new edges. and we need to fix the other half edges to get the correct "next edge"
    edge1_1 = HalfEdge.HalfEdge(node)
    edge1_2 = HalfEdge.HalfEdge(f.node1)
    
    edge2_1 = HalfEdge.HalfEdge(node)
    edge2_2 = HalfEdge.HalfEdge(f.node2)
    
    edge3_1 = HalfEdge.HalfEdge(node)
    edge3_2 = HalfEdge.HalfEdge(f.node3)
    
    # Set the new and correct "next edge" for all new half edges and the 3 half edges of the face.
    edge1.next_edge = edge1_1
    edge1_1.next_edge = edge3_2
    edge3_2.next_edge = edge1
    
    edge2.next_edge = edge2_1
    edge2_1.next_edge = edge1_2
    edge1_2.next_edge = edge2
    
    edge3.next_edge = edge3_1
    edge3_1.next_edge = edge2_2
    edge2_2.next_edge = edge3
    
    # Set the new and correct adjacent edges. These stay the same for the original 3 face edges, but should be set for the newly created edges.
    edge1_1.adjacent_edge = edge1_2
    edge1_2.adjacent_edge = edge1_1
    edge2_1.adjacent_edge = edge2_2
    edge2_2.adjacent_edge = edge2_1
    edge3_1.adjacent_edge = edge3_2
    edge3_2.adjacent_edge = edge3_1
    
    # We will add the 3 newly created faces. with a half edge for each face. and set the faces on the half edges
    # Create face 1
    node1Face1 = edge1_1.node
    node2Face1 = edge1_1.next_edge.node
    node3Face1 = edge1_1.next_edge.next_edge.node
    face1 = Face.Face(node1Face1, node2Face1, node3Face1, edge1_1)
    
    # Create face 2
    node1Face2 = edge2_1.node
    node2Face2 = edge2_1.next_edge.node
    node3Face2 = edge2_1.next_edge.next_edge.node
    face2 = Face.Face(node1Face2, node2Face2, node3Face2, edge2_1)
    
    node1Face3 = edge3_1.node
    node2Face3 = edge3_1.next_edge.node
    node3Face3 = edge3_1.next_edge.next_edge.node
    face3 = Face.Face(node1Face3, node2Face3, node3Face3, edge3_1)
    
    edge1_1.face = face1
    edge1_2.face = face2
    edge2_1.face = face2
    edge2_2.face = face3
    edge3_1.face = face3
    edge3_2.face = face1
    edge1.face = face1
    edge2.face = face2
    edge3.face = face3
    
    return [
        face1, face2, face3,
        edge1_1, edge1_2, edge2_1, edge2_2, edge3_1, edge3_2,
        edge1, edge2, edge3
    ]


def flip_edge(e):
    # First we find the 2 faces that the edge has.
    e1 = e
    e2 = e1.adjacent_edge
    node1 = e1.next_edge.node
    node2 = e2.next_edge.node
    
    # Create the new Half Edge.
    e1_1 = HalfEdge.HalfEdge(node1)
    e2_1 = HalfEdge.HalfEdge(node2)
    
    e1_1.adjacent_edge = e2_1
    e2_1.adjacent_edge = e1_1
    
    # Set the correct next edges.
    e1_1.next_edge = e1.next_edge.next_edge
    e2_1.next_edge = e2.next_edge.next_edge
    
    # The new next edge here used to be on the corner, so it's easier to take it from the other side
    e1_1.next_edge.next_edge = e2.next_edge
    e2_1.next_edge.next_edge = e1.next_edge
    
    e1_1.next_edge.next_edge.next_edge = e1_1
    e2_1.next_edge.next_edge.next_edge = e2_1
    
    # Create the new faces.
    node1Face1 = e1_1.node
    node2Face1 = e1_1.next_edge.node
    node3Face1 = e1_1.next_edge.next_edge.node
    newFace1 = Face.Face(node1Face1, node2Face1, node3Face1, e1_1)
    
    # Create face 2
    node1Face2 = e2_1.node
    node2Face2 = e2_1.next_edge.node
    node3Face2 = e2_1.next_edge.next_edge.node
    newFace2 = Face.Face(node1Face2, node2Face2, node3Face2, e2_1)
    
    e1_1.face = newFace1
    e2_1.face = newFace2
    
    e1_1.next_edge.face = newFace1
    e2_1.next_edge.face = newFace2
    
    e1_1.next_edge.next_edge.face = newFace1
    e2_1.next_edge.next_edge.face = newFace2
    
    return [e1, e2, newFace1, newFace2, e1_1, e2_1]
