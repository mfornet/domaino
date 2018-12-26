"""
    Script para calcular el ELO de varios players en un torneo.
"""

import random
import numpy as np

from players import BigDrop, Frequent, Random, SimpleHybrid
from domino import SimpleGame
from functools import partial


def select_pair(n):
    while True:
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        if a != b:
            return a, b


def tournament(players, engine):
    """ Compute ELO
    """
    tot = len(players)
    rounds = 160 * tot

    matches = np.zeros((tot, tot))
    wins = np.zeros(tot).astype(np.float)

    for _ in range(rounds):
        a, b = select_pair(tot)
        p0 = players[a]
        p1 = players[b]

        w = engine.start(p0, p1)

        matches[a, b] += 2
        matches[b, a] += 2

        if w == 0:
            wins[a] += 2.
        elif w == 1:
            wins[b] += 2.
        else:
            wins[a] += 1.
            wins[b] += 1.

    MEAN = 2300

    freqs = matches.sum(0)
    assert(min(freqs) > 0)

    reward = (wins / freqs - .5) * 850.

    elo = np.ones(tot) * MEAN

    if np.max(wins) - np.min(wins) < 1e-8:
        # No difference among players
        return elo

    it = 0

    while True:
        it += 1

        rival_mean = (matches * elo).sum(1) / freqs
        with_reward = rival_mean + reward

        with_reward -= with_reward.mean()
        with_reward /= with_reward.std()
        with_reward *= 100
        with_reward += 2300

        new_elo = with_reward

        if np.allclose(elo, new_elo):
            break

        elo = new_elo
        if it == 100:
            print(f"WARNING: Too many iterations: {elo}")
            break

    return elo


if __name__ == '__main__':
    players = [
        partial(BigDrop, "1"),
        partial(Random, "2"),
        partial(Frequent, "3"),
        partial(SimpleHybrid, "4", SimpleHybrid.PARAMETERS),
    ]

    engine = SimpleGame()
    elo = tournament(players, engine)

    stats = [(ply().name, scr) for ply, scr in zip(players, elo)]
    stats.sort(key=lambda x : -x[1])

    for nom, scr in stats:
        print(nom, round(scr))
