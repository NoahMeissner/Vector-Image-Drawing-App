import json
from Point import Point
class OpenFile:

    def __init__(self, url):
        self.url = url
        json_scheme = None

    def open(self):
        with open(self.url, 'r') as file:
            self.json_scheme = json.load(file)


    def set_point(self, obj):
        point = Point(obj["x"], obj["y"], obj["id"])
        point.set_control_Point(self.set_point(obj['control_Point']))
        point.set_polygon('polygon')
        point.set_bezier('bezier')
        return point

    def get_points(self, json_list):
        ls = []
        for obj in json_list:
            ls.append(self.set_point(obj))



    def get_data(self, json_scheme):
        color_line = json_scheme['color_line']
        color_polygon = json_scheme['color_polygon']
        list = json_scheme['list_points']
        ls_points = self.get_points(list)
        return [color_line, color_polygon, ls_points]

