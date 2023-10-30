from socha import *

gameState: GameState = None

def calculate_move() -> Move:
    global gameState
    
    possibleMoves = gameState.possible_moves
    return possibleMoves[0]

def on_update(state: game_state):
    global gameState
    
    gameState = state
        
if __name__ == "__main__":
    Starter(calculate_move = calculate_move, 
            on_update = on_update)
    