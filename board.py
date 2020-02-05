import random

# All the direcections around a cell
DIRECTIONS = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

class Board:
    def __init__(self, n, num_mines):
        self.n = n
        self.num_mines = num_mines

        # Initialize the game
        self.__initialize()

    # Check if the game is won by comparing number of current open cell and number of target open cell
    def check_win(self):
        if self.current_move == self.goal_move:
            return True
        return False

    # Uncover a cell
    def make_move(self, row, col):
        # If this is not the first move and the cell contains a bomb, game is lost(return False)
        if self.current_move != 0 and self.game_board[row][col] == 'M':
            for mine in self.mines:
                self.user_board[mine[0]][mine[1]] = 'M'
            return False
        # If this is the first move and the cell contains a bomb, relocate the bomb and make the move
        elif self.current_move == 0 and self.game_board[row][col] == 'M':
            self.__move_mine_away(row, col)
            self.__auto_open_surrounding(row, col)
        # Make the move
        else:
            self.__auto_open_surrounding(row, col)
        return True

    # Change the value in the cell into the actual number from the game board
    # If the cell is 0, uncover surrounding cell too using dfs and change the value in this cell to '.'
    def __auto_open_surrounding(self, row, col):
        if self.game_board[row][col] == 0 and self.user_board[row][col] != '.':
            self.current_move += 1
            self.user_board[row][col] = '.'
            self.game_board[row][col] = '.'

            for direc in DIRECTIONS:
                if self.is_valid(row+direc[0], col+direc[1]):
                    self.__auto_open_surrounding(row+direc[0], col+direc[1])

        elif self.game_board[row][col] != 0 and self.user_board[row][col] == 'X':
            self.current_move += 1
            self.user_board[row][col] = self.game_board[row][col]

    # If the first move hits a bomb, relocate the bomb and regenerate the game board
    def __move_mine_away(self, row, col):
        newrow = random.randint(0, self.n-1)
        newcol = random.randint(0, self.n-1)
        while self.game_board[newrow][newcol] == 'M':
            newrow = random.randint(0, self.n-1)
            newcol = random.randint(0, self.n-1)
        self.game_board[row][col] = 0
        self.game_board[newrow][newcol] = 'M'
        self.mines.remove((row, col))
        self.mines.append((newrow, newcol))
        self.game_board = [[0 for i in range(0, self.n)] for j in range(0, self.n)]
        for mine in self.mines:
            self.game_board[mine[0]][mine[1]] = 'M'
        # Calculate number of mines surrounding each location
        self.__update_board()

    # Check if the index is within the range
    def is_valid(self, row, col):
        if row >= 0 and row < self.n and col >= 0 and col < self.n:
            return True
        return False

    # Check if the move is valid. 1) it is within the range 2) it is covered
    def is_valid_move(self, row, col):
        if self.is_valid(row, col) and self.user_board[row][col] == "X":
            return True
        return False

    # Reset the user_board and game_board
    def __initialize(self):
        # Game board is for internal system to track the actual state of the Board
        # User board is what the player sees
        self.current_move = 0
        self.goal_move = self.n**2 - self.num_mines
        self.user_board = [['X' for i in range(0, self.n)] for j in range(0, self.n)]
        self.game_board = [[0 for i in range(0, self.n)] for j in range(0, self.n)]
        self.mines = self.__random_mines()

        # Mark all the mines on the game board
        for mine in self.mines:
            self.game_board[mine[0]][mine[1]] = 'M'
        # Calculate number of mines surrounding each location
        self.__update_board()

    # Calculate number of mines surrounding each location
    def __update_board(self):
        for i in range(0, self.n):
            for j in range(0, self.n):
                if self.game_board[i][j] == 'M':
                    for direc in DIRECTIONS:
                        if(self.is_valid(i+direc[0], j+direc[1]) and self.game_board[i+direc[0]][j+direc[1]] != 'M'):
                            self.game_board[i+direc[0]][j+direc[1]] += 1

    # Get random num_mines locations to place mines
    def __random_mines(self):
        mines = []
        for i in range(0, self.num_mines):
            row = random.randint(0, self.n-1)
            col = random.randint(0, self.n-1)
            while (row, col) in mines:
                row = random.randint(0, self.n-1)
                col = random.randint(0, self.n-1)
            mines.append((row, col))
        return mines

    # Print out the board
    def print_user_board(self, board):
        first_line = "  "
        for i in range(0, self.n):
            first_line = first_line + str(i) + " "
        print("\u0332".join(first_line))
        for i in range(0, self.n):
            row = str(i) + "|"
            for j in range(0, self.n):
                row = row + str(board[i][j]) + " "
            print(row)
