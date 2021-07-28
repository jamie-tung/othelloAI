
from move import Move
from location import Location
from collections import deque
class Environment:
    
    '''
    init
    '''
    def __init__(self):
        self.grid = []
        self.gridWidth = 8
        self.gridHeight = 8
        self.turn = 1
        self.initializeGrid()
        self.last_player = None

    '''
    initialize Grid values.
    '''
    def initializeGrid(self):
        for i in range(self.gridWidth):
            self.grid.append([])
            for j in range(self.gridHeight):
                self.grid[i].append(0)
        self.grid[3][3] = 1
        self.grid[4][3] = 2
        self.grid[3][4] = 2
        self.grid[4][4] = 1


    def gridString(self):
        string_state = ""
        for i in range(self.gridWidth):
            for j in range(self.gridHeight):
                string_state += str(self.grid[i][j])
        return string_state

    '''
    Count discs for player
    '''
    def countDiscs(self, player):
        count = 0
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if self.grid[x][y] == player:
                    count = count + 1
        return count


    '''
    Make move.
    '''
    def makeMove(self, player, move):
        if move in self.validMoves(player):
            self.last_player = player
            self.adjustBoard(player, move)
            self.switchTurn()

        

    '''
    Adjust board for player move.
    '''
    def adjustBoard(self, player, move):
        self.changeVerticalDirections(player, move)
        self.changeHorizontalDirections(player, move)
        self.changeDiagonalDirections(player, move)
    

    '''
    Change Vertical Directions on board to player where needs to be changed from move location.
    '''
    def changeVerticalDirections(self, player, move):
        self.changePositiveVerticalDirection(player, move)
        self.changeNegativeVerticalDirection(player, move)


    '''
    Helper function for changeVerticalDirections to change required discs in positive direction.
    '''
    def changePositiveVerticalDirection(self, player, move):
        location = Location(move.x, move.y+1)
        if location.y > self.gridHeight-1:
            return
        queue = deque([])
        opposite_player = self.oppositePlayer(player)
        while(self.grid[location.x][location.y] == opposite_player):
            queue.append(location)
            location = Location(location.x, location.y+1)
            if location.y > self.gridHeight-1:
                return
        if self.grid[location.x][location.y] == player:
            while(len(queue) > 0):
                changing_location = queue.popleft()
                self.grid[changing_location.x][changing_location.y] = player
            self.grid[move.x][move.y] = player
        elif self.grid[location.x][location.y] == 0:
            return
        


    '''
    Helper function for changeVerticalDirections to change required discs in negative direction.
    '''
    def changeNegativeVerticalDirection(self, player, move):
        location = Location(move.x, move.y-1)
        if location.y < 0:
            return
        queue = deque([])
        opposite_player = self.oppositePlayer(player)
        while(self.grid[location.x][location.y] == opposite_player):
            queue.append(location)
            location = Location(location.x, location.y-1)
            if location.y < 0:
                return
        if self.grid[location.x][location.y] == player:
            while(len(queue) > 0):
                changing_location = queue.popleft()
                self.grid[changing_location.x][changing_location.y] = player
            self.grid[move.x][move.y] = player
        elif self.grid[location.x][location.y] == 0:
            return




    '''
    Change Horizontal Directions on board to player where needs to be changed from move location.
    '''
    def changeHorizontalDirections(self, player, move):
        self.changePositiveHorizontalDirection(player, move)
        self.changeNegativeHorizontalDirection(player, move)



    '''
    Helper function for changeHorizontalDirections to change required discs in positive direction.
    '''
    def changePositiveHorizontalDirection(self, player, move):
        location = Location(move.x+1, move.y)
        if location.x > self.gridWidth-1:
            return
        queue = deque([])
        opposite_player = self.oppositePlayer(player)
        try:
            while(self.grid[location.x][location.y] == opposite_player):
                queue.append(location)
                location = Location(location.x+1, location.y)
                if location.x > self.gridWidth - 1:
                    return
            if self.grid[location.x][location.y] == player:
                while(len(queue) > 0):
                    changing_location = queue.popleft()
                    self.grid[changing_location.x][changing_location.y] = player
                self.grid[move.x][move.y] = player
            elif self.grid[location.x][location.y] == 0:
                return
        except:
            print(location.x, location.y)

    '''
    Helper function for changeHorizontalDirections to change required discs in negative direction.
    '''
    def changeNegativeHorizontalDirection(self, player, move):
        location = Location(move.x-1, move.y)
        if location.x < 0:
            return
        queue = deque([])
        opposite_player = self.oppositePlayer(player)
        while(self.grid[location.x][location.y] == opposite_player):
            queue.append(location)
            location = Location(location.x-1, location.y)
            if location.x < 0:
                return
        if self.grid[location.x][location.y] == player:
            while(len(queue) > 0):
                changing_location = queue.popleft()
                self.grid[changing_location.x][changing_location.y] = player
            self.grid[move.x][move.y] = player
        elif self.grid[location.x][location.y] == 0:
            return



    '''
    Change Diagonal Directions on board to player where needs to be changed from move location.
    '''
    def changeDiagonalDirections(self, player, move):
        self.changeUpperLeftDirection(player, move)
        self.changeUpperRightDirection(player, move)
        self.changeLowerLeftDirection(player, move)
        self.changeLowerRightDirection(player, move)   


    '''
    Change Upper Left Direction 
    '''
    def changeUpperLeftDirection(self, player, move):
        queue = deque([])
        opposite_player = self.oppositePlayer(player)
        location = Location(move.x-1, move.y+1)
        if location.x < 0 or location.y > self.gridHeight - 1:
            return
        while(self.grid[location.x][location.y] == opposite_player):
            queue.append(location)
            location = Location(location.x-1, location.y+1)
            if location.x < 0 or location.y > self.gridHeight - 1:
                return
        if self.grid[location.x][location.y] == player:
            while(len(queue) > 0):
                changing_location = queue.popleft()
                self.grid[changing_location.x][changing_location.y] = player
            self.grid[move.x][move.y] = player
        elif self.grid[location.x][location.y] == 0:
            return

    '''
    Change Upper Right direction.
    '''
    def changeUpperRightDirection(self, player, move):
        queue = deque([])
        opposite_player = self.oppositePlayer(player)
        location = Location(move.x+1, move.y+1)
        if location.x > self.gridWidth - 1 or location.y > self.gridHeight - 1:
            return
        while(self.grid[location.x][location.y] == opposite_player):
            queue.append(location)
            location = Location(location.x+1, location.y+1)
            if location.x > self.gridWidth - 1 or location.y > self.gridHeight - 1:
                return
        if self.grid[location.x][location.y] == player:
            while(len(queue) > 0):
                changing_location = queue.popleft()
                self.grid[changing_location.x][changing_location.y] = player
            self.grid[move.x][move.y] = player
        elif self.grid[location.x][location.y] == 0:
            return

    '''
    Change Lower Left Direction.
    '''
    def changeLowerLeftDirection(self, player, move):
        queue = deque([])
        opposite_player = self.oppositePlayer(player)
        location = Location(move.x-1, move.y-1)
        if location.x < 0 or location.y < 0:
            return
        while(self.grid[location.x][location.y] == opposite_player):
            queue.append(location)
            location = Location(location.x-1, location.y-1)
            if location.x < 0 or location.y < 0:
                return
        if self.grid[location.x][location.y] == player:
            while(len(queue) > 0):
                changing_location = queue.popleft()
                self.grid[changing_location.x][changing_location.y] = player
            self.grid[move.x][move.y] = player
        elif self.grid[location.x][location.y] == 0:
            return


    '''
    Change Lower right Direcction.
    '''
    def changeLowerRightDirection(self, player, move):
        queue = deque([])
        opposite_player = self.oppositePlayer(player)
        location = Location(move.x+1, move.y-1)
        if location.x > self.gridWidth -1 or location.y < 0:
            return
        while(self.grid[location.x][location.y] == opposite_player):
            queue.append(location)
            location = Location(location.x+1, location.y-1)
            if location.x > self.gridWidth -1 or location.y < 0:
                return
        if self.grid[location.x][location.y] == player:
            while(len(queue) > 0):
                changing_location = queue.popleft()
                self.grid[changing_location.x][changing_location.y] = player
            self.grid[move.x][move.y] = player
        elif self.grid[location.x][location.y] == 0:
            return



    '''
    Return True if game is over.
    '''
    def gameIsOver(self):
        if len(self.validMoves(1)) == 0 and len(self.validMoves(2)) == 0:
            return True
        return False


    '''
    Return a list of valid moves for player.
    '''
    def validMoves(self, player):
        possibleMoves = set()
        discLocations = self.getDiscLocations(player)
        for loc in discLocations:
            current_loc = Move(loc.x, loc.y, player)
            vertical_moves = self.getVerticalMoves(current_loc)
            horizontal_moves = self.getHorizontalMoves(current_loc)
            diagonal_moves = self.getDiagonalMoves(current_loc)
            possibleMoves.update(vertical_moves)
            possibleMoves.update(horizontal_moves)
            possibleMoves.update(diagonal_moves)

        return possibleMoves


    '''
    Return a set of vertical possible moves.
    '''
    def getVerticalMoves(self, current_loc):
        vertical_moves = set()
        opposite_player = self.oppositePlayer(current_loc.player)
        for y in range(current_loc.y, self.gridHeight):
            if y == current_loc.y + 1:
                if not self.grid[current_loc.x][y] == opposite_player:
                    break
            elif not y == current_loc.y and self.grid[current_loc.x][y] == current_loc.player:
                break
            else:
                if self.grid[current_loc.x][y] == 0:
                    vertical_moves.add(Move(current_loc.x, y, current_loc.player))
                    break
        for y in range(current_loc.y, -1, -1):
            if y == current_loc.y - 1:
                if not self.grid[current_loc.x][y] == opposite_player:
                    break
            elif not y == current_loc.y and self.grid[current_loc.x][y] == current_loc.player:
                break
            else:
                if self.grid[current_loc.x][y] == 0:
                    vertical_moves.add(Move(current_loc.x, y, current_loc.player))
                    break
        return vertical_moves


    '''
    Return opposite player.
    '''
    def oppositePlayer(self, player):
        if player == 1:
            return 2
        return 1



    '''
    Return a set of horizontal possible moves.
    '''
    def getHorizontalMoves(self, current_loc):
        horizontal_moves = set()
        opposite_player = self.oppositePlayer(current_loc.player)
        for x in range(current_loc.x, self.gridWidth):
            if x == current_loc.x + 1:
                if not self.grid[x][current_loc.y] == opposite_player:
                    break
            elif not x == current_loc.x and self.grid[x][current_loc.y] == current_loc.player:
                break
            else:
                if self.grid[x][current_loc.y] == 0:
                    horizontal_moves.add(Move(x, current_loc.y, current_loc.player))
                    break
        for x in range(current_loc.x, -1, -1):
            if x == current_loc.x - 1:
                if not self.grid[x][current_loc.y] == opposite_player:
                    break
            elif not x == current_loc.x and self.grid[x][current_loc.y] == current_loc.player:
                break
            else:
                if self.grid[x][current_loc.y] == 0:
                    horizontal_moves.add(Move(x, current_loc.y, current_loc.player))
                    break
        return horizontal_moves
        


    '''
    Return a set of diagonal possible moves.
    '''
    def getDiagonalMoves(self, current_loc):
        diagonal_moves = set()
        diagonal_moves.update(self.getUpperLeftMove(current_loc.x, current_loc.y, current_loc.player, current_loc))
        diagonal_moves.update(self.getLowerLeftMove(current_loc.x, current_loc.y, current_loc.player, current_loc))
        diagonal_moves.update(self.getUpperRightMove(current_loc.x, current_loc.y, current_loc.player, current_loc))
        diagonal_moves.update(self.getLowerRightMove(current_loc.x, current_loc.y, current_loc.player, current_loc))
        return diagonal_moves


    '''
    Return upper left move.
    '''
    def getUpperLeftMove(self, x, y, player, current_loc):
        opposite_player = self.oppositePlayer(player)
        if x > -1 and y < self.gridHeight:
            if x == current_loc.x - 1 and y == current_loc.y + 1:
                if self.grid[x][y] == 0 or self.grid[x][y] == player:
                    return set()
                elif x == current_loc.x - 1 and y == current_loc.y + 1 and self.grid[x][y] == opposite_player:
                    return self.getUpperLeftMove(x-1, y+1, player, current_loc)
            elif not x==current_loc.x and not y==current_loc.y and self.grid[x][y] == current_loc.player:
                return set()
            elif self.grid[x][y] == 0:
                return {Move(x, y, player)}
            else:
                return self.getUpperLeftMove(x-1, y+1, player, current_loc)
        return set()


    '''
    Return lower left move.
    '''
    def getLowerLeftMove(self, x, y, player, current_loc):
        opposite_player = self.oppositePlayer(player)
        if x > -1 and y > -1:
            if x == current_loc.x - 1 and y == current_loc.y - 1:
                if self.grid[x][y] == 0 or self.grid[x][y] == player:
                    return set()
                elif x == current_loc.x - 1 and y == current_loc.y - 1 and self.grid[x][y] == opposite_player:
                    return self.getLowerLeftMove(x-1, y-1, player, current_loc)
            elif not x==current_loc.x and not y==current_loc.y and self.grid[x][y] == current_loc.player:
                return set()
            elif self.grid[x][y] == 0:
                return {Move(x, y, player)}
            else:
                return self.getLowerLeftMove(x-1, y-1, player, current_loc)
        return set()


    '''
    Return upper right move.
    '''
    def getUpperRightMove(self, x, y, player, current_loc):
        opposite_player = self.oppositePlayer(player)
        if x < self.gridWidth and y < self.gridHeight:
            if x == current_loc.x + 1 and y == current_loc.y + 1:
                if self.grid[x][y] == 0 or self.grid[x][y] == player:
                    return set()
                elif x == current_loc.x + 1 and y == current_loc.y + 1 and self.grid[x][y] == opposite_player:
                    return self.getUpperRightMove(x+1, y+1, player, current_loc)
            elif not x==current_loc.x and not y==current_loc.y and self.grid[x][y] == current_loc.player:
                return set()
            elif self.grid[x][y] == 0:
                return {Move(x, y, player)}
            else:
                return self.getUpperRightMove(x+1, y+1, player, current_loc)
        return set()


    '''
    Return lower right move.
    '''
    def getLowerRightMove(self, x, y, player, current_loc):
        opposite_player = self.oppositePlayer(player)
        if x < self.gridWidth and y > -1:
            if x == current_loc.x + 1 and y == current_loc.y - 1:
                if self.grid[x][y] == 0 or self.grid[x][y] == player:
                    return set()
                elif x == current_loc.x + 1 and y == current_loc.y - 1 and self.grid[x][y] == opposite_player:
                    return self.getLowerRightMove(x+1, y-1, player, current_loc)
            elif not x==current_loc.x and not y==current_loc.y and self.grid[x][y] == current_loc.player:
                return set()
            elif self.grid[x][y] == 0:
                return {Move(x, y, player)}
            else:
                return self.getLowerRightMove(x+1, y-1, player, current_loc)
        return set()


    '''
    Get player disc locations.
    '''
    def getDiscLocations(self, player):
        discLocations = []
        for x in range(self.gridWidth):
            for y in range(self.gridHeight):
                if self.grid[x][y] == player:
                    discLocations.append(Location(x, y))
        return discLocations

    '''
    Switch Turn to next player.
    '''
    def switchTurn(self):
        if self.last_player == 1:
            if len(self.validMoves(2)) > 0:
                self.turn = 2
            else:
                self.turn = 1
        elif self.last_player == 2:
            if len(self.validMoves(1)) > 0:
                self.turn = 1
            else:
                self.turn = 2


    '''
    Visualize grid layout.
    '''
    def visualizeGrid(self):
        for x in range(self.gridWidth):
            line = ""
            for y in range(self.gridHeight):
                line = line + str(self.grid[x][y])
            print(line)
        print("======================================================")


if __name__ == "__main__":
    env = Environment()
    print(env.gridString())