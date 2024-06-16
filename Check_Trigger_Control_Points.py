from __future__ import annotations
import math

class TriggerPoints:

    def __init__(self):
        self.SIZE = (20, 20)

    def length(self,p: tuple):
        """Returns the length of a 2D vector p (same as the distance of the point p from the origin)"""
        x, y = p
        return math.sqrt(x * x + y * y)

    # %%

    def rect(self, p: tuple[int | float], size: tuple[int | float], center: tuple[int | float] = (0, 0)):
        # unpack tuples because Python does not allow e.g., subtracting one tuple from another (numpy does)
        x, y = p
        cx, cy = center
        w, h = size
        # transform point
        x, y = (x - cx, y - cy)
        # calculate rect SDF (https://iquilezles.org/articles/distfunctions2d/)
        dx, dy = (abs(x) - w, abs(y) - h);
        return self.length((max(dx, 0.0), max(dy, 0.0))) + min(max(dx, dy), 0.0)

    def painted_points(self, points_list, trigger, ):
        pre_point = None
        post_point = None
        for x in range(0,len(points_list)):
            point = points_list[x]
            distance = self.rect(trigger, self.SIZE, (point.X(), point.Y()))
            if distance <= self.SIZE[0]:
                if x - 1 >= 0:
                    pre_point = points_list[x - 1]
                if x + 1 < len(points_list):
                    post_point = points_list[x + 1]
                return [pre_point, point, post_point]
        return False



    def bezier_points(self, points_list, trigger):
        pre_point = None
        for index in range(0, len(points_list)-1):
                control_point = points_list[index].get_control_Point()
                if control_point is not None:
                    distance = self.rect(trigger, self.SIZE, points_list[index].get_control_Point().coordinates())
                    if distance <= self.SIZE[0]:
                        print()
                        pre_point = points_list[index-1]
                        post_point = points_list[index]
                        print(pre_point)
                        return [pre_point, post_point]
        return False



