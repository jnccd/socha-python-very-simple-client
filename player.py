from socha import *

def calculate_move(game_state: GameState) -> Move:
    
    # TODO: Add logic here
    
    possible_moves = game_state.get_possible_moves()
    return possible_moves[0]
        
if __name__ == "__main__":
    Starter(calculate_move)
    