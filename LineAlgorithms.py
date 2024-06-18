import numpy as np

"""
- This script defines functions for drawing a Bezier curve and generating points
- along it using the De Casteljau's algorithm. It also includes an implementation
of the Bresenham's line algorithm for efficient rasterization of the curve on
a grid-based canvas.
- Additionally, there is a function to calculate a bounding
rectangle around a point or between two points.
"""


# https://tomrocksmaths.com/wp-content/uploads/2021/05/de-casteljaus-algorithm.pdf
def de_casteljau(points, t):
    if len(points) == 1:
        return points[0]
    else:
        new_points = []
        for i in range(len(points) - 1):
            x = int((1 - t) * points[i][0] + t * points[i + 1][0])
            y = int((1 - t) * points[i][1] + t * points[i + 1][1])
            new_points.append((x, y))
        return de_casteljau(new_points, t)


def bezier_curve(control_points, num_points=100):
    ls = [de_casteljau(control_points, t) for t in np.linspace(0, 1, num_points)]
    print(ls)
    final = []
    for index in range(1, len(ls)):
        pre = ls[index - 1]
        cur = ls[index]
        final.extend(bresenham_algorithm(pre, cur))
    return final


# https://www.roguebasin.com/index.php/Bresenham's_Line_Algorithm
def bresenham_algorithm(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    is_steep = abs(dy) > abs(dx)

    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    dx = x2 - x1
    dy = y2 - y1

    error = dx // 2
    y_step = 1 if y1 < y2 else -1

    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += y_step
            error += dx

    if swapped:
        points.reverse()
    return points


def calculate_rectangle(point_one, point_two):
    if point_two is None:
        mid_x = point_one[0]
        mid_y = point_one[1]
    else:
        mid_x = int((point_one[0] + point_two[0]) / 2)
        mid_y = int((point_one[1] + point_two[1]) / 2)
    start = (mid_x - 2, mid_y - 2)
    end = (mid_x + 2, mid_y + 2)
    return start, end
