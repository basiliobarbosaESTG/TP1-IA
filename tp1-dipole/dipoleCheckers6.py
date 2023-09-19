# Create me a python game described below:
# Dipole - is an extremely strategic game where you're tasked to outwit your opponent's pieces off the board before they eliminate all of yours. The game starts off with each player having a single stack of 12 pieces on their end of the board. Players take turns moving stacks of their own checkers, one stack per turn. You can move an entire stack or just a portion of one. Basic moves can only be made in the forward or diagonally forward directions.The number of squares a stack is moved must equal the number of checkres in the moved stack. Even though only the dark squares are used, white squares must be included in the count. If you move a stack out of bounds, you must remove that stack from play. When moving a stack out of bounds. pretend the board squares extend outward far beyond the boundaries, and make a basic move accordingly. Stacks can only be removed in the forward or diagonally forward directions. Players typically remove singletons from their far row because they have nowhere else to go.If you have no moves available, your turn is passed until you do have a move available. If you have any moves available, you must move. There will always be a move available to one player or the other.Merging Moves - Stacks can be moved onto other, liked-color stacks. Stack movement is never obstructed by intervening staks, regardless of size or color. This holds true for basic capturing moves as well. Merging moves can only be made in the forward or diagonally forward directions.Capturing Moves - Capturing moves can be made in any of the eight directions. A stack can capture only an entier enemy stack, which must be of an equal or smaller size than the capturing stack. Basic, merging, and capturing moves must be made in a straight line.


import copy
import random

# Set up the game board
board = [['-' for i in range(8)] for j in range(8)]
for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            board[i][j] = ' '
# Initialize the starting positions of the pieces
player1_pieces = [(i, 1) for i in range(8)]
player2_pieces = [(i, 6) for i in range(8)]

# Place the pieces on the board
for x, y in player1_pieces:
    board[y][x] = 'O'
for x, y in player2_pieces:
    board[y][x] = 'X'


def print_board(board):  # Define a function to print the board
    print('  0 1 2 3 4 5 6 7')
    for i in range(8):
        print(i, end=' ')
        for j in range(8):
            print(board[i][j], end=' ')
        print()


# Define a function to check if a move is valid
def is_valid_move(board, player_pieces, start, end):
    x1, y1 = start
    x2, y2 = end
    if x2 < 0 or x2 > 7 or y2 < 0 or y2 > 7:
        return False
    if board[y2][x2] != ' ':
        return False
    dx, dy = abs(x1 - x2), abs(y1 - y2)
    if dx != dy or dx == 0:
        return False
    if dx == 1:
        return True
    if dx > 1:
        if dx != len([p for p in player_pieces if x1 < p[0] <= x2 or x1 > p[0] >= x2]):
            return False
        for i in range(1, dx):
            x, y = x1 + i * (1 if x2 > x1 else -1), y1 + \
                i * (1 if y2 > y1 else -1)
            if board[y][x] != ' ':
                return False
    return True

# Define a function to move a stack of pieces


def move_stack(board, player_pieces, start, end):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    stack = [p for p in player_pieces if p[0] == x1 and p[1] >= y1]
    for p in stack:
        player_pieces.remove(p)
    for i in range(len(stack)):
        x, y = x2 + i * (1 if dx > 0 else -1), y2 + i * (1 if dy > 0 else -1)
        player_pieces.append((x, y))
        board[y][x] = 'O' if stack[0][1] == 1 else 'X'

# Define a function to merge stacks of pieces


def merge_stacks(board, player_pieces, start, end):
    x1, y1 = start
    x2, y2 = end
    stack1 = [p for p in player_pieces if p[0] == x1 and p[1] >= y1]
    stack2 = [p for p in player_pieces if p[0] == x2 and p[1] >= y2]
    player_pieces

    # Determine which stack is bigger
    bigger_stack = stack1 if len(stack1) >= len(stack2) else stack2
    smaller_stack = stack2 if len(stack1) >= len(stack2) else stack1
    # Remove the smaller stack from the board and player's pieces
    for p in smaller_stack:
        player_pieces.remove(p)
        board[p[1]][p[0]] = ' '
    # Move the bigger stack to the new location
    move_stack(board, player_pieces, start, end)


# Define a function to capture an enemy stack of pieces
def capture_stack(board, player_pieces, enemy_pieces, start, end):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    enemy_color = 'X' if player_pieces[0][1] == 1 else 'O'
    enemy_stack = [p for p in enemy_pieces if p[0] == x2 and p[1] >= y2]
    if len(enemy_stack) >= len([p for p in player_pieces if p[0] == x1 and p[1] >= y1]):
        # Remove the captured stack from the board and enemy's pieces
        for p in enemy_stack:
            enemy_pieces.remove(p)
            board[p[1]][p[0]] = ' '

    # Move the capturing stack to the new location
    move_stack(board, player_pieces, start, end)

# Define a function to get all possible moves for a player


def get_possible_moves(board, player_pieces, enemy_pieces):
    moves = []
    for p in player_pieces:
        x, y = p
    # Check basic moves
    if is_valid_move(board, player_pieces, (x, y), (x, y+1)):
        moves.append(((x, y), (x, y+1)))
    if is_valid_move(board, player_pieces, (x, y), (x+1, y+1)):
        moves.append(((x, y), (x+1, y+1)))
    if is_valid_move(board, player_pieces, (x, y), (x-1, y+1)):
        moves.append(((x, y), (x-1, y+1)))

    # Check merging moves
    for p2 in player_pieces:
        if p2 == p:
            continue
        x2, y2 = p2
        if (x2 == x and y2 > y) or (abs(x2 - x) == abs(y2 - y) and y2 > y):
            if is_valid_move(board, player_pieces, (x, y), (x2, y2)):
                moves.append(((x, y), (x2, y2)))

    # Check capturing moves
    for p3 in enemy_pieces:
        x3, y3 = p3
        if abs(x3 - x) == abs(y3 - y) and y3 > y:
            if is_valid_move(board, player_pieces, (x, y), (x3, y3)):
                moves.append(((x, y), (x3, y3)))
                return moves

# Define a function to check if a player has any moves available


def has_moves_available(board, player_pieces, enemy_pieces):
    for p in player_pieces:
        x, y = p
        # Check basic moves
        if is_valid_move(board, player_pieces, (x, y), (x, y+1)):
            return True
        if is_valid_move(board, player_pieces, (x, y), (x+1, y+1)):
            return True
        if is_valid_move(board, player_pieces, (x, y), (x-1, y+1)):
            return True

        # Check merging moves
        for p2 in player_pieces:
            if p2 == p:
                continue
            x2, y2 = p2
            if (x2 == x and y2 > y) or (abs(x2 - x) == abs(y2 - y) and y2 > y):
                if is_valid_move(board, player_pieces, (x, y), (x2, y2)):
                    return True

                # Check capturing moves
                for p3 in enemy_pieces:
                    x3, y3 = p3
                    if abs(x3 - x) == abs(y3 - y) and y3 > y:
                        if is_valid_move(board, player_pieces, (x, y), (x3, y3)):
                            return True
                        return False

# Define the main game loop


def game_loop():
    # Set up the game board
    board = [[' ' for x in range(9)] for y in range(7)]
    board[0][4] = 'O'
    board[6][4] = 'X'
    player_pieces = [(4, 1) for i in range(12)]
    enemy_pieces = [(4, 5) for i in range(12)]
    player_turn = True

    while True:
        # Print the board
        print_board(board, player_pieces, enemy_pieces)
        # Get the player's move
        if player_turn:
            print("Your turn!")
            while True:
                try:
                    start = tuple(map(int, input(
                        "Enter the coordinates of the stack you want to move (x, y): ").split(',')))
                    end = tuple(map(int, input(
                        "Enter the coordinates of the square you want to move it to (x, y): ").split(',')))
                    if is_valid_move(board, player_pieces, start, end):
                        break
                    else:
                        print("Invalid move.")
                except:
                    print("Invalid input.")
                # Get the computer's move
                else:
                    print("Computer's turn.")
                possible_moves = get_possible_moves(
                    board, enemy_pieces, player_pieces)
                if possible_moves:
                    move = random.choice(possible_moves)
                start, end = move
                print(
                    f"Computer moves stack from ({start[0]}, {start[1]}) to ({end[0]}, {end[1]}).")
        else:
            print("Computer has no moves available.")
            # Make the move
        if player_turn:
            move_stack(board, player_pieces, start, end)
            if end[1] == 6:
                print("You win!")
            break
        if not has_moves_available(board, enemy_pieces, player_pieces):
            print("Computer has no moves available.")
            break
        else:
            move_stack(board, enemy_pieces, start, end)
        if end[1] == 0:
            print("Computer wins!")
            break
        if not has_moves_available(board, player_pieces, enemy_pieces):
            print("You have no moves available.")
            break
        # Switch turns
        player_turn = not player_turn


# Start the game
game_loop()
