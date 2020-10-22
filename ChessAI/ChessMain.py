# Main driver file. It is responsible for handling user input and displaying current game state.

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

#Initialize a global dicitonary of images, this will be called in main

def load_images():
    pieces = ['wP', 'wN', 'wB', 'wK', 'wQ', 'wR',
    'bP', 'bN', 'bB', 'bK', 'bQ', 'bR']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

#Main driver for our code handles user input and updating graphics

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made

    load_images()
    running = True
    sqSelected = () #keeps track of the last click of the user
    playerClicks = [] #keeps track of player clicks
    while(running):
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #clicking
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #x and y location of mousezx
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col): #clicking the same square cancels
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: 
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            print(validMoves[i].getChessNotation())
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = () #reset user click 
                            playerClicks = []
                    if not moveMade:
                        print('Invalid Move')
                        sqSelected = ()
                        playerClicks = []
            #key press
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True

            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False

        draw_gamestate(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def draw_gamestate(screen, gs):
    draw_board(screen) #draws squares on the board
    draw_pieces(screen, gs.board)

#top left square is white, draw squares on the board
def draw_board(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c ) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#draw the pieces on top of the board
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != ("--"): #not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()