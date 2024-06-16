

class Polygon:
    def __init__(self, canvas):
        self.canvas = canvas

    def is_point_in_polygon(self, x, y, polygon):
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def get_points_within_polygon(self, polygon):
        if not polygon:
            return []

        min_x = int(min(p[0] for p in polygon))
        max_x = int(max(p[0] for p in polygon))
        min_y = int(min(p[1] for p in polygon))
        max_y = int(max(p[1] for p in polygon))

        points_inside = []
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if self.is_point_in_polygon(x, y, polygon):
                    points_inside.append((x, y))

        return points_inside

    def draw_polygon(self, polygon):
        points_inside = self.get_points_within_polygon(polygon)
        step = max(1, len(points_inside) // 10000)  # Adjust step based on polygon size

        for index in range(0, len(points_inside), step):
            x, y = points_inside[index]
            self.canvas.create_rectangle(x, y, x + 1, y + 1, outline='red', fill='red')

        return self.canvas


