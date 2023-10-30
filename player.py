from socha import *

def calculate_move(state: GameState) -> Move:
    global gameState
    
    possibleMoves = gameState.possible_moves
    return possibleMoves[0]
        
if __name__ == "__main__":
    Starter(calculate_move)
    