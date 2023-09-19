import os
import sys


class Checkerboard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'black'
        self.player1_stack = [(0, i) for i in range(8)]
        self.player2_stack = [(7, i) for i in range(8)]
        self.player1_pieces = 12
        self.player2_pieces = 12

        for i in range(0, 8, 2):
            self.board[0][i+1] = 'black'
            self.board[1][i] = 'black'
            self.board[2][i+1] = 'black'

            self.board[5][i] = 'white'
            self.board[6][i+1] = 'white'
            self.board[7][i] = 'white'

    def __str__(self):
        result = '   0  1  2  3  4  5  6  7\n'
        for i in range(8):
            result += f'{i} '
            for j in range(8):
                piece = self.board[i][j]
                if piece is None:
                    result += '.  '
                elif piece == 'black':
                    result += 'B  '
                else:
                    result += 'W  '
            result += f'{i}\n'
        result += '   0  1  2  3  4  5  6  7\n'
        return result

    def play(self):
        os.system('clear')
        print(self)
        while True:
            if self.current_player == 'black':
                print("Player 1's turn (black pieces)")
            else:
                print("Player 2's turn (white pieces)")

            command = input(
                "Enter move (format: 'x1 y1 x2 y2') or 'q' to quit: ")

            if command == 'q':
                sys.exit()

            try:
                x1, y1, x2, y2 = map(int, command.split())
            except:
                print('Invalid move. Try again.')
                continue

            if not self.is_valid_move(x1, y1, x2, y2):
                print('Invalid move. Try again.')
                continue

            self.move(x1, y1, x2, y2)

            if self.player1_pieces == 0:
                print('Player 2 (white) wins!')
                sys.exit()
            elif self.player2_pieces == 0:
                print('Player 1 (black) wins!')
                sys.exit()

            os.system('clear')
            print(self)

    def is_valid_move(self, x1, y1, x2, y2):
        piece = self.board[x1][y1]
        if piece is None:
            return False

        if piece == 'black' and self.current_player != 'black':
            return False
        elif piece == 'white' and self.current_player != 'white':
            return False

        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) != abs(dy):
            return False

        if dx < 0 and piece == 'white':
            return False
        elif dx > 0 and piece == 'black':
            return False

        if dx == 0:
            return False

        dist = abs(dx)
        if dist > len(self.get_stack(x1, y1)):
            return False

        if not self.is_empty(x2, y2) and self.get_color(x1, y1) != self.get_color(x2, y2):
            return self.is_capture_move(x1, y1, x2, y2)
        else:
            return self.is_basic_move(x1, y1, x2, y2)

    def is_basic_move(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        dist = abs(dx)
        if dist == 0:
            return False

        if dy / dx != 1 and dy / dx != -1:
            return False

        stack = self.get_stack(x1, y1)
        if dist > len(stack):
            return False

        if dx < 0 and self.get_color(x1, y1) == 'white':
            return False
        elif dx > 0 and self.get_color(x1, y1) == 'black':
            return False

        return True

    def is_capture_move(self, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        dist = abs(dx)

        if dy / dx != 1 and dy / dx != -1:
            return False

        if dist != 2:
            return False

        if dx < 0 and self.get_color(x1, y1) == 'white':
            return False
        elif dx > 0 and self.get_color(x1, y1) == 'black':
            return False

        if self.get_size(x2, y2) >= self.get_size(x1, y1):
            return False

        return True

    def move(self, x1, y1, x2, y2):
        stack = self.get_stack(x1, y1)
        dist = abs(x2 - x1)

        if self.is_capture_move(x1, y1, x2, y2):
            self.capture(x1, y1, x2, y2)
        elif self.is_basic_move(x1, y1, x2, y2):
            self.board[x1][y1] = None
            self.board[x2][y2] = self.get_color(x1, y1)
            self.board[x2][y2] = stack[-dist:]
            self.board[x1][y1] = stack[:-dist]

        if self.current_player == 'black':
            self.current_player = 'white'
        else:
            self.current_player = 'black'

    def capture(self, x1, y1, x2, y2):
        stack1 = self.get_stack(x1, y1)
        stack2 = self.get_stack(x2, y2)
        size = len(stack1) + len(stack2)

        self.board[x1][y1] = None
        self.board[x2][y2] = self.get_color(x1, y1)
        self.board[x2][y2] = stack2 + stack1

        if self.get_color(x1, y1) == 'black':
            self.player2_pieces -= (size - len(stack2))
            self.player1_pieces -= len(stack1)
        else:
            self.player1_pieces -= (size - len(stack1))
            self.player2_pieces -= len(stack2)

    def get_stack(self, x, y):
        return self.board[x][y]

    def get_color(self, x, y):
        return self.board[x][y]

    def get_size(self, x, y):
        stack = self.get_stack(x, y)
        if stack:
            return len(stack)
        else:
            return 0

    def is_empty(self, x, y):
        return self.get_stack(x, y) is None

    def get_winner(self):
        if self.player1_pieces == 0:
            return 'white'
        elif self.player2_pieces == 0:
            return 'black'

        if not self.has_moves('black'):
            return 'white'
        elif not self.has_moves('white'):
            return 'black'

        return None

    def has_moves(self, color):
        for x in range(self.width):
            for y in range(self.height):
                if self.get_color(x, y) == color:
                    for dx in range(-self.get_size(x, y) + 1, self.get_size(x, y)):
                        for dy in range(-self.get_size(x, y) + 1, self.get_size(x, y)):
                            if self.is_valid_move(x, y, x+dx, y+dy):
                                return True
        return False

    def play(self):
        while True:
            print(self)
            winner = self.get_winner()
            if winner is not None:
                print(f'{winner} wins!')
                return

            if not self.has_moves(self.current_player):
                print(f'{self.current_player} has no moves, skipping turn...')
                if self.current_player == 'black':
                    self.current_player = 'white'
                else:
                    self.current_player = 'black'
                continue

            print(f'{self.current_player} turn')
            x1 = int(input('Enter x1: '))
            y1 = int(input('Enter y1: '))
            x2 = int(input('Enter x2: '))
            y2 = int(input('Enter y2: '))

            if not self.is_valid_move(x1, y1, x2, y2):
                print('Invalid move!')
                continue

            self.move(x1, y1, x2, y2)


def main():
    game = Checkerboard()
    game.play()


if __name__ == "__main__":
    main()
