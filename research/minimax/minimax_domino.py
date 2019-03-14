"""
    One state
    bitmask: all active pieces
    (h0, h1): head0 and head1
    participant: Current participant to play
"""

def get(mask, k):
    return (mask >> k) & 1

class Game:
    def __init__(self, pieces):
        self.pieces = pieces
        self.num_pieces = len(pieces[0])

        self._value = None
        self._pieces_mask = (1 << self.num_pieces) - 1
        self._active_states = dict()

    def first_state(self):
        return (
            (1 << (self.num_pieces * 4)) - 1,
            (None, None),
            0
        )

    def is_max_turn(self, state):
        _, _, position = state
        team = position & 1
        return team == 0

    def is_over(self, state):
        mask, (h0, h1), _ = state

        if h0 is None: # First move
            return False

        self._value = None

        for part in range(4):
            p_mask = mask >> (self.num_pieces * part)
            p_mask &= self._pieces_mask

            if p_mask == 0:
                # Participant `part` doesn't have more pieces
                team = part & 1
                self._value = 1 if team == 0 else -1
                return True

        # Find if someone have a valid move
        score = [0, 0, 0, 0]
        tmp_mask = mask
        for i in range(4):
            for j in range(self.num_pieces):
                if get(mask, 0):
                    score[i] += sum(self.pieces[i][j])

                    if h0 in self.pieces[i][j] or \
                        h1 in self.pieces[i][j]:
                        return False

                mask >>= 1

        # Find player with less score
        team0 = min(score[0], score[2])
        team1 = min(score[1], score[3])

        if team0 < team1:
            self._value = 1
        elif team1 < team0:
            self._value = -1
        else:
            self._value = 0
        return True

    def get_value(self, state):
        value = self._value
        self._value = None
        return value

    def apply(self, state, move):
        mask, _, turn = state
        if move == "PASS":
            return self._apply(state, move)
        token, h = move
        ix = 0
        p_mask = mask >> (turn * self.num_pieces)
        while ix < self.num_pieces and (get(p_mask, ix) == 0 or self.pieces[turn][ix] != token):
            ix += 1
        assert ix < self.num_pieces
        return self._apply(state, (ix, h))

    def _apply(self, state, move):
        mask, heads, turn = state
        if move == "PASS":
            return mask, heads, (turn + 1) % 4
        ix, h = move
        token = self.pieces[turn][ix]
        assert (None in heads and h == 0) or heads[h] in token
        x, y = token

        if None in heads:
            heads = list(token)
            assert heads[0] <= heads[1]
        else:
            heads = list(heads)
            heads[h] ^= x ^ y
            if heads[1] < heads[0]:
                heads = [heads[1], heads[0]]
        heads = tuple(heads)
        mask ^= 1 << (self.num_pieces * turn + ix)
        turn = (turn + 1) % 4

        new_state = mask, heads, turn
        return new_state

    def _convert(self, state, move):
        if move == "PASS":
            return "PASS"
        _, _, turn = state
        ix, h = move
        return tuple(self.pieces[turn][ix]), h

    def next_move(self, state, cur_position):
        if not state in self._active_states:
            # Compute all valid moves only the first time for each state
            moves = []

            mask, (h0, h1), turn = state
            p_mask = mask >> (turn * self.num_pieces)

            for i in range(self.num_pieces):
                if get(p_mask, 0) == 1:
                    if h0 is None or h0 in self.pieces[turn][i]:
                        moves.append((i, 0))
                    if h1 in self.pieces[turn][i]:
                        moves.append((i, 1))

                p_mask >>= 1

            if len(moves) == 0:
                moves.append("PASS")

            self._active_states[state] = moves

        moves = self._active_states[state]
        cur_move = moves[cur_position]
        new_state = self._apply(state, cur_move)

        cur_position += 1

        if cur_position == len(self._active_states[state]):
            del self._active_states[state]
            cur_position = None

        return (self._convert(state, cur_move), new_state, cur_position)
