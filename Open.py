import json
from Point import Point

"""
This class handles the process of opening a JSON file and processing its data into an internal structure.
It loads the JSON file, processes the data, and converts it into a list of Point objects with associated properties.
"""


def add_polygon(ls):
    ls_final = []
    for index, point in enumerate(ls):
        if point.get_polygon() is not None:
            for i in range(0, index):
                polygon = ls[i]
                if point.get_polygon() == point.get_id():
                    point.set_polygon(polygon)
                    break
        ls_final.append(point)
    return ls_final


class OpenFile:

    def __init__(self, url):
        self.url = url
        self.json_scheme = None

    def open(self):
        with open(self.url, 'r') as file:
            self.json_scheme = json.load(file)
            return self.json_scheme

    def set_point(self, obj):
        if obj is None:
            return None
        point = Point(obj['x'], obj['y'], obj['id'])
        control = self.set_point(obj['control_Point'])
        if control is not None:
            point.set_control_point(control.get_x(), control.get_y())
        point.set_polygon(obj['polygon'])
        point.set_bezier(obj['bezier'])
        return point

    def get_points(self, json_list):
        ls = []
        for obj in json_list:
            ls.append(self.set_point(obj))
        return ls

    def get_data(self):
        self.json_scheme = self.open()
        color_line = self.json_scheme['color_line']
        color_polygon = self.json_scheme['color_polygon']
        ls_points = self.get_points(self.json_scheme['list_points'])
        ls_points = add_polygon(ls_points)
        return [color_line, color_polygon, ls_points]
