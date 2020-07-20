""" This file stores the app class which is the driver class for the program """

import sys
import logging
import os

# Import Constants.py
try:
    from Constants import *
    logging.debug("Constants.py imported successfully")
except:
    logging.critical("Missing Constants.py")
    logging.critical("Program closing...")
    sys.exit(0)

# Import GameClasses.py
try:
    from GameClasses import *
    logging.debug("GameClasses.py imported successfully")
except:
    logging.critical("Missing GameClasses.py")
    logging.critical("Program closing...")
    sys.exit(0)

# Import pygame
try:
    # Disables starting pygame output
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame
    logging.debug("pygame imported successfully")
except:
    logging.critical("Missing pygame")
    logging.critical("Program closing...")
    sys.exit(0)

# Import of chess font
if os.path.isfile("Fonts\\ChrysanthiUnicodeRegular-KEzo.ttf"):
    logging.debug("ChrysanthiUnicodeRegular-KEzo.ttf imported successfully")
else:
    logging.debug("ChrysanthiUnicodeRegular-KEzo.ttf unable to be imported")


class App:
    def __init__(self):
        # Allows pygame to be used
        pygame.init()
        # Display dimensions for the pygame window
        self.displaySize = (768, 768)
        # Height/width of individual squares as an integer
        self.squareSize = self.displaySize[0] // SQUARES
        # Keeps track of what screen should be displayed
        self.state = "start"
        # Image dictionary holding piece name as the key and piece image as the value
        self.images = {}
        # Stores the button name as key and the rect as value for the current screen
        self.buttonDict = {}
        # Keeps track of whose the first move it is
        self.whiteFirstMove = True
        # Keeps track of whether to display the help menu
        self.help = False
        # Keeps track of if the piece images have been imported successfully
        self.pieceImport = False
        # Initializes pygame window to specific height and width defined
        self.screen = pygame.display.set_mode(self.displaySize)
        # Sets window title
        pygame.display.set_caption("Chess")
        # Sets window image
        try:
            pygame.display.set_icon(pygame.image.load(os.path.join('IMG', 'icon.png')))
            logging.debug("icon.png imported successfully")
        except:
            logging.debug("icon.png unable to be imported")
        # Initializes clock function in pygame
        self.clock = pygame.time.Clock()
        # Calls reset function to set starting variable values
        self.reset()

    # Resets variables to starting values
    def reset(self):
        # Game class from ChessGameClasses.py
        self.g = Game()
        # Sets the players first move to the correct options
        self.g.whitesMove = self.whiteFirstMove
        # List of valid moves to compare with move made by the user
        self.validMoves = self.g.getValidMoves()
        # Identifies if a move was made so a new list of valid moves can be generated
        self.moveMade = False
        # Keeps track of when a move should be animated
        self.animate = False
        # Keeps track of when the game is over
        self.gameOver = False
        # Keeps track of the square clicked as tuple of row and column
        self.squareSelected = ()
        # Keeps track of where a piece starts and where it moves to as list of squareSelected
        self.playerClicks = []

    # Main program function where other functions are called from
    def run(self):
        while True:
            # Checks the user input
            for event in pygame.event.get():
                # Allows for X to close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                # Checks if left mouse click is made
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Coordinates of the mouse click
                    mouse = event.pos
                    # Iterates through all the buttons to see if one was clicked
                    for key, value in self.buttonDict.items():
                        # Checks if the mouse click was at the location of a button
                        if value.collidepoint(mouse):
                            # Checks to see what option was clicked and changes the state depending on the choice
                            if self.state == "start":
                                if key == "Play":
                                    self.state = "play"
                                elif key == "How to Play":
                                    self.state = "how"
                                elif key == "Options":
                                    self.state = "options"
                                elif key == "Quit":
                                    pygame.quit()
                                    sys.exit(0)
                            # Checks to see what option was clicked and changes the state depending on the choice
                            elif self.state == "how":
                                if key == "←":
                                    self.state = "start"
                            # Checks to see what option was clicked and changes the state depending on the choice
                            elif self.state == "options":
                                if key == "←":
                                    self.state = "start"
                                elif key == "Screen Resolution":
                                    self.state = "resolution"
                                elif key == "First Move":
                                    self.state = "first"
                            # Checks to see what option was clicked and changes the resolution depending on the choice
                            elif self.state == "resolution":
                                if key == "←":
                                    self.state = "options"
                                elif key == "512 x 512":
                                    self.displaySize = (512, 512)
                                    self.squareSize = self.displaySize[0] // SQUARES
                                    self.screen = pygame.display.set_mode(self.displaySize)
                                elif key == "768 x 768":
                                    self.displaySize = (768, 768)
                                    self.squareSize = self.displaySize[0] // SQUARES
                                    self.screen = pygame.display.set_mode(self.displaySize)
                                elif key == "1024 x 1024":
                                    self.displaySize = (1024, 1024)
                                    self.squareSize = self.displaySize[0] // SQUARES
                                    self.screen = pygame.display.set_mode(self.displaySize)
                            # Checks to see what color was clicked and changes the first move depending on the choice
                            elif self.state == "first":
                                if key == "←":
                                    self.state = "options"
                                elif key == "♔" or key == "White":
                                    self.whiteFirstMove = True
                                    self.reset()
                                elif key == "♚"or key == "Black":
                                    self.whiteFirstMove = False
                                    self.reset()
                                    
            # Calls the corresponding function to change the screen based on the current state
            if self.state == "start":
                self.drawStartMenu()
            elif self.state == "how":
                self.drawHowToPlay()
            elif self.state == "play":
                self.play()
            elif self.state == "options":
                self.drawOptionsMenu()
            elif self.state == "resolution":
                self.drawResolutions()
            elif self.state == "first":
                self.drawFirstMove()
            
            # Maximum amount of frames displayed every second
            self.clock.tick(FPS)
            # Updates screen
            pygame.display.flip()

    # Draws start menu
    def drawStartMenu(self):
        self.drawBaseMenu(LIGHTGRAY, title=True, titleText="CHESS", titleSize=self.displaySize[0] // 7, titleColor=MENUGRAY, titleLocation=(self.displaySize[0] // 2, self.displaySize[0] // 5))
        # Draws king pieces by title if font exists
        if os.path.isfile("Fonts\\ChrysanthiUnicodeRegular-KEzo.ttf"):
            self.drawText("♚", self.displaySize[0] // 7, MENUGRAY, center=(self.displaySize[0] * 3 // 16, self.displaySize[0] * 3 // 16), fontName="Fonts\\ChrysanthiUnicodeRegular-KEzo.ttf", sFont=False)
            self.drawText("♚", self.displaySize[0] // 7, MENUGRAY, center=(self.displaySize[0] * 13 // 16, self.displaySize[0] * 3 // 16), fontName="Fonts\\ChrysanthiUnicodeRegular-KEzo.ttf", sFont=False)
        # Draws buttons to click
        self.drawText(" Play ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 3 // 8) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)
        self.drawText(" How to Play ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] // 2) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)
        self.drawText(" Options ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 5 // 8) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)
        self.drawText(" Quit ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 6 // 8) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)

    # Draws the how to play screen
    def drawHowToPlay(self):
        self.drawBaseMenu(LIGHTGRAY, back=True, backSize=self.displaySize[0] // 8, backColor=MENUGRAY, backLocation=(self.displaySize[0] // 20, self.displaySize[0] // 24))
        # Draws how to play text
        self.drawText("This is a multiplayer chess game that goes by normal chess rules. The pieces are moved by clicking on the piece and then clicking again on where the piece should move to. The white pieces have the first turn unless changed in the options. The games will continue until a checkmate or a stalemate occurs. Some helpful keyboard shortcuts are listed below:", 
                      self.displaySize[0] // 32, MENUGRAY, rect=(self.displaySize[0] // 10, self.displaySize[0] // 10, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] - self.displaySize[0] // 10 * 2))
        # Draws keyboard shortcuts
        self.drawText("H - Displays a help menu during the game with these tips", 
                      self.displaySize[0] // 36, MENUGRAY, rect=(self.displaySize[0] // 10, self.displaySize[0] * 6 // 16, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))
        self.drawText("Z - Undoes the last move made and any number of moves can be undone", 
                      self.displaySize[0] // 36, MENUGRAY, rect=(self.displaySize[0] // 10, self.displaySize[0] * 7 // 16, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))
        self.drawText("R - Resets the game during any point throughout the game", 
                      self.displaySize[0] // 36, MENUGRAY, rect=(self.displaySize[0] // 10, self.displaySize[0] * 8 // 16, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))
        self.drawText("M - Resets the game and returns you back to the main menu", 
                      self.displaySize[0] // 36, MENUGRAY, rect=(self.displaySize[0] // 10, self.displaySize[0] * 9 // 16, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))
        self.drawText("X - Closes the window", 
                      self.displaySize[0] // 36, MENUGRAY, rect=(self.displaySize[0] // 10, self.displaySize[0] * 10 // 16, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))

    # Draws main options menu
    def drawOptionsMenu(self):
        self.drawBaseMenu(LIGHTGRAY, title=True, titleText="Options", titleSize=self.displaySize[0] // 8, titleColor=MENUGRAY, titleLocation=(self.displaySize[0] // 2, self.displaySize[0] // 5), back=True, backSize=self.displaySize[0] // 8, backColor=MENUGRAY, backLocation=(self.displaySize[0] // 20, self.displaySize[0] // 24))
        # Draws options
        self.drawText(" Screen Resolution ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 3 // 8) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)
        self.drawText(" First Move ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 4 // 8) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)

    # Draw screen resolutions menu
    def drawResolutions(self):
        self.drawBaseMenu(LIGHTGRAY, title=True, titleText="Screen Resolution", titleSize=self.displaySize[0] // 10, titleColor=MENUGRAY, titleLocation=(self.displaySize[0] // 2, self.displaySize[0] // 5), back=True, backSize=self.displaySize[0] // 8, backColor=MENUGRAY, backLocation=(self.displaySize[0] // 20, self.displaySize[0] // 24))
        # Draws resolution options
        self.drawText(" 512 x 512 ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 3 // 8) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)
        self.drawText(" 768 x 768 ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] // 2) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)
        self.drawText(" 1024 x 1024 ", self.displaySize[0] // 12, LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 5 // 8) + (self.displaySize[0] // 16)), backgroundColor=MENUGRAY, isButton=True)

    # Draw first move option menu
    def drawFirstMove(self):
        self.drawBaseMenu(LIGHTGRAY, title=True, titleText="First Move", titleSize=self.displaySize[0] // 8, titleColor=MENUGRAY, titleLocation=(self.displaySize[0] // 2, self.displaySize[0] // 4), back=True, backSize=self.displaySize[0] // 8, backColor=MENUGRAY, backLocation=(self.displaySize[0] // 20, self.displaySize[0] // 24))
        # Draws button for who to go first with piece if font exists else with just the color
        try:
            self.drawText(" ♔ ", self.displaySize[0] // 6, WHITE, center=(self.displaySize[0] * 5 // 16, (self.displaySize[0] // 2) + (self.displaySize[0] // 16)), backgroundColor=GREEN if self.whiteFirstMove else RED, isButton=True, fontName="Fonts\\ChrysanthiUnicodeRegular-KEzo.ttf", sFont=False)
            self.drawText(" ♚ ", self.displaySize[0] // 6, BLACK, center=(self.displaySize[0] * 11 // 16, (self.displaySize[0] // 2) + (self.displaySize[0] // 16)), backgroundColor=GREEN if not self.whiteFirstMove else RED, isButton=True, fontName="Fonts\\ChrysanthiUnicodeRegular-KEzo.ttf", sFont=False)
        except:
            self.drawText(" White ", self.displaySize[0] // 10, WHITE, center=(self.displaySize[0] // 2, (self.displaySize[0] * 7 // 16) + (self.displaySize[0] // 16)), backgroundColor=GREEN if self.whiteFirstMove else RED, isButton=True)
            self.drawText(" Black ", self.displaySize[0] // 10, BLACK, center=(self.displaySize[0] // 2, (self.displaySize[0] * 10 // 16) + (self.displaySize[0] // 16)), backgroundColor=GREEN if not self.whiteFirstMove else RED, isButton=True)

    # Draws the basic structure of a menu
    def drawBaseMenu(self, backgroundColor, title=False, titleText=None, titleSize=None, titleColor=None, titleBackgroundColor=None, titleLocation=None, back=False, backSize=None, backColor=None, backLocation=None, backgroundOpacity=255):
        # Clears button dictionary
        self.buttonDict = {}
        # Draws background
        self.drawHightlight(backgroundColor, backgroundOpacity, (0,0), self.displaySize)
        if back:
            # Draws back button
            self.drawText("←", backSize, backColor, center=backLocation, isButton=True)
        if title:
            # Draws title
            self.drawText(titleText, titleSize, titleColor, center=titleLocation,  backgroundColor=titleBackgroundColor)

    # Main function that controls the chess game itself
    def play(self):
        # Call of load image function before while loop to set piece images once
        self.loadImages()
        # Keeps tracks of if game should be displayed
        playRunning = True
        # Main loop for game to run in
        while playRunning:
            # Checks the user input
            for event in pygame.event.get():
                # Allows for X to close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                # Checks if left mouse click is made
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Coordinates of the mouse click
                    mouse = event.pos
                    # Checks if the help menu is displayed
                    if self.help:
                        # Checks if outside the help text is clicked
                        if not pygame.Rect(self.displaySize[0] // 12, int(self.displaySize[0] * 5.5 // 24), self.displaySize[0] - self.displaySize[0] // 12 * 2, self.displaySize[0] * 13 // 24).collidepoint(mouse):
                            # Closes the help screen
                            self.help = False
                    # Checks to make sure the moves can still be made
                    if not self.gameOver and not self.help:
                        # Determines which square was clicked
                        column = mouse[0]//self.squareSize
                        row = mouse[1]//self.squareSize
                        # Checks to see if a different square was clicked 
                        if self.squareSelected != (row, column):
                            self.squareSelected = (row, column)
                            # Appends both first and second click to playerCLicks
                            self.playerClicks.append(self.squareSelected)
                        else:
                            # Deselects the selected square if it is clicked again
                            self.squareSelected = ()
                            self.playerClicks = []
                        # Moves the piece if a unique second click was made
                        if len(self.playerClicks) == 2:
                            # Tells what the move was
                            move = Move(self.playerClicks[0], self.playerClicks[1], self.g.board)
                            # Makes sure a valid move is made
                            for i in range(len(self.validMoves)):
                                # Move class equality operator is used to compare objects of the Move class
                                if move == self.validMoves[i]:
                                    # The move is made
                                    self.g.makeMove(self.validMoves[i])
                                    self.moveMade = True
                                    self.animate = True
                                    # Resets clicks allowing for another move to be made
                                    self.squareSelected = ()
                                    self.playerClicks = []
                            if not self.moveMade:
                                # Selects a new piece if an invalid move was made
                                self.playerClicks = [self.squareSelected]
                                self.animate = False
                    # Checks to see if a button was clicked once the game finished
                    else:
                        # Iterates through all the buttons to see if one was clicked
                        for key, value in self.buttonDict.items():
                            # Checks if the mouse click was at the location of a button
                            if value.collidepoint(mouse):
                                if key == "Play Again":
                                    self.reset()
                                elif key == "Main Menu":
                                    self.reset()
                                    playRunning = False
                                    self.state = "start"
                # Checks if a key is pressed
                elif event.type == pygame.KEYDOWN:
                    # Checks if the 'x' key is pressed
                    if event.key == pygame.K_x:
                        # Closes the window
                        pygame.quit()
                        sys.exit(0)
                    # Checks if the help menu is not displayed
                    if not self.help:
                        # Checks if the 'z' key is pressed 
                        if event.key == pygame.K_z:
                            # The move is undone
                            self.g.undoMove()
                            # Allows for new moves to be generated
                            self.moveMade = True
                            self.gameOver = False
                        # Checks if 'r' key is pressed
                        elif event.key == pygame.K_r:
                            # Resets game back to starting values
                            self.reset()
                        # Checks if 'm' key is pressed
                        elif event.key == pygame.K_m:
                            # Resets the board and returns to start screen
                            self.reset()
                            playRunning = False
                            self.state = "start"
                    # Checks if the game has ended
                    if not self.gameOver:
                        # Checks if 'h' key is pressed
                        if event.key == pygame.K_h:
                            self.help = not self.help

            # After a move occurs
            if self.moveMade:
                if self.animate:
                    # Animates the previous move made
                    self.animateMove(self.g.moveHistory[-1])
                # Generates a new set of valid moves
                self.validMoves = self.g.getValidMoves()
                self.moveMade = False
                self.animate = False

            # Draws board and pieces
            self.drawPlayScreen()

            # Checks if the game has ended
            if self.g.checkmate:
                # Ends the game and prints out the winner
                self.gameOver = True
                self.drawGameOver(" Black Wins " if self.g.whitesMove else " White Wins ")
            elif self.g.stalemate:
                # Ends the game and prints out stalemate
                self.gameOver = True
                self.drawGameOver(" Stalemate ")

            # Checks if help menu should be displayed
            if self.help:
                # Displays a help menu
                self.drawHelp()

            # Maximum amount of frames displayed every second
            self.clock.tick(FPS)
            # Updates screen
            pygame.display.flip()

    # Inputs piece images into IMAGES dictionary
    def loadImages(self):
        try:
            # Adds piece images to dictionary as value and piece name as key
            path = os.path.join('IMG','Pieces')
            for filename in os.listdir(path):
                # Resizes images to fit in squares before inputting
                self.images[os.path.splitext(filename)[0]] = pygame.transform.scale(pygame.image.load(os.path.join(path, filename)), (self.squareSize, self.squareSize))
            if len(self.images) < 12:
                logging.critical("Piece images missing")
                logging.critical("Program closing...")
                pygame.quit()
                sys.exit(0)
        except:
            logging.critical("Piece images unable to import")
            logging.critical("Program closing...")
            pygame.quit()
            sys.exit(0)

    #Returns the color of a board's square depending on the location
    @staticmethod
    def boardSquareColor(row, column, reverse=False):
        if reverse:
            return [DARKGRAY, LIGHTGRAY][((row + column) % 2)]
        return [LIGHTGRAY, DARKGRAY][((row + column) % 2)]


    """ Display Functions """
    # Print text onto the screen
    def drawText(self, text, textSize, textColor, center=(), backgroundColor=None, fontName="Consolas", sFont=True, isButton=False, rect=None):
        # Initializes font
        font = pygame.font.SysFont(fontName, textSize) if sFont else pygame.font.Font(fontName, textSize)
        
        # Draws a single line of text centered at the position
        if not rect:
            # Renders text and colors
            textObject = font.render(text, True, textColor, backgroundColor)
            # Places text at the specified location
            textRect = textObject.get_rect()
            textRect.center = center
            # Displays text onto the screen
            self.screen.blit(textObject, textRect)
        # Draws text on multiple line within a given area left aligned
        else:
            textRect = pygame.Rect(rect)
            # Coordinates for the beginning of the text
            y = textRect.top
            # Spaces between lines outputted
            lineSpacing = -2
            # Gets the height in pixels of the font
            fontHeight = font.size(fontName)[1]
            
            while text:
                i = 1
                # Determines the maximum width of the line of text
                while font.size(text[:i])[0] < textRect.width and i < len(text):
                    i += 1

                # Checks if the text has been wrapped
                if i < len(text):
                    # Adjusts the text wrapping to the last word
                    i = text.rfind(" ", 0, i) + 1

                # Renders text and colors
                textObject = font.render(text[:i], True, textColor, backgroundColor)
                # Displays the line of text on screen
                self.screen.blit(textObject, (textRect.left, y))
                # Moves to the next line
                y += fontHeight + lineSpacing
                #Removes the text already displayed
                text = text[i:]

        # Checks if the text drawn is a button
        if isButton:
            # Adds the button name as key and rect as value to button dictionary
            self.buttonDict[text.strip()] = textRect

    # Draws graphics on the screen
    def drawPlayScreen(self):
        # Draw the squares on the board
        self.drawBoard()
        # Highlights squares of the piece selected with possible moves
        self.highlightSquares()
        # Draws the ranks and files on the board
        self.drawRankFiles()
        # Draws the pieces on top of the squares
        self.drawPieces()

    # Draws squares on the board
    def drawBoard(self):
        # Iterates through every square on the board
        for row in range(SQUARES):
            for column in range(SQUARES):
                # Draws the squares evenly throughout the screen switching between colors on odd and even squares
                pygame.draw.rect(self.screen, self.boardSquareColor(row, column), pygame.Rect(column * self.squareSize, row * self.squareSize, self.squareSize, self.squareSize))

    # Draws pieces on the board using current game
    def drawPieces(self):
        try:
            # Iterates through every square on the board
            for row in range(SQUARES):
                for column in range(SQUARES):
                    # Sets which piece to draw corresponding to where it is in board list
                    piece = self.g.board[row][column]
                    # Draws the piece in the corresponding square if it is not empty
                    if piece != "--":
                        self.screen.blit(self.images[piece], pygame.Rect(column * self.squareSize, row * self.squareSize, self.squareSize, self.squareSize))
            # Logs the pieces successully imported on the fx's first call
            if not self.pieceImport:
                logging.debug("Piece images imported successfuly")
                self.pieceImport = True
        except:
            logging.critical("Piece images unable to import")
            logging.critical("Program closing...")
            pygame.quit()
            sys.exit(0)

    # Draws the numbers and letters on the board
    def drawRankFiles(self):
        # Iterates through every square on the board
        for row in range(SQUARES):
            for column in range(SQUARES):
                if column == 0:
                    # Calls the drawText to draw the ranks with the opposite color of the square in the upper left corner
                    self.drawText(ROWSTORANKS[row], self.squareSize // 4, self.boardSquareColor(row, column, reverse=True), center=(int(column * self.squareSize + self.squareSize // 12), int(row * self.squareSize + self.squareSize // 8)))
                if row == 0:
                    # Calls the drawText to draw the files with the opposite color of the square in the upper right corner
                    self.drawText(COLUMNSTOFILES[column], self.squareSize // 4, self.boardSquareColor(row, column, reverse=True), center=(int(column * self.squareSize + self.squareSize // 1.11), int(row * self.squareSize + self.squareSize // 8)))

    # Draws the game over menu 
    def drawGameOver(self, winnerText):
        self.drawBaseMenu(BLACK, backgroundOpacity=100, title=True, titleText=winnerText, titleSize=self.displaySize[0] // 12, titleColor=WHITE if self.g.whitesMove else BLACK, titleBackgroundColor=BLACK if self.g.whitesMove else WHITE, titleLocation=(self.displaySize[0] // 2, self.displaySize[0] * 5 // 16))
        # Draws the game over buttons
        self.drawText(" Play Again ", self.displaySize[0] // 14, MENUGRAY if self.g.whitesMove else LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 7 // 16) + (self.displaySize[0] // 16)), backgroundColor=LIGHTGRAY if self.g.whitesMove else MENUGRAY, isButton=True)
        self.drawText(" Main Menu ", self.displaySize[0] // 14, MENUGRAY if self.g.whitesMove else LIGHTGRAY, center=(self.displaySize[0] // 2, (self.displaySize[0] * 9 // 16) + (self.displaySize[0] // 16)), backgroundColor=LIGHTGRAY if self.g.whitesMove else MENUGRAY, isButton=True)

    # Draws the help screen over top the board
    def drawHelp(self):
        self.drawHightlight(BLACK, 100, (0,0), self.displaySize)
        self.drawHightlight(LIGHTGRAY, 255, (self.displaySize[0] // 12, int(self.displaySize[0] * 5.5 // 24)), (self.displaySize[0] - self.displaySize[0] // 12 * 2, self.displaySize[0] * 13 // 24))
        self.drawText("H - Closes this help screen", self.displaySize[0] // 24, MENUGRAY, 
                      rect=(self.displaySize[0] // 10, self.displaySize[0] * 6 // 24, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))
        self.drawText("Z - Undoes the last move made and any number of moves can be undone", self.displaySize[0] // 24, MENUGRAY, 
                      rect=(self.displaySize[0] // 10, self.displaySize[0] * 8 // 24, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))
        self.drawText("R - Resets the game during any point throughout the game", self.displaySize[0] // 24, MENUGRAY, 
                      rect=(self.displaySize[0] // 10, self.displaySize[0] * 11 // 24, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))
        self.drawText("M - Resets the game and returns you back to the main menu", self.displaySize[0] // 24, MENUGRAY, 
                      rect=(self.displaySize[0] // 10, self.displaySize[0] * 14 // 24, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))
        self.drawText("X - Closes the window", self.displaySize[0] // 24, MENUGRAY, 
                      rect=(self.displaySize[0] // 10, self.displaySize[0] * 17 // 24, self.displaySize[0] - self.displaySize[0] // 10 * 2, self.displaySize[0] * 1 // 16))

    # Highlights the squares selected, possible moves, previous move, and king in check
    def highlightSquares(self):
        # Checks to see if a king is in check
        if self.g.inCheck():
            # Highlights the king's square red
            self.drawHightlight(RED, 125, (self.g.whiteKingLocation[1]*self.squareSize if self.g.whitesMove else self.g.blackKingLocation[1]*self.squareSize, self.g.whiteKingLocation[0]*self.squareSize if self.g.whitesMove else self.g.blackKingLocation[0]*self.squareSize), (self.squareSize, self.squareSize))
        # Checks if move has been made
        if len(self.g.moveHistory) != 0:
            # Uses move history to find last move and highlight those squares
            self.drawHightlight(CYAN, 125, (self.g.moveHistory[-1].endColumn*self.squareSize, self.g.moveHistory[-1].endRow*self.squareSize), (self.squareSize, self.squareSize))
            self.drawHightlight(CYAN, 125, (self.g.moveHistory[-1].startColumn*self.squareSize, self.g.moveHistory[-1].startRow*self.squareSize), (self.squareSize, self.squareSize))
        # Makes sure a piece is selected
        if self.squareSelected != ():
            row, column = self.squareSelected
            # Makes sure the correct color piece is selcted depending on whose turn it is
            if self.g.board[row][column][0] == ('w' if self.g.whitesMove else 'b'):
                # Checks to see if the selected square is the king in check
                if self.g.inCheck and row == self.g.whiteKingLocation[0] if self.g.whitesMove else self.g.blackKingLocation[0] and column == self.g.whiteKingLocation[1] if self.g.whitesMove else self.g.blackKingLocation[1]:
                    # Replaces the red check square with the normal gray square in order to be highlighted yellow
                    self.drawHightlight(self.boardSquareColor(row, column), 255, (column*self.squareSize, row*self.squareSize), (self.squareSize, self.squareSize))
                # highlights the selected square on the board
                self.drawHightlight(YELLOW, 125, (column*self.squareSize, row*self.squareSize), (self.squareSize, self.squareSize))
                # Goes through all the moves 
                for move in self.validMoves:
                    # Checks for the moves starting on the selected square
                    if move.startRow == row and move.startColumn == column:
                        # Checks if either blue square is a possible move
                        if len(self.g.moveHistory) != 0 and ((self.g.moveHistory[-1].endColumn, self.g.moveHistory[-1].endRow) == (move.endColumn, move.endRow) or (self.g.moveHistory[-1].startColumn, self.g.moveHistory[-1].startRow) == (move.endColumn, move.endRow)):
                            # Replaces that square with the normal gray square in order to be highlighted green
                            self.drawHightlight(self.boardSquareColor(move.endRow, move.endColumn), 255, (move.endColumn*self.squareSize, move.endRow*self.squareSize), (self.squareSize, self.squareSize))
                        # Draw the possible moves onto the board
                        self.drawHightlight(GREEN, 125, (move.endColumn*self.squareSize, move.endRow*self.squareSize), (self.squareSize, self.squareSize))

    # Draws a colored highlight at a specific location
    def drawHightlight(self, color, opacity, location, surfaceSize):
        # Initializes highlight layer on the board
        highlight = pygame.Surface(surfaceSize)
        # Sets the transparency value
        highlight.set_alpha(opacity)
        # Color of the highlighted square
        highlight.fill(color)
        # Draws the highlight onto the board at at the location
        self.screen.blit(highlight, location)

    # Animates the piece moving to its new square
    def animateMove(self, move):
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
            self.drawBoard()
            self.drawPieces()
            # Erases piece at ending square by drawing over its location with a new square
            endSquare = pygame.Rect(move.endColumn*self.squareSize, move.endRow*self.squareSize, self.squareSize, self.squareSize)
            pygame.draw.rect(self.screen, self.boardSquareColor(move.endRow, move.endColumn), endSquare)
            # Checks to see if a move is a castle move
            if move.isCastle:
                # Checks to see if the move was to the king or queen's side and sets the distances the rook is located from the king accordingly
                if move.endColumn - move.startColumn == 2:
                    endRook = -1
                    startRook = 1
                else:
                    endRook = 1
                    startRook = -2
                # Draws over the ending square of the rook with an empty square
                pygame.draw.rect(self.screen, self.boardSquareColor(move.endRow, move.endColumn+endRook), pygame.Rect((move.endColumn+endRook)*self.squareSize, (move.endRow)*self.squareSize, self.squareSize, self.squareSize))
                # Draws the rook its starting location
                self.screen.blit(self.images["wR" if move.pieceMoved[0] == 'w' else "bR"], pygame.Rect((move.endColumn+startRook)*self.squareSize, (move.endRow)*self.squareSize, self.squareSize, self.squareSize))
            # Draws ranks and files so they do not disappear during the animation
            self.drawRankFiles()
            # Checks to see if the end square was not empty
            if move.pieceCaptured != "--":
                # Checks to see if the move is an en passant move
                if move.isEnPassant:
                    # Moves the captured piece to its original square to be removed
                    endSquare = pygame.Rect(move.endColumn*self.squareSize, (move.endRow + 1 if move.pieceMoved == 'wP' else move.endRow - 1)*self.squareSize, self.squareSize, self.squareSize)
                    self.screen.blit(self.images[move.pieceCaptured], endSquare)
                else:
                    # Draws the piece at the ending square
                    self.screen.blit(self.images[move.pieceCaptured], endSquare)
            # Displays moved piece at current frame in animation
            self.screen.blit(self.images[move.pieceMoved], pygame.Rect(int(y*self.squareSize), int(x*self.squareSize), self.squareSize, self.squareSize))
            # Displays animation on screen
            pygame.display.update()
            # Controls frame rate of animation
            self.clock.tick(60)