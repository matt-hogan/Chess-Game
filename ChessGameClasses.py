""" This file stores the game and move classes """


# Converts the board indexes of the rows to standard chess notation as number 1 - 8
ROWSTORANKS = ('8', '7', '6', '5', '4', '3', '2', '1')
# Converts the board indexes of the columns to standard chess notation as letters a - h
COLUMNSTOFILES = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')


# Stores information about the board and piece movement
class Game():
    def __init__(self):
        # Board list stores the location of each piece within the board
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        # Keeps track of whose turn it is
        self.whitesMove = True
        # A list of all the move in chess notation
        self.moveHistory = []
        # Sets each piece on the board to the corresponding move function
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        # WHITE KING location
        self.whiteKingLocation = (7, 4)
        # BLACK KING location
        self.blackKingLocation = (0, 4)
        # Keeps track if the king is in check and has no legal moves
        self.checkmate = False
        # Keeps track if the king is not in check and has no legal moves
        self.stalemate = False
        # Keeps track of if en passant is a possible move and the location the move would occur
        self.enPassantPossible = ()
        # Keeps track of what piece the pawn will change to. Currently, it will only change to a queen without a choice for another piece
        self.promotionChoice = 'Q'

    """ Game Update Functions """
    # The main move function takes in the move and executes it. Special cases are needed for pawn promotion, en passant, and castling
    def makeMove(self, move):
        # Represents the starting square as blank
        self.board[move.startRow][move.startColumn] = "--"
        # Moves the piece to the new square
        self.board[move.endRow][move.endColumn] = move.pieceMoved
        # Move added to moveHistory in order for it to be undone
        self.moveHistory.append(move)
        # The turn is switched to the other player
        self.whitesMove = not self.whitesMove
        # Updates white or black king location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endColumn)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endColumn)
        # Check for a pawn promotion
        if move.isPawnPromotion:
            # Changes the pawn to a new piece
            self.board[move.endRow][move.endColumn] = move.pieceMoved[0] + self.promotionChoice
        # Check for en passant move
        if move.isEnPassant:
            # Captures the pawn
            self.board[move.startRow][move.endColumn] = "--"
        # Updates where the en passant is possible if a pawn moves 2 squares
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            # Adds the location between the start and end of the pawn move to where en pasant is possible
            self.enPassantPossible = ((move.startRow + move.endRow)//2, move.startColumn)
        # En passant is no longer possible if any other move occured
        else:
            self.enPassantPossible = ()
    
    # Undoes the last move. Reverse of makeMove fx
    def undoMove(self):
        # Makes sure a move is available to be undone
        if len(self.moveHistory) != 0:
            # Removes the last move from the history list and stores it in a move variable
            move = self.moveHistory.pop()
            # Replaces the starting position with the piece
            self.board[move.startRow][move.startColumn] = move.pieceMoved
            # Replaces the captured square with the captured piece or nothing if the square was empty
            self.board[move.endRow][move.endColumn] = move.pieceCaptured
            # Switches the turn back to the other player
            self.whitesMove = not self.whitesMove
            # Updates white or black king location if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startColumn)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startColumn)
            # Checks to see if an en passant move is undone
            if move.isEnPassant:
                # Makes the ending square blank
                self.board[move.endRow][move.endColumn] = "--"
                # Sets the piece captured back to the original location
                self.board[move.startRow][move.endColumn] = move.pieceCaptured
                # Allows for the undone en passant move to be redone
                self.enPassantPossible = (move.endRow, move.endColumn)
            # Checks if the move undone made en passant possible
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                # Sets en passant to empty because it is no longer possible
                self.enPassantPossible = ()

    # Generates all legal moves
    def getValidMoves(self):
        ########################### Edit this function to make it more efficient without having to generate moves for every piece on the board #####################
        # Saves the value of enPassantPossible without changing the original value when moves are generated
        tempEnPassantPossible = self.enPassantPossible
        # Generates all possible moves
        moves = self.getAllPossibleMoves()
        # Iterates backwords through the list to remove any illegal moves without skipping
        for i in range(len(moves)-1, -1, -1):
            # Makes the the moves and switches the turn to the opposing player in the process
            self.makeMove(moves[i])
            # Switches turns back to check if the player who made the move made an illegal move
            self.whitesMove = not self.whitesMove
            if self.inCheck():
                # Removes the illegal move from the list of valid moves because the king is in check
                moves.remove(moves[i])
            # Switches turn back
            self.whitesMove = not self.whitesMove
            # Undoes the illegal move
            self.undoMove()
        # Determines if any moves are able to be made
        if len(moves) == 0:
            # Determins if the king is in check
            if self.inCheck():
                # The king is in check without any valid moves so it is checkmate
                self.checkmate = True
            else:
                # The king is not in check but doesn't have any valid moves so it is stalemate
                self.stalemate = True
        else:
            # Allows for moves to be undone after checkmate and stalemate are true
            self.checkmate = False
            self.stalemate = False

        # Returns the list of valid moves that keep the king out of check
        return moves

    # Determines if the king is in check
    def inCheck(self):
        # Checks if the white king's square is in check using the squareUnderAttack fx
        if self.whitesMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        # Checks if the black king's square is in check using the squareUnderAttack fx
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
        
    # Determines if the enemy can attack a certain location
    def squareUnderAttack(self, row, column):
        # Switches to enemy to see their possible moves
        self.whitesMove = not self.whitesMove
        # Generates opponents moves
        oppMoves = self.getAllPossibleMoves()
        # Switches turn back
        self.whitesMove = not self.whitesMove
        # See if any of the opponents moves attack the particular location
        for move in oppMoves:
            # Checks to see if any of the moves end on the particular row and column
            if move.endRow == row and move.endColumn == column:
                # The particular row and column are under attack
                return True
        # The location is not under attack
        return False

    # Generates every move possible on the board both legal and illegal (king in check)
    def getAllPossibleMoves(self):
        moves = []
        # Iterates through all squares on the board
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                # Determines what color is at that space on the board
                turn = self.board[row][column][0]
                # Validates that the correct color was picked for each players turn
                if (turn == 'w' and self.whitesMove) or (turn == 'b' and not self.whitesMove):
                    # Determines what piece is at that space on the board
                    piece = self.board[row][column][1]
                    # Calls the correct generate moves function depending on which piece is at the current location
                    self.moveFunctions[piece](row, column, moves)
        # Returns list of every possible move as an object of the Move class
        return moves

    """ Piece Move Functions """
    # Get all of the possible moves for the PAWN at the specific location
    def getPawnMoves(self, row, column, moves):
        # Sets variables for the white pawns' moves
        if self.whitesMove:
            moveAmount = -1
            startingRow = 6
            endingRow = 0
            enemyColor = 'b'
        # Sets variables for the black pawns' moves
        else:
            moveAmount = 1
            startingRow = 1
            endingRow = 7
            enemyColor = 'w'
        # Keeps track of is pawn promotion is possible
        pawnPromotion = False

        # Checks to see if the white pawn can move one square forward
        if self.board[row+moveAmount][column] == "--":
            # Checks if the pawn is on the ending row where pawn promotion is possible
            if row+moveAmount == endingRow:
                pawnPromotion = True
            # Adds the possible move to moves list
            moves.append(Move((row, column), (row+moveAmount, column), self.board, isPawnPromotion=pawnPromotion))
            # Checks to see if the pawn is at the starting row and can move two squares forward
            if row == startingRow and self.board[row+moveAmount*2][column] == "--":
                # Adds the possible move to moves list
                moves.append(Move((row, column), (row+moveAmount*2, column), self.board))
        # Checks to see it is possible to capture a piece to the LEFT without going off the board
        if column - 1 >= 0:
            # Checks to see if a piece is able to be captures
            if self.board[row+moveAmount][column-1][0] == enemyColor:
                # Checks if the pawn is on the ending row where pawn promotion is possible
                if row+moveAmount == endingRow:
                    pawnPromotion = True
                moves.append(Move((row, column), (row+moveAmount, column-1), self.board, isPawnPromotion=pawnPromotion))
            # Checks if an en passant move is possible to be made
            elif (row+moveAmount, column-1) == self.enPassantPossible:
                moves.append(Move((row, column), (row+moveAmount, column-1), self.board, isEnPassant=True))
        # Checks to see it is possible to capture a piece to the RIGHT without going off the board
        if column + 1 <= 7:
            # Checks to see if a piece is able to be captures
            if self.board[row+moveAmount][column+1][0] == enemyColor:
                # Checks if the pawn is on the ending row where pawn promotion is possible
                if row+moveAmount == endingRow:
                    pawnPromotion = True
                moves.append(Move((row, column), (row+moveAmount, column+1), self.board, isPawnPromotion=pawnPromotion))
            # Checks if an en passant move is possible to be made
            elif (row+moveAmount, column+1) == self.enPassantPossible:
                moves.append(Move((row, column), (row+moveAmount, column+1), self.board, isEnPassant=True))

    # Get all of the possible moves for the ROOK at the specific location
    def getRookMoves(self, row, column, moves):
        # Possible directions a rook can move (up, left, down, right)
        directionMoves = ((-1, 0), (0, -1), (1, 0), (0, 1))
        # Specifies what piece can be captured
        enemyColor = 'b' if self.whitesMove else 'w'
        # Iterate through all possible directions the rook can move
        for d in directionMoves:
            # Iterate through maximum squares it can move
            for i in range(1, 8):
                # Possible space that the rook can move in a particular direction
                endRow = row + d[0] * i
                endColumn = column + d[1] * i
                # Makes sure the piece stays on the board
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    # Determins what piece is at the end square
                    endPiece = self.board[endRow][endColumn]
                    # Checks to see if the square is empty and adds the move to moves list
                    if endPiece == "--":
                         moves.append(Move((row, column), (endRow, endColumn), self.board))
                    # Checks to see if the square has an enemy in it to be captured and adds the move to moves list
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                        #The piece cannot go any further past the enemy and the next direction is checked
                        break
                    # The piece is on its cxolored piece and the move is not valid
                    else:
                        # Check in a new direction if one is avialble to check
                        break
                # The piece is off the board and the move is not valid
                else:
                    # Check in a new direction if one is avialble to check
                    break

    # Get all of the possible moves for the KNIGHT at the specific location
    def getKnightMoves(self, row, column, moves):
        # Possible movement directions a knight can move
        directionMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        # Specifies what piece can be captured
        enemyColor = 'b' if self.whitesMove else 'w'
        # Iterates through all the possible directions the knight can move
        for d in directionMoves:
            # Possible space the knight in a particular direction
            endRow = row + d[0]
            endColumn = column + d[1]
            # Makes sure the piece stays on the board
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                # Determins what piece is at the end square
                endPiece = self.board[endRow][endColumn]
                # Checks to see if the knight can move to that square and adds the move to move list
                if endPiece[0] == enemyColor or endPiece == "--":
                    moves.append(Move((row, column), (endRow, endColumn), self.board))

    # Get all of the possible moves for the BISHOP at the specific location
    def getBishopMoves(self, row, column, moves):
        # Similar to the moves of rooks but the directions are diagonals instead of vertical and horizontal
        # Possible directions a bishop can move (up left, up right, down left, down right)
        directionMoves = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        # Specifies what piece can be captured
        enemyColor = 'b' if self.whitesMove else 'w'
        # Iterate through all possible directions the bishop can move
        for d in directionMoves:
            # Iterate through maximum squares it can move
            for i in range(1, 8):
                # Possible space that the bishop can move in a particular direction
                endRow = row + d[0] * i
                endColumn = column + d[1] * i
                # Makes sure the piece stays on the board
                if 0 <= endRow < 8 and 0 <= endColumn < 8:
                    # Determins what piece is a the end square
                    endPiece = self.board[endRow][endColumn]
                    # Checks to see if the square is empty and adds the move to moves list
                    if endPiece == "--":
                         moves.append(Move((row, column), (endRow, endColumn), self.board))
                    # Checks to see if the square has an enemy in it to be captured and adds the move to moves list
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((row, column), (endRow, endColumn), self.board))
                        #The piece cannot go any further past the enemy and the next direction is checked
                        break
                    # The piece is on its colored piece and the move is not valid
                    else:
                        # Check in a new direction if one is avialble to check
                        break
                # The piece is off the board and the move is not valid
                else:
                    # Check in a new direction if one is avialble to check
                    break

    # Get all of the possible moves for the QUEEN at the specific location
    def getQueenMoves(self, row, column, moves):
        # Combination of both the rook and bishop moves
        self.getRookMoves(row, column, moves)
        self.getBishopMoves(row, column, moves)

    # Get all of the possible moves for the KING at the specific location
    def getKingMoves(self, row, column, moves):
        # Similiar to the movement of the knight except directionMoves are different
        # Possible movement directions a king can move
        directionMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        # Specifies what piece can be captured
        enemyColor = 'b' if self.whitesMove else 'w'
        # Iterates through all the possible directions the king can move
        for d in directionMoves:
            # Possible space the king moves in a particular direction
            endRow = row + d[0]
            endColumn = column + d[1]
            # Makes sure the piece stays on the board
            if 0 <= endRow < 8 and 0 <= endColumn < 8:
                # Determins what piece is at the end square
                endPiece = self.board[endRow][endColumn]
                # Checks to see if the king can move to that square and adds the move to move list
                if endPiece[0] == enemyColor or endPiece == "--":
                    moves.append(Move((row, column), (endRow, endColumn), self.board))


# Stores information about the move being made
class Move():
    def __init__(self, startSquare, endSquare, board, isEnPassant=False, isPawnPromotion=False):
        # Location of where a piece starts as index for board
        self.startRow = startSquare[0]
        self.startColumn = startSquare[1]
        # Location of where a piece ends as index for board
        self.endRow = endSquare[0]
        self.endColumn = endSquare[1]
        # What piece was at the start location
        self.pieceMoved = board[self.startRow][self.startColumn]
        # What piece was at the end location or if no piece was there
        self.pieceCaptured = board[self.endRow][self.endColumn]
        # Gives each move a unique number storing each start and end location on the board as its own digit
        self.moveID = self.startRow * 1000 + self.startColumn * 100 + self.endRow * 10 + self.endColumn
        
        # Keeps track of if a pawn is changing to a different piece or not
        self.isPawnPromotion = isPawnPromotion
        
        # Keeps track of if en passant move is possible or not
        self.isEnPassant = isEnPassant
        if self.isEnPassant:
            # Sets the piece captured to the enemy pawn instead of the empty square it moves to
            self.pieceCaptured = "wP" if self.pieceMoved == "bP" else "bP"

    # Allows for objects in Move class to be compared and the moves validated
    def __eq__(self, other):
        # Makes sure the items compared are objects of the Move class
        if isinstance(other, Move):
            # Compares two objects with each other to determine if they are equal or not
            return self.moveID == other.moveID
        return False

    # Determines move in chess notation
    def getChessNotation(self):
        # Returns a string of the move
        ######################### Add notation to determine what happened during move ######################
        return self.getRankFile(self.startRow, self.startColumn) + self.getRankFile(self.endRow, self.endColumn)

    # Converts to rank file notation from the row and column notation used in board list
    def getRankFile(self, row, column):
        # Returns a string of the conversion ie "a1", "b3", "c6"
        return self.COLUMNSTOFILES[column] + self.ROWSTORANKS[row]