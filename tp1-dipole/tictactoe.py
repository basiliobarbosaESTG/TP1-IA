board = [' ' for i in range(9)]


def print_board():
    print('-------------')
    for i in range(3):
        print('| ' + ' | '.join(board[i*3:i*3+3]) + ' |')
        print('-------------')


def player_move(player):
    while True:
        move = input("Player " + player + ", enter a position (1-9): ")
        try:
            move = int(move)
            if move >= 1 and move <= 9 and board[move-1] == ' ':
                board[move-1] = player
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Try again.")


def check_win(player):
    for i in range(0, 9, 3):
        if board[i] == board[i+1] == board[i+2] == player:
            return True
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] == player:
            return True
    if board[0] == board[4] == board[8] == player:
        return True
    if board[2] == board[4] == board[6] == player:
        return True
    return False


print("Welcome to Tic-Tac-Toe!")
print_board()

while True:
    player_move('X')
    print_board()
    if check_win('X'):
        print("X wins!")
        break
    if ' ' not in board:
        print("Tie!")
        break
    player_move('O')
    print_board()
    if check_win('O'):
        print("O wins!")
        break
