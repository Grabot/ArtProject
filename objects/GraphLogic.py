import objects.HalfEdge as HalfEdge
import objects.Face as Face

def addNode(f, node):
    # The 3 edges of the face that is chosen.
    edge1 = f.getEdge()
    edge2 = edge1.getNextEdge()
    edge3 = edge2.getNextEdge()

    # Create 3 new edges. and we need to fix the other half edges to get the correct "next edge"
    edge1_1 = HalfEdge.HalfEdge(node)
    edge1_2 = HalfEdge.HalfEdge(f.getNode1())

    edge2_1 = HalfEdge.HalfEdge(node)
    edge2_2 = HalfEdge.HalfEdge(f.getNode2())

    edge3_1 = HalfEdge.HalfEdge(node)
    edge3_2 = HalfEdge.HalfEdge(f.getNode3())

    # Set the new and correct "next edge" for all new half edges and the 3 half edges of the face.
    edge1.setNextEdge(edge1_1)
    edge1_1.setNextEdge(edge3_2)
    edge3_2.setNextEdge(edge1)

    edge2.setNextEdge(edge2_1)
    edge2_1.setNextEdge(edge1_2)
    edge1_2.setNextEdge(edge2)

    edge3.setNextEdge(edge3_1)
    edge3_1.setNextEdge(edge2_2)
    edge2_2.setNextEdge(edge3)

    # Set the new and correct adjacent edges. These stay the same for the original 3 face edges, but should be set for the newly created edges.
    edge1_1.setAdjacentEdge(edge1_2)
    edge1_2.setAdjacentEdge(edge1_1)
    edge2_1.setAdjacentEdge(edge2_2)
    edge2_2.setAdjacentEdge(edge2_1)
    edge3_1.setAdjacentEdge(edge3_2)
    edge3_2.setAdjacentEdge(edge3_1)

    # We will add the 3 newly created faces. with a half edge for each face. and set the faces on the half edges
    # Create face 1
    node1Face1 = edge1_1.getNode()
    node2Face1 = edge1_1.getNextEdge().getNode()
    node3Face1 = edge1_1.getNextEdge().getNextEdge().getNode()
    face1 = Face.Face(node1Face1, node2Face1, node3Face1, edge1_1)

    # Create face 2
    node1Face2 = edge2_1.getNode()
    node2Face2 = edge2_1.getNextEdge().getNode()
    node3Face2 = edge2_1.getNextEdge().getNextEdge().getNode()
    face2 = Face.Face(node1Face2, node2Face2, node3Face2, edge2_1)

    node1Face3 = edge3_1.getNode()
    node2Face3 = edge3_1.getNextEdge().getNode()
    node3Face3 = edge3_1.getNextEdge().getNextEdge().getNode()
    face3 = Face.Face(node1Face3, node2Face3, node3Face3, edge3_1)

    edge1_1.setFace(face1)
    edge1_2.setFace(face2)
    edge2_1.setFace(face2)
    edge2_2.setFace(face3)
    edge3_1.setFace(face3)
    edge3_2.setFace(face1)
    edge1.setFace(face1)
    edge2.setFace(face2)
    edge3.setFace(face3)

    return [
            face1, face2, face3, 
            edge1_1, edge1_2, edge2_1, edge2_2, edge3_1, edge3_2, 
            edge1, edge2, edge3
            ]


def flipEdge(e):
    # First we find the 2 faces that the edge has.
    e1 = e
    e2 = e1.getAdjacentEdge()
    node1 = e1.getNextEdge().getNode()
    node2 = e2.getNextEdge().getNode()

    # Create the new Half Edge.
    e1_1 = HalfEdge.HalfEdge(node1)
    e2_1 = HalfEdge.HalfEdge(node2)

    e1_1.setAdjacentEdge(e2_1)
    e2_1.setAdjacentEdge(e1_1)

    # Set the correct next edges.
    e1_1.setNextEdge(e1.getNextEdge().getNextEdge())
    e2_1.setNextEdge(e2.getNextEdge().getNextEdge())

    # The new next edge here used to be on the corner, so it's easier to take it from the other side
    e1_1.getNextEdge().setNextEdge(e2.getNextEdge())
    e2_1.getNextEdge().setNextEdge(e1.getNextEdge())

    e1_1.getNextEdge().getNextEdge().setNextEdge(e1_1)
    e2_1.getNextEdge().getNextEdge().setNextEdge(e2_1)

    # Create the new faces.
    node1Face1 = e1_1.getNode()
    node2Face1 = e1_1.getNextEdge().getNode()
    node3Face1 = e1_1.getNextEdge().getNextEdge().getNode()
    newFace1 = Face.Face(node1Face1, node2Face1, node3Face1, e1_1)

    # Create face 2
    node1Face2 = e2_1.getNode()
    node2Face2 = e2_1.getNextEdge().getNode()
    node3Face2 = e2_1.getNextEdge().getNextEdge().getNode()
    newFace2 = Face.Face(node1Face2, node2Face2, node3Face2, e2_1)

    e1_1.setFace(newFace1)
    e2_1.setFace(newFace2)

    e1_1.getNextEdge().setFace(newFace1)
    e2_1.getNextEdge().setFace(newFace2)

    e1_1.getNextEdge().getNextEdge().setFace(newFace1)
    e2_1.getNextEdge().getNextEdge().setFace(newFace2)

    return [e1, e2, newFace1, newFace2, e1_1, e2_1]