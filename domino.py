import random
import json
import numpy as np

from jugador import BotaGorda, Aleatorio, Cantidad
from jugador_inteligente import Inteligente

from functools import partial
from pprint import pprint

# TODO: Pasar información del juego a todos los jugadores
# TODO: Unittest

class Domino:
    """
    Instancia para jugar una partida de domino en parejas.
    Usualmente hay dos configuraciones con las que se juega.

    Doble 6:
        FICHA_MAXIMA = 6
        FICHAS_POR_JUGADOR = 7

    Doble 9:
        FICHA_MAXIMA = 9
        FICHAS_POR_JUGADOR = 10
    """

    FICHA_MAXIMA = 6
    FICHAS_POR_JUGADOR = 7

    def __init__(self):
        self.logs = []

        # Iniciar las fichas
        self.fichas = []
        for i in range(Domino.FICHA_MAXIMA + 1):
            for j in range(i + 1):
                self.fichas.append((i, j))

        self.cabezas = [-1, -1]
        self.puntos_finales = None

    def log(self, *data):
        self.logs.append(data)

    def start(self, jugadores):
        self.logs.clear()

        # Inicializar mesa
        self.jugadores = jugadores
        for puesto, jugador in enumerate(self.jugadores):
            jugador.empieza_partida(puesto)

        self.cabezas = [-1, -1]
        self.log("nuevo juego")

        # Repartiendo las fichas
        random.shuffle(self.fichas)
        for i in range(Domino.FICHAS_POR_JUGADOR):
            for jugador in self.jugadores:
                jugador.repartiendo(self.fichas.pop(0))

        # Ejectuando el juego
        while True:
            se_tranco = True

            for puesto, jugador in enumerate(self.jugadores):
                # print(jugador.nombre)
                accion = jugador.jugar(self.cabezas)

                if not accion:
                    # El jugador no lleva ficha
                    self.log('no lleva', puesto)
                    continue

                se_tranco = False
                jugada, cabeza = accion

                if -1 in self.cabezas:
                    # Primera jugada de la partida
                    self.cabezas = list(jugada)
                    self.log('salida', puesto, jugada, cabeza)

                else:
                    assert self.cabezas[cabeza] in jugada

                    if jugada[0] == self.cabezas[cabeza]:
                        self.cabezas[cabeza] = jugada[1]
                    else:
                        self.cabezas[cabeza] = jugada[0]

                    self.log('jugada', puesto, jugada, cabeza)

                if len(jugador.fichas) == 0:
                    self.log('se pego', puesto)
                    self.log('gano', puesto % 2)

                    self.puntos_finales = [
                        jugador.sum() for jugador in self.jugadores
                    ]

                    return

            if se_tranco:
                self.log('se tranco')

                self.puntos_finales = [
                    jugador.sum() for jugador in self.jugadores
                ]

                equipo0 = min(self.puntos_finales[0], self.puntos_finales[2])
                equipo1 = min(self.puntos_finales[1], self.puntos_finales[3])

                if equipo0 < equipo1:
                    self.log('gano', 0)
                elif equipo1 < equipo0:
                    self.log('gano', 1)
                else:
                    self.log('empate')

                return

class JuegoSimple:
    """
    Se juega una sola partida. Si hay tablas gana el segundo jugador
    """

    def start(self, jugador0, jugador1):
        """
            Devuelve True si gano el jugador0 y False en caso contrario.
            Si la partida queda empate cuenta como victoria para el jugador1
        """
        jugadores = [jugador0(), jugador1(), jugador0(), jugador1()]
        domino = Domino()
        domino.start(jugadores)

        resultado = domino.logs[-1]
        # pprint(domino.logs)

        if resultado[0] == 'gano':
            return resultado[1] == 0
        return False

if __name__ == '__main__':
    juego = JuegoSimple()
    juego.start(partial(BotaGorda, "1"), partial(Aleatorio, "2"))

    # juegos = []
    # uno = Inteligente('3', [0.36760645349812066, 0.079849156030557131, 0.068292140445869134, 0.61909221402983905, 0.15014843724360663, 0.94146798512271024])
    # dos = Inteligente('3', [0.50319271, 0.89254, 0.05187015, 0.42540609, 0.19632677, 0.92883179])
    # tres = Inteligente('3', [0.50328748, 0.89258251, 0.05182548, 0.42549345, 0.19590833, 0.92901494])
    # jugadores = [BotaGorda('1'), Aleatorio('2'), tres, Cantidad('4')]

    # ganadores = [[jugadores[0].nombre, 0], [jugadores[1].nombre, 0], [jugadores[2].nombre, 0], [jugadores[3].nombre, 0]]

    # for i in range(500):
    #     juego = Domino(jugadores)
    #     ganador = juego.start()

    #     # indx = jugadores.index(ganador)
    #     # ganadores[indx] += 1

    #     for j in ganadores:
    #         if j[0] == ganador.nombre:
    #             j[1] += 1
    #             break

    #     juegos.append(juego.log)

    # info = json.dumps(juegos)
    # archivo = open('info.json', 'a+')
    # archivo.write(info)
    # archivo.close()
    # print(ganadores)
