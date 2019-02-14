import random
from domino import Domino

class BaseRule:
    """
        Several matches of domino are played most of the time
        on particular rules to determine the winner. This is a
        wrapper to implement and play with different rules.
    """
    def run(self, players):
        """
            Return id of winner team (-1 for tie)
        """
        raise NotImplementedError()


class OneGame:
    """
        Play one game
    """
    def start(self, player0, player1):
        players = [player0("0"), player1("1"), player0("2"), player1("3")]
        env = Domino()
        env.start(players)
        return env.winner()


class TwoOfThree:
    """
        First to win two games. Last winner start next match
    """
    def __init__(self, random_start=True):
        self.random_start = random_start

    def start(self, player0, player1):
        players = [player0("0"), player1("1"), player0("2"), player1("3")]
        env = Domino()
        cur_start = 0

        if self.random_start:
            if random.choice([False, True]):
                cur_start ^= 1
                players[0], players[1] = players[1], players[0]
                players[2], players[3] = players[3], players[2]

        wins = [0, 0]

        while max(wins) < 2:
            env.start(players)
            result = env.winner()

            if result != -1:
                wins[result ^ cur_start] += 1

            if result == -1 or result != cur_start:
                # Swap players
                cur_start ^= 1
                players[0], players[1] = players[1], players[0]
                players[2], players[3] = players[3], players[2]

        return 0 if wins[0] > wins[1] else 1

RULES = [
    OneGame,
    TwoOfThree,
]