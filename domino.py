import random

from pprint import pprint
from copy import deepcopy
from enum import Enum

from common.logger import add_logger, INFO

logger = add_logger("domino", INFO)

class Event(Enum):
    # Report begining
    # params: ()
    NEW_GAME = 0

    # Player don't have any valid piece
    # params: (position)
    PASS = 1

    # Player makes a move
    # params: (position, piece, head)
    MOVE = 2

    # Last piece of a player is put
    # params: (position)
    FINAL = 3

    # None player has a valid piece
    # params: ()
    OVER = 4

    # Report winner
    # params: (team) team=0(First team) team=1(Second team) team=-1(Tie)
    WIN = 5

class Domino:
    """
    Instance that contains the logic of a single match.
    There are usually two main formats as showed below:

    Format 1:
        MAX_NUMBER = 6
        PIECES_PER_PLAYER = 7

    Format 2:
        MAX_NUMBER = 9
        PIECES_PER_PLAYER = 10
    """
    MAX_NUMBER = 6
    PIECES_PER_PLAYER = 7

    def __init__(self):
        self.logs = []
        self.players = None

        self.heads = [-1, -1]
        self.score = None

    def log(self, *data):
        event, *params = data
        logger.info(f"{event.name}: {params}")
        self.logs.append(data)
        for player in self.players:
            player.log(deepcopy(data))

    def winner(self):
        assert self.logs[-1][0] == Event.WIN
        return self.logs[-1][1]

    def start(self, players):
        # Intialize match
        self.logs.clear()

        pieces = []
        for i in range(Domino.MAX_NUMBER + 1):
            for j in range(i + 1):
                pieces.append((i, j))

        self.players = players
        random.shuffle(pieces)

        for position, player in enumerate(self.players):
            begin = Domino.PIECES_PER_PLAYER * position
            end = begin + Domino.PIECES_PER_PLAYER
            player.start(position, pieces[begin:end])

        self.heads = [-1, -1]
        self.log(Event.NEW_GAME)

        # Ejectuando el juego
        while True:
            is_over = True

            for position, player in enumerate(self.players):
                action = player.step(self.heads)

                if not action:
                    # Player doesn't have any valid piece
                    self.log(Event.PASS, position)
                    continue

                is_over = False
                piece, head = action

                if -1 in self.heads:
                    # First piece of the game (Head is ignored)
                    self.heads = list(piece)
                    head = 0
                    self.log(Event.MOVE, position, piece, head)
                else:
                    assert self.heads[head] in piece

                    if piece[0] == self.heads[head]:
                        self.heads[head] = piece[1]
                    else:
                        self.heads[head] = piece[0]

                    self.log(Event.MOVE, position, piece, head)

                if len(player.pieces) == 0:
                    team = position % 2

                    self.log(Event.FINAL, position)
                    self.log(Event.WIN, team)
                    self.score = [player.score() for player in self.players]

                    return

            if is_over:
                self.log(Event.OVER)
                self.score = [player.score() for player in self.players]

                team0 = min(self.score[0], self.score[2])
                team1 = min(self.score[1], self.score[3])

                if team0 < team1:
                    self.log(Event.WIN, 0)
                elif team1 < team0:
                    self.log(Event.WIN, 1)
                else:
                    self.log(Event.WIN, -1)

                break
