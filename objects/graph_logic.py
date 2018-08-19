from objects.face import Face
from objects.half_edge import HalfEdge
from objects.voronoi_face import VoronoiFace
from objects.node import Node
from objects.edge import Edge
import numpy
import math


def add_node(face, node):
    # The 3 edges of the face that is chosen.
    edge1 = face.edge
    edge2 = edge1.next_edge
    edge3 = edge2.next_edge

    # Create 3 new edges. and we need to fix the other half edges to get the correct "next edge"
    edge1_1 = HalfEdge(node)
    edge1_2 = HalfEdge(face.node1)

    edge2_1 = HalfEdge(node)
    edge2_2 = HalfEdge(face.node2)

    edge3_1 = HalfEdge(node)
    edge3_2 = HalfEdge(face.node3)

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

    # Set the new and correct adjacent edges.
    # These stay the same for the original 3 face edges, but should be set for the newly created edges.
    edge1_1.adjacent_edge = edge1_2
    edge1_2.adjacent_edge = edge1_1
    edge2_1.adjacent_edge = edge2_2
    edge2_2.adjacent_edge = edge2_1
    edge3_1.adjacent_edge = edge3_2
    edge3_2.adjacent_edge = edge3_1

    # We will add the 3 newly created faces. with a half edge for each face. and set the faces on the half edges
    # Create face 1
    node1_face1 = edge1_1.node
    node2_face1 = edge1_1.next_edge.node
    node3_face1 = edge1_1.next_edge.next_edge.node
    face1 = Face(node1_face1, node2_face1, node3_face1, edge1_1)

    # Create face 2
    node1_face2 = edge2_1.node
    node2_face2 = edge2_1.next_edge.node
    node3_face2 = edge2_1.next_edge.next_edge.node
    face2 = Face(node1_face2, node2_face2, node3_face2, edge2_1)

    node1_face3 = edge3_1.node
    node2_face3 = edge3_1.next_edge.node
    node3_face3 = edge3_1.next_edge.next_edge.node
    face3 = Face(node1_face3, node2_face3, node3_face3, edge3_1)

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


def flip_edge(edge):
    # First we find the 2 faces that the edge has.
    e1 = edge
    e2 = e1.adjacent_edge
    node1 = e1.next_edge.node
    node2 = e2.next_edge.node

    # Create the new Half Edge.
    e1_1 = HalfEdge(node1)
    e2_1 = HalfEdge(node2)

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
    node1_face1 = e1_1.node
    node2_face1 = e1_1.next_edge.node
    node3_face1 = e1_1.next_edge.next_edge.node
    new_face1 = Face(node1_face1, node2_face1, node3_face1, e1_1)

    # Create face 2
    node1_face2 = e2_1.node
    node2_face2 = e2_1.next_edge.node
    node3_face2 = e2_1.next_edge.next_edge.node
    new_face2 = Face(node1_face2, node2_face2, node3_face2, e2_1)

    e1_1.face = new_face1
    e2_1.face = new_face2

    e1_1.next_edge.face = new_face1
    e2_1.next_edge.face = new_face2

    e1_1.next_edge.next_edge.face = new_face1
    e2_1.next_edge.next_edge.face = new_face2

    return [e1, e2, new_face1, new_face2, e1_1, e2_1]


def get_slope(p1, p2):
    if (p1.x - p2.x) == 0:
        # simple way to avoid a division by zero
        return (p1.y - p2.y) / ((p1.x - p2.x)+0.00000001)
    else:
        return (p1.y - p2.y) / (p1.x - p2.x)


def get_intersection(line1, line2):
    slope1, slope2 = line1[0], line2[0]
    yint1, yint2 = line1[1], line2[1]
    matA = numpy.matrix([[(slope1 * -1), 1], [(slope2 * -1), 1]])
    matB = numpy.matrix([[yint1], [yint2]])
    invA = matA.getI()
    resultant = invA * matB
    return Node(resultant[0, 0], resultant[1, 0])


def get_midpoint(p1, p2):
    midNode = Node(((p1.x + p2.x) / 2), ((p1.y + p2.y) / 2))
    return midNode


def perp_slope(slope):
    # takes slope and returns the slope of a line perpendicular to it
    if slope == 0:
        slope += 0.00000000000001
    return (slope * -1) ** -1


def line_from_slope(slope, point):
    return [slope, (slope * (-1 * point.x)) + point.y]


def calculate_voronoi_nodes(faces):
    voronoi_nodes = []
    for f in faces:
        # We need to get the circumcenter of all the faces and that will be the nodes of the voronoi.

        mid1 = get_midpoint(f.node1, f.node2)
        mid2 = get_midpoint(f.node2, f.node3)
        line1 = get_slope(f.node1, f.node2)
        line2 = get_slope(f.node2, f.node3)
        perp1 = perp_slope(line1)
        perp2 = perp_slope(line2)
        perpbi1 = line_from_slope(perp1, mid1)
        perpbi2 = line_from_slope(perp2, mid2)
        circumcent = get_intersection(perpbi1, perpbi2)

        voronoi_nodes.append(circumcent)
        f.set_voronoi_node(circumcent)
    return voronoi_nodes


def calculate_voronoi_edges(faces, nodes):
    # first clear all the edges because we are going to re-calculate them
    for f in faces:
        f.clear_voronoi_edges()

    for n in nodes:
        n.clear_voronoi_edges()

    for f in faces:
        # We will connect all voronoi nodes with the 3 adjacent voronoi nodes in the faces of it's corresponding face.
        face_edge1 = f.edge
        face_edge2 = face_edge1.next_edge
        face_edge3 = face_edge1.next_edge.next_edge

        face1 = None
        face2 = None
        face3 = None
        if face_edge1.adjacent_edge is not None:
            face1 = face_edge1.adjacent_edge.face

        if face_edge2.adjacent_edge is not None:
            face2 = face_edge2.adjacent_edge.face

        if face_edge3.adjacent_edge is not None:
            face3 = face_edge3.adjacent_edge.face

        # We now have the current face and all it's adjacent faces.
        # We have already calculated the voronoi nodes for these faces, so we can connect them
        if face1 is not None:
            edge = Edge(f.get_voronoi_node(), face1.get_voronoi_node())

            if f.node1 == face1.node1 or f.node1 == face1.node2 or f.node1 == face1.node3:
                f.node1.add_voronoi_edge(edge)

            if f.node2 == face1.node1 or f.node2 == face1.node2 or f.node2 == face1.node3:
                f.node2.add_voronoi_edge(edge)

            if f.node3 == face1.node1 or f.node3 == face1.node2 or f.node3 == face1.node3:
                f.node3.add_voronoi_edge(edge)

        if face2 is not None:
            edge = Edge(f.get_voronoi_node(), face2.get_voronoi_node())

            if f.node1 == face2.node1 or f.node1 == face2.node2 or f.node1 == face2.node3:
                f.node1.add_voronoi_edge(edge)

            if f.node2 == face2.node1 or f.node2 == face2.node2 or f.node2 == face2.node3:
                f.node2.add_voronoi_edge(edge)

            if f.node3 == face2.node1 or f.node3 == face2.node2 or f.node3 == face2.node3:
                f.node3.add_voronoi_edge(edge)

        if face3 is not None:
            edge = Edge(f.get_voronoi_node(), face3.get_voronoi_node())

            if f.node1 == face3.node1 or f.node1 == face3.node2 or f.node1 == face3.node3:
                f.node1.add_voronoi_edge(edge)

            if f.node2 == face3.node1 or f.node2 == face3.node2 or f.node2 == face3.node3:
                f.node2.add_voronoi_edge(edge)

            if f.node3 == face3.node1 or f.node3 == face3.node2 or f.node3 == face3.node3:
                f.node3.add_voronoi_edge(edge)


def calculate_voronoi_faces(nodes):
    for n in nodes:
        if n.get_voronoi_face() is None:
            # Create a new Voronoi face object fo the node
            n.set_voronoi_face(VoronoiFace())

        # First we remove all the nodes on the face, this is because we're going to calculate them again
        voronoi_face = n.get_voronoi_face()
        voronoi_face.clear_nodes()

        # Find all the nodes from the face from the edges on the node.
        for e in n.get_voronoi_edges():
            node_from = e.node_from
            node_to = e.node_to
            if not voronoi_face.contains(node_from):
                voronoi_face.add_node(node_from)
            if not voronoi_face.contains(node_to):
                voronoi_face.add_node(node_to)

        voronoi_face.gift_wrapping()


def is_valid_edge(A, B, C, D):
    """
    Returns True is D lies in the circumcircle of ABC
    This is done by determining the determinant of a matrix.
    """
    M = [[A.x, A.y, (pow(A.x, 2) + pow(A.y, 2)), 1],
         [B.x, B.y, (pow(B.x, 2) + pow(B.y, 2)), 1],
         [C.x, C.y, (pow(C.x, 2) + pow(C.y, 2)), 1],
         [D.x, D.y, (pow(D.x, 2) + pow(D.y, 2)), 1]]
    det_result = numpy.linalg.det(M)
    return not det_result > 0


def calculate_voronoi_colour(width, height, nodes, pixels):
    for x in range(0, width):
        for y in range(0, height):
            smallest_distance_to_node = 999999999999
            selected_node = None
            for n in nodes:
                if abs(n.x) is not 9999999 or abs(n.y) is not 9999999:
                    distance_to_node = distance(x, y, n.x, n.y)
                    if distance(x, y, n.x, n.y) < smallest_distance_to_node:
                        selected_node = n
                        smallest_distance_to_node = distance_to_node
            if selected_node is not None:
                pixel = pixels[x, abs(y-height)-1]
                selected_node.get_voronoi_face().add_pixel_value(pixel)

        if x % int((width/100)) == 0:
            print("progress: " + str((x/width)*100)[0:4] + "%")

    for n in nodes:
        n.get_voronoi_face().calculate_colour()


def create_image(width, height, nodes):
    image_array = []

    # first we fill the array with empty pixel values so we can replace them with the correct values.
    for y in range(0, height):
        image_array.append([])
        for x in range(0, width):
            image_array[y].append([0, 0, 0])

    for x in range(0, width):
        for y in range(0, height):
            smallest_distance_to_node = 999999999999
            selected_node = None
            for n in nodes:
                if abs(n.x) is not 9999999 or abs(n.y) is not 9999999:
                    distance_to_node = distance(x, y, n.x, n.y)
                    if distance(x, y, n.x, n.y) < smallest_distance_to_node:
                        selected_node = n
                        smallest_distance_to_node = distance_to_node
            if selected_node is not None:
                face = selected_node.get_voronoi_face()
                pixel = [face.colour[0], face.colour[1], face.colour[2]]
                image_array[abs(y-height)-1][x] = pixel

        if x % int((width/100)) == 0:
            print("progress: " + str((x/width)*100)[0:4] + "%")

    return image_array


def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

