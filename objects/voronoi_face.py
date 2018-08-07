from random import randint


# noinspection SpellCheckingInspection
class VoronoiFace:
    def __init__(self):
        self.nodes = []
        self.colour = [randint(0, 255), randint(0, 255), randint(0, 255), 1.0]

    def add_node(self, node):
        self.nodes.append(node)

    def contains(self, node):
        return node in self.nodes

    def clear_nodes(self):
        self.nodes = []

    def get_nodes(self):
        return self.nodes

    # We will find the convex hull using the gift wrapping algorithm. We know the the voronoi face is convex
    # But we will use this algorithm to get the points in the correct order.
    def gift_wrapping(self):
        # We are going to find the left most node in the set, this node will always be in the convex hull.
        if len(self.nodes) < 3:
            print("not enough nodes for a convex hull calculation")
            return

        finalPoints = []
        minX = 999999
        hullPoint = ""
        for n in self.nodes:
            if n.x < minX:
                hullPoint = n
                minX = n.x

        remainingNodes = self.nodes.copy()

        endPoint = ""
        finalPoints = []
        while finalPoints == [] or endPoint != finalPoints[0]:
            finalPoints.append(hullPoint)
            endPoint = remainingNodes[0]

            for index in range(1, len(remainingNodes)):
                # We want to find the angle between the last found point (finalPoints[-1]), the currently selected
                # endPoint and the node we're looping over. If the angle is better between the last found point
                # and the current point we're checking (n) we will put the endPoint on that node.
                if hullPoint == endPoint or self.orientation(finalPoints[-1], endPoint, remainingNodes[index]) > 0:
                    # The orientation is on the leftside.
                    endPoint = remainingNodes[index]

            hullPoint = endPoint

        # We should now have found the points in correct order so we override the current node ordering with the new one
        self.nodes = finalPoints

    def orientation(self, p1, p2, p3):
        orientation = (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)

        return orientation
