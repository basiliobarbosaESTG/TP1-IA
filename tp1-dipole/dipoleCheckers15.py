import sys

# Define the game board
BOARD_SIZE = 8
board = [[0 for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
white_row = int(input("Enter the row number for white pieces stack (0-7): "))
black_row = int(input("Enter the row number for black pieces stack (0-7): "))
board[white_row] = [1 for i in range(BOARD_SIZE)]
board[black_row] = [-1 for i in range(BOARD_SIZE)]

# Define player states
WHITE = 1
BLACK = -1
WIN = 1
LOSE = -1

# Define functions for checking valid moves and executing them


def is_valid_move(player, start, end):
    if not is_within_board(end):
        return False
    if not is_same_color(player, start, end):
        return False
    if not is_legal_distance(start, end):
        return False
    if not is_valid_capture(player, start, end):
        return False
    return True


def is_within_board(pos):
    row, col = pos
    return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE


def is_same_color(player, start, end):
    row1, col1 = start
    row2, col2 = end
    return board[row1][col1] * player > 0 and board[row2][col2] * player > 0


def is_legal_distance(start, end):
    row1, col1 = start
    row2, col2 = end
    return abs(row2 - row1) == abs(col2 - col1) or row1 == row2 or col1 == col2


def is_valid_capture(player, start, end):
    row1, col1 = start
    row2, col2 = end
    dist = abs(row2 - row1)
    if dist == 0:
        step = 1 if col2 > col1 else -1
        for col in range(col1 + step, col2, step):
            if board[row1][col] * player < 0:
                return False
        return True
    elif dist == abs(col2 - col1):
        step_row = 1 if row2 > row1 else -1
        step_col = 1 if col2 > col1 else -1
        row, col = row1 + step_row, col1 + step_col
        while row != row2 and col != col2:
            if board[row][col] * player < 0:
                return False
            row += step_row
            col += step_col
        return True
    else:
        return False


def execute_move(player, start, end):
    row1, col1 = start
    row2, col2 = end
    if board[row2][col2] == -player:
        capture_piece(start, end)
    else:
        board[row2][col2] += board[row1][col1]
        board[row1][col1] = 0


def capture_piece(start, end):
    row1, col1 = start
    row2, col2 = end
    size = abs(board[row1][col1])
    step_row = 1 if row2 > row1 else -1
    step_col = 1 if col2 > col1 else -1
    for i in range(1, size + 1):
        board[row1 + i * step_row][col1 + i * step_col] = 0
        board[row2][col2] += size * board[row1][col1]
        board[row1][col1] = 0


def has_no_pieces(player):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] * player > 0:
                return False
        return True


def get_game_state():
    if has_no_pieces(BLACK):
        return WIN, WHITE
    elif has_no_pieces(WHITE):
        return WIN, BLACK
    else:
        return None, None


def play():
    player = WHITE
    while True:
        print("Current board:")
        for row in board:
            print(row)
        if player == WHITE:
            print("White player's turn")
        else:
            print("Black player's turn")
            start = input(
                "Enter the starting position (row, col) of the stack to move (e.g., 0 0): ").split()
            start = (int(start[0]), int(start[1]))
            end = input(
                "Enter the ending position (row, col) of the stack to move (e.g., 0 0): ").split()
            end = (int(end[0]), int(end[1]))
            if not is_valid_move(player, start, end):
                print("Invalid move. Please try again.")
                continue
            execute_move(player, start, end)
            result, winner = get_game_state()
            if result is not None:
                if result == WIN:
                    print(f"{winner} wins!")
                else:
                    print("Tie game.")
                sys.exit()
            player = -player


play()
