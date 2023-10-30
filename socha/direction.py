from enum import Enum
from socha.cube_coords import CubeCoord

class Dir(Enum):
    RIGHT=CubeCoord(1, 0, -1)
    DOWN_RIGHT=CubeCoord(0, 1, -1)
    DOWN_LEFT=CubeCoord(-1, 1, 0)
    LEFT=CubeCoord(-1, 0, 1)
    UP_LEFT=CubeCoord(0, -1, 1)
    UP_RIGHT=CubeCoord(1, -1, 0)