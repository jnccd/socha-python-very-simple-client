import socket
from bs4 import BeautifulSoup
from socha import *
from socha.field import Field, CubeCoords, Dir, Team
from socha.ship import Ship

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Starter:
    def __init__(self, calculate_move) -> None:
        self.calculate_move = calculate_move
        
        self.do_a_barrel_roll()
        
    def do_a_barrel_roll(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect(("localhost", 13050))
        
        # Welcome
        self.send(sock, payload=f"<protocol><join gameType=\"swc_2023_penguins\" />")
        
        # Init data
        self.game_state = GameState()
        
        while True: # Rolls here
            print(f'{bcolors.HEADER}---')
            
            # Receive answer and coat it
            answer: str = self.receive(sock)
            answer = answer.removeprefix('<protocol>')
            answer = "<received>" + answer + "</received>"
            if answer.__contains__('</protocol>'):
                break
            
            # Yummy
            soup = BeautifulSoup(answer, "html.parser")
            #rint(f'{bcolors.OKCYAN}Got:\n{soup.prettify()}')
            
            if soup.joined is not None:
                self.room_id = soup.joined.get('roomid')
                print(f'{bcolors.WARNING}Room ID: {self.room_id}')
            if soup.left is not None and soup.left.roomid == self.room_id:
                break
            for room in soup.find_all('room'):
                room: BeautifulSoup = room # Linting
                if room.data.get('class') == ['moveRequest']:
                    print(f"{bcolors.WARNING}I got a movereq")
                    move_answer: Move = self.calculate_move(self.game_state)
                    xml_send_payload = f'<room roomId="{self.room_id}">\n{move_answer.to_xml()}</room>'
                    self.send(sock, xml_send_payload)
                if room.data.get('class') == ['memento']:
                    in_state = room.data.state
                    
                    self.game_state.turn = int(in_state.get('turn'))
                    self.game_state.start_team = in_state.get('startteam')
                    self.game_state.current_team = in_state.get('currentteam')
                    
                    # Parse segments into board dict
                    self.game_state.board = {}
                    for seg in room.find_all('segment'):
                        seg: BeautifulSoup = seg # Linting
                        dir = Dir[seg.get('direction')]
                        center: BeautifulSoup = seg.find('center')
                        center_q = int(center.get('q'))
                        center_r = int(center.get('r'))
                        center_s = int(center.get('s'))
                        center_coords = CubeCoords(center_q, center_r, center_s)
                        for x, field_arr in enumerate(seg.find_all('field-array')):
                            field_arr: BeautifulSoup = field_arr # Linting
                            for y, field in enumerate([c for c in field_arr.children if c.name is not None]):
                                #print(x,y, len(self.game_state.seg_offsets), len(self.game_state.seg_offsets[0]))
                                field_coords = self.game_state.seg_offsets[y][x].\
                                    rotate_by_dir(dir).\
                                    add(center_coords)
                                self.game_state.board[(field_coords.q, field_coords.r)] = Field(type = field.name, coords = field_coords, is_midstream = y == 2)
                    
                    # Parse Ships
                    for i, ship in enumerate(in_state.find_all('ship')):
                        ship: BeautifulSoup = ship # Linting
                        position = ship.find_all('position')[0]
                        
                        new_ship = Ship(
                            int(ship.get('coal')), 
                            Dir[ship.get('direction')], 
                            int(ship.get('freeturns')), 
                            int(ship.get('passengers')), 
                            int(ship.get('points')), 
                            int(ship.get('speed')), 
                            Team[ship.get('team')], 
                            CubeCoords(
                                int(position.get('q')),
                                int(position.get('r')),
                                int(position.get('s')),
                        ))
                        
                        if i == 0:
                            self.game_state.p_one_ship = new_ship
                        elif i == 1:
                            self.game_state.p_two_ship = new_ship
                        else:
                            print(f'{bcolors.FAIL}Theres too many of them, what are we going to do?')
                            
                    print(f'{bcolors.WARNING}Got new board:')
                    self.game_state.pretty_print_board()
                    #print(f'{bcolors.WARNING}Gamestate: {self.game_state}')
            
        sock.close()
        
    def receive(self, sock) -> str:
        received: str = ''
        while not received.__contains__('</room>') and not received.__contains__('</protocol>'):
            received += sock.recv(256).decode()
        print(f'{bcolors.OKCYAN}Received:\n{received}')
        return received
    
    def send(self, sock, payload: str):
        sock.send(payload.encode())
        print(f'{bcolors.OKGREEN}Sent:\n{payload}')