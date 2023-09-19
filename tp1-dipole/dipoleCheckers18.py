import random


class DipoleBoard:
    def __init__(self, white_start_row, black_start_row):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_start_row = white_start_row
        self.black_start_row = black_start_row
        self.turn = 'white'
        self.game_state = None
        self.white_captured = 0
        self.black_captured = 0
        self.white_stacks = [[(self.white_start_row, col)] for col in range(8)]
        self.black_stacks = [[(self.black_start_row, col)] for col in range(8)]

        for row in range(8):
            for col in range(8):
                if row == self.white_start_row and col % 2 == 0:
                    self.board[row][col] = 'W'
                elif row == self.black_start_row and col % 2 == 1:
                    self.board[row][col] = 'B'

    def play(self):
        print("Welcome to Dipole! The objective of the game is to remove all of your opponent's checkers from the board.\n")
        print("To move a stack, enter its starting row and column and its ending row and column, separated by spaces.")
        print("For example, to move a stack from (2, 3) to (3, 3), enter '2 3 3 3'.")
        print("If you want to move a portion of a stack, enter the starting and ending coordinates for that portion, separated by a colon.")
        print("For example, to move the top 2 checkers from a stack at (2, 3) to (3, 3), enter '2 3:3 3'.\n")

        while not self.game_state:
            print(self)
            self.make_move()
            self.check_win_condition()

        print(self)
        if self.game_state == 'white':
            print("Congratulations, white player! You win!")
        else:
            print("Congratulations, black player! You win!")

    def make_move(self):
        if self.turn == 'white':
            print("White player's turn.\n")
            start, end = self.get_move_coordinates()
            stack = self.white_stacks[start[1]]
            self.white_stacks[start[1]] = self.remove_stack_from_board(stack)
            self.white_stacks[end[1]] = self.add_stack_to_board(stack, end)

        else:
            print("Black player's turn.\n")
            if isinstance(self, HumanPlayer):
                start, end = self.get_move_coordinates()
            else:
                start, end = self.get_computer_move()
            stack = self.black_stacks[start[1]]
            self.black_stacks[start[1]] = self.remove_stack_from_board(stack)
            self.black_stacks[end[1]] = self.add_stack_to_board(stack, end)
            self.turn = 'black' if self.turn == 'white' else 'white'

    def get_move_coordinates(self):
        while True:
            start_row, start_col = map(int, input(
                "Enter the starting row and column for your stack: ").split())
            end_row, end_col = map(int, input(
                "Enter the ending row and column for your stack: ").split())

            if start_row < 0 or start_row > 7 or start_col < 0 or start_col > 7 or end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
                print("Invalid coordinates. Please enter coordinates between 0 and 7.")
            continue

            start_stack = self.get_stack_at_coordinates(start_row, start_col)
            if not start_stack:
                print("There is no stack at the starting coordinates.")
                continue

            end_stack = self.get_stack_at_coordinates(end_row, end_col)
            if end_stack and end_stack[0][0] != start_row and end_stack[0][1] != start_col:
                print(
                    "You cannot move a stack onto another stack that does not share an edge with the starting stack.")
            continue

        return (start_row, start_col), (end_row, end_col)

    def get_stack_at_coordinates(self, row, col):
        if self.board[row][col]:
            return self.white_stacks[col] if self.board[row][col] == 'W' else self.black_stacks[col]
        else:
            return None

    def remove_stack_from_board(self, stack):
        for coord in stack:
            self.board[coord[0]][coord[1]] = None

        return []

    def add_stack_to_board(self, stack, end_coord):
        for i, coord in enumerate(stack):
            self.board[end_coord[0] + i][end_coord[1]
                                         ] = 'W' if self.turn == 'white' else 'B'

        return stack

    def check_win_condition(self):
        if not self.black_stacks:
            self.game_state = 'white'
        elif not self.white_stacks:
            self.game_state = 'black'

    def __str__(self):
        s = ''
        s += '   0 1 2 3 4 5 6 7\n'
        s += '  ----------------\n'

        for row in range(8):
            s += str(row) + ' |'
            for col in range(8):
                if self.board[row][col]:
                    s += ' ' + self.board[row][col]
                else:
                    s += '  '
            s += '|\n'

        s += '  ----------------\n'
        s += f"White captured: {self.white_captured}\n"
        s += f"Black captured: {self.black_captured}\n"
        s += f"It is {self.turn}'s turn.\n"

        return s


class HumanPlayer:
    def init(self):
        pass

    def get_move_coordinates(self):
        return DipoleBoard.get_move_coordinates(self)


class RandomComputerPlayer:
    def init(self):
        pass

    def get_computer_move(self):
        start_col = random.randint(0, 7)
        start_stack = DipoleBoard.black_stacks[start_col]
        end_col = random.randint(0, 7)
        end_stack = DipoleBoard.white_stacks[end_col]

        while not start_stack or start_col == end_col or (end_stack and end_stack[0][0] != start_stack[0][0] and end_stack[0][1] != start_col):
            start_col = random.randint(0, 7)
            start_stack = DipoleBoard.black_stacks[start_col]
            end_col = random.randint(0, 7)
            end_stack = DipoleBoard.white_stacks[end_col]
            start_row, _ = start_stack[0]
            end_row, end_col = end_stack[0][0]
        return (start_row, start_col), (end_row, end_col)


if __name__ == "__main__":
    game_mode = input(
        "Enter game mode (human vs human, human vs computer, or computer vs computer): ")
    while game_mode not in ['human vs human', 'human vs computer', 'computer vs computer']:
        game_mode = input(
            "Invalid game mode. Please enter 'human vs human', 'human vs computer', or 'computer vs computer': ")

    if game_mode == 'human vs human':
        player1 = HumanPlayer()
        player2 = HumanPlayer()
    elif game_mode == 'human vs computer':
        player1 = HumanPlayer()
        player2 = RandomComputerPlayer()
    else:
        player1 = RandomComputerPlayer()
        player2 = RandomComputerPlayer()

    dipole_board = DipoleBoard()
    print(dipole_board)

    while dipole_board.game_state is None:
        if dipole_board.turn == 'white':
            move_coords = player1.get_move_coordinates()
        else:
            move_coords = player2.get_move_coordinates()
        dipole_board.make_move(*move_coords)
        print(dipole_board)

    print(f"{dipole_board.game_state.capitalize()} wins!")
