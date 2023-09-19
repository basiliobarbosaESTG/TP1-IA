class Board:
    """ a datatype representing a C4 board
    with an arbitrary number of rows and cols """

    def __init__(self, width, height):
        """ the constructor for objects of type Board """
        self.width = width
        self.height = height
        W = self.width
        H = self.height
        self.data = [[' ']*W for row in range(H)]

        # we do not need to return inside a constructor!

    def __repr__(self):
        """ this method returns a string representation
            for an object of type Board
        """
        H = self.height
        W = self.width
        s = ''   # the string to return
        for row in range(0, H):
            s += '|'
            for col in range(0, W):
                s += self.data[row][col] + '|'
            s += '\n'

        s += (2*W+1) * '-'    # bottom of the board
        s += '\n'
        num = 0
        for col in range(0, W):
            s += ' ' + str(num % 10)
            num += 1

        return s       # the board is complete, return it

    def addMove(self, col, ox):
        """ the first input col represents the index of the column to which the checker will be added; the second input ox will be a 1-character string representing the checker to add to the board """
        H = self.height
        W = self.width
        D = self.data
        for row in range(0, H):
            if D[row][col] != ' ':
                D[row-1][col] = ox
                return
        D[H-1][col] = ox

    def clear(self):
        """ clears the board """
        H = self.height
        W = self.width
        for row in range(0, H):
            for col in range(0, W):
                self.data[row][col] = ' '

    def setBoard(self, moveString):
        """ takes in a string of columns and places
            alternating checkers in those columns,
            starting with 'X'

            For example, call b.setBoard('012345')
            to see 'X's and 'O's alternate on the
            bottom row, or b.setBoard('000000') to
            see them alternate in the left column.
            moveString must be a string of integers
        """
        nextCh = 'X'   # start by playing 'X'
        for colString in moveString:
            col = int(colString)
            if 0 <= col <= self.width:
                self.addMove(col, nextCh)
            if nextCh == 'X':
                nextCh = 'O'
            else:
                nextCh = 'X'

    def allowsMove(self, c):
        """ returns True if the calling object does allow a move into column c and False if c is not a legal calling object or if it is full """
        H = self.height
        W = self.width
        if W < c and c < 0:
            return False
        elif self.data[0][c] != ' ':
            return False
        else:
            return True

    def isFull(self):
        """ returns True if the calling object is completely full of checkers and False otherwise """
        H = self.height
        W = self.width
        D = self.data
        for row in range(0, H):
            for col in range(0, W):
                if self.allowsMove(col) == True:
                    return False
        else:
            return True

    def delMove(self, col):
        """ removes the top checker from column c. if the column is emply, delMove does nothing """
        H = self.height
        W = self.width
        D = self.data
        for row in range(0, H):
            if D[row][col] != ' ':
                D[row][col] = ' '
                return

    def winsFor(self, ox):
        """ takes in the character and returns True if there are four of the type on the board and false otherwise """
        H = self.height
        W = self.width
        D = self.data
        # check for horizontal wins
        for row in range(0, H):
            for col in range(0, W-3):
                if D[row][col] == ox and \
                   D[row][col+1] == ox and \
                   D[row][col+2] == ox and \
                   D[row][col+3] == ox:
                    return True
        for row in range(0, H-3):
            for col in range(0, W):
                if D[row][col] == ox and \
                   D[row+1][col] == ox and \
                   D[row+2][col] == ox and \
                   D[row+3][col] == ox:
                    return True
        for row in range(0, H-3):
            for col in range(0, W-3):
                if D[row][col] == ox and \
                   D[row+1][col+1] == ox and \
                   D[row+2][col+2] == ox and \
                   D[row+3][col+3] == ox:
                    return True
        for row in range(0, H-3):
            for col in range(2, W):
                if D[row][col] == ox and \
                   D[row+1][col-1] == ox and \
                   D[row+2][col-2] == ox and \
                   D[row+3][col-3] == ox:
                    return True
        return False

    def playGame(self, px, po):
        print("Welcome to Connect Four!")
        while True:
            if px == 'human':
                userX_col = input("X's Choice: ")
                while self.allowsMove(userX_col) == False:
                    userX_col = input("Choose another column please: ")
                self.addMove(userX_col, 'X')
                print(self)
            elif px != 'human':
                userX_col = px.nextMove(b)
                self.addMove(userX_col, 'X')
                print(self)
            if self.isFull() == True:
                break
            if self.winsFor('X') == True:
                print(self)
                print("X wins!")
                break
            else:
                print(self)

            if po == 'human':
                userO_col = input("O's Choice: ")
                while self.allowsMove(userO_col) == False:
                    userO_col = input("Choose another column please: ")
                self.addMove(userO_col, 'O')
                print(self)
            elif po != 'human':
                userO_col = po.nextMove(b)
                self.addMove(userO_col, 'O')
                print(self)
            if self.isFull() == True:
                break
            if self.winsFor('O') == True:
                print(self)
                print("O wins!")
                break
            else:
                print(self)


class Player:
    """ an AI player for Connect Four """

    def __init__(self, ox, tbt, ply):
        """ the constructor """
        self.ox = ox
        self.tbt = tbt
        self.ply = ply

    def __repr__(self):
        """ creates an appropriate string """
        s = "Player for " + self.ox + "\n"
        s += "  with tiebreak type: " + self.tbt + "\n"
        s += "  and ply == " + str(self.ply) + "\n\n"
        return s

    def oppCh(self):
        """ returns the other kind of playing piece """
        if self.ox == 'X':
            return 'O'
        else:
            return 'X'

    def scoreBoard(self, b):
        """ returns a single float value representing the score of the input b. 100 if b is a win for self, 50 if neither win nor loss, and 0 if a loss for self """
        if b.winsFor(self.ox) == True:
            return 100.0
        elif b.winsFor(self.oppCh()) == True:
            return 0.0
        else:
            return 50.0

    def tiebreakMove(self, scores):
        """ takes in scores and if there is only one highest, returns the column number in that scores list. if there is more than one, it returns the column number of the highest score appropriate to the player's tbt """
        import random
        maxIndicies = []
        best = max(scores)
        for i in range(len(scores)):
            if scores[i] == max(scores):
                maxIndicies += [i]
        if len(maxIndicies) == 1:
            return maxIndicies[0]
        elif self.tbt == 'LEFT':
            return maxIndicies[0]
        elif self.tbt == 'RIGHT':
            return maxIndicies[-1]
        elif self.tbt == 'RANDOM':
            return random.choice(maxIndicies)

    def scoresFor(self, b):
        """ returns a list of scores, with the cth score representing the "goodness" of teh input board after the player moves to column c. """
        scores = [50]*b.width
        for col in range(b.width):
            if b.allowsMove(col) == False:
                scores[col] = -1.0
            elif b.winsFor(self.ox) == True:
                scores[col] = 100.0
            elif b.winsFor(self.oppCh()) == True:
                scores[col] = 0.0
            elif self.ply == 0:
                scores[col] = 50.0
            else:
                b.addMove(col, self.ox)
                op = Player(self.oppCh(), self.tbt, self.ply-1)
                oppscore = op.scoresFor(b)
                opmove = op.tiebreakMove(oppscore)
                scores[col] = 100-max(oppscore)
                b.delMove(col)
        return scores

    def nextMove(self, b):
        """ returns next move """
        scores = self.scoresFor(b)
        return self.tiebreakMove(scores)
