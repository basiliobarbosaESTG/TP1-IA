import doctest
import random


class Board:
    """ A user-defined data structure that
        stores and manipulates dates
    """

    def __init__(self, width, height):
        """ the constructor for objects of type Board
        """
        self.data = [[' ' for i in range(width)] for j in range(height)]
        self.height = height
        self.width = width

    def __repr__(self):
        """ Returns a string representation for an object of type Board. 
        """
        s = ''  # the string to return
        for row in range(self.height):
            s += '|'    # add the spacer character
            for col in range(self.width):
                s += self.data[row][col] + '|'
            s += '\n'

        # *** You add the bottom of the board
        # and the numbers underneath here ***
        s += '-'
        for col in range(self.width):
            s += '--'
        s += '\n'
        for col in range(self.width):
            s += ' ' + str(col % 10)

        return s      # the board is complete, return it

    def addMove(self, col, xo):
        assert (xo == 'X' or xo == 'O')
        for i in range(self.height):
            if self.data[self.height-i-1][col] == ' ':
                self.data[self.height-i-1][col] = xo
                return

    def clear(self):
        self.data = [[' ' for i in range(self.width)]
                     for j in range(self.height)]

    def setBoard(self, moveString):
        """ Takes in a string of columns and places alternating 
            checkers in those columns, starting with 'X'. 
            For example, call board.setBoard('0123456') to see 'X's and 
            'O's alternate on the bottom row, or 
            board.setBoard('000000') to see them alternate in the left
            column. 
            moveString must be a string of integers. 
        """
        nextChar = 'X'    # start by playing 'X'
        for colString in moveString:
            col = int(colString)
            if 0 <= col < self.width:
                self.addMove(col, nextChar)
            if nextChar == 'X':
                nextChar = 'O'
            else:
                nextChar = 'X'

    def isMoveLegal(self, col):
        if col in range(self.width):
            if self.data[0][col] == ' ':
                return True
        return False

    def isFull(self):
        for col in range(self.width):
            if self.isMoveLegal(col):
                return False
        return True

    def deleteMove(self, col):
        for i in range(self.height):
            if self.data[i][col] == 'X' or self.data[i][col] == 'O':
                self.data[i][col] = ' '
                return

    def isHorizontalWin(self, ox):
        """ Checks for a horizontal win. 
        """
        for row in range(self.height):
            for col in range(self.width - 3):
                if (self.data[row][col] == self.data[row][col + 1] ==
                        self.data[row][col + 2] == self.data[row][col + 3] == ox):
                    return True
        return False

    def isVerticalWin(self, ox):
        """ Checks for a horizontal win. 
        """
        for col in range(self.width):
            for row in range(self.height - 3):
                if (self.data[row][col] == self.data[row+1][col] ==
                        self.data[row + 2][col] == self.data[row + 3][col] == ox):
                    return True
        return False

    def isPosSlopeDiagWin(self, ox):
        """ Checks for a horizontal win. 
        """
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.data[row + 3][col] == self.data[row + 2][col + 1] ==\
                   self.data[row + 1][col + 2] == self.data[row][col + 3] == ox:
                    return True
        return False

    def isNegSlopeDiagWin(self, ox):
        """ Checks for a horizontal win. 
        """
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                if self.data[-row - 1][-col - 1] == self.data[-row - 2][-col - 2] ==\
                   self.data[-row - 3][-col - 3] == self.data[-row - 4][-col - 4] == ox:
                    return True
        return False

    def isWinFor(self, xo):
        assert (xo == 'X' or xo == 'O')
        if self.isHorizontalWin(xo) or self.isVerticalWin(xo) or\
           self.isPosSlopeDiagWin(xo) or self.isNegSlopeDiagWin(xo):
            return True
        else:
            return False

    def hostGame(self):
        print()
        print('Welcome to Connect Four!')
        vision = int(input("How many moves can your opponent see ahead: "))
        print()
        turn = 'X'
        oppPlayer = Player('O', "RANDOM", vision)
        while True:
            print(self)
            print()
            if turn == 'X':
                col = int(input("X's choice:  "))
                self.addMove(col, 'X')
                if self.isWinFor('X'):
                    print(self)
                    print("X wins. O, eat dirt!")
                    self.clear()
                    break
                turn = 'O'
            elif turn == 'O':
                oppMove = oppPlayer.nextMove(self)
                self.addMove(oppMove, 'O')
                print('O chooses', oppMove)
                if self.isWinFor('O'):
                    print(self)
                    print("O wins. X, eat dirt!")
                    self.clear()
                    break
                turn = 'X'


def menu():
    """ Prints a menu of options. 
    """
    print("(1) Create Board ")
    print("(2) Play Game ")
    print("(3) Print Board ")
    print("(4) Add move ")
    print("(5) Delete move ")
    print("(6) Clear board ")
    print("(7) Set board ")
    print("(8) Move Legality")
    print("(9) Is Full")
    print("(10) Is Win For Player")
    print("(0) Quit")


def connect4():
    while True:
        print()
        menu()
        print()
        choice = int(input("Choose an option: "))
        print()
        if choice == 1:
            width = int(input("Choose an width (7): "))
            height = int(input("Choose an height (6): "))
            board = Board(width, height)

        elif choice == 2:
            try:
                board
            except UnboundLocalError:
                print('Please make a board first')
            else:
                board.hostGame()

        elif choice == 3:
            print(board)

        elif choice == 4:
            col = int(input("Choose an column: "))
            xo = int(input("Choose an player ('X'/'O'): "))
            board.addMove(col, xo)

        elif choice == 5:
            col = int(input("Choose an column: "))
            board.deleteMove(col)

        elif choice == 6:
            board.clear()

        elif choice == 7:
            setString = input("Enter a string representing the board state: ")
            board.setBoard(setString)

        elif choice == 8:
            col = input("Pick a column to check move validity: ")
            board.isMoveLegal(col)

        elif choice == 9:
            board.isFull()

        elif choice == 10:
            team = input("What Team ('X'/'O'): ")
            board.isWinFor(team)

        elif choice == 0:
            break
        else:
            print("That is not on the menu!")


class Player:
    """ A user-defined data structure that
        stores and manipulates dates
    """

    def __init__(self, ox, tieBreakingType, ply):
        """ the constructor for objects of type Board
        """
        assert (ox == 'X' or ox == 'O')
        assert (tieBreakingType == 'LEFT' or tieBreakingType == 'RIGHT' or
                tieBreakingType == 'RANDOM')
        assert (isinstance(ply, int) and ply < 10)
        self.ox = ox
        self.tieBreakingType = tieBreakingType
        self.ply = ply

    def __repr__(self):
        """ Creates a string representation of the Player object.
        >>> player = Player("X", "LEFT", 2)
        >>> print(player)
        Player for X
        with tiebreak type: LEFT
        and ply is 2
        >>> player = Player("O", "RANDOM", 0)
        >>> print(player)
        Player for O
        with tiebreak type: RANDOM
        and ply is 0
        """
        s = "Player for " + self.ox + "\n"
        s += "with tiebreak type: " + self.tieBreakingType + "\n"
        s += "and ply is " + str(self.ply)
        return s

    def opponentChecker(self):
        """
        >>> player = Player('X', 'LEFT', 3)
        >>> player.opponentChecker()
        'O'
        >>> Player('O', 'LEFT', 0).opponentChecker()
        'X'
        """
        if self.ox == "X":
            return 'O'
        else:
            return 'X'

    def scoreBoard(self, board):
        """ 
        >>> board = Board(7, 6)
        >>> board.setBoard('01020305')
        >>> player = Player('X', 'LEFT', 0)
        >>> player.scoreBoard(board)
        100.0
        >>> Player('O', 'LEFT', 0).scoreBoard(board)
        0.0
        >>> Player('O', 'LEFT', 0).scoreBoard(Board(7, 6))
        50.0
        """
        if board.isWinFor(self.ox):
            return 100.0
        elif board.isWinFor(self.opponentChecker()):
            return 0.0
        else:
            return 50.0

    def tiebreakMove(self, scores):
        """
        >>> scores = [0, 0, 50, 0, 50, 50, 0]
        >>> player = Player('X', 'LEFT', 1)
        >>> player2 = Player('X', 'RIGHT', 1)
        >>> player.tiebreakMove(scores)
        2
        >>> player2.tiebreakMove(scores)
        5
        """
        maxScore = max(scores)
        maxInd = []
        for i in range(len(scores)):
            if scores[i] == maxScore:
                maxInd += [i]
        if len(maxInd) < 2:
            return maxInd[0]
        else:
            if self.tieBreakingType == "LEFT":
                return maxInd[0]
            elif self.tieBreakingType == "RIGHT":
                return maxInd[-1]
            elif self.tieBreakingType == "RANDOM":
                return random.choice(maxInd)

    def scoresFor(self, board):
        # print('looking again for', self.ox, 'with', self.ply, 'moves left')
        scores = [50.0]*board.width
        for col in range(board.width):
            # print('looking at col', col, 'for player', self.ox, 'with', self.ply, 'moves left')
            if not board.isMoveLegal(col):
                scores[col] = -1.0
            else:
                board.addMove(col, self.ox)
                if board.isWinFor(self.ox):
                    scores[col] = 100.0
                # elif board.isWinFor(self.opponentChecker()):
                #     scores[col] = 0.0
                elif self.ply == 0:
                    scores[col] = 50.0
                else:
                    # if board.isWinFor(self.ox):
                    #     scores[col] = 100.0
                    # else:
                    newPlayer = Player(self.opponentChecker(),
                                       self.tieBreakingType, self.ply - 1)
                    oppScores = newPlayer.scoresFor(board)
                    # print('got scores back for', self.ox, 's opponent with', self.ply, 'moves left:', oppScores)
                    if max(oppScores) == 100:
                        scores[col] = 0.0
                    elif max(oppScores) == 0.0:
                        scores[col] = 100.0
                    else:
                        scores[col] = 50.0
                board.deleteMove(col)

        return scores

    def nextMove(self, board):
        """
        """
        scores = self.scoresFor(board)
        return self.tiebreakMove(scores)


doctest.testmod()

connect4()
