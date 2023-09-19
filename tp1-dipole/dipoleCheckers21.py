import numpy as np


class Stack:
    def __init__(self, color, size):
        self.color = color
        self.size = size

    def __repr__(self):
        return f"{self.color}_{self.size}"


class Checkers:
    def __init__(self):
        self.board = np.array([
            [None, Stack('black', 1), None, Stack('black', 1), None,
             Stack('black', 1), None, Stack('black', 1)],
            [Stack('black', 1), None, Stack('black', 1), None,
             Stack('black', 1), None, Stack('black', 1), None],
            [None, Stack('black', 1), None, Stack('black', 1), None,
             Stack('black', 1), None, Stack('black', 1)],
            [None] * 8,
            [None] * 8,
            [Stack('white', 1), None, Stack('white', 1), None,
             Stack('white', 1), None, Stack('white', 1), None],
            [None, Stack('white', 1), None, Stack('white', 1), None,
             Stack('white', 1), None, Stack('white', 1)],
            [Stack('white', 1), None, Stack('white', 1), None,
             Stack('white', 1), None, Stack('white', 1), None]
        ])

        self.current_player = 'black'

    def get_possible_moves(self, row, col):
        stack = self.board[row][col]
        moves = []

        if not stack:
            return moves

        forward = -1 if stack.color == 'black' else 1

        if col > 0:
            moves.append((row + forward, col - 1))
        if col < 7:
            moves.append((row + forward, col + 1))
        if col > 1 and self.board[row + forward][col - 1] and self.board[row + forward][col - 1].color == stack.color:
            moves.append((row + forward, col - 2))
        if col < 6 and self.board[row + forward][col + 1] and self.board[row + forward][col + 1].color == stack.color:
            moves.append((row + forward, col + 2))

        for i in range(1, stack.size):
            if row + forward * i > 7 or row + forward * i < 0:
                break
            if self.board[row + forward * i][col]:
                break
            moves.append((row + forward * i, col))

        return moves

    def move_stack(self, from_row, from_col, to_row, to_col):
        stack = self.board[from_row][from_col]
        distance = abs(from_row - to_row)

        if distance == stack.size and self.current_player == stack.color:
            if to_col < 0 or to_col > 7:
                self.board[from_row][from_col] = None
                return True

            if self.board[to_row][to_col]:
                if self.board[to_row][to_col].color == stack.color:
                    return False
                if self.board[to_row][to_col].size > stack.size:
                    return False
                self.board[to_row][to_col] = Stack(
                    stack.color, self.board[to_row][to_col].size + stack.size)
            else:
                self.board[to_row][to_col] = Stack(stack.color, stack.size)
                self.board[from_row][from_col] = Stack(stack.color, stack.size)
                if from_row != to_row or from_col != to_col:
                    self.board[from_row][from_col] = None
            return True
        return False

    def capture_stack(self, from_row, from_col, to_row, to_col):
        stack = self.board[from_row][from_col]

        if not stack:
            return False

        if self.board[to_row][to_col]:
            return False

        dx, dy = to_col - from_col, to_row - from_row
        distance = max(abs(dx), abs(dy))

        if distance > stack.size:
            return False

        forward = -1 if stack.color == 'black' else 1

        if abs(dx) == abs(dy):
            direction = (int(dx / distance), int(dy / distance))
            for i in range(1, distance):
                if self.board[from_row + direction[1] * i][from_col + direction[0] * i]:
                    return False
            self.board[to_row][to_col] = Stack(stack.color, stack.size)
            self.board[from_row][from_col] = None
            return True

        if dx == 0:
            if dy * forward < 0:
                return False
            for i in range(1, distance):
                if self.board[from_row + forward * i][from_col]:
                    return False
            self.board[to_row][to_col] = Stack(stack.color, stack.size)
            self.board[from_row][from_col] = None
            return True

        if dy != forward:
            return False

        if dx < 0:
            return False

        if dx > stack.size:
            return False

        for i in range(1, dx):
            if self.board[from_row][from_col + i]:
                return False
        self.board[to_row][to_col] = Stack(stack.color, stack.size)
        self.board[from_row][from_col] = None
        return True

    def check_victory(self):
        black_stacks = set()
        white_stacks = set()

        for row in range(8):
            for col in range(8):
                stack = self.board[row][col]
                if stack:
                    if stack.color == 'black':
                        black_stacks.add((row, col))
                    else:
                        white_stacks.add((row, col))

        if not black_stacks or not white_stacks:
            return True

        for row in range(8):
            for col in range(8):
                if self.board[row][col] and self.board[row][col].color == self.current_player:
                    if self.get_possible_moves(row, col):
                        return False

        return True

    def switch_player(self):
        if self.current_player == 'black':
            self.current_player = 'white'
        else:
            self.current_player = 'black'

    def play(self):
        while not self.check_victory():
            print(self.board)
            moves = []

            while not moves:
                from_pos = input(
                    f"{self.current_player} player, enter the row and column of the stack you want to move: ")
                from_row, from_col = map(int, from_pos.split())
                moves = self.get_possible_moves(from_row, from_col)

            print(f"Possible moves: {moves}")

            to_pos = input(
                f"{self.current_player} player, enter the row and column you want to move the stack to: ")
            to_row, to_col = map(int, to_pos.split())

            if (to_row, to_col) not in moves:
                print("Invalid move!")
                continue

            if not self.move_stack(from_row, from_col, to_row, to_col):
                if not self.capture_stack(from_row, from_col, to_row, to_col):
                    self.switch_player()

        print(f"{self.current_player} player wins!")
