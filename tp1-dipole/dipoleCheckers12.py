class Dipole:
    def __init__(self, white_start_row, black_start_row):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.white_start_row = white_start_row
        self.black_start_row = black_start_row
        self.white_pieces = 12
        self.black_pieces = 12
        self.turn = 'W'

        # Place the starting pieces on the board
        for i in range(8):
            if i == white_start_row:
                for j in range(8):
                    if j % 2 != white_start_row % 2 and self.white_pieces > 0:
                        self.board[i][j] = 'W'
                        self.white_pieces -= 1
            elif i == black_start_row:
                for j in range(8):
                    if j % 2 == black_start_row % 2 and self.black_pieces > 0:
                        self.board[i][j] = 'B'
                        self.black_pieces -= 1

    def check_win(self):
        # define the check_win method
        # ...
        if self.white_pieces == 0:
            return 'W'
        elif self.black_pieces == 0:
            return 'B'
        else:
            return None
        return win_state

    def print_board(self):
        print('   0 1 2 3 4 5 6 7')
        for i in range(8):
            print(f'{i}  ', end='')
            for j in range(8):
                print(f'{self.board[i][j]} ', end='')
            print()

    def make_move(self, start_row, start_col, end_row, end_col):
        if self.turn == 'W' and self.board[start_row][start_col] != 'W':
            print('Invalid move: You can only move white pieces on this turn.')
            return False
        elif self.turn == 'B' and self.board[start_row][start_col] != 'B':
            print('Invalid move: You can only move black pieces on this turn.')
            return False

        stack_size = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == self.board[start_row][start_col]:
                    stack_size += 1

        if abs(end_row - start_row) > stack_size or abs(end_col - start_col) > stack_size:
            print(
                f'Invalid move: The number of squares moved must equal the size of the stack ({stack_size}).')
            return False

        direction_row = 0
        direction_col = 0
        if end_row > start_row:
            direction_row = 1
        elif end_row < start_row:
            direction_row = -1
        if end_col > start_col:
            direction_col = 1
        elif end_col < start_col:
            direction_col = -1

        captured = False
        for i in range(stack_size):
            row = start_row + i*direction_row
            col = start_col + i*direction_col
            if row == end_row and col == end_col:
                if self.board[row][col] != ' ':
                    print('Invalid move: You cannot move onto another stack of pieces.')
                    return False
                else:
                    self.board[row][col] = self.board[start_row][start_col]
                    self.board[start_row][start_col] = ' '
                break
            elif self.board[row][col] != ' ':
                if self.board[row][col] == self.board[start_row][start_col]:
                    print('Invalid move: You cannot move onto another stack of pieces.')
                    return False
                elif abs(i) == stack_size - 1 and len(self.get_stack(row, col)) <= stack_size:
                    captured = True
                    break
                else:
                    print(
                        'Invalid move: You can only capture an enemy stack that is smaller than or equal to your own stack.')
                return False

        if captured:
            self.capture_stack(start_row, start_col, end_row, end_col)

        if self.turn == 'W':
            self.turn = 'B'
        else:
            self.turn = 'W'

        return True


def get_stack(self, row, col):
    stack = []
    for i in range(8):
        for j in range(8):
            if i == row and j == col:
                stack.append(self.board[i][j])
            elif abs(i-row) == abs(j-col):
                stack.append(self.board[i][j])
    return stack


def capture_stack(self, start_row, start_col, end_row, end_col):
    stack = self.get_stack(start_row, start_col)
    for i in range(len(stack)):
        row = start_row + i*(end_row - start_row)
        col = start_col + i*(end_col - start_col)
        if row == end_row and col == end_col:
            self.board[row][col] = stack[i]
        else:
            self.board[row][col] = ' '
            if stack[i] == 'W':
                self.white_pieces -= 1
            else:
                self.black_pieces -= 1


def check_win(self):
    if self.white_pieces == 0:
        return 'W'
    elif self.black_pieces == 0:
        return 'B'
    else:
        return None


white_start_row = int(input('Enter starting row for white pieces (0-7): '))
black_start_row = int(input('Enter starting row for black pieces (0-7): '))
game = Dipole(white_start_row, black_start_row)

while True:
    game.print_board()
    win_state = game.check_win()
    if win_state == 'W':
        print('White wins!')
        break
    elif win_state == 'B':
        print('Black wins!')
    break

print(f'{game.turn}\'s turn')

start_row = int(input('Enter starting row: '))
start_col = int(input('Enter starting col: '))
end_row = int(input('Enter ending row: '))
end_col = int(input('Enter ending col: '))

game.make_move(start_row, start_col, end_row, end_col)

# To play the game, simply run the script and follow the prompts to enter the starting rows for the white and black pieces, as well as your moves during the game. The board will be printed after each move, and the game will end when one player has captured all of their opponent's pieces.
