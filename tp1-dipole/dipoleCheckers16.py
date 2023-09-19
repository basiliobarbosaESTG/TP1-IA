import copy


class DipoleBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_row = None
        self.black_row = None
        self.turn = 'white'
        self.state = None
        self.initialize_board()

    def initialize_board(self):
        # Initialize the board with 2 stacks of 12 white and 12 black pieces
        for i in range(12):
            self.board[0][i] = 'W'
            self.board[7][i] = 'B'
        for i in range(12, 24):
            self.board[0][i] = None
            self.board[7][i] = None

    def set_starting_rows(self):
        # Set the starting rows for white and black pieces chosen by user input
        while True:
            try:
                white_row = int(
                    input('Enter the starting row number for white pieces (0-5): '))
                black_row = int(
                    input('Enter the starting row number for black pieces (2-7): '))
                if white_row < 0 or white_row > 5 or black_row < 2 or black_row > 7:
                    print('Invalid row numbers. Try again.')
                elif white_row >= black_row - 2 and white_row <= black_row + 2:
                    print('Rows are too close to each other. Try again.')
                else:
                    self.white_row = white_row
                    self.black_row = black_row
                    break
            except ValueError:
                print('Invalid input. Try again.')

    def print_board(self):
        # Print the current state of the board
        print('  0 1 2 3 4 5 6 7')
        for i in range(8):
            row_str = str(i) + ' '
            for j in range(8):
                if self.board[i][j] is None:
                    row_str += '-'
                else:
                    row_str += self.board[i][j]
                row_str += ' '
            print(row_str)

    def get_valid_moves(self, row, col):
        # Get a list of valid moves for the given stack
        stack_size = 0
        valid_moves = []
        for i in range(row, 8):
            if self.board[i][col] is None:
                break
            stack_size += 1
        if stack_size == 0:
            return valid_moves

        # Non-capturing moves
        if row > 0:
            if self.board[row-1][col] is None:
                valid_moves.append((row-1, col, stack_size))
            if col > 0 and self.board[row-1][col-1] is None:
                valid_moves.append((row-1, col-1, stack_size))
            if col < 7 and self.board[row-1][col+1] is None:
                valid_moves.append((row-1, col+1, stack_size))
        if col > 0 and self.board[row][col-1] is None:
            valid_moves.append((row, col-1, stack_size))
        if col < 7 and self.board[row][col+1] is None:
            valid_moves.append((row, col+1, stack_size))
        if row < 7:
            if self.board[row+1][col] is None:
                valid_moves.append((row+1, col, stack_size))
            if col > 0 and self.board[row+1][col-1] is None:
                valid_moves.append((row+1, col-1, stack_size))
        if col < 7 and self.board[row+1][col+1] is None:
            valid_moves.append((row+1, col+1, stack_size))

        # Capturing moves
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r = row + dr
                c = col + dc
                captured_stacks = []
                while r >= 0 and r < 8 and c >= 0 and c < 8 and len(captured_stacks) < stack_size:
                    if self.board[r][c] is None:
                        break
                    if self.board[r][c] != self.turn[0]:
                        captured_stacks.append((r, c))
                    r += dr
                    c += dc
                if r >= 0 and r < 8 and c >= 0 and c < 8 and len(captured_stacks) == stack_size:
                    valid_moves.append((r, c, stack_size, captured_stacks))

        return valid_moves

    def make_move(self, start_row, start_col, end_row, end_col, size, captured_stacks=None):
        # Make a move on the board
        self.board[start_row][start_col] = None
        for i in range(size):
            self.board[end_row][end_col] = self.turn[0]
            end_row += end_row - start_row
            end_col += end_col - start_col
        if captured_stacks is not None:
            for r, c in captured_stacks:
                self.board[r][c] = None

    def get_opponent_turn(self):
        # Get the color of the opponent
        return 'black' if self.turn == 'white' else 'white'

    def get_game_state(self):
        # Check if the game is over
        white_stacks = 0
        black_stacks = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'W':
                    white_stacks += 1
                elif self.board[i][j] == 'B':
                    black_stacks += 1
        if white_stacks == 0:
            self.state = 'Lose'
        elif black_stacks == 0:
            self.state = 'Win'

    def play(self):
        # Play the game
        self.set_starting_rows()
        self.print_board()
        while True:
            print(f"It's {self.turn}'s turn.")
            while True:
                try:
                    start_row = int(
                        input('Enter the starting row of the stack you want to move: '))
                    start_col = int(
                        input('Enter the starting column of the stack you want to move: '))
                    if self.board[start_row][start_col] is None:
                        print('There is no stack there. Try again.')
                    elif self.board[start_row][start_col] != self.turn[0]:
                        print("You can't move the opponent's stack. Try again.")
                    else:
                        break
                except ValueError:
                    print('Invalid input. Try again.')
            valid_moves = self.get_valid_moves(start_row, start_col)
            if len(valid_moves) == 0:
                print('There are no valid moves for that stack. Try again.')
                continue
            print('Valid moves:')
            for i, move in enumerate(valid_moves):
                row, col, size = move[:3]
                print(
                    f'{i+1}. Move {size} checker(s from ({start_row}, {start_col}) to ({row}, {col})')
            while True:
                try:
                    move_num = int(
                        input('Enter the number of the move you want to make: '))
                    if move_num < 1 or move_num > len(valid_moves):
                        print('Invalid move number. Try again.')
                    else:
                        break
                except ValueError:
                    print('Invalid input. Try again.')
                    move = valid_moves[move_num-1]
                    end_row, end_col, size = move[:3]
                    captured_stacks = move[3] if len(move) > 3 else None
                    self.make_move(start_row, start_col, end_row,
                                   end_col, size, captured_stacks)
                    self.print_board()
                    self.turn = self.get_opponent_turn()
                    self.get_game_state()
                    if self.state is not None:
                        print(f'{self.turn} wins!')
                    break
