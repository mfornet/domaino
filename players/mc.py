""" Montecarlo agent

    TODO: Tune MCTS hyperparameters
"""
from player import BasePlayer
from domino import Event
from copy import deepcopy
from random import shuffle, choice
from math import log

import numpy as np

def canonical(piece):
    a, b = piece
    return max(a, b), min(a, b)


class MonteCarlo(BasePlayer):
    def __init__(self, name):
        super().__init__(f"Carlos::{name}")
        self.history_pointer = 0

    def my_init(self):
        self.my_pieces = deepcopy(self.pieces)
        self.remaining = [7] * 4

        self.pool = set()

        # For each player which number we know for sure it doesn't have
        # Its implemented using bitmask
        # TODO: Use it while sampling
        self.dont_have = [0] * 4

        for i in range(7):
            for j in range(i + 1):
                self.pool.add(canonical((i, j)))

        for piece in self.my_pieces:
            self.pool.remove(canonical(piece))

    def feed(self):
        # Save
        if self.history_pointer == 0:
            self.my_init()

        # Game simulation
        # team = self.position % 2
        while self.history_pointer < len(self.history):
            # Read and proc next event
            event, *args = self.history[self.history_pointer]
            self.history_pointer += 1

            if event == Event.MOVE:
                position, piece, head = args
                self.remaining[position] -= 1

                if position != self.position:
                    self.pool.remove(canonical(piece))

            elif event == Event.PASS:
                self.dont_have[position] |= 1 << self.heads[0]
                self.dont_have[position] |= 1 << self.heads[1]

            elif event == Event.NEW_GAME:
                pass
            else:
                raise ValueError(f"Invalid event: {event}")

    def sample(self):
        order = list(self.pool)
        shuffle(order)

        pieces = [[] for _ in range(4)]

        for pos in range(4):
            if pos == self.position:
                pieces[pos] = deepcopy(self.pieces)
            else:
                r = self.remaining[pos]
                pieces[pos] = order[:r]
                order = order[r:]

                assert len(pieces[pos]) == r

        assert len(order) == 0

        return pieces

    def choice(self):
        self.feed()

        NUM_SAMPLING = 10
        NUM_EXPANDED = 2000

        scores = {} # Score of each move (piece, head)
        winpredictions = {}

        # from pprint import pprint
        # pprint(self.history)

        from pprint import pprint
        for _ in range(NUM_SAMPLING):
            distribution = self.sample()
            cscores, cwinprediction = montecarlo(distribution, tuple(self.heads), self.position, NUM_EXPANDED)

            # pprint(cscores)

            for move, scr in cscores.items():
                scores[move] = scores.get(move, 0.) + scr

            for move, scr in cwinprediction.items():
                winpredictions[move] = winpredictions.get(move, 0.) + scr

        assert len(scores) > 0

        # pprint(scores)

        best_score = -1.
        best_move = None

        # for move, scr in scores.items():
        for move, scr in winpredictions.items():
            if scr > best_score:
                best_score = scr
                best_move = move

        # print(best_move)
        # assert False

        print("Score:", best_score / NUM_SAMPLING, winpredictions[move] / NUM_SAMPLING)

        return move

## Utils for Montecarlo

class Node:
    WIN_POINTS = 2
    TIE_POINTS = 1
    EXPLORATION = 2.

    def __init__(self, state):
        self.state = state

        self.visit_count = 0
        # Wins | Tie | Loose
        self.rate = [0, 0, 0]

        self.children = None
        self.end_node = None

    def score(self, parent_visit_count, me):
        if self.visit_count == 0:
            return float('inf')

        assert sum(self.rate) == self.visit_count

        if me: # Current player is from my team
            exploitation = self.rate[0] * Node.WIN_POINTS + self.rate[1] * Node.TIE_POINTS
        else:  # Current player is NOT from my team
            exploitation = self.rate[2] * Node.WIN_POINTS + self.rate[1] * Node.TIE_POINTS

        # Mean of all simulations so far
        exploitation /= self.visit_count

        exploration = Node.EXPLORATION * (log(parent_visit_count) / self.visit_count)**.5

        score = exploitation + exploration

        # print(f"!{exploitation} + !{exploration} = !{score}")

        return score


def intersect(pieceA, pieceB):
    """ Check if two 2-len tuples have at least one element in common
    """
    return pieceA[0] in pieceB or pieceA[1] in pieceB


def winner(state, position, distribution):
    """ Find winner in current state
    """
    WIN, TIE, LOOSE = 0, 1, 2

    team = position & 1
    mask, heads, pos = state

    winner_team = None

    light_hand = float('inf')
    light_player = set()

    for i in range(4):
        # Player `i` don't have any remaining piece
        if (mask >> (7 * i)) & ((1 << 7) - 1) == 0:
            winner_team = i & 1
            break

        hand = 0

        for j in range(7):
            if ((mask >> (i * 7 + j)) & 1):
                hand += sum(distribution[i][j])

        if hand < light_hand:
            light_hand = hand
            light_player = set()

        if hand == light_hand:
            light_player.add(i & 1)

    if winner_team is None:
        if len(light_player) == 2:
            return TIE

        winner_team = list(light_player)[0]

    return WIN if winner_team == team else LOOSE


def is_over(state, distribution):
    """ Check if game is over
    """
    mask, heads, pos = state

    exist_move = False

    for i in range(4):
        # Player `i` don't have any remaining piece
        if (mask >> (7 * i)) & ((1 << 7) - 1) == 0:
            return True

        for j in range(7):
            if ((mask >> (i * 7 + j)) & 1) and intersect(distribution[i][j], heads):
                exist_move = True

    return not exist_move


def neighbors(state, distribution):
    mask, heads, pos = state

    count = 0

    for i in range(7):
        # If player contains this piece yet
        if ((mask >> (7 * pos + i)) & 1) == 1:
            piece = distribution[pos][i]

            # If piece can be played throug head_0
            if heads[0] in piece or heads[0] == -1:
                nmask = mask ^ (1 << (7 * pos + i))
                nheads = (heads[0] ^ piece[0] ^ piece[1], heads[1])
                npos = (pos + 1) & 3 # % 4
                count += 1
                yield (nmask, nheads, npos)

            # If piece can be played throug head_1
            if heads[1] in distribution[pos][i]:
                nmask = mask ^ (1 << (7 * pos + i))
                nheads = (heads[0], heads[1] ^ piece[0] ^ piece[1])
                npos = (pos + 1) & 3
                count += 1
                yield (nmask, nheads, npos)

    # Player can't make any valid move other than passs
    if count == 0:
        npos = (pos + 1) & 3
        yield (mask, heads, npos)

def show(state):
    mask, heads, pos = state
    print(f"{bin(mask)} | {heads[0]} {heads[1]} | {pos}")


def montecarlo(distribution, heads, position, NUM_EXPANDED):
    """
        state: (bitmask, heads, pos)

        bitmask: 7 bits each player 2**28 states that denotes which pieces are still holding relative to `distribution`

        parent visit count:     PC
        visit count:            VC
        win count:              WC
        exploration control:    K

        WC / VC + K * sqrt(log(PC) / VC)
    """
    team = position & 1

    # print("Position:", position)
    # print([len(x) for x in distribution])
    # Compute first state
    mask = 0
    for dist in reversed(distribution):
        assert len(dist) <= 7
        mask <<= 7
        mask |= (1 << len(dist)) - 1
    heads = tuple(heads)
    pos = position

    start = (mask, heads, pos)

    # Intialize states for MonteCarlo Tree Search
    state_map = {start : Node(start)}

    # Run MonteCarlo
    iterations = 0

    # print("START")

    while True:
        iterations += 1
        # print(f"ITERATION: {iterations} | STATES: {len(state_map)}")

        # Stop condition
        if len(state_map) >= NUM_EXPANDED or \
            iterations >= 1e4:
            break

        # if iterations >= 1000:
        #     print(iterations, len(state_map))

        cur = start
        # path = [state_map[cur]]
        path = []

        # Traverse the tree search from the root down to one leaf
        while True:
            # show(cur)

            node = state_map[cur]
            path.append(node)

            if node.visit_count == 0:
                break

            best_score = float('-inf')
            best_child = None

            for child in node.children:
                scr = child.score(node.visit_count, (cur[2] & 1) == team)

                if scr > best_score:
                    best_score = scr
                    best_child = child

            assert best_child is not None

            cur = best_child.state


        # Expand `cur` children if needed
        if node.children is None:
            node.children = []
            for neig in neighbors(cur, distribution):
                child = Node(neig)

                node.children.append(child)
                state_map[neig] = child

        # print("SIMULATING FROM...")
        # show(cur)

        # Run simulation from `cur`
        while not is_over(cur, distribution):
            cur = choice(list(neighbors(cur, distribution)))

        w = winner(cur, position, distribution)

        # Update path with new information
        for s in path:
            s.visit_count += 1
            s.rate[w] += 1

    # Find action values
    root = state_map[start]
    answer = {}
    winprediction = {}

    for i, piece in enumerate(distribution[position]):
        if heads[0] in piece or heads[0] == -1:
            nmask = mask ^ (1 << (7 * position + i))
            nheads = (heads[0] ^ piece[0] ^ piece[1], heads[1])
            npos = (position + 1) & 3 # % 4

            nnode = state_map[(nmask, nheads, npos)]

            move = canonical(piece), 0
            answer[move] = nnode.visit_count / root.visit_count
            winprediction[move] = (nnode.rate[0] * 2 + nnode.rate[1]) / nnode.visit_count

        if heads[1] in piece:
            nmask = mask ^ (1 << (7 * position + i))
            nheads = (heads[0], heads[1] ^ piece[0] ^ piece[1])
            npos = (position + 1) & 3 # % 4

            nnode = state_map[(nmask, nheads, npos)]

            move = canonical(piece), 1
            answer[move] = nnode.visit_count / root.visit_count
            winprediction[move] = (nnode.rate[0] * 2 + nnode.rate[1]) / nnode.visit_count

    # from pprint import pprint
    # pprint(answer)
    # print(distribution[position])
    # assert(False)
    return answer, winprediction
