import copy

# define constants
ROWS = 8
COLS = 8
WHITE = "O"
BLACK = "X"
EMPTY = " "


class DipoleGame:
    def __init__(self):
        self.board = [[EMPTY] * COLS for _ in range(ROWS)]
        self.white_stack = None
        self.black_stack = None
        self.turn = WHITE
        self.game_state = None

    def start(self):
        # get user input for starting positions of white and black stacks
        white_row = int(input("Enter row for white stack (0-1): "))
        black_row = int(input("Enter row for black stack (6-7): "))
        self.white_stack = [(white_row, i) for i in range(COLS)]
        self.black_stack = [(black_row, i) for i in range(COLS)]
        # initialize the board with the starting positions of the stacks
        for row, col in self.white_stack + self.black_stack:
            self.board[row][col] = WHITE if row <= 1 else BLACK
        # set game state to ongoing
        self.game_state = "ongoing"

    def print_board(self):
        # print the current state of the board
        print("  " + " ".join(str(i) for i in range(COLS)))
        for i, row in enumerate(self.board):
            print(str(i) + " " + " ".join(cell for cell in row))

    def get_possible_moves(self, stack):
        moves = []
        row, col = stack[0]
        # check all possible moves in 8 directions
        for d_row in [-1, 0, 1]:
            for d_col in [-1, 0, 1]:
                # skip the current cell
                if d_row == d_col == 0:
                    continue
                new_row = row + d_row
                new_col = col + d_col
                # check if the new position is within the board boundaries
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    # check if the new position is empty or has like-colored stack
                    if self.board[new_row][new_col] in (EMPTY, self.turn):
                        moves.append((new_row, new_col))
        return moves

    def get_capturing_moves(self, stack):
        moves = []
        row, col = stack[0]
        stack_size = len(stack)
        # check all possible capturing moves in 8 directions
        for d_row in [-1, 0, 1]:
            for d_col in [-1, 0, 1]:
                # skip the current cell
                if d_row == d_col == 0:
                    continue
                new_row = row + d_row
                new_col = col + d_col
                # check if the new position is within the board boundaries
                if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                    # check if the new position has enemy stack
                    if self.board[new_row][new_col] == BLACK if self.turn == WHITE else WHITE:
                        enemy_stack = [(new_row, new_col)]
                        for i in range(2, stack_size + 1):
                            enemy_row = new_row + i*d_row
                            enemy_col = new_col + i*d_col
                            # check if the enemy stack is within the board boundaries and has correct size
                            if 0 <= enemy_row < ROWS and 0 <= enemy_col < COLS and \
                                    self.board[enemy_row][enemy_col] == BLACK if self.turn == WHITE else WHITE:
                                enemy_stack.append((enemy_row, enemy_col))
                            else:
                                break
                    # check if the enemy stack is of equal or smaller size than the capturing stack
                            if len(enemy_stack) <= stack_size:
                                moves.append(
                                    (enemy_stack, (new_row-d_row, new_col-d_col)))
        return moves

    def make_move(self, stack, move):
        # update the board with the new position of the moved stack
        old_row, old_col = stack[0]
        new_row, new_col = move
        stack_size = len(stack)
        self.board[old_row][old_col] = EMPTY
        if self.board[new_row][new_col] == EMPTY:
            self.board[new_row][new_col] = self.turn
            stack = [(new_row, new_col)]
        else:
            stack = [(new_row, new_col)] + stack
            # check if the move resulted in a capture
            capturing_moves = self.get_capturing_moves(stack)
            if capturing_moves:
                for enemy_stack, enemy_pos in capturing_moves:
                    for enemy_row, enemy_col in enemy_stack:
                        self.board[enemy_row][enemy_col] = EMPTY
                        stack_size -= len(enemy_stack)
                        # check if the move resulted in a win
                        if stack_size == 0:
                            self.game_state = "win"
                        # check if the turn should be switched
                        if not capturing_moves:
                            self.turn = BLACK if self.turn == WHITE else WHITE
        return stack

    def play(self):
        self.start()
        while self.game_state == "ongoing":
            self.print_board()
            # get user input for the stack to move and the destination
            stack_row = int(input("Enter row of stack to move: "))
            stack_col = int(input("Enter column of stack to move: "))
            stack = [(stack_row, stack_col)]
            possible_moves = self.get_possible_moves(stack)
            capturing_moves = self.get_capturing_moves(stack)
            if not possible_moves and not capturing_moves:
                print("No possible moves for this stack. Try again.")
                continue
            if capturing_moves:
                print("Capturing moves available: ")
                for i, (enemy_stack, enemy_pos) in enumerate(capturing_moves):
                    print(
                        f"{i+1}: {len(enemy_stack)} enemy piece(s) at ({enemy_pos[0]}, {enemy_pos[1]})")
            else:
                print("No capturing moves available.")
                dest_row = int(input("Enter row of destination: "))
                dest_col = int(input("Enter column of destination: "))
                dest = (dest_row, dest_col)
            if dest not in possible_moves and \
                    not any(dest == enemy_pos for _, enemy_pos in capturing_moves):
                print("Invalid move. Try again.")
                continue
            # make the move and update the board
            stack = self.make_move(stack, dest)
            if self.game_state == "win":
                print(f"{self.turn} wins!")
        self.print_board()


game = DipoleGame()
game.play()
