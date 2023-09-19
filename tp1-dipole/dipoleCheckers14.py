class CheckerBoard:
    def __init__(self):
        self.board = [[' ' for j in range(8)] for i in range(8)]
        self.white_pieces = 12
        self.black_pieces = 12
        self.current_player = 'W'

    def play(self, game_state):
        game_state = GameState()
        game = CheckerBoard()
        game.play(game_state)
        self.print_board()
        print("Starting position for white pieces:")
        white_row = int(input("Enter row (0-7): "))
        print("Starting position for black pieces:")
        black_row = int(input("Enter row (0-7): "))
        self.board[white_row][0] = 'W'
        self.board[black_row][7] = 'B'
        self.current_player = 'W'

        while self.game_state == 'Playing':
            self.print_board()
            print(f"{self.current_player}'s turn")
            from_square = input("Enter starting square (e.g. a3): ")
            to_square = input("Enter ending square (e.g. b4): ")
            if not self.move(from_square, to_square):
                continue

        if self.game_state == 'Win':
            print("Congratulations, you win!")
        else:
            print("Sorry, you lose.")

    def print_board(self):
        print("   0 1 2 3 4 5 6 7 ")
        print("  -----------------")
        for i in range(8):
            print(str(i) + " |" + "|".join(self.board[i]) + "| " + str(i))
        print("  -----------------")
        print("   0 1 2 3 4 5 6 7 ")

    def setup_board(self):
        white_row = int(input("Enter the row number for white pieces (0-5): "))
        for i in range(white_row, white_row+2):
            for j in range(8):
                if (i+j) % 2 != 0:
                    self.board[i][j] = 'W'

        black_row = int(input("Enter the row number for black pieces (2-7): "))
        for i in range(black_row, black_row+2):
            for j in range(8):
                if (i+j) % 2 != 0:
                    self.board[i][j] = 'B'

    def check_win(self):
        if self.white_pieces == 0:
            return 'B'
        elif self.black_pieces == 0:
            return 'W'
        else:
            return None

    def make_move(self, start, end):
        x1, y1 = start
        x2, y2 = end
        stack_size = ord(self.board[x1][y1]) - ord('A') + 1
        dx = x2 - x1
        dy = y2 - y1
        distance = abs(dx) + abs(dy)

        if self.board[x2][y2] == ' ':
            # non-capturing move
            if self.current_player == 'W':
                if dx < 0:
                    print("Invalid move: white pieces can only move forward")
                    return False
            else:
                if dx > 0:
                    print("Invalid move: black pieces can only move forward")
                    return False

            if dx == 0 and dy != 0:
                # horizontal move
                if dy < 0:
                    direction = -1
                else:
                    direction = 1
                for j in range(y1+direction, y2, direction):
                    if self.board[x1][j] != ' ':
                        print("Invalid move: cannot jump over other pieces")
                        return False
                self.board[x2][y2] = chr(ord('A') + stack_size - 1)
                self.board[x1][y1] = ' '
            elif dy == 0 and dx != 0:
                # vertical move
                if dx < 0:
                    direction = -1
                else:
                    direction = 1
                for i in range(x1+direction, x2, direction):
                    if self.board[i][y1] != ' ':
                        print("Invalid move: cannot jump over other pieces")
                        return False
                self.board[x2][y2] = chr(ord('A') + stack_size - 1)
                self.board[x1][y1] = ' '
            elif abs(dx) == abs(dy):
                # diagonal move
                if dx < 0:
                    idir = -1
                else:
                    idir = 1
                if dy < 0:
                    jdir = -1
                else:
                    jdir = 1
                for i, j in zip(range(x1+idir, x2, idir), range(y1+jdir, y2, jdir)):
                    if self.board[i][j] != ' ':
                        print("Invalid move: cannot jump over other pieces")
                        return False
                self.board[x2][y2] = chr(ord('A') + stack_size - 1)
                self.board[x1][y1] = ' '
            else:
                print(
                    "Invalid move: non-capturing move must be forward, horizontal, or diagonal")
                return False
        else:
            # capturing move
            if self.board[x2][y2] == self.current_player:
                print("Invalid move: cannot capture own pieces")
                return False

            cap_size = ord(self.board[x2][y2]) - ord('A') + 1
            if cap_size > stack_size:
                print("Invalid move: cannot capture larger stack")
                return False
            elif cap_size == stack_size:
                if dx != 0 and dy != 0:
                    print("Invalid move: cannot merge stacks diagonally")
                    return False
                self.board[x2][y2] = chr(ord('A') + stack_size + cap_size - 1)
                self.board[x1][y1] = ' '
                self.current_player = 'W' if self.current_player == 'B' else 'B'
                if self.current_player == 'W':
                    self.white_pieces += cap_size
                    self.black_pieces -= cap_size
                else:
                    self.white_pieces -= cap_size
                    self.black_pieces += cap_size
            else:
                if dx == 0 and dy != 0:
                    # horizontal capture
                    if dy < 0:
                        direction = -1
                    else:
                        direction = 1
                    for j in range(y1+direction, y2, direction):
                        if self.board[x1][j] != ' ':
                            print("Invalid move: cannot jump over other pieces")
                            return False
                    self.board[x2][y2] = chr(ord('A') + stack_size - 1)
                    self.board[x1][y1] = ' '
                    for j in range(y2+direction, y2+cap_size*direction, direction):
                        self.board[x2][j] = ' '
                    self.current_player = 'W' if self.current_player == 'B' else 'B'
                    if self.current_player == 'W':
                        self.white_pieces += cap_size
                        self.black_pieces -= cap_size
                    else:
                        self.white_pieces -= cap_size
                        self.black_pieces += cap_size
                elif dy == 0 and dx != 0:
                    # vertical capture
                    if dx < 0:
                        direction = -1
                    else:
                        direction = 1
                    for i in range(x1+direction, x2, direction):
                        if self.board[i][y1] != ' ':
                            print("Invalid move: cannot jump over other pieces")
                            return False
                    self.board[x2][y2] = chr(ord('A') + stack_size - 1)
                    self.board[x1][y1] = ' '
                    for i in range(x2+direction, x2+cap_size*direction, direction):
                        self.board[i][y2] = ' '
                    self.current_player = 'W'
                    if self.current_player == 'B':
                        self.white_pieces += cap_size
                        self.black_pieces -= cap_size
                        return True
                    else:
                        # diagonal capture
                        if dx < 0:
                            idir = -1
                        else:
                            idir = 1
                        if dy < 0:
                            jdir = -1
                        else:
                            jdir = 1
                        for i, j in zip(range(x1+idir, x2, idir), range(y1+jdir, y2, jdir)):
                            if self.board[i][j] != ' ':
                                print("Invalid move: cannot jump over other pieces")
                        return False
                else:
                    self.board[x2][y2] = chr(ord('A') + stack_size - 1)
                    self.board[x1][y1] = ' '
                    for i, j in zip(range(x2+idir, x2+cap_sizeidir, idir), range(y2+jdir, y2+cap_sizejdir, jdir)):
                        self.board[i][j] = ' '
                        self.current_player = 'W' if self.current_player == 'B' else 'B'
                        if self.current_player == 'W':
                            self.white_pieces += cap_size
                            self.black_pieces -= cap_size
                        else:
                            self.white_pieces -= cap_size
                            self.black_pieces += cap_size
                            # check for end game conditions
            if self.white_pieces == 0:
                self.game_state = 'Lose'
            elif self.black_pieces == 0:
                self.game_state = 'Win'
            return True

    def print_board(self):
        print("  ", end="")
        for j in range(8):
            print(chr(ord('a')+j), end=" ")
        print()
        for i in range(8):
            print(i+1, end=" ")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()


# class GameState():
#     def __init__(self, current_player, game_state):
#         self.current_player = current_player
#         self.game_state = game_state
#         # self.state == "WIN"
#         # self.state == "LOSE"
