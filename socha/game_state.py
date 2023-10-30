import copy
from socha.field import CubeCoords, Dir, Field
from socha.move import Move
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
        
    def get_field(self, coords: CubeCoords) -> Field:
        if coords.qr_tuple() not in self.board:
            return None
        else:
            return self.board[coords.qr_tuple()]
            
    def get_possible_moves(self, fast = True):
        if self.current_team == 'ONE':
            cur_ship = copy.deepcopy(self.p_one_ship)
            other_ship = copy.deepcopy(self.p_two_ship)
        elif self.current_team == 'TWO':
            cur_ship = copy.deepcopy(self.p_two_ship)
            other_ship = copy.deepcopy(self.p_one_ship)
        else:
            print('huh?')
            
        moves = self._recursed_movement(actions = [], cur_ship = cur_ship, other_ship = other_ship, fast = fast)
        
        return moves
        
    def _recursed_movement(self, actions: list[Move.IAction], cur_ship: Ship, other_ship: Ship, fast: bool) -> list[Move]:
        #print('len(actions)', len(actions), len([x for x in actions if type(x) is Move.Turn]))
        
        re_moves = []
        if cur_ship.movement_points == None:
            # --------- Accel Actions
            for speed in range(1, 6+1):
                # Copy everything
                copy_actions: list[Move.Action] = copy.deepcopy(actions)
                copy_cur_ship: Ship = copy.deepcopy(cur_ship)
                copy_other_ship: Ship = copy.deepcopy(other_ship)
                
                # Update vars
                speed_diff = abs(speed - copy_cur_ship.speed)
                coal_cost = speed_diff - 1 if speed_diff > 1 else 0
                copy_cur_ship.speed = speed
                copy_cur_ship.coal -= coal_cost
                copy_cur_ship.movement_points = speed
                if copy_cur_ship.free_turns is None:
                    copy_cur_ship.free_turns = 1
                
                # Create Action obj
                if speed_diff > 0:
                    copy_actions.append(Move.Acceleration(speed_diff))
                
                # Check for illegal state
                if copy_cur_ship.coal < 0:
                    continue
                
                # You're on a path in the woods, and at the end of that path is a cabin...
                rec_call_re = self._recursed_movement(copy_actions, copy_cur_ship, copy_other_ship, fast)
                if rec_call_re is not None:
                    re_moves.extend(rec_call_re)
            # ---------------------------
            
            # --- Return move objs
            return re_moves
        else:
            # --- Check for illegal state
            # Coal
            if cur_ship.coal < 0:
                return None
            # Movement Points
            if cur_ship.movement_points < 0:
                return None
            # Ship position on board
            if cur_ship.pos.qr_tuple() not in self.board or \
                self.board[cur_ship.pos.qr_tuple()].type != 'water':
                return None
            
            # --- Wrap finished actions in move obj
            if cur_ship.movement_points == 0:
                new_move = Move(actions)
                re_moves.append(new_move)
                return re_moves
            
            if cur_ship.movement_points > 0:
                # --------- Advance Action
                # Copy everything
                copy_actions: list[Move.Action] = copy.deepcopy(actions)
                copy_cur_ship: Ship = copy.deepcopy(cur_ship)
                copy_other_ship: Ship = copy.deepcopy(other_ship)
                
                # Update vars
                copy_cur_ship.movement_points -= 1
                copy_cur_ship.pos = copy_cur_ship.pos.add(CubeCoords.dir_to_offset(copy_cur_ship.dir))
                if self.get_field(copy_cur_ship.pos) is not None and self.get_field(copy_cur_ship.pos).is_midstream:
                    copy_cur_ship.movement_points -= 1
                
                # Create Action obj
                copy_actions.append(Move.Advance(1))
                
                # You're on a path in the woods, and at the end of that path is a cabin...
                rec_call_re = self._recursed_movement(copy_actions, copy_cur_ship, copy_other_ship, fast)
                if rec_call_re is not None:
                    re_moves.extend(rec_call_re)
                # ---------------------------
            if (cur_ship.free_turns > 0 or cur_ship.coal > 0) and \
                ((type(actions[-1]) is not Move.Turn) if len(actions) > 0 else True) and \
                (not fast or (fast and len([x for x in actions if type(x) is Move.Turn]) < 1)):
                # --------- Turn Action
                for dir in [x for x in Dir if x != cur_ship.dir]:
                    # Copy everything
                    copy_actions: list[Move.Action] = copy.deepcopy(actions)
                    copy_cur_ship: Ship = copy.deepcopy(cur_ship)
                    copy_other_ship: Ship = copy.deepcopy(other_ship)
                    
                    # Update vars
                    for x in range(copy_cur_ship.dir.diff(dir)):
                        if copy_cur_ship.free_turns > 0:
                            copy_cur_ship.free_turns -= 1
                        else:
                            copy_cur_ship.coal -= 1
                    copy_cur_ship.dir = dir
                    
                    # Check for illegal state
                    if copy_cur_ship.coal < 0:
                        continue
                    
                    # Create Action obj
                    copy_actions.append(Move.Turn(dir))
                    
                    # You're on a path in the woods, and at the end of that path is a cabin...
                    rec_call_re = self._recursed_movement(copy_actions, copy_cur_ship, copy_other_ship, fast)
                    if rec_call_re is not None:
                        re_moves.extend(rec_call_re)
                # ---------------------------
            # --- Return move objs
            return re_moves
    
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