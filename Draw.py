from LineAlgorithms import bresenham_algorithm, bezier_curve
import numpy as np
from Polygon import Polygon


class Draw:
    def __init__(self, canvas):
        self.canvas = canvas
        self.draw_control_points = True
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 600
        self.lines_polygon = []

    def get_draw_control_points(self):
        return self.draw_control_points

    def set_draw_control_points(self, bol):
        self.draw_control_points = bol

    def draw_line(self, point1, point2, line_color):
        line = bresenham_algorithm(point1, point2)
        self.lines_polygon.extend(line)
        pixels = np.zeros((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), dtype=bool)
        for p in line:
            if 0 < p[0] < self.CANVAS_WIDTH and 0 < p[1] < self.CANVAS_HEIGHT:
                self.canvas.create_rectangle(p[0], p[1], p[0], p[1], fill=line_color, outline=line_color)
                pixels[p[0], p[1]] = True

    def draw_bezier(self, point1, point2, point3, line_color):
        ls = [point1, point2, point3]
        line = bezier_curve(ls)
        self.lines_polygon.extend(line)
        pixels = np.zeros((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), dtype=bool)
        for p in line:
            if 0 < int(p[0]) < self.CANVAS_WIDTH and 0 < int(p[1]) < self.CANVAS_HEIGHT:
                self.canvas.create_rectangle(p[0], p[1], p[0], p[1], fill=line_color, outline=line_color)
                pixels[p[0], p[1]] = True

    def draw_polygon(self, vertices, polygon_color, polygon_muster):
        ls = [(p.get_x(), p.get_y()) for p in vertices]
        for index, point in enumerate(vertices):
            if point.get_bezier():
                pre = vertices[index - 1]
                control = point.get_control_point()
                bezier = [pre.get_coordinates(), control.get_coordinates(), point.get_coordinates()]
                line = bezier_curve(bezier)
                ls.extend(line)
            else:
                pre = vertices[index - 1]
                line_points = bresenham_algorithm(pre.get_coordinates(), point.get_coordinates())
                ls.extend(line_points)
        polygon = Polygon(self.canvas, self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.canvas = polygon.draw_polygon(ls, polygon_color, polygon_muster)

    def check_polygon(self, point_list, polygon_color, polygon_muster):
        all_polygons = []
        for index, point in enumerate(point_list):
            if point.get_polygon() is not None:
                start_point = point.get_polygon()
                end_point = point
                start_track = False
                ls = []
                for point in point_list:
                    if point.get_id() == start_point.get_id() or (
                            start_track == True and point.get_id() != end_point.get_id()):
                        start_track = True
                        ls.append(point)
                    elif point.get_id() != end_point.get_id():
                        break
                ls.append(end_point)
                all_polygons.append(ls)
        for a in all_polygons:
            self.draw_polygon(a, polygon_color, polygon_muster)

    # TODO polygon option
    def draw(self, points_list, line_color, polygon_color, polygon_muster):
        self.lines_polygon = []
        if len(points_list) > 0:
            current_point = points_list[-1]
            if len(points_list) > 1:
                last_point = points_list[-2]
                print(current_point)
                self.draw_line(last_point.get_coordinates(), current_point.get_coordinates(), line_color)

        if self.draw_control_points:
            coordinates_rectangle = current_point.get_rectangle()
            rectangle_start = coordinates_rectangle[0]
            rectangle_end = coordinates_rectangle[1]
            self.canvas.create_rectangle(rectangle_start[0], rectangle_start[1], rectangle_end[0], rectangle_end[1],
                                         outline=line_color)

            if current_point.get_control_point() is not None:
                current_control = current_point.get_control_point()
                coordinates_rectangle = current_control.get_rectangle()
                rectangle_start = coordinates_rectangle[0]
                rectangle_end = coordinates_rectangle[1]
                self.canvas.create_rectangle(rectangle_start[0], rectangle_start[1], rectangle_end[0], rectangle_end[1],
                                             outline=line_color)

        self.check_polygon(points_list, polygon_color, polygon_muster)
        return self.canvas

    def draw_all(self, points_list, line_color, polygon_color, polygon_muster):
        self.lines_polygon = []
        if self.draw_control_points:
            coordinates_rectangle = points_list[0].get_rectangle()
            rectangle_start = coordinates_rectangle[0]
            rectangle_end = coordinates_rectangle[1]
            self.canvas.create_rectangle(rectangle_start[0], rectangle_start[1], rectangle_end[0], rectangle_end[1],
                                         outline=line_color)

        list_p = points_list
        for i in range(1, len(list_p)):
            last_point = list_p[i - 1]
            current_point = list_p[i]
            if len(list_p) > 0:
                if current_point.get_bezier():
                    self.draw_bezier(last_point.get_coordinates(), current_point.get_control_point().get_coordinates(),
                                     current_point.get_coordinates(), line_color)
                else:
                    self.draw_line(last_point.get_coordinates(), current_point.get_coordinates(), line_color)

            if self.draw_control_points:
                coordinates_rectangle = current_point.get_rectangle()
                rectangle_start = coordinates_rectangle[0]
                rectangle_end = coordinates_rectangle[1]
                self.canvas.create_rectangle(rectangle_start[0], rectangle_start[1], rectangle_end[0], rectangle_end[1],
                                             outline=line_color)

                # Control Point
                if current_point.get_control_point() is not None:
                    current_control = current_point.get_control_point()
                    coordinates_rectangle = current_control.get_rectangle()
                    rectangle_start = coordinates_rectangle[0]
                    rectangle_end = coordinates_rectangle[1]
                    self.canvas.create_rectangle(rectangle_start[0], rectangle_start[1], rectangle_end[0],
                                                 rectangle_end[1],
                                                 outline=line_color)

        self.check_polygon(points_list, polygon_color, polygon_muster)
        return self.canvas
