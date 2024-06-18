# Noah Meißner 18.06.2024
import numpy as np
from LineAlgorithms import bresenham_algorithm, bezier_curve
from Polygon import Polygon
from config import CANVAS_HEIGHT, CANVAS_WIDTH

"""
The Draw class offers methods for drawing lines,
Bezier curves and polygons on a canvas.
It also contains options for drawing control points
and for checking and drawing closed polygons.
"""


class Draw:
    def __init__(self, canvas):
        self.canvas = canvas
        self.draw_control_points = True

    def get_draw_control_points(self):
        return self.draw_control_points

    def set_draw_control_points(self, flag):
        self.draw_control_points = flag

    def draw_line(self, point1, point2, line_color):
        line = bresenham_algorithm(point1, point2)
        pixels = np.zeros((CANVAS_WIDTH, CANVAS_HEIGHT), dtype=bool)
        for p in line:
            if 0 <= p[0] < CANVAS_WIDTH and 0 <= p[1] < CANVAS_HEIGHT:
                self.canvas.create_rectangle(p[0],
                                             p[1],
                                             p[0],
                                             p[1],
                                             fill=line_color,
                                             outline=line_color)
                pixels[p[0], p[1]] = True

    def draw_bezier(self, point1, point2, point3, line_color):
        control_points = [point1, point2, point3]
        line = bezier_curve(control_points)
        pixels = np.zeros((CANVAS_WIDTH, CANVAS_HEIGHT), dtype=bool)
        for p in line:
            if 0 <= int(p[0]) < CANVAS_WIDTH and 0 <= int(p[1]) < CANVAS_HEIGHT:
                self.canvas.create_rectangle(p[0],
                                             p[1],
                                             p[0],
                                             p[1],
                                             fill=line_color,
                                             outline=line_color)
                pixels[p[0], p[1]] = True

    def draw_polygon(self, vertices, polygon_color, polygon_pattern):
        points = [(p.get_x(), p.get_y()) for p in vertices]
        for index, point in enumerate(vertices):
            if point.get_bezier():
                prev_point = vertices[index - 1]
                control = point.get_control_point()
                bezier_points = [prev_point.get_coordinates(),
                                 control.get_coordinates(),
                                 point.get_coordinates()]
                bezier_line = bezier_curve(bezier_points)
                points.extend(bezier_line)
            else:
                prev_point = vertices[index - 1]
                line_points = bresenham_algorithm(prev_point.get_coordinates(),
                                                  point.get_coordinates())
                points.extend(line_points)

        polygon = Polygon(self.canvas, CANVAS_WIDTH, CANVAS_HEIGHT)
        self.canvas = polygon.draw_polygon(points,
                                           polygon_color,
                                           polygon_pattern)

    def check_polygon(self, point_list, polygon_color, polygon_pattern):
        all_polygons = []
        for index, point in enumerate(point_list):
            if point.get_polygon() is not None:
                start_point = point.get_polygon()
                end_point = point
                start_track = False
                polygon_points = []
                for point_two in point_list:
                    if point_two.get_id() == start_point.get_id() or (
                            start_track and point_two.get_id() != end_point.get_id()):
                        start_track = True
                        polygon_points.append(point_two)
                    elif point_two.get_id() != end_point.get_id():
                        break
                polygon_points.append(end_point)
                all_polygons.append(polygon_points)

        for polygon in all_polygons:
            self.draw_polygon(polygon, polygon_color, polygon_pattern)

    def draw_point(self, point, line_color):
        if self.draw_control_points:
            coordinates_rectangle = point.get_rectangle()
            rectangle_start = coordinates_rectangle[0]
            rectangle_end = coordinates_rectangle[1]
            self.canvas.create_rectangle(rectangle_start[0],
                                         rectangle_start[1],
                                         rectangle_end[0],
                                         rectangle_end[1],
                                         outline=line_color)

            if point.get_control_point() is not None:
                control_point = point.get_control_point()
                coordinates_rectangle = control_point.get_rectangle()
                rectangle_start = coordinates_rectangle[0]
                rectangle_end = coordinates_rectangle[1]
                self.canvas.create_rectangle(rectangle_start[0],
                                             rectangle_start[1],
                                             rectangle_end[0],
                                             rectangle_end[1],
                                             outline=line_color)

    def draw(self, points_list, line_color, polygon_color, polygon_pattern):
        if len(points_list) > 0:
            current_point = points_list[-1]
            if len(points_list) > 1:
                last_point = points_list[-2]
                self.draw_line(last_point.get_coordinates(),
                               current_point.get_coordinates(),
                               line_color)
            self.draw_point(current_point, line_color)
            self.check_polygon(points_list, polygon_color, polygon_pattern)
        return self.canvas

    def re_draw(self, points_list, line_color, polygon_color, polygon_pattern):
        self.draw_point(points_list[0], line_color)
        for i in range(1, len(points_list)):
            last_point = points_list[i - 1]
            current_point = points_list[i]
            if len(points_list) > 0:
                if current_point.get_bezier():
                    self.draw_bezier(last_point.get_coordinates(),
                                     current_point.get_control_point().get_coordinates(),
                                     current_point.get_coordinates(),
                                     line_color)
                else:
                    self.draw_line(last_point.get_coordinates(),
                                   current_point.get_coordinates(),
                                   line_color)

            self.draw_point(current_point, line_color)
        self.check_polygon(points_list, polygon_color, polygon_pattern)
        return self.canvas
