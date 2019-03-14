import random
import minimax
import minimax_domino
import domino_ux
import unittest

def generate_game(num_tokens, max_value, seed):
    rnd = random.Random(seed)
    tokens = []
    for i in range(4):
        row = []
        for j in range(num_tokens):
            x, y = rnd.randint(0, max_value), rnd.randint(0, max_value)
            if x > y: x, y = y, x
            row.append((x, y))
        tokens.append(row)
    return minimax_domino.Game(tokens)

class TestStringMethods(unittest.TestCase):
    def test_simple(self):
        # Simple hardcoded game for debugging
        game = minimax_domino.Game([
            [(0, 0), (1, 2)],
            [(0, 1), (2, 2)],
            [(1, 1), (0, 0)],
            [(0, 2), (0, 1)],
        ])

        mm = minimax.Minimax(game)
        state = game.first_state()
        value = mm.find(state)
        self.assertEqual(value, 1)

    def test_first_win(self):
        # First team wins
        game = generate_game(2, 2, 0)
        mm = minimax.Minimax(game)

        cur_state = game.first_state()
        first_value = mm.find(cur_state)

        # print(game.pieces)
        # print(first_value)
        # print(cur_state)

        while not game.is_over(cur_state):
            moves = mm.get_moves(cur_state)
            move = moves[0]
            cur_state = game.apply(cur_state, move)
            # print(moves)
            # print(">>", move)
            # print(cur_state)
            value = mm.find(cur_state)
            self.assertEqual(value, first_value)

    def test_second_win(self):
        # Second team wins
        game = generate_game(2, 2, 12)
        mm = minimax.Minimax(game)

        cur_state = game.first_state()
        first_value = mm.find(cur_state)

        # print(game.pieces)
        # print(first_value)
        # print(cur_state)

        while not game.is_over(cur_state):
            moves = mm.get_moves(cur_state)
            move = moves[0]
            cur_state = game.apply(cur_state, move)
            # print(moves)
            # print(">>", move)
            # print(cur_state)
            value = mm.find(cur_state)
            self.assertEqual(value, first_value)

    def test_large(self):
        # Game with max_value up to 6

        game = domino_ux.generate_game(seed=7)
        mm = minimax.Minimax(game)

        cur_state = game.first_state()
        first_value = mm.find(cur_state)

        # print(game.pieces)
        # print(first_value)
        # print(cur_state)

        while not game.is_over(cur_state):
            moves = mm.get_moves(cur_state)
            move = moves[0]
            cur_state = game.apply(cur_state, move)
            # print(moves)
            # print(">>", move)
            # print(cur_state)
            value = mm.find(cur_state)
            self.assertEqual(value, first_value)

if __name__ == '__main__':
    unittest.main()
