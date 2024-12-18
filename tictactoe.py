import numpy as np


EMPTY, PLAYER_X, PLAYER_O = 0, 1, 2
SYMBOLS = {EMPTY: ".", PLAYER_X: "X", PLAYER_O: "O"}


class TicTacToe:
    def __init__(self) -> None:
        self.board = np.zeros((3, 3), dtype=int)
        self.player = PLAYER_X
        self.draw = False

    def make_move_at_pos(self, pos) -> None:
        self.board[pos] = self.player

    def is_valid_move(self, move) -> bool:
        return self.board[move] == EMPTY

    def play_move(self, move) -> None:
        if self.is_valid_move(move):
            self.make_move_at_pos(move)
            if not self.is_over():
                self.player = PLAYER_X if self.player == PLAYER_O else PLAYER_O
        else:
            raise ValueError

    def is_over(self) -> bool:
        check = np.array([self.player] * 3)
        # Check rows, cols and diags
        for row in self.board:
            if np.all(row == check):
                return True
        for col in self.board.T:
            if np.all(col == check):
                return True
        for diag in [np.diag(self.board), np.diag(np.flip(self.board, 1))]:
            if np.all(diag == check):
                return True
        # Check for draw
        if not np.any(self.board == 0):
            self.draw = True
            return True
        return False

    def __str__(self) -> str:
        return "\n".join(
            [" ".join(SYMBOLS[int(mark)] for mark in row) for row in self.board]
        )


if __name__ == "__main__":
    game = TicTacToe()

    print(game.board)

    print("Testing make move of PLAYER_X at 0, 0")
    game.make_move_at_pos((0, 0))
    print(game.board)

    print("Testing making move of PLAYER_O at 0, 1")
    game.player = PLAYER_O
    game.make_move_at_pos((0, 1))
    print(game.board)

    print(game.is_over())

    # Testing new game

    print("Starting a fresh game")
    game = TicTacToe()

    while not game.is_over():  # Iterate while game is not over
        # Print player turn and game state
        print(f"It is time for {SYMBOLS[game.player]} to play")
        print(game)

        try:
            move = input().split()
            move = int(move[0]), int(move[1])
            game.play_move(move)
        except ValueError:
            print("Invalid position")
        except IndexError:
            print("Try to be in range")

    print("Game over")
    print(game)
