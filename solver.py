# Return a boolean indicating if the board was successfully solved.
import random
import collections

DIRECTIONS = [(1, 0), (-1, 0), (0, -1), (0, 1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

def search_sorrounding(board, i, j, mines, covered_not_mine_cell, potential_bomb_cell):
    # Covered cells around this cell
    covered_surrounding = []
    # Mines around this cell
    mine_count = 0

    for direc in DIRECTIONS:
        if board.is_valid_move(i+direc[0], j+direc[1]) and (i+direc[0], j+direc[1]) not in mines:
            covered_surrounding.append((i+direc[0], j+direc[1]))
        elif (i+direc[0], j+direc[1]) in mines:
            mine_count += 1

    # If number of mines around this cell equal the number in the cell,
    # all the other cells around the cell are definitely not mines
    if mine_count == board.user_board[i][j]:
        covered_not_mine_cell += covered_surrounding
    # If number of mines + number of covered surrounding cells equal the number
    # All the covered surrounding cells are bombs
    if (len(covered_surrounding) + mine_count) == board.user_board[i][j]:
        mines += covered_surrounding
    # Else those surrounding cells probably contain bombs
    else:
        potential_bomb_cell += covered_surrounding


def solve(board) -> bool:
    # All the mine cells
    mines = []
    # First move: make a random first move
    row = random.randint(0, board.n-1)
    col = random.randint(0, board.n-1)
    board.make_move(row, col)

    while not board.check_win():

        found_mine = len(mines)
        first = True

        # If new mines are found from this round or this is the first time searching after last move
        while first or len(mines) != found_mine:
            # update the number of mines found before this round
            first = False
            found_mine = len(mines)
            # Potential_cells are cells around any number and probability contain a bomb
            potential_bomb_cell = []
            # Cell that is covered and definitely not bombs
            covered_not_mine_cell = []
            # All the covered cells in the board
            covered_cell = []
            for i in range(0, board.n):
                for j in range(0, board.n):
                    # if the cell contains a number, check its surrounding
                    if board.user_board[i][j] != 'X' and board.user_board[i][j] != '.':
                        search_sorrounding(board, i, j, mines, covered_not_mine_cell, potential_bomb_cell)
                    if board.user_board[i][j] == 'X' and (i, j) not in mines:
                        covered_cell.append((i, j))
            # Remove duplicates in the list
            covered_not_mine_cell = list(dict.fromkeys(covered_not_mine_cell))

        # If there are cells that are definitely not mines, make all those moves
        if covered_not_mine_cell:
            for cell in covered_not_mine_cell:
                board.make_move(cell[0], cell[1])
        # Else if there are some potential cells, pick the least common one from the list
        # More frequent cell means it is voted by more cells, which means it is more likely to contain bombs
        elif potential_bomb_cell:
            least_common = collections.Counter(potential_bomb_cell).most_common()[-1][0]
            result = board.make_move(least_common[0], least_common[1])
            if not result:
                return False
        # Else make a random move
        else:
            random_cell = random.randint(0, len(covered_cell)-1)
            result = board.make_move(covered_cell[random_cell][0], covered_cell[random_cell][1])
            if not result:
                return False
    return True
