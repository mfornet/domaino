from domino import Domino
from jugador_inteligente import Inteligente

import random
import string
import copy
import numpy as np


class tester:
    def __init__(self):
        self.jugadores = []
        self.top_ten = []
        self.juegos_jugados = []

        for i in range(100):
            self.jugadores.append(Inteligente(str(i), np.random.rand(6)))

    def prueba(self):

        # corriendo 50 torneos y en cada torneo cada jugador juega 20 veces
        for torneo in range(50):

            self.top_ten = []
            self.juegos_jugados = []

            for jugador in self.jugadores:
                self.top_ten.append([0, jugador])
                self.juegos_jugados.append([0, jugador])

            count = 0
            # corriendo un torneo de 20 juegos por jugador
            while len(self.juegos_jugados) > 3:
                # tomo 4 jugadores random para jugar este juego
                lista = random.sample(self.juegos_jugados, 4)

                # le incremento en 1 los juegos jugados y si ya son 20
                # los elimino para no tomarlos en la proxima ronda
                for i in lista:
                    indx = self.juegos_jugados.index(i)
                    self.juegos_jugados[indx][0] += 1

                    if(self.juegos_jugados[indx][0] == 20):
                        self.juegos_jugados.remove(self.juegos_jugados[indx])

                # inicio el juego
                juego = Domino([lista[0][1], lista[1][1], lista[2][1], lista[3][1]])

                # corro el juego
                ganador = juego.start()
                count += 1
                print('juego %s terminado' %(count))

                # le aumento los juegos ganados en uno al ganador
                for i in self.top_ten:
                    if i[1].nombre == ganador.nombre:
                        i[0] += 1
                        break

            # aqui se termino el while
            # quitar los 10 peores y duplicar los 10 mejores con cambios chiquitos

            # tomo los 10 mejores y los 10 peores
            self.top_ten.sort(key=lambda x: x[0], reverse=True)

            mejores = self.top_ten[:10]

            if (torneo + 1) % 5 == 0:
                print(torneo + 1, np.round(mejores[0][1].coeficientes, 5))

            peores = self.top_ten[90:100]

            # busco los 10 peores en el array de jugadores y los reemplazo por
            # 10 nuevos jugadores. Estos 10 nuevos son los que quedaron en mejores
            # posiciones en este torneo pero con algun cambio
            for i in range(10):
                self.jugadores.remove(peores[i][1])
                new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                self.jugadores.append(Inteligente(new_name,
                                      mejores[i][1].coeficientes + (np.random.randn(6) * 0.0001)))

                # self.jugadores.append(Inteligente(str(indx) + '_' + str(torneo),
                #                       mejores[i][1].coeficientes + (np.random.randn(6) * 0.0001)))


if __name__ == '__main__':
    probando = tester()
    probando.prueba()

    # result = sorted(probando.top_ten, key=lambda x: x[0], reverse=True)
    # archivo = open('partidos2.domino', 'a+')

    # archivo.write('\n**********Nuevos jugadores inteligentes**********\n')

    # for i in result:
    #     archivo.write('gano:%s\ncoeficientes:%s\n' %(i[0], list(i[1].coeficientes)))

    # archivo.close()