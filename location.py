class Location():

    '''
    Initialization.
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y


    '''
    Hash
    '''
    def __hash__(self) -> int:
        return int(str(self.x)+"0"+str(self.y))


    '''
    EQ
    '''
    def __eq__(self, o: object) -> bool:
        if self.x == o.x and self.y == o.y:
            return True
        return False