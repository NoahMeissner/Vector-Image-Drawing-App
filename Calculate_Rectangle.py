
class Calculate_Rectangle:

    def __init__(self, point_one, point_two):
        self.point_one = point_one
        self.point_two = point_two


    def calculate_rectangle_area(self):
        if self.point_two is None:
            mid_x = self.point_one[0]
            mid_y = self.point_one[1]
        else:
            print(self.point_two)
            mid_x = int((self.point_one[0] + self.point_two[0]) / 2)
            mid_y = int((self.point_one[1] + self.point_two[1]) / 2)
        start = (mid_x -2, mid_y - 2)
        end = (mid_x + 2, mid_y + 2)
        return (start, end)




