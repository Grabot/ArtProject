from random import randint


def orientation(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p3.x - p1.x) * (p2.y - p1.y)


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

    # We will find the convex hull using the gift wrapping algorithm.
    # We know the the voronoi face is convex but we will use
    # this algorithm to get the points in the correct order.
    def gift_wrapping(self):
        if len(self.nodes) < 3:
            print("not enough nodes for a convex hull calculation")
            return

        # We are going to find the left most node in the set
        min_x = 999999
        hull_point = ""
        for n in self.nodes:
            if n.x < min_x:
                hull_point = n
                min_x = n.x

        remaining_nodes = self.nodes.copy()

        end_point = ""
        final_points = []
        while final_points == [] or end_point != final_points[0]:
            final_points.append(hull_point)
            end_point = remaining_nodes[0]

            for index in range(1, len(remaining_nodes)):
                # We want to find the angle between the last found point (finalPoints[-1]), the currently selected
                # end_point and the node we're looping over. If the angle is better between the last found point
                # and the current point we're checking (n) we will put the end_point on that node.
                if hull_point == end_point or orientation(final_points[-1], end_point, remaining_nodes[index]) > 0:
                    # The orientation is on the leftside.
                    end_point = remaining_nodes[index]

            hull_point = end_point

        # We should now have found the points in correct order so we override the current node ordering with the new one
        self.nodes = final_points

    def set_colour(self, colour):
        self.colour = colour
