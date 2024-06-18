# Noah Meißner 18.06.2024
from __future__ import annotations
import math

"""
TriggerPoints class for geometric operations:
- Calculate 2D vector length
- Compute distance between point and rectangle
- Identify points within trigger area
- Find Bézier curve control points within trigger area
"""


def length(coordinates):
    x, y = coordinates
    return math.sqrt(x * x + y * y)


# https://iquilezles.org/articles/distfunctions2d/
def rect(p, size, center=(0, 0)):
    x, y = p
    cx, cy = center
    w, h = size
    x, y = (x - cx, y - cy)
    dx, dy = (abs(x) - w, abs(y) - h)
    return length((max(dx, 0.0), max(dy, 0.0))) + min(max(dx, dy), 0.0)


class TriggerPoints:

    def __init__(self):
        self.size = (20, 20)

    def painted_points(self, points_list, trigger, ):
        pre_point = None
        post_point = None
        for x in range(0, len(points_list)):
            point = points_list[x]
            distance = rect(trigger, self.size, (point.get_x(), point.get_y()))
            if distance <= self.size[0]:
                if x - 1 >= 0:
                    pre_point = points_list[x - 1]
                if x + 1 < len(points_list):
                    post_point = points_list[x + 1]
                return [pre_point, point, post_point]
        return False

    def bezier_points(self, points_list, trigger):
        for index in range(0, len(points_list)):
            control_point = points_list[index].get_control_point()
            if control_point is not None:
                distance = rect(trigger, self.size, points_list[index]
                                .get_control_point().get_coordinates())
                if distance <= self.size[0]:
                    pre_point = points_list[index - 1]
                    post_point = points_list[index]
                    return [pre_point, post_point]
        return False
