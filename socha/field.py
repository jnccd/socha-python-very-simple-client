from enum import Enum

class Team(Enum):
    ONE=1
    TWO=2

class Dir(Enum):
    RIGHT=0
    DOWN_RIGHT=1
    DOWN_LEFT=2
    LEFT=3
    UP_LEFT=4
    UP_RIGHT=5
    
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
        
    def rotate_by_dir(self, dir: Dir):
        if dir is Dir.RIGHT:
            return CubeCoords(self.q, self.r, self.s)
        elif dir is Dir.DOWN_RIGHT:
            return self.rotate(True)
        elif dir is Dir.DOWN_LEFT:
            return self.rotate(True).rotate(True)
        elif dir is Dir.LEFT:
            return self.rotate(True).rotate(True).rotate(True)
        elif dir is Dir.UP_LEFT:
            return self.rotate(False).rotate(False)
        elif dir is Dir.UP_RIGHT:
            return self.rotate(False)
        
    def dir_to_offset(dir: Dir):
        if dir is Dir.RIGHT:
            return CubeCoords(1, 0, -1)
        elif dir is Dir.DOWN_RIGHT:
            return CubeCoords(0, 1, -1)
        elif dir is Dir.DOWN_LEFT:
            return CubeCoords(-1, 1, 0)
        elif dir is Dir.LEFT:
            return CubeCoords(-1, 0, 1)
        elif dir is Dir.UP_LEFT:
            return CubeCoords(0, -1, 1)
        elif dir is Dir.UP_RIGHT:
            return CubeCoords(1, -1, 0)
        
    def __str__(self) -> str:
        return str(vars(self))
    
class Field:
    def __init__(self, type: str, coords: CubeCoords, is_midstream: bool):
        self.type = type
        self.coords = coords
        self.is_midstream = is_midstream
        
    def chr(self):
        if self.type == 'water':
            if self.is_midstream:
                return 'm'
            else:
                return 'w'
        elif self.type == 'island':
            return 'O'
        elif self.type == 'passenger':
            return 'P'
        else:
            return '?'
        
    def __str__(self) -> str:
        return str(vars(self))