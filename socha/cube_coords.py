from enum import Enum
from socha.cube_coords import CubeCoord

class CubeCoord:
    def __init__(self, q, r, s = None):
        if s is None:
            s = -(q+r)
        
        self.q = q
        self.r = r
        self.s = s
        
    def rotate(self, clockwise: bool):
        if clockwise:
            return CubeCoord(-self.r, -self.s, -self.q)
        else:
            return CubeCoord(-self.s, -self.q, -self.r)
        
class Dir(Enum):
    RIGHT=CubeCoord(1, 0, -1)
    DOWN_RIGHT=CubeCoord(0, 1, -1)
    DOWN_LEFT=CubeCoord(-1, 1, 0)
    LEFT=CubeCoord(-1, 0, 1)
    UP_LEFT=CubeCoord(0, -1, 1)
    UP_RIGHT=CubeCoord(1, -1, 0)
    
class Team(Enum):
    ONE=1
    TWO=2