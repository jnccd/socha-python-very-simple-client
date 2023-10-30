from socha.field import CubeCoords, Dir

class GameState:
    def __init__(self) -> None:
        self.turn = 0
        self.start_team = ''
        self.current_team = ''
        
        board = {}
        
        self.seg_offset_starts = [CubeCoords(-1, -2), CubeCoords(-1, -1), CubeCoords(-1, 0), CubeCoords(-2, 1), CubeCoords(-3, 2)]
        self.seg_offsets = [
            [ 
                start.add(Dir.RIGHT.value.mult_scalar(x))
                for x 
                in range(5)
            ]
            for start 
            in self.seg_offset_starts
        ]
        
    def __str__(self) -> str:
        return str(vars(self))