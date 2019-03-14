from minimax import Minimax
from minimax_domino import Game
from random import Random

def generate_game(seed=None):
    rnd = Random(seed)

    tokens = [(j, i) for i in range(7) for j in range(i + 1)]
    assert len(tokens) == 28
    tokens = rnd.sample(tokens, 28)

    assigned_tokens = []
    while len(tokens) > 0:
        assigned_tokens.append(tokens[:7])
        tokens = tokens[7:]

    return Game(assigned_tokens)

def main():
    team = [0]
    game = generate_game(seed)
    cur_state = game.first_state()

    mm = Minimax(game)

    for tokens in game.pieces:
        print(tokens)

    first_value = mm.find(cur_state)

    while not game.is_over(cur_state):
        print(cur_state)
        value = mm.find(cur_state)
        print(value)

        moves = mm.get_moves(cur_state)
        move = moves[0]
        print(move)
        cur_state = game.apply(cur_state, move)

        assert first_value == value

if __name__ == '__main__':
    main()