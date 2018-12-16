"""
    Script para calcular el ELO de varios jugadores en un torneo.
"""

import random
import numpy as np

def select_pair(n):
    while True:
        a = random.randint(0, n - 1)
        b = random.randint(0, n - 1)
        if a != b:
            return a, b

def tournament(players, engine):
    tot = len(players)
    rounds = 160 * tot

    matches = np.zeros((tot, tot))
    wins = np.zeros(tot).astype(np.float)

    for _ in range(rounds):
        a, b = select_pair(tot)
        p0 = players[a]
        p1 = players[b]

        w = engine.start(p0, p1)

        matches[a, b] += 1
        matches[b, a] += 1

        if w:
            wins[a] += 1.
        else:
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
    from jugador import BotaGorda, Aleatorio, Cantidad
    from jugador_inteligente import Inteligente
    from domino import JuegoSimple

    from functools import partial

    # Calcula el elo de los siguientes jugadores haciendo un torneo cerrado entre ellos
    jugadores = [
        partial(BotaGorda, "1"),
        partial(Aleatorio, "2"),
        partial(Cantidad, "3"),
        partial(Inteligente, "4.1", [0.36761, 0.07985, 0.06829, 0.61909, 0.15015, 0.94147]),
        partial(Inteligente, "4.2", [0.50319, 0.89254, 0.05187, 0.42541, 0.19633, 0.92883]),
        partial(Inteligente, "4.3", [0.50329, 0.89258, 0.05183, 0.42549, 0.19591, 0.92901]),
    ]

    engine = JuegoSimple()
    elo = tournament(jugadores, engine)

    stats = [(jug().nombre, pnt) for jug, pnt in zip(jugadores, elo)]
    stats.sort(key=lambda x : -x[1])

    for nom, pnt in stats:
        print(nom, round(pnt))
