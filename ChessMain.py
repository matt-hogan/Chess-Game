# INF360 - Programming in Python
# Matthew Hogan
# Midterm Project

"""
This is a multiplayer chess game using pygame. It goes by normal chess rules but some have yet to be implemented.
The pieces are moved by clicking on the piece and then clicking again on where the piece should move to.
The white pieces have the first turn. The games goes until a checkmate or a stalemate occurs.
Pressing 'R' will reset the game once the game is over or at any point throughout the game.
Pressing 'Z' will undo the last move made. Any number of moves can be undone.
Pressing 'X' on the keyboard or in the upper right corner will close the window.


The game is still missing a few rules that will come in the final version. Moves that still need implementing are castling 
and being able to choose which piece will replace a pawn from pawn promotion. A menu at the beginning of the game will display 
a play button to start the game, a how to play button, and an options button to change who goes first and other gameplay settings.
Adding a time is another option for the user. A menu at the end of the game will also allow the user to easily play again 
or exit. Currently, the game is not resizable and may cause issues depending on the screen size. More rules for ending the 
game need to be implemented like inssuffiecent materials. The function that looks for check could also be changed to be more 
effiecient without have to run through every possible move on the board for both players. The option to play against an AI 
is another addition if I can implement it.
"""

from ChessGameClasses import *
import os
import sys
import pygame
######## Must install pygame using pip install ########

# Allows pygame to be used throughout ChessMain.py
pygame.init()

""" Constant Variables """
# Display dimensions for the pygame window
DISPLAYWIDTH = 768
DISPLAYHEIGHT = 768

# Number of squares in columns and rows
SQUARES = 8
# Height/width of individual squares as an integer
SQUARESIZE = DISPLAYHEIGHT // SQUARES

# Frames per second
FPS = 30

# Image dictionary holding piece name as the key and piece image as the value
IMAGES = {}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGRAY = (232, 235, 239)
DARKGRAY = (125, 135, 150)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CYAN = (0, 255 ,255)


# Inputs piece images into IMAGES dictionary
def loadImages():
    # Adds piece images to dictionary as value and piece name as key
    path = "IMG\\Pieces\\"
    for filename in os.listdir(path):
        # Resizes images to fit in squares before inputting
        IMAGES[os.path.splitext(filename)[0]] = pygame.transform.scale(pygame.image.load(os.path.join(path, filename)), (SQUARESIZE, SQUARESIZE))


# Main game function for updating the screen and controlling user input
def main():
    # Initializes pygame window to specific height and width defined
    screen = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
    # Sets window title
    pygame.display.set_caption("Chess")
    # Sets window image
    pygame.display.set_icon(pygame.image.load('IMG\\icon.png'))
    # Initializes clock function in pygame
    clock = pygame.time.Clock()
    # Sets background of screen to white
    screen.fill(WHITE)
    # Game class from ChessGameClasses.py
    g = Game()
    # List of valid moves to compare with move made by the user
    validMoves = g.getValidMoves()
    # Identifies if a move was made so a new list of valid moves can be generated
    moveMade = False
    # Keeps track of when a move should be animated
    animate = False
    # Keeps track of when the game is over
    gameOver = False
    # Keeps track of the square clicked as tuple of row and column
    squareSelected = ()
    # Keeps track of where a piece starts and where it moves to as list of squareSelected
    playerClicks = []

    # Call of load image function before while loop to set piece images once
    loadImages()

    # Main loop for game to run in
    while True:
        # Checks the user input
        for event in pygame.event.get():
            # Allows for X to close the window
            if event.type == pygame.QUIT:
                sys.exit(0)
            # Checks if mouse is clicked
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Checks to make sure the moves can still be made
                if not gameOver:
                    # Coordinates of the mouse click
                    location = pygame.mouse.get_pos()
                    # Determines which square was clicked
                    column = location[0]//SQUARESIZE
                    row = location[1]//SQUARESIZE
                    # Checks to see if a different square was clicked 
                    if squareSelected != (row, column):
                        squareSelected = (row, column)
                        # Appends both first and second click to playerCLicks
                        playerClicks.append(squareSelected)
                    # Moves the piece if a unique second click was made
                    if len(playerClicks) == 2:
                        # Tells what the move was
                        move = Move(playerClicks[0], playerClicks[1], g.board)
                        # Makes sure a valid move is made
                        for i in range(len(validMoves)):
                            # Move class equality operator is used to compare objects of the Move class
                            if move == validMoves[i]:
                                # The move is made
                                g.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                # Resets clicks allowing for another move to be made
                                squareSelected = ()
                                playerClicks = []
                        if not moveMade:
                            # Selects a new piece if an invalid move was made
                            playerClicks = [squareSelected]
                            animate = False
            # Checks if a key is pressed
            elif event.type == pygame.KEYDOWN:
                # Checks if the 'x' key is pressed
                if event.key == pygame.K_x:
                    # Closes the window
                    sys.exit(0)
                # Checks if the 'z' key is pressed 
                elif event.key == pygame.K_z:
                    # The move is undone
                    g.undoMove()
                    # Allows for new moves to be generated
                    moveMade = True
                    gameOver = False
                # Checks if 'r' key is pressed
                elif event.key == pygame.K_r:
                    # Resets game back to starting values
                    g = Game()
                    validMoves = g.getValidMoves()
                    squareSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

        # After a move occurs
        if moveMade:
            if animate:
                # Animates the previous move made
                animateMove(g.moveHistory[-1], screen, g, clock)
            # Generates a new set of valid moves
            validMoves = g.getValidMoves()
            moveMade = False
            animate = False

        # Draws board and pieces
        drawScreen(screen, g, validMoves, squareSelected)

        # Checks if the game has ended
        if g.checkmate:
            # Ends the game and prints out the winner
            gameOver = True
            drawText(screen, g, " Black Wins " if g.whitesMove else " White Wins ", DISPLAYHEIGHT // 12, DISPLAYWIDTH // 2, DISPLAYHEIGHT // 2, WHITE if g.whitesMove else BLACK, backgroundColor=BLACK if g.whitesMove else WHITE)
        elif g.stalemate:
            # Ends the game and prints out stalemate
            gameOver = True
            drawText(screen, g, " Stalemate ", DISPLAYHEIGHT // 12, DISPLAYWIDTH // 2, DISPLAYHEIGHT // 2, WHITE if g.whitesMove else BLACK, backgroundColor=BLACK if g.whitesMove else WHITE)
        # Maximum amount of frames displayed every second
        clock.tick(FPS)
        # Updates screen
        pygame.display.update()


""" Display Functions """
# Draws graphics on the screen
def drawScreen(screen, g, validMoves, squareSelected):
    # Draw the squares on the board
    drawBoard(screen)
    # Highlights squares of the piece selected with possible moves
    highlightSquares(screen, g, validMoves, squareSelected)
    # Draws the ranks and files on the board
    drawRankFiles(screen, g)
    # Draws the pieces on top of the squares
    drawPieces(screen, g.board)

# Draws squares on the board
def drawBoard(screen):
    # Iterates through every square on the board
    for row in range(SQUARES):
        for column in range(SQUARES):
            # Draws the squares evenly throughout the screen switching between colors on odd and even squares
            pygame.draw.rect(screen, boardSquareColor(row, column), pygame.Rect(column * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE))

# Draws pieces on the board using current game
def drawPieces(screen, board):
    # Iterates through every square on the board
    for row in range(SQUARES):
        for column in range(SQUARES):
            # Sets which piece to draw corresponding to where it is in board list
            piece = board[row][column]
            # Draws the piece in the corresponding square if it is not empty
            if piece != "--":
                screen.blit(IMAGES[piece], pygame.Rect(column * SQUARESIZE, row * SQUARESIZE, SQUARESIZE, SQUARESIZE))

# Draws the numbers and letters on the board
def drawRankFiles(screen, g):
    # Iterates through every square on the board
    for row in range(SQUARES):
        for column in range(SQUARES):
            if column == 0:
                # Calls the drawText to draw the ranks with the opposite color of the square in the upper left corner
                drawText(screen, g, ROWSTORANKS[row], SQUARESIZE // 4, int(column * SQUARESIZE + SQUARESIZE // 12), int(row * SQUARESIZE + SQUARESIZE // 8), boardSquareColor(row, column, reverse=True))
            if row == 0:
                # Calls the drawText to draw the files with the opposite color of the square in the upper right corner
                drawText(screen, g, COLUMNSTOFILES[column], SQUARESIZE // 4, int(column * SQUARESIZE + SQUARESIZE // 1.11), int(row * SQUARESIZE + SQUARESIZE // 8), boardSquareColor(row, column, reverse=True))

# Highlights the squares selected, possible moves, pervious move, and king in check
def highlightSquares(screen, g, validMoves, squareSelected):
    # Initializes highlight layer on the board
    highlight = pygame.Surface((SQUARESIZE, SQUARESIZE))
    # Sets the transparency value
    highlight.set_alpha(125)
    # Checks to see if a king is in check
    if g.inCheck():
        # Highlights the king's square red
        highlight.fill(RED)
        screen.blit(highlight, (g.whiteKingLocation[1]*SQUARESIZE if g.whitesMove else g.blackKingLocation[1]*SQUARESIZE, g.whiteKingLocation[0]*SQUARESIZE if g.whitesMove else g.blackKingLocation[0]*SQUARESIZE))
    # Checks if move has been made
    if len(g.moveHistory) != 0:
        # Uses move history to find last move and highlight those squares
        highlight.fill(CYAN)
        screen.blit(highlight, (g.moveHistory[-1].endColumn*SQUARESIZE, g.moveHistory[-1].endRow*SQUARESIZE))
        screen.blit(highlight, (g.moveHistory[-1].startColumn*SQUARESIZE, g.moveHistory[-1].startRow*SQUARESIZE))
    # Makes sure a piece is selected
    if squareSelected != ():
        row, column = squareSelected
        # Makes sure the correct color piece is selcted depending on whose turn it is
        if g.board[row][column][0] == ('w' if g.whitesMove else 'b'):
            # Checks to see if the selected square is the king in check
            if g.inCheck and row == g.whiteKingLocation[0] if g.whitesMove else g.blackKingLocation[0] and column == g.whiteKingLocation[1] if g.whitesMove else g.blackKingLocation[1]:
                # Replaces the red check square with the normal gray square in order to be highlighted yellow
                highlight.set_alpha(255)
                highlight.fill(boardSquareColor(row, column))
                screen.blit(highlight, (column*SQUARESIZE, row*SQUARESIZE))
                highlight.set_alpha(125)
            # Color of the highlighted square
            highlight.fill(YELLOW)
            # Draws the highlight of the selected square onto the board
            screen.blit(highlight, (column*SQUARESIZE, row*SQUARESIZE))
            # Goes through all the moves 
            for move in validMoves:
                # Checks for the moves starting on the selected square
                if move.startRow == row and move.startColumn == column:
                    # Checks if either blue square is a possible move
                    if len(g.moveHistory) != 0 and ((g.moveHistory[-1].endColumn, g.moveHistory[-1].endRow) == (move.endColumn, move.endRow) or (g.moveHistory[-1].startColumn, g.moveHistory[-1].startRow) == (move.endColumn, move.endRow)):
                        # Replaces that square with the normal gray square in order to be highlighted green
                        highlight.set_alpha(255)
                        highlight.fill(boardSquareColor(move.endRow, move.endColumn))
                        screen.blit(highlight, (move.endColumn*SQUARESIZE, move.endRow*SQUARESIZE))
                        highlight.set_alpha(125)
                    # Color of the move squares
                    highlight.fill(GREEN)
                    # Draws the highlight of possible moves onto the board
                    screen.blit(highlight, (move.endColumn*SQUARESIZE, move.endRow*SQUARESIZE))

# Animates the piece moving to its new square
def animateMove(move, screen, g, clock):
    # Change in rows and columns
    deltaRow = move.endRow - move.startRow
    deltaColumn = move.endColumn - move.startColumn
    # Controls animation speed. The lower the number the faster the animation
    framesPerSquare = 7 if (abs(deltaRow) + abs(deltaColumn)) < 5 else 5
    # Number of frames for a given animation
    frameCount = (abs(deltaRow) + abs(deltaColumn)) * framesPerSquare
    # Iterates through each frame in animation
    for frame in range(frameCount + 1):
        # Sets the location the piece should be at a specific frame
        x, y = ((move.startRow + deltaRow*frame/frameCount, move.startColumn + deltaColumn*frame/frameCount))
        # Updates the board with piece already moved
        drawBoard(screen)
        drawPieces(screen, g.board)
        # Erases piece at ending square by drawing over its location with a new square
        color = [LIGHTGRAY, DARKGRAY][(move.endRow + move.endColumn) % 2]
        endSquare = pygame.Rect(move.endColumn*SQUARESIZE, move.endRow*SQUARESIZE, SQUARESIZE, SQUARESIZE)
        pygame.draw.rect(screen, color, endSquare)
        # Draws ranks and files so they do not disappear during the animation
        drawRankFiles(screen, g)
        # Checks to see if the end square was not empty
        if move.pieceCaptured != "--":
            # Checks to see if the move is an en passant move
            if not move.isEnPassant:
                # Draws the piece at the ending square
                screen.blit(IMAGES[move.pieceCaptured], endSquare)
            else:
                # Moves the captured piece to its original square to be removed
                endSquare = pygame.Rect(move.endColumn*SQUARESIZE, (move.endRow + 1 if move.pieceMoved == 'wP' else move.endRow - 1)*SQUARESIZE, SQUARESIZE, SQUARESIZE)
                screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Displays moved piece at current frame in animation
        screen.blit(IMAGES[move.pieceMoved], pygame.Rect(int(y*SQUARESIZE), int(x*SQUARESIZE), SQUARESIZE, SQUARESIZE))
        # Displays animation on screen
        pygame.display.update()
        # Controls frame rate of animation
        clock.tick(60)

# Print text onto the screen
def drawText(screen, g, text, textSize, x, y, textColor, backgroundColor=None):
    # Initializes font
    font = pygame.font.SysFont("Arial", textSize, )
    # Adds text and color
    textObject = font.render(text, True, textColor, backgroundColor)
    # Places text at the specified location
    textRect = textObject.get_rect()
    textRect.center = (x, y)
    # Displays text onto the screen
    screen.blit(textObject, textRect)

#Returns the color of a board's square depending on the location
def boardSquareColor(row, column, reverse=False):
    if reverse:
        return [DARKGRAY, LIGHTGRAY][((row + column) % 2)]
    return [LIGHTGRAY, DARKGRAY][((row + column) % 2)]



# Allows the file to be imported without running the main function
if __name__ == "__main__":
    main()