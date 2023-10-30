from socha.field import Dir

class Move:
    # Action class structure
    class IAction():
        def to_xml(self):
            pass
    
    class Acceleration(IAction):
        def __init__(self, acc) -> None:
            self.acc = acc
            
        def to_xml(self):
            return f'<acceleration acc="{self.acc}" />'
            
    class Advance(IAction):
        def __init__(self, distance) -> None:
            self.distance = distance
            
        def to_xml(self):
            return f'<advance distance="{self.distance}" />'
            
    class Push(IAction):
        def __init__(self, direction: Dir) -> None:
            self.direction = direction
            
        def to_xml(self):
            return f'<push direction="{self.direction}" />'
            
    class Turn(IAction):
        def __init__(self, direction: Dir) -> None:
            self.direction = direction
            
        def to_xml(self):
            return f'<turn direction="{self.direction}" />'
    
    # Some methods too
    def __init__(self, actions: list[IAction] = []) -> None:
        self.actions = actions
        
    def to_xml(self):
        re = '<move>\n<actions>\n'
        for action in self.actions:
            re += f'{action.to_xml()}\n'
        re += '</actions>\n</move>\n'
        return re