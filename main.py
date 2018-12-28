#!/usr/bin/python3
from domino import SimpleGame
from players import BigDrop, Random, Frequent, SimpleHybrid, MonteCarlo
from functools import partial

# TODO: Add easy CLI

def allVsallReport(players, total):
    game = SimpleGame()

    for ix, player0 in enumerate(players):
        for iy, player1 in enumerate(players):
            winrate = [0, 0, 0]

            for _ in range(total):
                winner = game.start(player0, player1)
                winrate[winner] += 1

                if winner == 0:
                    print("WINNER:", player0().name)
                elif winner == 1:
                    print("WINNER:", player1().name)
                else:
                    print("TIE")

            print(f"{player0().name:12} {winrate[0]:2} - {winrate[2]:2} - {winrate[1]:2} {player1().name:12}")


if __name__ == '__main__':
    players = [
        # partial(BigDrop, "1"),
        partial(Random, "2"),
        # partial(Frequent, "3"),
        # partial(SimpleHybrid, "4", [0.613, 0.075, 0.171, 0.562, 0.007, 100]),
        partial(MonteCarlo, "5"),
    ]

    allVsallReport(players, 2)

