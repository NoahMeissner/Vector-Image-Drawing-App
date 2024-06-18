import numpy as np
import sys
from config import PolygonOptions
sys.setrecursionlimit(100000)


class Polygon:

    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height

    def get_box(self, ls):
        min_x = min(p[0] for p in ls)
        min_y = min(p[1] for p in ls)
        max_x = max(p[0] for p in ls)
        max_y = max(p[1] for p in ls)

        width = max_x - min_x
        height = max_y - min_y

        if width > height:
            center_y = (min_y + max_y) / 2
            half_width = width / 2
            min_y = int(center_y - half_width)
            max_y = int(center_y + half_width)
        else:
            center_x = (min_x + max_x) / 2
            half_height = height / 2
            min_x = int(center_x - half_height)
            max_x = int(center_x + half_height)

        min_x = max(min_x - 1, 0)
        min_y = max(min_y - 1, 0)
        max_x = min(max_x + 1, self.width)
        max_y = min(max_y + 1, self.height)

        return min_x, min_y, max_x, max_y

    def draw_polygon(self, polygon, polygon_color, polgon_muster):
        polygon = np.array(polygon)
        min_x, min_y, max_x, max_y = self.get_box(polygon)
        print(min_x, min_y, max_x, max_y)
        mask = np.zeros((self.width, self.height), dtype=int)

        for point in polygon:
            x, y = point
            mask[x, y] = 1

        start = (min_x, min_y)

        finish = self.fill4(start[0], start[1], mask, max_x, max_y, min_x, min_y)

        self.canvas = self.draw(finish, polgon_muster, polygon_color, min_x, min_y, max_x, max_y)

        return self.canvas

    def draw(self, arr, polygon_muster, color, min_x, min_y, max_x, max_y):
        rows, cols = arr.shape
        if polygon_muster == PolygonOptions.horizontal:
            for x in range(min_x, rows, 8):
                for y in range(min_y, cols):
                    if arr[x, y] == 0:
                        self.canvas = self.paint(x, y, max_y, min_y, min_x, max_x, color, arr)

        elif polygon_muster == PolygonOptions.vertical:
            for x in range(rows):
                for y in range(min_y, cols, 8):
                    self.canvas = self.paint(x, y, max_y, min_y, min_x, max_x, color, arr)

        elif polygon_muster == PolygonOptions.dot:
            for x in range(min_x, rows, 8):
                for y in range(min_y, cols, 8):
                    self.canvas = self.paint(x, y, max_y, min_y, min_x, max_x, color, arr)
        elif polygon_muster == PolygonOptions.full:
            for x in range(min_x, rows):
                for y in range(min_y, cols):
                    self.canvas = self.paint(x, y, max_y, min_y, min_x, max_x, color, arr)

        return self.canvas

    def paint(self, x, y, max_y, min_y, min_x, max_x, color, arr):
        if arr[x, y] == 0 and y % 2 == 0 and x % 2 == 0:
            if min_x <= x < max_x and min_y <= y < max_y:
                self.canvas.create_rectangle(x, y, x + 1, y + 1, outline=color)
        return self.canvas

    def fill4(self, x, y, mask, max_x, max_y, min_x, min_y):
        if x < min_x or x >= max_x or y < min_y or y >= max_y or mask[x, y] == 1:
            return mask
        if mask[x, y] == 0:
            mask[x, y] = 2
            if min_y <= y + 1 < max_y and mask[x, y + 1] != 1 and mask[x, y + 1] != 2:
                y_new = y + 1
                self.fill4(x, y_new, mask, max_x, max_y, min_x, min_y)
            if min_y <= y - 1 < max_y and mask[x, y - 1] != 1 and mask[x, y - 1] != 2:
                y_new = y - 1
                self.fill4(x, y_new, mask, max_x, max_y, min_x, min_y)

            if min_x <= x + 1 < max_x and mask[x + 1, y] != 1 and mask[x + 1, y] != 2:
                x_new = x + 1
                self.fill4(x_new, y, mask, max_x, max_y, min_x, min_y)
            if min_x <= x - 1 < max_x and mask[x - 1, y] != 1 and mask[x - 1, y] != 2:
                x_new = x - 1
                self.fill4(x_new, y, mask, max_x, max_y, min_x, min_y)
            return mask
