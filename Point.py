from Calculate_Rectangle import Calculate_Rectangle

"""
Diese Klasse behandelt jeden Punkt, welcher gezeichnet wurde
"""

class Point:

    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.point = None
        self.calculate_rectangle()
        self.id = id
        self.bezier = False
        self.polygon = None


    def X(self):
        return self.x
    def Y(self):
        return self.y

    def get_id(self):
        return self.id

    def coordinates(self):
        return [self.x, self.y]

    def set_coordinates(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
        self.calculate_rectangle()

    def calculate_rectangle(self):
        rect_obj = Calculate_Rectangle([self.x, self.y],None)
        self.rectangle = rect_obj.calculate_rectangle_area()

    def set_control_Point(self, x,y):
        self.point = Point(x,y,self.id)

    def set_bezier(self, bol):
        self.bezier = bol

    def get_bezier(self):
        return self.bezier

    def set_polygon(self, point):
        self.polygon = point

    def get_polygon(self):
        return self.polygon


    def get_control_Point(self):
        return self.point

    def get_rectangle(self):
        return self.rectangle


