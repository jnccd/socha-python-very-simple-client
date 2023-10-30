

class GameState:
    def __init__(self) -> None:
        self.turn = 0
        self.start_team = ''
        self.current_team = ''
        
        self.seg_offsets = [
            []
        ]
        
        board = {}
        
    def __str__(self) -> str:
        return str(vars(self))