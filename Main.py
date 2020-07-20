# INF360 - Programming in Python
# Matthew Hogan
# Midterm Project

######## Must install pygame using pip install pygame ########
######## Using version 1.9.6 ########


"""
This is a multiplayer chess game that goes by normal chess rules. The pieces are moved by clicking on the piece and then clicking 
again on where the piece should move to. The white pieces have the first turn unless changed in the options. The games will continue 
until a checkmate or a stalemate occurs. Some helpful keyboard shortcuts are listed below:
H - Displays a help menu during the game with these tips
Z - Undoes the last move made and any number of moves can be undone
R - Resets the game during any point throughout the game
M - Resets the game and returns you back to the main menu
X - Closes the window
"""

import sys
import logging
logging.basicConfig(filename="GameLog.txt", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Import AppClass.py
try:
    from AppClass import *
    logging.debug("AppClass.py imported successfully")
except:
    logging.critical("Missing AppClass.py")
    logging.critical("Program closing...")
    sys.exit(0)


if __name__ == "__main__":
    App().run()