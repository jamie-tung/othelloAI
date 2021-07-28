from environment import Environment
from agent import Agent
from tkinter import *
from move import Move
import random
import threading

class Othello:
    
    '''
    Initialization.
    '''
    def __init__(self):
        self.environment = Environment()
        self.agent = Agent(self.environment)
        self.gui=Tk()
        self.buttonGrid = []
        self.green_square = PhotoImage(file=r"emptysquare.png").subsample(2, 2)
        self.black_disc = PhotoImage(file=r"blackdisc.png").subsample(2, 2)
        self.white_disc = PhotoImage(file=r"whitedisc.png") .subsample(2, 2)
        self.black_disc_count = 0
        self.white_disc_count = 0
        #self.game_count = 0
        self.useRandomPlayerMoves = False
        self.buildGUI()
        self.gui.mainloop()
        
        

    '''
    Build GUI
    '''
    def buildGUI(self):
        self.gui.title("Othello AI")
        for x in range(self.environment.gridWidth):
            self.buttonGrid.append([])
            for y in range(self.environment.gridHeight):
                if (self.environment.grid[x][y] == 0):
                    self.buttonGrid[x].append(Button(self.gui, image=self.green_square, height=50, command=lambda  c =(str(x)+":"+str(y)): self.buttonClick(c)))
                elif (self.environment.grid[x][y] == 1):
                    self.buttonGrid[x].append(Button(self.gui, image=self.white_disc, command=lambda c =(str(x)+":"+str(y)): self.buttonClick(c)))
                elif (self.environment.grid[x][y] == 2): 
                    self.buttonGrid[x].append(Button(self.gui, image=self.black_disc, command=lambda c =(str(x)+":"+str(y)): self.buttonClick(c)))       
                self.buttonGrid[x][y].grid(row=x, column=y)
        self.white_disc_count = Label(text=str(self.environment.countDiscs(1)) + " White\n Discs", font=('Verdana', 15), bg="cyan")       
        self.black_disc_count = Label(text=str(self.environment.countDiscs(2)) + " Black\n Discs", font=('Verdana', 15), bg="black", fg="white")
        self.turn_indicator = Label(text="White's\n Turn" if self.environment.turn==1 else "Black's\n Turn", font=('Verdana', 15))
        self.newgame_button = Button(self.gui, text="New\n Game", bg="red", font=('Verdana', 15), command=self.newGame)
        self.random_player_button = Button(self.gui, text="Random\n Player", font=('Verdana', 15), command=self.enableRandomPlayer)
        self.human_player_button = Button(self.gui, text="Human\n Player", font=('Verdana', 15), command=self.disableRandomPlayer)
        self.white_disc_count.grid(row=0, column=8, columnspan=1)
        self.black_disc_count.grid(row=1, column=8, columnspan=1)
        self.turn_indicator.grid(row=2, column=8)
        self.newgame_button.grid(row=3, column=8, columnspan=1)
        self.random_player_button.grid(row=4, column=8, columnspan=2)
        self.human_player_button.grid(row=5, column=8)

    '''
    Disable Random Player
    '''
    def disableRandomPlayer(self):
        self.useRandomPlayerMoves = False
        self.updateBoardAndScore()

    '''
    Enable Random Player
    '''
    def enableRandomPlayer(self):
        self.useRandomPlayerMoves = True
        self.updateBoardAndScore()


    '''
    New Game.
    '''
    def newGame(self):
        self.environment.grid=[]
        self.environment.initializeGrid()
        self.environment.turn = 1
        self.updateBoardAndScore()



    '''
    Update board and score.
    '''
    def updateBoardAndScore(self):
        self.updateBoardInterface()
        self.updateTurnIndicator()
        self.updateWhiteDiscCount()
        self.updateBlackDiscCount()
        if self.environment.turn == 2:
            t = threading.Thread(target=self.agentMakeMove, args=())
            t.start()
        if self.useRandomPlayerMoves and not self.environment.gameIsOver():
            if self.environment.turn == 1:
                possible_moves = list(self.environment.validMoves(1))
                random_number = random.randint(0, len(possible_moves)-1)
                chosen_random_move = possible_moves[random_number]
                self.environment.makeMove(1, chosen_random_move)
                self.updateBoardAndScore()
        # elif self.useRandomPlayerMoves and self.environment.gameIsOver():
        #     if self.game_count < 1000:
        #         self.game_count += 1
        #         f = open("resultFile.txt", "a")
        #         if self.environment.countDiscs(2) > self.environment.countDiscs(1):
        #             f.write("2\n")
        #         elif self.environment.countDiscs(2) < self.environment.countDiscs(1):
        #             f.write("1\n")
        #         elif self.environment.countDiscs(2) == self.environment.countDiscs(1):
        #             f.write("0\n")
        #         f.close()
        #         self.newGame()
        #         self.enableRandomPlayer()

    '''
    Update turn indicator.
    '''
    def updateTurnIndicator(self):
        if self.environment.gameIsOver():
            if self.environment.countDiscs(1) > self.environment.countDiscs(2):
                self.turn_indicator["text"] = "White\n Wins!"
            elif self.environment.countDiscs(2) > self.environment.countDiscs(1):
                self.turn_indicator["text"] = "Black\n wins!"
            else:
                self.turn_indicator["text"] = "Tie\n Game!"
        else:
            self.turn_indicator["text"] = "White's\n Turn" if self.environment.turn==1 else "Black's\n Turn"
        


    '''
    Update white disc count.
    '''
    def updateWhiteDiscCount(self):
        self.white_disc_count["text"] = str(self.environment.countDiscs(1)) + " White\n Discs"


    '''
    Update black disc count.
    '''
    def updateBlackDiscCount(self):
        self.black_disc_count["text"] = str(self.environment.countDiscs(2)) + " Black\n Discs"

    '''
    Handle Grid button click.
    '''
    def buttonClick(self, coordinate):
        coordinate_list = coordinate.split(":")
        x_coordinate=int(coordinate_list[0])
        y_coordinate=int(coordinate_list[1])
        human_move = Move(x_coordinate, y_coordinate, 1)
        if human_move in self.environment.validMoves(1):
            if self.environment.turn == 1:
                self.environment.makeMove(1, human_move)
                self.updateBoardAndScore()
            
       


    '''
    Agent make move
    '''
    def agentMakeMove(self):
        if not self.environment.gameIsOver():
            agent_move = self.agent.chooseMove()
            self.environment.makeMove(2, agent_move)
            self.updateBoardAndScore()


    '''
    Update board interface.
    '''
    def updateBoardInterface(self):
        for x in range(self.environment.gridWidth):
            for y in range(self.environment.gridHeight):
                if self.environment.grid[x][y] == 1:
                    self.buttonGrid[x][y]["image"] = self.white_disc
                elif self.environment.grid[x][y] == 2:
                    self.buttonGrid[x][y]["image"] = self.black_disc
                elif self.environment.grid[x][y] == 0:
                    self.buttonGrid[x][y]["image"] = self.green_square

        



if __name__ == "__main__":
    game = Othello()