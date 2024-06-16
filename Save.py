import json


class Save:
    def __init__(self, list_points, url, color_line, color_polygon):
        self.list_points = list_points
        self.url = url
        self.color = color_line
        self.polygon = color_polygon
        json_scheme = self.create_file_json(self.create_json(), self.color_line, color_polygon)
        self.save_json(json_scheme)

    def create_json(self):
        ls = self.list_points
        ls_points = []

        for point in ls:
            control_point = None
            if point.get_control_Point() is not None:
                control = point.get_control_Point()
                control_point = self.create_point_json(control.get_id(), control.X(), control.Y(), None,
                                                       control.get_bezier(), control.get_polygon_line())
            point_json = self.create_point_json(control.get_id(), control.X(), control.Y(), control_point,
                                                control.get_bezier(), control.get_polygon_line())
            ls.append(point_json)
        return ls_points

    def create_point_json(self, id, x, y, control_point, bezier, polygon):
        return {
            "id": id,
            "x": x,
            "y": y,
            "control_Point": control_point,
            "bezier": bezier,
            "polygon": polygon
        }

    def create_file_json(self, list_points, color_line, color_polygon):
        return {
            "color_line": color_line,
            "color_polygon": color_polygon,
            "list_points": list_points
        }

    def save_json(self, json_scheme):
        with open(self.url, 'w') as file:
            json.dump(json_scheme, file, indent=4)
