from socha import *
from socha.game_state import GameState 
import socket
from bs4 import BeautifulSoup

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
        sock.settimeout(1)
        sock.connect(("localhost", 13050))
        
        # Welcome
        sock.send(f"<protocol><join gameType=\"swc_2023_penguins\" />".encode())
        
        # Init data
        self.gameState = GameState()
        
        while True: # Rolls here
            print(f'{bcolors.HEADER}---')
            
            # Receive answer and coat it
            answer: str = self.receive(sock)
            answer = answer.removeprefix('<protocol>')
            answer = "<received>" + answer + "</received>"
            if answer.__contains__('</protocol>'):
                break
            
            soup = BeautifulSoup(answer, "html.parser")
            print(f'{bcolors.OKCYAN}Got: {soup.prettify()}')
            
            if soup.joined is not None:
                self.room_id = soup.joined.get('roomid')
                print(f'{bcolors.WARNING}Room ID: {self.room_id}')
            if soup.left is not None and soup.left.roomid == self.room_id:
                break
            for room in soup.find_all('room'):
                if room.data.get('class') == ['moveRequest']:
                    print(f"{bcolors.WARNING}I got a movereq D:")
                    # TODO: Do something with it
                if room.data.get('class') == ['memento']:
                    in_state = room.data.state
                    
                    self.gameState.turn = int(in_state.get('turn')[0])
                    self.gameState.start_team = in_state.get('startteam')
                    self.gameState.current_team = in_state.get('currentteam')
                    
                    
                    
                    print(f'{bcolors.WARNING} {self.gameState}')
            
        s.close()
        
    def receive(self, sock) -> str:
        received: str = ''
        while not received.__contains__('</room>') and not received.__contains__('</protocol>'):
            received += sock.recv(256).decode()
        #print(received)
        return received