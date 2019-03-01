"""
    Explore the optimal strategy when participants play
    with the pieces uncovered.

    # TODO: Incompatible memoization + alphabeta prunning
    # TODO: CLI Interface is awful!
"""
TIE = 0
BEST_HAND = 1
NO_PIECE = 2

def can_play(head, piece):
    if head == piece[0]:
        return piece[1]
    if head == piece[1]:
        return piece[0]
    return None

def is_better(new_value, old_value, team):
    if old_value is None:
        return 2

    if new_value == old_value:
        return 1

    if team == 0:
        return 2 if new_value > old_value else 0
    else:
        return 0 if new_value < old_value else 0


def sign(value, team):
    return value if team == 0 else -value


def alphabeta_update(alpha, beta, value, team):
    if team == 0: # Maximizing team
        alpha = max(alpha, value)
    else: # Minimizing team
        beta = min(beta, value)
    return (alpha, beta)


class Minimax:
    def __init__(self, pieces):
        self.memo_value = {}
        self.memo_piece = {}
        self.pieces = pieces
        self.total = len(pieces[0])
        self.visited = 0

    def first_state(self):
        return (1 << 4 * self.total) - 1, (-1, -1), 0

    def compute_utils(self, state):
        max_number = max(max(piece) for pieces in self.pieces for piece in pieces)
        counter = [0] * (max_number + 1)

        mask, *_ = state

        for i, pieces in enumerate(self.pieces):
            for j, (x, y) in enumerate(pieces):
                if mask >> i * self.total + j & 1:
                    counter[x] += 1
                    counter[y] += 1

        return counter

    def best_score(self, mask):
        points = []
        for i in range(4):
            p = 0
            for j in range(self.total):
                if mask >> j & 1:
                    p += sum(self.pieces[i][j])
            points.append(p)
            mask >>= self.total
        team0 = min(points[0], points[2])
        team1 = min(points[1], points[3])
        return -1 if team0 == team1 else int(team1 < team0)

    def print_state(self, state):
        if self.visited % 100000 == 0:
            print(self.visited)
            mask, heads, player = state
            print(bin(mask), heads, player)

        self.visited += 1

    def is_over(self, state, utils=None):
        if utils is None:
            utils = self.compute_utils(state)

        mask, (h0, h1), cur_player = state
        team = cur_player & 1

        # Check game over
        # Previous player put its last piece
        previous = (cur_player + 3) & 3
        pmask = mask >> (previous * self.total)
        if pmask == pmask >> self.total << self.total:
            return sign(NO_PIECE, team)
        elif max(utils[h0], utils[h1]) == 0:
            winner = self.best_score(mask)
            if winner == -1:
                return TIE
            else:
                return sign(BEST_HAND, winner)
        return None

    def find(self, state, alpha, beta, utils=None):
        if state in self.memo_value:
            return self.memo_value[state]

        self.print_state(state)

        if utils is None:
            utils = self.compute_utils(state)

        mask, (h0, h1), cur_player = state
        team = cur_player & 1

        # Check game over
        # Previous player put its last piece
        value = self.is_over(state, utils)
        if value is not None:
            self.memo_value[state] = value
            return value

        best_value = None
        best_move = None

        if (h0, h1) == (-1, -1):
            # First move of the game
            assert(cur_player == 0)
            for i, piece in enumerate(self.pieces[0]):
                # Next state
                nh0 = min(piece)
                nh1 = max(piece)
                nmask = mask ^ (1 << + i)
                ncur_player = 1

                # Update utils
                utils[piece[0]] -= 1
                utils[piece[1]] -= 1

                # Compute next state value
                value = self.find((nmask, (nh0, nh1), ncur_player), alpha, beta, utils)

                # Rollback utils
                utils[piece[0]] += 1
                utils[piece[1]] += 1

                # Update best move
                status = is_better(value, best_value, team)

                if status == 2:
                    best_value = value
                    best_move = [(piece, 0)]

                if status == 1:
                    best_move.append((piece, 0))

                alpha, beta = alphabeta_update(alpha, beta, value, team)
                if alpha >= beta:
                    break
        else:
            p_mask = mask >> (cur_player * self.total)
            has_something = False
            for piece_index, piece in enumerate(self.pieces[cur_player]):
                bit = p_mask >> piece_index & 1
                if bit == 1:
                    for head_index, (ph0, ph1) in enumerate([(h0, h1), (h1, h0)]):
                        nhead = can_play(ph0, piece)
                        if nhead is not None:
                            # Player can move
                            has_something = True

                            # Next state
                            nh0 = min(nhead, ph1)
                            nh1 = max(nhead, ph1)
                            nmask = mask ^ (1 << (cur_player * self.total + piece_index))
                            ncur_player = (cur_player + 1) & 3

                            # Update utils
                            utils[piece[0]] -= 1
                            utils[piece[1]] -= 1

                            # Compute next state value
                            value = self.find((nmask, (nh0, nh1), ncur_player), alpha, beta, utils)

                            # Rollback utils
                            utils[piece[0]] += 1
                            utils[piece[1]] += 1

                            # Update best move
                            status = is_better(value, best_value, team)

                            if status == 2:
                                best_value = value
                                best_move = [(piece, head_index)]

                            if status == 1:
                                best_move.append((piece, head_index))

                            alpha, beta = alphabeta_update(alpha, beta, value, team)
                            if alpha >= beta:
                                break

            if not has_something:
                ncur_player = (cur_player + 1) & 3
                value = self.find((mask, (h0, h1), ncur_player), alpha, beta, utils)

                best_value = value
                best_move = []

        self.memo_value[state] = best_value
        self.memo_piece[state] = best_move

        return best_value

def run():
    domino = Domino()
    domino.reset()
    pieces = domino.get_pieces()
    minimax = Minimax(pieces)
    first_state = minimax.first_state()
    value = minimax.find(first_state, -2, 2)
    print(value)
    print(len(minimax.memo_value))


def apply(state, action, pieces):
    mask, heads, player = state
    h0, h1 = heads

    if action is None:
        return mask, heads, (player + 1) & 3

    piece, head = action

    ix = pieces[player].index(piece)
    assert (mask >> len(pieces[0]) * player + ix & 1) == 1
    assert heads[head] in list(piece) + [-1]
    mask ^= 1 << (len(pieces[0]) * player + ix)

    if heads[0] == -1:
        h0, h1 = piece
    elif head == 0:
        h0 ^= piece[0] ^ piece[1]
    else:
        h1 ^= piece[0] ^ piece[1]

    if h0 > h1:
        h0, h1 = h1, h0

    player = (player + 1) & 3

    return mask, (h0, h1), player


def get_move(state, pieces):
    print(state)
    mask, heads, player = state
    h0, h1 = heads

    print("Remaining piece:")
    for i, ps in enumerate(pieces):
        print(f"Player {i}:", end="")
        for j in range(len(ps)):
            if (mask >> (len(pieces[0]) * i + j)) & 1:
                print(f" {ps[j]}", end="")
        print()
    print("Heads:", heads)

    valid_moves = []
    index_moves = []
    cur_mask = mask >> len(pieces[0]) * player

    for i in range(len(pieces[0])):
        if cur_mask >> i & 1:
            p = pieces[player][i]
            if heads[0] == -1 or p[0] in heads or p[1] in heads:
                valid_moves.append(p)
                index_moves.append(i)

    if len(valid_moves) == 0:
        print("No valid move")
        return None

    print("Valid moves:", valid_moves)

    while True:
        print("Choose a valid move from the list.")
        print("For example to play the piece (1, 2) write 1 2")
        print("Notice that the order is important.")
        print("To specify the head write 1 2 1 to play the piece (1, 2) on the head 1.")
        print("Head will be detected automatically, in case two heads are valid and is unespecified, head 0 will be used.")

        print("")
        line = input(">>> ")

        try:
            values = tuple(list(map(int, line.split())))

            if len(values) == 2:
                assert values in valid_moves
                if h0 == -1 or h0 in values:
                    return values, 0
                elif h1 in values:
                    return values, 1
                else:
                    raise ValueError(f"Invalid piece: {piece}")

            elif len(values) == 3:
                piece = values[:2]
                head = values[2]
                assert piece in valid_moves
                assert h0 == -1 or heads[head] in piece
                return piece, head
            else:
                raise ValueError("Wrong number of parameters.")

        except Exception as e:
            print(e)
            continue

def play():
    import __init__
    from domino import Domino

    my_team = 0

    domino = Domino()
    domino.reset()

    pieces = domino.get_pieces()
    minimax = Minimax(pieces)

    state = minimax.first_state()

    while minimax.is_over(state) is None:
        mask, (h0, h1), player = state
        team = player & 1

        if team == my_team:
            piece = get_move(state, pieces)
        else:
            print("Thinking...")
            value = minimax.find(state, -2, 2)

            # This is wrong, it depends on who starts the game
            if value > 0:
                print("I'm sure I'll win this game.")
            elif value == 0:
                print("If you play good this game is ties.")
            else:
                print("You've got a chance to win.")

            moves = minimax.memo_piece[state]
            print("This are my better moves:")
            print(moves)
            piece = None if len(moves) == 0 else moves[0]

        if piece is None:
            print(f"Player {player} passed.")
        else:
            print(f"Player {player} put {piece}")

        state = apply(state, piece, pieces)


if __name__ == '__main__':
    play()