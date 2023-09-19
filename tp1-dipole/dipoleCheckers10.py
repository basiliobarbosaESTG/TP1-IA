class Dipole:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.white_stack = [12]
        self.black_stack = [12]
        self.white_reserve = 0
        self.black_reserve = 0
        self.turn = 'white'
        self.moves = {'forward': [
            (1, 1), (1, -1)], 'capture': [(2, 2), (2, -2), (-2, 2), (-2, -2)]}

    def print_board(self):
        print('  0 1 2 3 4 5 6 7')
        for i in range(8):
            print(i, end=' ')
            for j in range(8):
                print(self.board[i][j], end=' ')
            print()

    def get_input(self):
        while True:
            try:
                move = input(
                    f"{self.turn.capitalize()} player's turn. Enter move (e.g. '2,3 to 3,4'): ")
                start, end = move.split(' to ')
                start_row, start_col = map(int, start.split(','))
                end_row, end_col = map(int, end.split(','))
                return (start_row, start_col), (end_row, end_col)
            except:
                print('Invalid input. Please try again.')

    def is_valid_move(self, start, end):
        if self.turn == 'white':
            stack = self.white_stack
            reserve = self.white_reserve
        else:
            stack = self.black_stack
            reserve = self.black_reserve

        if start[0] % 2 != 0 and end[0] % 2 != 0:
            return False

        if end[0] < 0 or end[0] > 7 or end[1] < 0 or end[1] > 7:
            return False

        if end[0] % 2 != 0:
            return False

        if end[0] == start[0] and end[1] == start[1]:
            return False

        if end[0] < start[0]:
            return False

        if end[0] - start[0] != stack[start[0]][start[1]]:
            return False

        if end[1] - start[1] not in [-1, 0, 1]:
            return False

        if end[1] - start[1] == 0 and self.board[end[0]][end[1]] != ' ':
            return False

        if end[1] - start[1] != 0 and self.board[end[0]][end[1]] == ' ':
            return False

        if end[1] - start[1] == 0 and end[0] - start[0] > 1:
            return False

        if end[1] - start[1] != 0 and end[0] - start[0] > 2:
            return False

        if end[1] - start[1] == 0 and end[0] - start[0] == 1:
            return True

        if end[1] - start[1] != 0 and end[0] - start[0] == 2:
            if self.board[(start[0] + end[0]) // 2][(start[1] + end[1]) // 2] == ' ':
                return False
            if self.board[(start[0] + end[0]) // 2][(start[1] + end[1]) // 2] == self.turn[0]:
                return False
            if stack[start[0]][start[1]] <= stack[(start[0] + end[0]) // 2][(start[1] + end[1]) // 2]:
                return False
            return True

        if end[1] - start[1] == 0 and end[0] - start[0] == 2:
            if reserve == 0:
                return False
            if stack[start[0]][start[1]] + stack[end[0]][end[1]] > 6:
                return False
            return True

        if end[1] - start[1] != 0 and end[0] - start[0] == 4:
            if reserve == 0:
                return False
            if stack[start[0]][start[1]] + stack[(start[0] + end[0]) // 2][(start[1] + end[1]) // 2] + stack[end[0]][end[1]] > 6:
                return False
            return True

        return False

    def make_move(self, start, end):
        if self.turn == 'white':
            stack = self.white_stack
            reserve = self.white_reserve
            opponent_stack = self.black_stack
        else:
            stack = self.black_stack
            reserve = self.black_reserve
            opponent_stack = self.white_stack

        if end[1] - start[1] == 0 and end[0] - start[0] == 2:
            reserve -= stack[start[0]][start[1]]
            stack[end[0]][end[1]] += stack[start[0]][start[1]]
            stack[start[0]][start[1]] = 0
            self.board[start[0]][start[1]] = ' '
            self.board[end[0]][end[1]] = self.turn[0]
            self.turn = 'black' if self.turn == 'white' else 'white'
            self.white_reserve = reserve if self.turn == 'white' else self.white_reserve
            self.black_reserve = reserve if self.turn == 'black' else self.black_reserve
            return

        if end[1] - start[1] != 0 and end[0] - start[0] == 4:
            reserve -= stack[start[0]][start[1]]
            stack[(start[0] + end[0]) // 2][(start[1] + end[1]) // 2] = 0
            stack[end[0]][end[1]] += stack[start[0]][start[1]] + \
                stack[(start[0] + end[0]) // 2][(start[1] + end[1]) // 2]
            stack[start[0]][start[1]] = 0
            self.board[start[0]][start[1]] = ' '
            self.board[(start[0] + end[0]) //
                       2][(start[1] + end[1]) // 2] = ' '
            self.board[end[0]][end[1]] = self.turn[0]
            self.turn = 'black' if self.turn == 'white' else 'white'
            self.white_reserve = reserve if self.turn == 'white' else self.white_reserve
            self.black_reserve = reserve if self.turn == 'black' else self.black_reserve
            return

        if self.board[end[0]][end[1]] == ' ':
            stack[end[0]][end[1]] = stack[start[0]][start[1]]
            stack[start[0]][start[1]] = 0
            self.board[start[0]][start[1]] = ' '
            self.board[end[0]][end[1]] = self.turn[0]
            self.turn = 'black' if self.turn == 'white' else 'white'
            self.white_reserve = reserve if self.turn == 'white' else self.white_reserve
            self.black_reserve = reserve if self.turn == 'black' else self.black_reserve
            return

        if self.board[end[0]][end[1]] == opponent_stack[end[0]][end[1]]:
            if stack[start[0]][start[1]] <= opponent_stack[end[0]][end[1]]:
                return
            opponent_stack[end[0]][end[1]] = 0
            stack[end[0]][end[1]] = stack[start[0]][start[1]]
            stack[start[0]][start[1]] = 0
            self.board[start[0]][start[1]] = ' '
            self.board[end[0]][end[1]] = self.turn[0]
            self.turn = 'black' if self.turn == 'white' else 'white'
            self.white_reserve = reserve if self.turn == 'white' else self.white_reserve
            self.black_reserve = reserve if self.turn == 'black' else self.black_reserve
            return

    def play(self):
        while True:
            self.print_board()
            start, end = self.get_input()
            if self.is_valid_move(start, end):
                self.make_move(start, end)
                if self.black_stack == [0] * 8:
                    print('White wins!')
                    break
                if self.white_stack == [0] * 8:
                    print('Black wins!')
                    break
            else:
                print('Invalid move. Please try again.')


game = Dipole()
game.play()
