from board import Board
import argparse

def main(n, num_mines):
    # TODO: Write commandline game
    game = Board(n,num_mines)
    print("Game Start")
    # While the game is not over, continue ask for inputs
    while not game.check_win():
        game.print_user_board(game.user_board)
        row = int(input("Input row number of a covered square: "))
        col = int(input("Input column number of a covered square: "))

        # If the input row column pair is not valid, ask for input again
        while not game.is_valid_move(row, col):
            print("Invalid index")
            ow = int(input("Input row number of the square: "))
            col = int(input("Input column number of the square: "))

        # If the new move hits bomb, game is over. print out the board
        if game.make_move(row,col) == False:
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
