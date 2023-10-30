

class GameState:
    def __init__(self) -> None:
        self.turn = 0
        self.start_team = ''
        self.current_team = ''
        
    def __str__(self) -> str:
        return vars(self)