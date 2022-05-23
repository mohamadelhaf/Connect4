
#!pip install pygame
#!pip install numpy
import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7
DEPTH=5

def create_board(): #Don't change
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

# places a piece on the board
def drop_piece(board, row, col, piece): 
    board[row][col] = piece

# check if your move is valid
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# utility function to be used in getLegalActions
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# returns a list of tuples representing the legal actions
# [(0,0), (0,1)] means that the only actions available are
# row 0, column 0 and row 0, column 1
# you only need the column number for the action. 
def getLegalActions(board):
        actions=[]
        for col in range(7):
                row=get_next_open_row(board, col)
                
                if row is not None:
                        actions.append((row,col))
        return actions

def print_board(board):
    print(np.flip(board, 0))

# function that returns true if the board is a winning position
# for the player designated by piece
# piece=1 is human player, piece=2 is AI. 
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
            
# For visualization only
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):        
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

def Eval(board):
       
        total=0
        for i in range(6):
            ai=0
            human=0
            for j in range(7):
                if board[i][j]== 1 :
                    human+=1
                elif board[i][j]==2 :
                    ai+=1
            total+=ai-human
        for i in range(7):
            ai=0
            human=0
            for j in range(6):
                if board[j][i]== 1 :
                    human+=1
                elif board[j][i]== 2 :
                    ai+=1
            total+=ai-human
        return total


def Value(board,player,alfa,beta,depth):
    if winning_move(board,1):
        return -50
    elif winning_move(board,2):
        return +50
    elif depth==0:
        return Eval(board)
    if player==1 :
        return Min_value(board,player,alfa,beta,depth)
    if player==2 :
        return Max_value(board,player,alfa,beta,depth)

def Max_value(board,player,alfa,beta,depth):
        valid = getLegalActions(board)
        value = -math.inf
        for action in valid:
            copy_board = board.copy()
            drop_piece(copy_board, action[0],action[1],2)
            score = Value(copy_board, 1 , alfa, beta, depth-1)
            if score > value:
                value = score
            alfa = max(alfa, value)
            if alfa >= beta:
                break
        return value

def Min_value(board,player,alfa,beta,depth):
        value = math.inf
        valid = getLegalActions(board)
        for action in valid:
            copy_board = board.copy()
            drop_piece(copy_board, action[0],action[1],1)
            score = Value(copy_board, 2, alfa, beta, depth-1)
            if score < value:
                value = score
            beta = min(beta, value)
            if alfa>=beta:
                break
        return value

def GetBestAction(board,depth):
    value=-math.inf
    att=0
    valid=getLegalActions(board)
    for action in valid:
        copy_board = board.copy()
        drop_piece(copy_board, action[0],action[1],2)
        score = Value(copy_board, 1 ,-math.inf,+math.inf, depth)
        if score > value :
            value=score
            att=action[1]
    return att,value

board = create_board()
print_board(board)
print(Eval(board))
game_over = False
turn = 0

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            #print(event.pos)
            # Ask for Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True
                #print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2


    # # AI Turn
    if turn==1 and not game_over:

        col,score = GetBestAction(board,5)

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if winning_move(board, 2):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True

        
        draw_board(board)
        turn += 1
        turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
        pygame.display.quit()
        pygame.quit()

  
