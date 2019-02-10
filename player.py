import random


class BasePlayer:
    """
        TODO: Explain information that have each player in order to implement their AIs
        Pieces
        History
        Heads
    """
    def __init__(self, name):
        self.name = name
        self.position = None
        self.pieces = []
        self.history = []
        self.heads = None

    def step(self, heads):
        should_pass = True

        if -1 in heads:
            # First move of the game
            should_pass = False
        else:
            for piece in self.pieces:
                if piece[0] in heads or piece[1] in heads:
                    should_pass = False
                    break

        if should_pass:
            # If player should pass because it doesn't have any valid piece
            return False

        self.heads = heads
        piece, head = self.choice()

        assert piece in self.pieces, f"Invalid piece: {piece}"
        self.pieces.remove(piece)

        return piece, head

    def valid(self, piece, head):
        """ Check if `piece` can be put on head `head`
        """
        return self.heads[head] == -1 or self.heads[head] in piece

    def start(self, position, pieces):
        self.position = position
        self.pieces = pieces

        self.history.clear()

    def log(self, data):
        self.history.append(data)

    def choice(self):
        """
            Logic of each agent. This function will be called from `step` when
            there is at least one valid piece. Notice that rules force player to
            always make a move whenever is possible.

            Player can access to current heads using `self.heads` or even full match history
            through `self.history`

            Return:
                piece:  (tuple<int>) Piece player is going to play. It must have it.
                head:   (int in {0, 1}) What head is it going to put the piece. This will be ignored in the first move.
        """
        raise NotImplementedError()

    def sum(self):
        """
            Current score of each player relative to the weights of its pieces
        """
        result = 0
        for piece in self.pieces:
            result += piece[0] + piece[1]
        return result

    @property
    def me(self):
        return self.position

    @property
    def partner(self, position=None):
        if position is None:
            position = self.me
        return position ^ 2

    @property
    def team(self, position=None):
        """ Players 0 and 2 belong to team 0
            Players 1 and 3 belong to team 1
        """
        if position is None:
            position = self.me
        return position & 1

    @property
    def next(self, position=None):
        """ Next player to play
        """
        if position is None:
            position = self.me
        return (position + 1) & 3
