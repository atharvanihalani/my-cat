class Coderack():
    """
    Properties:
        a data structure that stores all pending codelets (will this suffer from population explosion?)
        
    Methods:
        an access method to add certain codelets (with urgency values)
        a method to stochastically pop codelets off the structure (based on priority + pressure)
        an update method for each time-step
    
    
    how am i gonna store these? let's just say urgency = number of codelets? and that adds to the pressure directly lmao
        wait idt that would work lmao. difficult to incorporate temperature now!
        
        
    """

    def __init__(self) -> None:
        pass

    def add(self):
        # add codelets
        pass

    def run(self):
        # stochastically pick a codelet to run next
        pass

    def update(self):
        pass
    
    pass