# Noah Meißner 18.06.2024
import json

"""
The Save class handles the process of saving a list
of Point objects and associated properties to a JSON file.
It converts the list of Point objects into a JSON-compatible
format and writes it to the specified file.
"""


def create_point_json(id_code, x, y, control_point, bezier, polygon):
    return {
        "id": id_code,
        "x": x,
        "y": y,
        "control_Point": control_point,
        "bezier": bezier,
        "polygon": polygon
    }


def create_file_json(list_points, color_line, color_polygon):
    return {
        "color_line": color_line,
        "color_polygon": color_polygon,
        "list_points": list_points
    }


class Save:
    def __init__(self, list_points, url, color_line, color_polygon):
        self.list_points = list_points
        self.url = url
        json_scheme = create_file_json(self.create_json(),
                                       color_line,
                                       color_polygon)
        self.save_json(json_scheme)

    def create_json(self):
        ls_points = []

        for index, point in enumerate(self.list_points):
            control_point = None
            id_code = None
            if point.get_control_point() is not None:
                control = point.get_control_point()
                control_point = create_point_json(control.get_id(),
                                                  control.get_x(),
                                                  control.get_y(),
                                                  None,
                                                  control.get_bezier(),
                                                  control.get_polygon())

            if point.get_polygon() is not None:
                polygon = point.get_polygon()
                id_code = polygon.get_id()
            point_json = create_point_json(point.get_id(),
                                           point.get_x(),
                                           point.get_y(),
                                           control_point,
                                           point.get_bezier(),
                                           id_code)
            ls_points.append(point_json)
        return ls_points

    def save_json(self, json_scheme):
        with open(self.url, 'w') as file:
            json.dump(json_scheme, file, indent=4)
