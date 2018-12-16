import random
import json
import numpy as np

from jugador import BotaGorda, Aleatorio, Cantidad
from jugador_inteligente import Inteligente

class Domino:
    def __init__(self, jugadores):
        self.jugadores = jugadores

        random.shuffle(self.jugadores) # esto es mejor hacerlo abajo
                                       # para poder controlar los jugadores
                                       # y el orden de los mismos

        self.fichas = []
        self.log = []

        for i in range(7):
            for j in range(i + 1):
                self.fichas.append((i, j))

        self.cabeza1 = -1
        self.cabeza2 = -1

    def start(self):
        random.shuffle(self.fichas)

        # print(self.fichas)

        for i in range(7):
            for jugador in self.jugadores:
                jugador.repartiendo(self.fichas.pop(0))

        while 1:

            se_tranco = True
            jugada_invalida = False
            se_pego = False

            for jugador in self.jugadores:
                # print(jugador.nombre)
                jugada = jugador.jugar(self.cabeza1, self.cabeza2)

                if self.cabeza1 == -1 and self.cabeza2 == -1:
                    se_tranco = False
                    self.cabeza1 = jugada[0]
                    self.cabeza2 = jugada[1]
                    self.log.append(('salida', jugador.nombre, jugada))
                elif jugada:
                    if jugada[0] == self.cabeza1 or jugada[0] == self.cabeza2 or \
                      jugada[1] == self.cabeza1 or jugada[1] == self.cabeza2:
                        se_tranco = False
                        if jugada[0] == self.cabeza1:
                            self.log.append(('jugada', jugador.nombre, 'cabeza1', jugada))
                            self.cabeza1 = jugada[1]
                        elif jugada[1] == self.cabeza1:
                            self.log.append(('jugada', jugador.nombre, 'cabeza1', jugada))
                            self.cabeza1 = jugada[0]
                        elif jugada[0] == self.cabeza2:
                            self.log.append(('jugada', jugador.nombre, 'cabeza2', jugada))
                            self.cabeza2 = jugada[1]
                        elif jugada[1] == self.cabeza2:
                            self.log.append(('jugada', jugador.nombre, 'cabeza2', jugada))
                            self.cabeza2 = jugada[0]
                    else:
                        self.log.append('jugada_invalida')
                        self.log.append((self.cabeza1, self.cabeza2, jugada))
                        jugador.jugada_invalida(jugada, self.cabeza1, self.cabeza2)
                        jugada_invalida = True
                        break
                else:
                    self.log.append(('no_lleva', jugador.nombre, self.cabeza1, self.cabeza2))

                if len(jugador.fichas) == 0:
                    self.log.append(('se_pego', jugador.nombre))
                    self.log.append(('gano', jugador.nombre))
                    return jugador

            if se_tranco:
                self.log.append(('se_tranco'))

                ganador = []
                mano = 2**32

                for jugador in self.jugadores:
                    if jugador.sum() < mano:
                        ganador = [jugador]
                    elif jugador.sum() == mano:
                        ganador.append(jugador)

                if len(ganador) == 1:
                    self.log.append(('gano', ganador[0].nombre))
                    return ganador[0]
                elif len(ganador) > 1:
                    ganadores = ''
                    for i in ganador:
                        ganadores += i.nombre + ' '

                    self.log.append(('empate', ganadores))
                    return ganadores
            elif jugada_invalida or se_pego:
                break

if __name__ == '__main__':
    juegos = []
    uno = Inteligente('3', [0.36760645349812066, 0.079849156030557131, 0.068292140445869134, 0.61909221402983905, 0.15014843724360663, 0.94146798512271024])
    dos = Inteligente('3', [0.50319271, 0.89254, 0.05187015, 0.42540609, 0.19632677, 0.92883179])
    tres = Inteligente('3', [0.50328748, 0.89258251, 0.05182548, 0.42549345, 0.19590833, 0.92901494])
    jugadores = [BotaGorda('1'), Aleatorio('2'), tres, Cantidad('4')]
    ganadores = [[jugadores[0].nombre, 0], [jugadores[1].nombre, 0], [jugadores[2].nombre, 0], [jugadores[3].nombre, 0]]
    
    for i in range(500):
        juego = Domino(jugadores)
        ganador = juego.start()

        # indx = jugadores.index(ganador)
        # ganadores[indx] += 1

        for j in ganadores:
            if j[0] == ganador.nombre:
                j[1] += 1
                break

        juegos.append(juego.log)

    info = json.dumps(juegos)
    archivo = open('info.json', 'a+')
    archivo.write(info)
    archivo.close()
    print(ganadores)


'''
game con step(ficha, cabeza), restart
openai gym 

llevar
'''