# Noah Meißner 18.06.2024
from enum import Enum

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600


class PolygonOptions(Enum):
    VERTICAL = 1,
    HORIZONTAL = 2,
    FULL = 3,
    DOT = 4


class ObjectTypes(Enum):
    LINE = 1,
    RECTANGLE = 2,
