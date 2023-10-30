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