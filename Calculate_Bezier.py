# https://tomrocksmaths.com/wp-content/uploads/2021/05/de-casteljaus-algorithm.pdf
import numpy as np
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
    #ls = [de_casteljau(control_points, t) for t in np.linspace(0, 1, num_points)]
    return [de_casteljau(control_points, t) for t in np.linspace(0, 1, num_points)]



# TODO Quelle finden und umschreiben
def Bresenham_Algorithm(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    steep = dy > dx
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        dx, dy = dy, dx
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    ystep = 1 if y0 < y1 else -1
    error = 0
    for x in range(round(x0), round(x1) + 1):
        if steep:
            yield (int(y), int(x))
        else:
            yield (int(x), int(y))
        error += dy
        if 2 * error >= dx:
            y += ystep
            error -= dx
