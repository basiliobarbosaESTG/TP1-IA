class Board:
    def __init__(self):
        self.board = [[' ' for _ in range(8)] for _ in range(8)]
        self.board[0][1] = 'B'
        self.board[0][3] = 'B'
        self.board[0][5] = 'B'
        self.board[0][7] = 'B'
        self.board[1][0] = 'B'
        self.board[1][2] = 'B'
        self.board[1][4] = 'B'
        self.board[1][6] = 'B'
        self.board[2][1] = 'B'
        self.board[2][3] = 'B'
        self.board[2][5] = 'B'
        self.board[2][7] = 'B'
        self.board[5][0] = 'W'
        self.board[5][2] = 'W'
        self.board[5][4] = 'W'
        self.board[5][6] = 'W'
        self.board[6][1] = 'W'
        self.board[6][3] = 'W'
        self.board[6][5] = 'W'
        self.board[6][7] = 'W'
        self.board[7][0] = 'W'
        self.board[7][2] = 'W'
        self.board[7][4] = 'W'
        self.board[7][6] = 'W'

    def print_board(self):
        print('    0   1   2   3   4   5   6   7')
        print('  +---+---+---+---+---+---+---+---+')
        for i in range(8):
            print(f"{i} | {' | '.join(self.board[i])} |")
            print('  +---+---+---+---+---+---+---+---+')

    def move(self, piece, x, y):
        if self.is_valid_move(piece, x, y):
            self.board[piece[0]][piece[1]] = ' '
            self.board[x][y] = piece[2]
            return True
        return False

    def is_valid_move(self, piece, x, y):
        if x < 0 or x > 7 or y < 0 or y > 7:
            return False
        if self.board[x][y] != ' ':
            return False
        if piece[2] == 'W' and x <= piece[0]:
            return False
        if piece[2] == 'B' and x >= piece[0]:
            return False
        if abs(piece[0] - x) == 1 and abs(piece[1] - y) == 1:
            return True
        if abs(piece[0] - x) == 2 and abs(piece[1] - y) == 2:
            cx = (piece[0] + x) // 2
            cy = (piece[1] + y) // 2
            if self.board[cx][cy] == ' ':
                return False
            if self.board[cx][cy] == piece[2]:
                return False
            return True
        return False

    def get_pieces(self, color):
        pieces = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    pieces.append
                    return pieces

    class Game:
        def init(self):
            self.board = Board()
            self.current_player = 'B'

    def play(self):
        while True:
            self.board.print_board()
            pieces = self.board.get_pieces(self.current_player)
            if not pieces:
                print(f"{self.current_player} has lost!")
                return
            print(f"{self.current_player} player's turn")
            piece = self.get_piece_input(pieces)
            x, y = self.get_move_input(piece)
            if self.board.move(piece, x, y):
                if self.current_player == 'B':
                    self.current_player = 'W'
                else:
                    self.current_player = 'B'

    def get_piece_input(self, pieces):
        while True:
            piece_str = input("Choose a piece to move (row,col): ")
            try:
                row, col = map(int, piece_str.split(','))
                for piece in pieces:
                    if piece[0] == row and piece[1] == col:
                        return piece
            except:
                pass
            print("Invalid input. Try again.")

    def get_move_input(self, piece):
        while True:
            move_str = input("Choose a move (row,col): ")
            try:
                row, col = map(int, move_str.split(','))
                if self.board.is_valid_move(piece, row, col):
                    return row, col
            except:
                pass
            print("Invalid move. Try again.")

    name = "main"
    if name == 'main':
        game = Game()
        game.play()
