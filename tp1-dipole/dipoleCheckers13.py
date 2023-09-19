class DipoleGameBoard:
    def __init__(self, white_row, black_row):
        self.board = [[' ']*8 for i in range(8)]
        self.white_stack = [(white_row, i) for i in range(8)]
        self.black_stack = [(black_row, i) for i in range(8)]
        for row, col in self.white_stack + self.black_stack:
            self.board[row][col] = 'W' if (
                row, col) in self.white_stack else 'B'
        self.turn = 'W'

    def display_board(self):
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            print(f"{i} {' '.join(self.board[i])}")

    def make_move(self, move):
        start_row, start_col, end_row, end_col = move
        if (start_row, start_col) not in (self.white_stack + self.black_stack):
            return 'Invalid'
        if self.board[start_row][start_col] != self.turn:
            return 'Invalid'
        if (end_row, end_col) in (self.white_stack + self.black_stack):
            return 'Invalid'
        if abs(start_row - end_row) > 1 or abs(start_col - end_col) > 1:
            return 'Invalid'
        if (start_row != end_row) and (start_col != end_col):
            return 'Invalid'
        stack_size = len([pos for pos in (self.white_stack + self.black_stack)
                         if pos[0] == start_row and pos[1] == start_col])
        if stack_size == 0:
            return 'Invalid'
        if (start_row == end_row) and (start_col != end_col):
            direction = 1 if end_col > start_col else -1
            for col in range(start_col+direction, end_col, direction):
                if (start_row, col) in (self.white_stack + self.black_stack):
                    return 'Invalid'
            new_stack = [(start_row, col) for col in range(
                end_col, end_col-stack_size, -direction)]
            if (end_row, end_col) in (self.white_stack + self.black_stack):
                if self.board[end_row][end_col] != self.turn:
                    return 'Invalid'
                if len([pos for pos in (self.white_stack + self.black_stack) if pos[0] == end_row and pos[1] == end_col]) < stack_size:
                    return 'Invalid'
                if (end_row, end_col) in self.white_stack:
                    self.white_stack = [
                        pos for pos in self.white_stack if pos not in new_stack]
                else:
                    self.black_stack = [
                        pos for pos in self.black_stack if pos not in new_stack]
            else:
                if self.turn == 'W':
                    self.white_stack = [
                        pos for pos in self.white_stack if pos not in new_stack]
                else:
                    self.black_stack = [
                        pos for pos in self.black_stack if pos not in new_stack]
            for row, col in new_stack:
                self.board[row][col] = self.turn
        elif (start_col == end_col) and (start_row != end_row):
            direction = 1 if end_row > start_row else -1
            for row in range(start_row+direction, end_row, direction):
                if (row, start_col) in (self.white_stack + self.black_stack):
                    return 'Invalid'
            new_stack = [(row, start_col) for row in range(
                end_row, end_col)] if row != start_row else [] + new_stack
            if (end_row, end_col) in (self.white_stack + self.black_stack):
                if self.board[end_row][end_col] != self.turn:
                    return 'Invalid'
                if len([pos for pos in (self.white_stack + self.black_stack) if pos[1] == end_col and end_row <= pos[0] <= end_row+stack_size-1]) < stack_size:
                    return 'Invalid'
                if (end_row, end_col) in self.white_stack:
                    self.white_stack = [
                        pos for pos in self.white_stack if pos not in new_stack]
                else:
                    self.black_stack = [
                        pos for pos in self.black_stack if pos not in new_stack]
            else:
                if self.turn == 'W':
                    self.white_stack = [
                        pos for pos in self.white_stack if pos not in new_stack]
                else:
                    self.black_stack = [
                        pos for pos in self.black_stack if pos not in new_stack]
            for row, col in new_stack:
                self.board[row][col] = self.turn
        if self.turn == 'W':
            self.turn = 'B'
        else:
            self.turn = 'W'
        return 'Valid'

    def is_win(self):
        return len(self.white_stack) == 0 or len(self.black_stack) == 0

    def play(self):
        while not self.is_win():
            self.display_board()
            print(f"{self.turn}'s turn:")
            while True:
                start_pos = input("Enter start position (row, col): ")
                end_pos = input("Enter end position (row, col): ")
                try:
                    start_row, start_col = [int(x)
                                            for x in start_pos.split(',')]
                    end_row, end_col = [int(x) for x in end_pos.split(',')]
                    move = (start_row, start_col, end_row, end_col)
                    result = self.make_move(move)
                    if result == 'Invalid':
                        print("Invalid move. Try again.")
                    else:
                        break
                except:
                    print("Invalid input. Try again.")
        self.display_board()
        print(f"{self.turn} wins!")


game_board = DipoleGameBoard(0, 7)
game_board.play()
