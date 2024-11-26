from typing import List, Tuple
from openai import OpenAI
from tictactoe import TicTacToe
import os
import numpy as np


def valid_moves(board: np.ndarray) -> List[Tuple[int, int]]:
    return [(i, j) for j in range(3) for i in range(3) if board[i, j] == 0]


def play_game() -> None:
    # This game will play until completion
    game: TicTacToe = TicTacToe()
    print("Initialized empty game")
    print(game)

    # Init the OpenAI client
    api_key: str | None = os.getenv("XAI_API_KEY")

    client: OpenAI = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
    )

    system_prompt: str = "You are a professional TicTacToe Player, You will be given a TicTacToe board and you need to respond with your prefered moves in 0 based indexing of rows and columns, respond in the form 'r c', that is a row and column seperated by a single space character, e.g. if I want to make the move 2, 2, I would just print 2 2"

    safety: int = 12

    # Game loop
    while not game.is_over() and safety != 0:
        # Get input for the moves
        safety -= 1
        try:
            if game.player == 1:
                grok_message: List = [
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": str(game) + "\n" + f"{valid_moves(game.board)=}",
                    },
                ]
                completions = client.chat.completions.create(
                    model="grok-beta",
                    messages=grok_message,
                )
                move = completions.choices[0].message.content
                if move is not None:
                    move = move.split()
                    print(f"Grok chooses {move}")
                else:
                    raise Exception
            else:
                move = input("Enter your move: ").split()

            move = (int(move[0]), int(move[1]))
            game.play_move(move)
            print(game)

        except Exception as e:
            print(e)
            print("Something went wrong, try again!")

    print("Game over!")

    if game.draw:
        print("It's a draw")
    elif game.player == 1:
        print("Grok wins!")
    else:
        print("You win :)")
    print(game)


play_game()
