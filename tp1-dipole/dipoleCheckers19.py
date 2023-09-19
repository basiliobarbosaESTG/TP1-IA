import random


class DipoleBoard:
    def __init__(self, white_row=0, black_row=7):
        self.white_row = white_row
        self.black_row = black_row
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = 'white'
        self.game_state = None

        # Place white pieces
        for i in range(12):
            self.board[white_row][i] = 'W'

        # Place black pieces
        for i in range(12):
            self.board[black_row][i] = 'B'

    def __str__(self):
        board_str = '  0 1 2 3 4 5 6 7\n'
        for i, row in enumerate(self.board):
            row_str = f'{i} '
            for piece in row:
                row_str += f'{piece or "-"} '
            board_str += row_str + '\n'
        return board_str

    def make_move(self, start_coord, end_coord):
        start_row, start_col = start_coord
        end_row, end_col = end_coord

        # Make sure start position has a piece of the current player's color
        if self.board[start_row][start_col] is None or self.board[start_row][start_col][0] != self.turn[0]:
            print(
                "Invalid move. Start position does not have a piece of the current player's color.")
            return False

        # Make sure number of squares moved matches size of stack
        size_of_stack = int(self.board[start_row][start_col][1])
        distance = abs(end_row - start_row) + abs(end_col - start_col)
        if distance != size_of_stack:
            print("Invalid move. Number of squares moved does not match size of stack.")
            return False

        # Make sure end position is within board bounds
        if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
            print("Invalid move. End position is outside of board bounds.")
            return False

        # Make sure non-capturing move is forward, horizontal, or diagonal forward
        if start_col == end_col:
            direction = 1 if end_row > start_row else -1
            for row in range(start_row + direction, end_row, direction):
                if self.board[row][start_col] is not None:
                    print("Invalid move. Non-capturing move is obstructed.")
                    return False
        elif start_row == end_row:
            direction = 1 if end_col > start_col else -1
            for col in range(start_col + direction, end_col, direction):
                if self.board[start_row][col] is not None:
                    print("Invalid move. Non-capturing move is obstructed.")
                    return False
        elif end_col - start_col == end_row - start_row:
            direction = 1 if end_row > start_row else -1
            for i in range(1, distance):
                row, col = start_row + i * direction, start_col + i * direction
                if self.board[row][col] is not None:
                    print("Invalid move. Non-capturing move is obstructed.")
                    return False
        elif end_col - start_col == start_row - end_row:
            direction = 1 if end_col > start_col else -1
            for i in range(1, distance):
                row, col = start_row - i * direction, start_col + i * direction
                if self.board[row][col] is not None:
                    # Make sure end position is empty or contains a stack of like-colored pieces
                    if self.board[end_row][end_col] is not None:
                        if self.board[end_row][end_col][0] != self.turn[0]:
                            print(
                                "Invalid move. End position contains an enemy stack.")
                            return False
                        else:
                            merged_stack_size = size_of_stack + \
                                int(self.board[end_row][end_col][1])
                            if merged_stack_size > 5:
                                print("Invalid move. Stack size limit exceeded.")
                                return False
                            # Make the move
                            if self.board[end_row][end_col] is not None:
                                self.board[end_row][end_col] = self.turn[0] + \
                                    str(merged_stack_size)
                            else:
                                self.board[end_row][end_col] = self.turn[0] + \
                                    str(size_of_stack)
                            self.board[start_row][start_col] = None

        # Check for captured stacks
        for direction in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
            row, col = end_row + direction[0], end_col + direction[1]
            if row >= 0 and row < 8 and col >= 0 and col < 8 and self.board[row][col] is not None and self.board[row][col][0] != self.turn[0]:
                stack_size = int(self.board[row][col][1])
                if merged_stack_size >= stack_size:
                    if merged_stack_size == stack_size:
                        print(
                            f"Player {self.turn} captured an enemy stack of size {stack_size}.")
                        self.board[row][col] = None
                    else:
                        print(
                            f"Player {self.turn} captured an enemy stack of size {stack_size}.")
                        self.board[row][col] = self.turn[0] + \
                            str(merged_stack_size - stack_size)

        # Check for win condition
        if 'B' not in [piece[0] for row in self.board for piece in row if piece is not None] or \
                'W' not in [piece[0] for row in self.board for piece in row if piece is not None]:
            self.game_state = f"{self.turn} wins!"
            print(self.game_state)
            return True

        # Switch turns
        self.turn = 'white' if self.turn == 'black' else 'black'
        return True

    def play_game(self):
        print(self)
        while self.game_state is None:
            if self.turn == 'white':
                (map(int, input(
                    "Enter the coordinates of the stack you want to move (row, col): ").split(',')))
                end_coord = tuple(map(int, input(
                    "Enter the coordinates of the position you want to move the stack to (row, col): ").split(',')))
                self.move(start_coord[0], start_coord[1],
                          end_coord[0], end_coord[1])
            else:
                print("Computer is making a move...")
            time.sleep(2)  # Simulate computer thinking time
            start_row, start_col, end_row, end_col = self.computer_move()
            self.move(start_row, start_col, end_row, end_col)
            print(self)
            print(self.game_state)


if __name__ == "__main__":
    game_mode = input(
        "Select game mode (1 for human vs. human, 2 for human vs. computer, 3 for computer vs. computer): ")
    if game_mode == '1':
        start_row_w = int(
            input("Enter the starting row for white stack (0-7): "))
        start_row_b = int(
            input("Enter the starting row for black stack (0-7): "))
        game = DipoleBoard(start_row_w, start_row_b)
        game.play_game()
    elif game_mode == '2':
        start_row_w = int(
            input("Enter the starting row for white stack (0-7): "))
        game = DipoleBoard(start_row_w, None)
        game.play_game()
    elif game_mode == '3':
        game = DipoleBoard(None, None)
        game.play_game()
    else:
        print("Invalid game mode selection. Please enter 1, 2, or 3.")
