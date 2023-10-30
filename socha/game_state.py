from socha.field import CubeCoords, Dir, Field
from socha.ship import Ship

class GameState:
    def __init__(self) -> None:
        self.turn = 0
        self.start_team = ''
        self.current_team = ''
        
        self.p_one_ship: Ship = None
        self.p_two_ship: Ship = None
        self.board: dict[Field] = {}
        
        self.seg_offset_starts = [CubeCoords(-1, -2), CubeCoords(-1, -1), CubeCoords(-1, 0), CubeCoords(-2, 1), CubeCoords(-3, 2)]
        self.seg_offsets = [
            [ 
                start.add(CubeCoords.dir_to_offset(Dir.RIGHT).mult_scalar(x))
                for x 
                in range(5)
            ]
            for start 
            in self.seg_offset_starts
        ]
          
    def get_possible_moves():
        pass
         
    def pretty_print_board(self):
        qs = [q for q,r in self.board.keys()]
        rs = [r for q,r in self.board.keys()]
        
        min_q = min(qs)
        max_q = max(qs)
        min_r = min(rs)
        max_r = max(rs)
        
        for r in range(min_r, max_r+1):
            norm_r = r - min_r
            print(''.join([' ' for x in range(norm_r)]), end='')
            for q in range(min_q, max_q+1):
                if self.p_one_ship.pos.q == q and self.p_one_ship.pos.r == r:
                    print('1|', end='')
                elif self.p_two_ship.pos.q == q and self.p_two_ship.pos.r == r:
                    print('2|', end='')
                elif (q,r) in self.board:
                    print(self.board[(q,r)].chr()+'|', end='')
                else:
                    print('  ', end='')
            print()
           
    def __str__(self) -> str:
        return str(vars(self))