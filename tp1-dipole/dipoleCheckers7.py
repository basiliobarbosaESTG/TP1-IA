# This implementation defines a DipoleBoard class that represents the game board. The board is represented as a 2D list of squares, where each square can be either None (empty) or a string 'W' (white checker) or 'B' (black checker). The class also keeps track of the current turn, the number of checkers in each player's stack, and the checkers held in reserve.
# The move method takes a starting position and an ending position, and moves a stack of checkers from the starting position to the ending position. The method first checks if the move is valid, and raises a ValueError if it is not. If the move is valid, the method moves the stack, checks for captures, and updates the turn.
# The is_valid_move method checks if a move from a starting position to an ending position is valid. The method checks if the starting and ending positions are on the board, if the starting position contains a stack of checkers, if the ending position is empty or contains a stack of like-colored checkers, if the number of checkers in the moved stack is valid, if the move is forward or diagonally forward, and if the move takes the stack out of bounds.
# The check_captures method checks for captures after a move to a given position. The method checks for captures in all eight directions, and captures any enemy stacks that are smaller than or equal to the capturing stack.
# The is_on_board method checks if a position is on the board.

class DipoleBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_stack = [12]
        self.black_stack = [12]
        self.white_reserve = []
        self.black_reserve = []
        self.turn = 'white'

        # Initialize the board with checkers
        for i in range(0, 8, 2):
            self.board[0][i+1] = 'W'
            self.board[1][i] = 'W'
            self.board[6][i+1] = 'B'
            self.board[7][i] = 'B'

    def move(self, start_pos, end_pos):
        """
        Move a stack of checkers from start_pos to end_pos.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Check if the move is valid
        if not self.is_valid_move(start_pos, end_pos):
            raise ValueError("Invalid move")

        # Calculate the number of checkers in the moved stack
        num_checkers = abs(start_row - end_row) + 1

        # Move the stack
        stack = self.board[start_row][start_col:start_col+num_checkers]
        self.board[start_row][start_col:start_col +
                              num_checkers] = [None] * num_checkers
        self.board[end_row][end_col:end_col+num_checkers] = stack

        # Check for captures
        self.check_captures(end_pos)

        # Update the turn
        self.turn = 'black' if self.turn == 'white' else 'white'

    def is_valid_move(self, start_pos, end_pos):
        """
        Check if a move from start_pos to end_pos is valid.
        """
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Check if the start and end positions are on the board
        if not self.is_on_board(start_pos) or not self.is_on_board(end_pos):
            return False

        # Check if the start position contains a stack of checkers
        if self.board[start_row][start_col] is None:
            return False

        # Check if the end position is empty or contains a stack of like-colored checkers
        if self.board[end_row][end_col] is not None and self.board[end_row][end_col] != self.board[start_row][start_col]:
            return False

        # Calculate the number of checkers in the moved stack
        num_checkers = abs(start_row - end_row) + 1

        # Check if the number of checkers in the moved stack is valid
        if num_checkers != len(self.board[start_row][start_col:start_col+num_checkers]):
            return False

        # Check if the move is forward or diagonally forward
        if self.turn == 'white':
            if end_row <= start_row:
                return False
            if end_col != start_col and end_col != start_col + 1:
                return False
        else:
            if end_row >= start_row:
                return False
            if end_col != start_col and end_col != start_col - 1:
                return False

        # Check if the move takes the stack out of bounds
        if end_row < 0 or end_row > 7 or end_col < 0 or end_col > 7:
            return False

        return True

    def check_captures(self, pos):
        """
        Check for captures after a move to pos.
        """
        row, col = pos

        # Check for captures in all eight directions
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                while self.is_on_board((r, c)) and self.board[r][c] is not None and self.board[r][c] != self.turn[0]:
                    if len(self.board[row][col:]) >= len(self.board[r][c:]):
                        captured_stack = self.board[r][c:]
                        self.board[r][c:] = [None] * len(captured_stack)
                        if self.turn == 'white':
                            self.black_reserve += captured_stack
                        else:
                            self.white_reserve += captured_stack
                    r += dr
                    c += dc

    def is_on_board(self, pos):
        """
        Check if a position is on the board.
        """
        row, col = pos
        return row >= 0 and row < 8 and col >= 0 and col < 8
