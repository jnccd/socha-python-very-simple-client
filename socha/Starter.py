import socket
from lxml import objectify

class Starter:
    def __init__(self, calculate_move, on_update) -> None:
        self.calculate_move = calculate_move
        self.on_update = on_update
        
        self.do_a_barrel_roll()
        
    def do_a_barrel_roll(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)
        sock.connect(("localhost", 13050))
        
        # Welcome
        sock.send(f"<protocol><join gameType=\"swc_2023_penguins\" />".encode())
        
        while True: # Rolls here
            # Receive answer and coat it
            answer: str = self.receive(sock)
            answer = answer.removeprefix('<protocol>')
            answer = "<received>" + answer + "</received>"
            if answer.__contains__('</protocol>'):
                break
            
            parsed_answer = objectify.fromstring(answer)
            print(answer, parsed_answer)
            
            
            
        s.close()
        
    def receive(self, sock) -> str:
        received: str = ''
        while not received.__contains__('</room>') and not received.__contains__('</protocol>'):
            received += sock.recv(256).decode()
        #print(received)
        return received