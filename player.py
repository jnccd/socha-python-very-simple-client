from socha import *

def calculate_move(state: GameState) -> Move:
    
    return state.possible_moves[0]
        
if __name__ == "__main__":
    Starter(calculate_move)
    