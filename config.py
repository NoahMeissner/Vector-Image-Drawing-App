from enum import Enum


class PolygonOptions(Enum):
    vertical = 1,
    horizontal = 2,
    full = 3,
    dot = 4


class ObjectTypes(Enum):
    Line = 1,
    Rectangle = 2,


CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
