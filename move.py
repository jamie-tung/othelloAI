from location import Location

class Move(Location):

    '''
    Initialization.
    '''
    def __init__(self, x, y, player):
        self.player = player
        super().__init__(x, y)
