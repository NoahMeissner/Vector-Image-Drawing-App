from LineAlgorithms import calculate_rectangle

"""
The Point class represents a point in a 2D space with additional properties and methods.
Each point has x and y coordinates, an ID, and can optionally be part of a Bezier curve or a polygon.
The class also calculates the rectangular area that bounds the point.
"""


class Point:

    def __init__(self, x, y, id_code):
        self.x = x
        self.y = y
        self.point = None
        self.calculate_rectangle()
        self.id = id_code
        self.bezier = False
        self.polygon = None
        self.rectangle = None

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_id(self):
        return self.id

    def get_coordinates(self):
        return [self.x, self.y]

    def set_coordinates(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.calculate_rectangle()

    def calculate_rectangle(self):
        return calculate_rectangle([self.x, self.y], None)

    def set_control_point(self, x, y):
        self.point = Point(x, y, self.id)

    def set_bezier(self, bol):
        self.bezier = bol

    def get_bezier(self):
        return self.bezier

    def set_polygon(self, point):
        self.polygon = point

    def get_polygon(self):
        return self.polygon

    def get_control_point(self):
        return self.point

    def get_rectangle(self):
        self.rectangle = self.calculate_rectangle()
        print(f"rectangle: {self.rectangle}")
        return self.rectangle
