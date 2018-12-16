from domino import Domino
from jugador_inteligente import Inteligente

import numpy as np

jugadores = []

for i in range(100):
    jugadores.append(Inteligente(str(i), np.random.rand(6)))

top_ten = []

for i in jugadores:
    top_ten.append([0, i])

count = 0

for i in range(100):
    for j in range(i+1, 100):
        for k in range(j+1, 100):
            for l in range(k+1, 100):
                juego = Domino([top_ten[i][1], top_ten[j][1], top_ten[k][1], top_ten[l][1]])
                count += 1

                ganador = juego.start()

                print('partido %s terminado' %(count))

                if ganador.nombre == top_ten[i][1].nombre:
                    top_ten[i][0] += 1
                elif ganador.nombre == top_ten[j][1].nombre:
                    top_ten[j][0] += 1
                elif ganador.nombre == top_ten[k][1].nombre:
                    top_ten[k][0] += 1
                elif ganador.nombre == top_ten[l][1].nombre:
                    top_ten[l][0] += 1

top_ten.sort()
top_ten.reverse()

for i in range(10):
    print(top_ten[i][1].coeficientes)