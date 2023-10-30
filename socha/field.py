from enum import Enum

class CubeCoords:
    def __init__(self, q, r, s = None):
        if s is None:
            s = -(q+r)
        
        self.q = q
        self.r = r
        self.s = s
        
    def add(self, cc):
        return CubeCoords(self.q + cc.q, self.r + cc.r, self.s + cc.s)
    
    def mult_scalar(self, scalar: float):
        return CubeCoords(self.q * scalar, self.r * scalar, self.s * scalar)
        
    def rotate(self, clockwise: bool):
        if clockwise:
            return CubeCoords(-self.r, -self.s, -self.q)
        else:
            return CubeCoords(-self.s, -self.q, -self.r)
        
    def __str__(self) -> str:
        return str(vars(self))
    
class Field:
    def __init__(self, type: str, coords: CubeCoords, is_midstream: bool):
        self.type = type
        self.coords = coords
        self.is_midstream = is_midstream
        
    def __str__(self) -> str:
        return str(vars(self))
        
class Dir(Enum):
    RIGHT: CubeCoords = CubeCoords(1, 0, -1)
    DOWN_RIGHT=CubeCoords(0, 1, -1)
    DOWN_LEFT=CubeCoords(-1, 1, 0)
    LEFT=CubeCoords(-1, 0, 1)
    UP_LEFT=CubeCoords(0, -1, 1)
    UP_RIGHT=CubeCoords(1, -1, 0)
    
class Team(Enum):
    ONE=1
    TWO=2