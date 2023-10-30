from socha.field import CubeCoords, Dir, Team

class Ship:
    def __init__(self, coal: int, dir: Dir, free_turns: int, passengers: int, points: int, speed: int, team: Team, pos: CubeCoords):
        self.coal = coal
        self.dir = dir
        self.free_turns = free_turns
        self.passengers = passengers
        self.points = points
        self.speed = speed
        self.team = team
        self.pos = pos
        
        self.movement_points: int = None
        self.free_turns: int = None