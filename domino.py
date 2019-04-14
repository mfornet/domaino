import random

from pprint import pprint
from copy import deepcopy
from enum import Enum

from common.logger import add_logger, INFO

logger = add_logger("domino", INFO)


class Event(Enum):
    # Report beginning
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


class PlayerView:
    def __init__(self, pieces):
        self.pieces = pieces
        self.remaining = set(pieces)
        self.nums = {}
        # Doubles are counted twice
        for (x, y) in pieces:
            self.nums[x] = self.nums.get(x, 0) + 1
            self.nums[y] = self.nums.get(y, 0) + 1

    def have_num(self, num):
        return self.nums.get(num, 0) > 0

    def have_piece(self, piece):
        return piece in self.remaining

    def remove(self, piece):
        # Only call this function if the player has such piece
        self.remaining.remove(piece)
        (x, y) = piece
        self.nums[x] -= 1
        self.nums[y] -= 1

    def total(self):
        return len(self.remaining)

    def have_move(self, piece):
        (x, y) = piece
        return self.have_num(x) or self.have_num(y)

    def points(self):
        return sum(sum(piece) for piece in self.remaining)


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
        self.logs = None
        self.heads = None
        self.current_player = None
        self.winner = None

    def log(self, *data):
        event, *params = data
        # logger.info(f"{event.name}: {params}")
        self.logs.append(data)

    def get_pieces(self):
        return [player.pieces for player in self.players]

    def winner(self):
        assert self.logs[-1][0] == Event.WIN
        return self.logs[-1][1]

    def reset(self, max_number=6, pieces_per_player=7):
        self.max_number = max_number
        self.pieces_per_player = pieces_per_player
        self.players = hand_out(self.max_number, self.pieces_per_player)

        self.logs = []
        self.heads = [-1, -1]
        self.current_player = 0

        self.log(Event.NEW_GAME)

    def check_valid(self, action):
        # TODO: For intensive calculation disable check_valid.
        if action is None:
            return  self.heads[0] != -1 and \
                    not self.players[self.current_player].have_num(self.heads[0]) and \
                    not self.players[self.current_player].have_num(self.heads[1])
        else:
            piece, h = action
            return  0 <= piece[0] <= piece[1] <= self.max_number and \
                    self.players[self.current_player].have_piece(piece) and \
                    (self.heads[0] == -1 or self.heads[h] in piece)

    def _is_over(self):
        # It is the beginning of the game
        if self.heads[0] == -1:
            return False

        # There is one player with no pieces
        for i, player in enumerate(self.players):
            if player.total() == 0:

                self.winner = i % 2
                self.log(Event.FINAL, i)
                self.log(Event.WIN, self.winner)
                return True

        # At least one player can make a move
        for h in self.heads:
            if any([player.have_num(h) for player in self.players]):
                return False

        points = [player.points() for player in self.players]
        team0 = min(points[0], points[2])
        team1 = min(points[1], points[3])

        self.winner = -1 if team0 == team1 else int(team1 > team0)
        self.log(Event.OVER)
        self.log(Event.WIN, self.winner)
        return True

    def step(self, action):
        """
        `action` must be:

        * a tuple of the form `((a, b), h)` where `(a, b)` is the piece
          the current player is playing and `h` is the proper head.

        * None if the player have no valid piece.

        raise ValueError if it's an invalid move.
        """

        if not self.check_valid(action):
            raise ValueError("Invalid move.")

        if action is None:
            self.log(Event.PASS, self.current_player)
        else:
            piece, head = action
            v0, v1 = piece

            if -1 in self.heads:
                # First piece of the game (Head is ignored)
                self.heads = list(piece)
                head = 0
            else:
                if v0 == self.heads[head]:
                    self.heads[head] = v1
                else:
                    self.heads[head] = v0

            self.log(Event.MOVE, self.current_player, piece, head)
            self.players[self.current_player].remove(piece)

        self.current_player = (self.current_player + 1) % 4

        return self._is_over()

class DominoManager:
    def cur_player(self):
        return self.players[self.domino.current_player]

    def feed_logs(self):
        while self.logs_transmitted < len(self.domino.logs):
            data = self.domino.logs[self.logs_transmitted]
            for player in self.players:
                player.log(data)
            self.logs_transmitted += 1

    def run(self, players):
        self.logs_transmitted = 0
        self.players = players
        self.domino = Domino()

        self.domino.reset()

        for i, player in enumerate(players):
            player.reset(i, self.domino.players[i].pieces[:])

        done = False
        self.feed_logs()

        while not done:
            heads = self.domino.heads
            action = self.cur_player().step(heads[:])
            done = self.domino.step(action)
            self.feed_logs()

        return self.domino.winner

def hand_out(max_number, pieces_per_player):
    """
    Randomly distribute pieces among every player.
    Valid pieces are all integer tuples of the form:
        (i, j) 0 <= i <= j <= max_number
    Each player will have `pieces_per_player`.
    """
    pieces = [(i, j) for i in range(max_number + 1) for j in range(max_number + 1) if i <= j]
    assert 4 * pieces_per_player <= len(pieces)
    hand = random.sample(pieces, 4 * pieces_per_player)
    hands = [hand[i:i+pieces_per_player] for i in range(0, 4 * pieces_per_player, pieces_per_player)]
    return [PlayerView(h) for h in hands]
