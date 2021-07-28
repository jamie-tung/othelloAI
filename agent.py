import copy
import threading

class Agent:
    
    '''
    Initialization.
    '''
    def __init__(self, environment):
        self.environment = environment
        self.grid_value_dictionary = {}


    '''
    Choose move.
    '''
    def chooseMove(self):
        move_list = list(self.environment.validMoves(2))
        move_dictionary = {}
        thread_pool = []
        if len(move_list) > 0:
            value_list = []
            for move in move_list:
                t = threading.Thread(target=self.findValue, args=(move, move_dictionary, value_list))
                thread_pool.append(t)
                t.start()
            for t in thread_pool:
                t.join()
            maximum_value = max(value_list)
            move_of_interest = None
            for move, value in move_dictionary.items():
                if value == maximum_value:
                    move_of_interest = move
            return move_of_interest


    '''
    Find value.
    '''
    def findValue(self, move, move_dictionary, move_value_list):
        remaining_moves = int((8*8 - self.environment.countDiscs(2) - self.environment.countDiscs(1))/8)
        minimax_depth = remaining_moves
        value = self.minimax(move, minimax_depth, -99999999, 999999999, True, self.environment)
        move_dictionary[move] = value
        move_value_list.append(value)
    


    '''
    Evaluate grid state for player.
    '''
    def evaluateGrid(self, grid, player):
        state_value = 0
        other_player_value = 0
        evaluation_grid = [
                [99, -8, 8, 6, 6, 8, -8, 99],
                [-8, -24, -4, -3, -3, -4, -24, -8],
                [8, -4, 7, 4, 4, 7, -4, 8],
                [6, -3, 4, 0, 0, 4, -3, 6],
                [6, -3, 4, 0, 0, 4, -3, 6],
                [8, -4, 7, 4, 4, 7, -4, 8],
                [-8, -24, -4, -3, -3, -4, -24, -8],
                [99, -8, 8, 6, 6, 8, -8, 99]
        ]
        for x in range(self.environment.gridWidth):
            for y in range(self.environment.gridHeight):
                if grid[x][y] == player:
                    state_value += evaluation_grid[x][y]
                elif grid[x][y] == self.environment.oppositePlayer(player):
                    other_player_value += evaluation_grid[x][y]
        mobility = len(self.environment.validMoves(player)) - len(self.environment.validMoves(self.environment.oppositePlayer(player)))
        return (0.6 * (state_value - other_player_value)) + (0.4 * mobility)


    '''
    Minimax
    '''
    def minimax(self, move, depth, alpha, beta, maximizingPlayer, environment):
        environment_copy = copy.deepcopy(environment)
        environment_copy.makeMove(2, move)
        if depth == 0 or environment.gameIsOver():
            gridString = environment_copy.gridString()
            if not self.grid_value_dictionary.get(gridString) == None:
                return self.grid_value_dictionary.get(gridString)
            else:
                self.grid_value_dictionary[gridString] = self.evaluateGrid(environment.grid, 2)
            return self.grid_value_dictionary[gridString]
        if maximizingPlayer:
            available_moves = environment_copy.validMoves(2)
            max_value = -99999999999
            max_value_list = []
            max_thread_pool = []
            for new_move in available_moves:
                #t = threading.Thread(target=self.minimaxHelper, args=(new_move, depth-1, alpha, beta, False, environment_copy, max_value_list))
                #max_thread_pool.append(t)
                #t.start()
                #for t in max_thread_pool:
                #    t.join()
                self.minimaxHelper(new_move, depth-1, alpha, beta, False, environment_copy, max_value_list)
                max_value = max([max_value]+max_value_list)
                alpha = max(alpha, max_value)
                if beta <= alpha:
                    break
            return max_value
        else:
            min_value = 99999999999
            available_moves = environment_copy.validMoves(1)
            min_value_list = []
            min_thread_pool = []
            for new_move in available_moves:
                #t = threading.Thread(target=self.minimaxHelper, args=(new_move, depth-1, alpha, beta, True, environment_copy, min_value_list))
                #min_thread_pool.append(t)
                #t.start()
                #for t in min_thread_pool:
                #    t.join()
                self.minimaxHelper(new_move, depth-1, alpha, beta, True, environment_copy, min_value_list)
                min_value = min([min_value] + min_value_list)
                beta = min(beta, min_value)
                if beta <= alpha:
                    break
            return min_value
        return 0
            

    '''
    Minimax helper.
    '''
    def minimaxHelper(self, new_move, depth, alpha, beta, maximizingPlayer, environment, value_list):
        env_copy = copy.deepcopy(environment)
        env_copy.makeMove(2 if maximizingPlayer else 1, new_move)
        gridString = env_copy.gridString()
        if not self.grid_value_dictionary.get(gridString) == None:
            eval = self.grid_value_dictionary.get(gridString)
        else:
            eval = self.minimax(new_move, depth, alpha, beta, maximizingPlayer, environment)
            self.grid_value_dictionary[gridString] = eval
        value_list.append(self.grid_value_dictionary.get(gridString))