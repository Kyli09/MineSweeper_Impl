import argparse
from board import Board

def main(n, num_mines):
    # Start Game
    game = Board(n, num_mines)
    print("Game Start")
    # While the game is not over, continue ask for inputs
    while not game.check_win():
        game.print_user_board(game.user_board)
        row = input("Input row number of a covered square: ")
        col = input("Input column number of a covered square: ")

        # If the input row column pair is not valid, ask for input again
        while not row.isdigit() or not col.isdigit() or not game.is_valid_move(int(row), int(col)):
            print("Invalid index")
            row = input("Input row number of the square: ")
            col = input("Input column number of the square: ")
        row = int(row)
        col = int(col)
        # If the new move hits bomb, game is over. print out the board
        if not game.make_move(row, col):
            game.print_user_board(game.user_board)
            print("You Lost :(")
            quit()
    # If game is won, print out the board and end
    game.print_user_board(game.game_board)
    print("You Won!!!")
# DO NOT EDIT--------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('n', nargs='?', type=int, default=10)
    parser.add_argument('num_mines', nargs='?', type=int, default=10)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main(args.n, args.num_mines)

# DO NOT EDIT--------------------------------------------
