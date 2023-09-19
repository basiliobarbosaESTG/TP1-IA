class Dipole:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.white_stack = [12]
        self.black_stack = [12]
        self.white_reserve = []
        self.black_reserve = []
        self.turn = 'white'
        self.game_over = False

    def print_board(self):
        for row in self.board:
            print(row)

    def is_valid_move(self, start, end):
        if start == end:
            return False
        if self.board[start[0]][start[1]] is None:
            return False
        if self.board[start[0]][start[1]][0] != self.turn[0]:
            return False
        if end[0] < 0 or end[0] > 7 or end[1] < 0 or end[1] > 7:
            return False
        if self.board[end[0]][end[1]] is not None and self.board[end[0]][end[1]][0] == self.turn[0]:
            return False
        if abs(start[0] - end[0]) != self.board[start[0]][start[1]][1]:
            return False
        if abs(start[1] - end[1]) != self.board[start[0]][start[1]][1]:
            return False
        return True

    def move(self, start, end):
        if not self.is_valid_move(start, end):
            return False
        stack_size = self.board[start[0]][start[1]][1]
        if stack_size == 1:
            self.board[end[0]][end[1]] = self.board[start[0]][start[1]]
            self.board[start[0]][start[1]] = None
        else:
            self.board[end[0]][end[1]] = (self.turn[0], stack_size)
            self.board[start[0]][start[1]] = (self.turn[0], stack_size - 1)
        if self.turn == 'white':
            self.white_stack[-1] -= stack_size
            if self.white_stack[-1] == 0:
                self.white_stack.pop()
            if len(self.white_stack) == 0:
                self.game_over = True
                print("Black wins!")
        else:
            self.black_stack[-1] -= stack_size
            if self.black_stack[-1] == 0:
                self.black_stack.pop()
            if len(self.black_stack) == 0:
                self.game_over = True
                print("White wins!")
        if self.game_over:
            return True
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'
        return True

    def merge(self, start, end):
        if not self.is_valid_move(start, end):
            return False
        if self.board[end[0]][end[1]] is None or self.board[end[0]][end[1]][0] != self.turn[0]:
            return False
        stack_size = self.board[start[0]][start[1]][1]
        self.board[end[0]][end[1]] = (
            self.turn[0], self.board[end[0]][end[1]][1] + stack_size)
        self.board[start[0]][start[1]] = None
        if self.turn == 'white':
            self.white_stack[-1] -= stack_size
            if self.white_stack[-1] == 0:
                self.white_stack.pop()
        else:
            self.black_stack[-1] -= stack_size
            if self.black_stack[-1] == 0:
                self.black_stack.pop()
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'
        return True

    def capture(self, start, end):
        if not self.is_valid_move(start, end):
            return False
        if self.board[end[0]][end[1]] is None or self.board[end[0]][end[1]][0] == self.turn[0]:
            return False
        stack_size = self.board[start[0]][start[1]][1]
        if stack_size >= self.board[end[0]][end[1]][1]:
            if self.turn == 'white':
                self.black_reserve.extend(self.board[end[0]][end[1]])
                self.black_stack.remove(self.board[end[0]][end[1]][1])
            else:
                self.white_reserve.extend(self.board[end[0]][end[1]])
                self.white_stack.remove(self.board[end[0]][end[1]][1])
            self.board[end[0]][end[1]] = (
                self.turn[0], stack_size - self.board[end[0]][end[1]][1])
            self.board[start[0]][start[1]] = None
            if self.turn == 'white':
                self.white_stack[-1] -= stack_size
                if self.white_stack[-1] == 0:
                    self.white_stack.pop()
            else:
                self.black_stack[-1] -= stack_size
                if self.black_stack[-1] == 0:
                    self.black_stack.pop()
            if len(self.black_stack) == 0:
                self.game_over = True
                print("White wins!")
            elif len(self.white_stack) == 0:
                self.game_over = True
                print("Black wins!")
            if self.turn == 'white':
                self.turn = 'black'
            else:
                self.turn = 'white'
            return True
        return False


game = Dipole()
game.move((6, 1), (5, 2))  # white moves a 2-stack forward
game.move((1, 6), (2, 5))  # black moves a 2-stack diagonally forward
game.merge((5, 2), (4, 3))  # white merges a 2-stack onto a 1-stack
game.capture((2, 5), (3, 4))  # black captures a 1-stack with a 2-stack
game.print_board()  # prints the current state of the board
