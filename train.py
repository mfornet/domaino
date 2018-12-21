"""
    Script para entrenar un jugador paramétrico usando diferentes
    métodos de optimización.
"""

import string
import random
import numpy as np
import json

from domino import JuegoSimple
from functools import partial
from pprint import pprint

from jugador import BotaGorda, Aleatorio
from jugador_inteligente import Inteligente

def randname():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def stress_tourney(jugador0, jugador1, rounds):
    engine = JuegoSimple()

    win_jugador0 = 0
    win_jugador1 = 0

    for j in range(rounds):
        w = engine.start(jugador0, jugador1)
        if w:
            win_jugador0 += 1
        else:
            win_jugador1 += 1

        w = engine.start(jugador1, jugador0)
        if w:
            win_jugador1 += 1
        else:
            win_jugador0 += 1

    jugador0_winrate = win_jugador0 / (win_jugador1 + win_jugador0)

    return jugador0_winrate, win_jugador0, win_jugador1

def ga_train(smart, size):
    """
        Genetic algorithm

        P := sample POPULATION_SIZE players

        repeat ITERATIONS times:
            run a tourney with P
            drop last ELITISM players
            clone first ELITISM players
            mutate all elements but first ELISTIM players
    """
    POPULATION_SIZE = 100
    ITERATIONS = 100
    ELITISM = 10
    PERSONAL_MATCHES = 1

    population = [
        partial(smart, f"{randname()}_g0", np.random.randn(size))
        for _ in range(POPULATION_SIZE)
    ]

    engine = JuegoSimple()

    saved = []

    botagorda = partial(BotaGorda, "A")
    aleatorio = partial(Aleatorio, "B")
    inteligente = partial(Inteligente, "C", [0.613, 0.075, 0.171, 0.562, 0.007, 2.127])

    for generation in range(1, ITERATIONS + 1):
        winrate = [0] * POPULATION_SIZE

        for i in range(POPULATION_SIZE):
            for j in range(POPULATION_SIZE):
                if i == j:
                    # Avoid games against themselves
                    continue

                for _ in range(PERSONAL_MATCHES):
                    w = engine.start(population[i], population[j])

                    if w:
                        winrate[i] += 1
                    else:
                        winrate[j] += 1

        order = list(range(POPULATION_SIZE))
        order.sort(key=lambda x : -winrate[x])

        print("generation:", generation)

        cur_generation = []
        for u in order[:10]:
            x = population[u]()
            cur_generation.append(list(x.coeficientes))
        saved.append(cur_generation)

        with open('flat.json', 'w') as f:
            json.dump(saved, f)

        against_botagorda, _, _ = stress_tourney(population[order[0]], botagorda, 500)
        against_aleatorio, _, _ = stress_tourney(population[order[0]], aleatorio, 500)
        against_inteligente, _, _ = stress_tourney(population[order[0]], inteligente, 500)

        print("Vs Botagorda:", against_botagorda)
        print("Vs Aleatorio:", against_aleatorio)
        print("Vs Inteligente:", against_inteligente)
        print("Winnings:", [winrate[order[i]] for i in range(10)])

        new_population = []

        for i, u in enumerate(order):
            # Keep this element untouched
            if i < ELITISM:
                new_population.append(population[u])
            else:
                # Magic
                ru = u % (POPULATION_SIZE - ELITISM)
                # Mutate the element
                coef = population[ru]().coeficientes + np.random.randn(size) * .001
                new_population.append(partial(smart, f"{randname()}_g{generation}", coef))

        population = new_population


def hc_train(smart, start_coef):
    size = len(start_coef)
    champion = partial(smart, f"0", start_coef)

    entropy = .1 # Adaptive parameter
    max_entropy = 1.
    min_entropy = 1e-9
    entropy_step = .1

    last_update = 0
    step = 0

    botagorda = partial(BotaGorda, "A")
    aleatorio = partial(Aleatorio, "B")
    inteligente = partial(Inteligente, "C", [0.613, 0.075, 0.171, 0.562, 0.007, 2.127])

    while last_update < 100:
        step += 1

        if step % 10 == 0:
            print("Step:", step)

        coef = champion().coeficientes
        new_coef = coef + np.random.randn(size) * entropy
        runnerup = partial(smart, f"{step}", new_coef)

        runnerup_winrate, win_runnerup, win_champion = stress_tourney(runnerup, champion, 100)

        if runnerup_winrate > .5:
            against_botagorda, _, _ = stress_tourney(runnerup, botagorda, 500)
            against_aleatorio, _, _ = stress_tourney(runnerup, aleatorio, 500)
            against_inteligente, _, _ = stress_tourney(runnerup, inteligente, 500)

            print()
            print("New champion", step)
            print("Entropy:", entropy)
            print("Vs Champion:", runnerup_winrate)
            print("Vs Botagorda:", against_botagorda)
            print("Vs Aleatorio:", against_aleatorio)
            print("Vs Inteligente:", against_inteligente)
            print("Coeficientes:", list(np.round(runnerup().coeficientes, 5)))

            champion = runnerup

            entropy *= entropy_step
            entropy = max(entropy, min_entropy)
            last_update = 0
        else:
            entropy /= entropy_step
            entropy = min(entropy, max_entropy)
            last_update += 1



if __name__ == '__main__':
    # from jugador_inteligente import Inteligente
    # hc_train(Inteligente, [0.50329, 0.89258, 0.05183, 0.42549, 0.19591, 0.92901])

    # from jugador_flat import Flat
    # ga_train(Flat, 29 * 28)

    from jugador_repr import Representative
    # coef = np.random.randn(36)
    # coef = [4.33155, -1.95039, 0.86886, 5.17118, -3.70478, -1.05104, -3.54993, -4.57235, -1.36722, -1.80682, 0.87752, 1.9287, -3.91754, -2.53528, -0.05774, 0.0305, 3.70932, -4.20921, -3.98664, -1.84458, 2.55967, 1.5355, -1.62214, 2.42899, 4.24328, 0.90884, 2.36867, 0.85975, -2.81101, 1.53614, 3.04473, 4.41307, 0.10467, 0.23337, 1.06082, -0.47875]
    # hc_train(Representative, coef)
    ga_train(Representative, 36)
