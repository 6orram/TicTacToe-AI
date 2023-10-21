
print(""" 
  --------------------------------------------------------------------
    ______                                                       
   /      \                                                      
  |  $$$$$$\  ______    ______    ______   ______   ______ ____  
  | $$___\$$ /      \  /      \  /      \ |      \ |      \    \ 
  | $$    \ |  $$$$$$\|  $$$$$$\|  $$$$$$\ \$$$$$$\| $$$$$$\$$$$\ 
  | $$$$$$$\| $$  | $$| $$   \$$| $$   \$$/      $$| $$ | $$ | $$
  | $$__/ $$| $$__/ $$| $$      | $$     |  $$$$$$$| $$ | $$ | $$
   \$$    $$ \$$    $$| $$      | $$      \$$    $$| $$ | $$ | $$
    \$$$$$$   \$$$$$$  \$$       \$$       \$$$$$$$ \$$  \$$  \$$

  ---------------------------- TicTacToe AI -------------------------- -                                                                                                                                                                                
""")
print("Don't forget to check My GitHub")
print("https://github.com/6orram")


# import Librarys
import copy
import random
import sys
from time import sleep
import pygame
import numpy as np

# Import Constants From Other File
from constant import *

# PYGAME SETUP
pygame.init()
secreen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE AI")
secreen.fill(BG_COLOR)

# Track Movements
class Board:

    # setup moves and coordinates
    def __init__(self):
        self.squares = np.zeros((ROWS, COLMS))
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    # Win mouvement
    def final_state(self, show=False):

        """
            Player Win --> Return 1
            AI Win --> Return -1
            Draw || Notihnig --> Return 0
        """


        # vertical wins
        for col in range(COLMS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(secreen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
    
        # vertical wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20,  row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(secreen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]
            
        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20 ,HEIGHT - 20)
                pygame.draw.line(secreen, color, iPos, fPos, LINE_WIDTH + 10)
            return self.squares[1][1]
        
        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20 ,20)
                pygame.draw.line(secreen, color, iPos, fPos, LINE_WIDTH + 10)
            return self.squares[1][1]
        
        # no win yet
        return 0

    # mark player movements in the board
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    # give the value 0 to empty squares in the board
    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0
    
    # get empty squares
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLMS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    # check if the board is full
    def is_full(self):
        return self.marked_sqrs == 9
    
    # check the empty squares
    def isempty(self):
        return self.marked_sqrs == 0

# AI Functions
class AI:
    # intialise
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    # random AI mouvements
    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]
    
    # Algorithm Minimax Function
    def minimax(self, board, maximizing):
        # check the README FILE ON GITHUB TO UNDERSTAND THIS ALGORITHM
        # terminal case
        case = board.final_state()

        if case == 1:
            return 1, None
        

        if case == 2:
            return -1, None
        
        elif board.is_full():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # evaloution
    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = "random"
            move = self.rnd(main_board)
        else:
            # minimax algorithm
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        
        return move

# Game Class
class Game:
    # setup the game and the players
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.game_mode = "ai"
        self.running = True
        self.show_lines()

    # Change Mode Function (PvP or AI)
    def change_mode(self):
        if self.game_mode == "ai":
            self.game_mode = "pvp"
            print("game mode set to pvp")
        else:
            self.game_mode = "ai"
            print("game mode set to AI")

    # make move function
    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.change_player()
        print(self.board.squares)

    # Game line
    def show_lines(self):
        # start
        secreen.fill(BG_COLOR)
        # VERTICAL
        pygame.draw.line(secreen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(secreen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # HORIZONTAL
        pygame.draw.line(secreen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(secreen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)

    # Game Figure
    def draw_fig(self, row, col):
        if self.player == 1:
            #desc line
            start_desc = (col * SQSIZE + 50, row * SQSIZE + 50)
            end_desc = (col * SQSIZE + SQSIZE - 50, row * SQSIZE + SQSIZE - 50)
            #asc line
            start_asc = (col * SQSIZE + 50, row * SQSIZE + SQSIZE - 50)
            end_asc = (col * SQSIZE + SQSIZE - 50, row * SQSIZE + 50)
            # Draw Cross 
            pygame.draw.line(secreen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)
            pygame.draw.line(secreen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
        else:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            # Draw Circle
            pygame.draw.circle(secreen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # Change Player Function
    def change_player(self):
        self.player = self.player % 2 + 1

    # Check if the round isover
    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.is_full()
    # restart the round
    def restart(self):
        self.__init__()
        print("the mode has been restarted")
    # change who start the game
    def Starting(self):
        if self.player == 1:
            self.player = 2
            print("AI Start the Game, Just Wait....")
    
# Main 
def main():
    # OBJECT
    game = Game()
    board = game.board
    ai = game.ai

    # MAINLOOP
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Click Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE

                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False
            # event Keyboard
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_g:
                    # g --> change the game mode
                    game.change_mode()

                if event.key == pygame.K_0:
                    # 0 --> change Ai Level (easy, Unbeatable)
                    if ai.level == 1:
                        ai.level = 0
                        print("AI level set to easy")
                    else:
                        ai.level = 1
                        print("AI Level set to Unbeatable")

                if event.key == pygame.K_r:
                    # r --> restart the game
                    game.restart()
                    board = game.board
                    ai = game.ai


                if event.key == pygame.K_p:
                    # p --> set the starter
                    if game.game_mode == "ai":
                        game.Starting()




        if game.game_mode == "ai" and game.player == ai.player and game.running:
            pygame.display.update()

            # ai methods
            row, col = ai.eval(board)


            game.make_move(row, col)
            if game.isover():
                game.running = False

        pygame.display.update()


main()