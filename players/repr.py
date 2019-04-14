""" [WIP] This don't work with the new format
"""

from jugador import Jugador
from collections import OrderedDict
from copy import deepcopy

import numpy as np

class Representative(Jugador):
    """
    Características:

    * Valor
    * MasGorda
    * EsDoble
    ** Información del número que matas
    ** Información del número que pones
    ** Información del número que no tocas

    Número Características:
    * 0. Número
    * 1. Cuantos se han pasado rivales
    * 2. Cuantos se han pasado amigos
    * 3. Cuantos han matado rivales
    * 4. Cuantos han matado amigos
    * 5. Cuantos han puesto rivales [el doble cuenta como 2]
    * 6. Cuantos han puesto amigos [el doble cuenta como 2]
    * 7. Cuantos rivales han jugado por el otro lado
    * 8. Cuantos amigos han jugado por el otro lado
    * 9. Cuantas hay puestas en la mesa [el doble cuenta como 2]
    * 10. Cuantas yo tengo ahora mismo [el doble cuenta como 1]

    TODO: Incluir cual fue la salida
    """
    def __init__(self, nombre, coeficientes):
        Jugador.__init__(self, nombre)
        self.nombre = 'Repr_' + nombre

        self.coeficientes = coeficientes

        self.history_pointer = 0
        self.cabezas = [-1, -1]
        self.feat = [OrderedDict(
            number=i,
            rival_pass=0,
            friend_pass=0,
            rival_kill=0,
            friend_kill=0,
            rival_put=0,
            friend_put=0,
            rival_avoid=0,
            friend_avoid=0,
            on_table=0,
            have=0,
        ) for i in range(7)]

    def feed(self):
        # Simulación local del juego y calculo de características
        equipo = self.puesto % 2

        while self.history_pointer < len(self.historia):
            # Lee la próxima acción
            action, *args = self.historia[self.history_pointer]
            self.history_pointer += 1

            if action == "nuevo juego":
                continue

            elif action == "no lleva":
                us = args[0] % 2 == equipo
                for num in self.cabezas:
                    if us:
                        self.feat[num]['friend_pass'] += 1
                    else:
                        self.feat[num]['rival_pass'] += 1

            elif action == "salida":
                self.cabezas = list(args[1])
                us = args[0] % 2 == equipo
                for num in self.cabezas:
                    if us:
                        self.feat[num]['friend_put'] += 1
                    else:
                        self.feat[num]['rival_put'] += 1

                    self.feat[num]['on_table'] += 1

            elif action == "jugada":
                us = args[0] % 2 == equipo

                PUT, KILL = args[1]
                cabeza = args[2]

                if self.cabezas[cabeza] != KILL:
                    PUT, KILL = KILL, PUT

                assert self.cabezas[cabeza] == KILL
                self.cabezas[cabeza] = PUT
                AVOID = self.cabezas[cabeza ^ 1]

                if us:
                    self.feat[PUT]['friend_put'] += 1
                    self.feat[KILL]['friend_kill'] += 1
                    self.feat[AVOID]['friend_avoid'] += 1
                else:
                    self.feat[PUT]['rival_put'] += 1
                    self.feat[KILL]['rival_kill'] += 1
                    self.feat[AVOID]['rival_avoid'] += 1

                self.feat[PUT]['on_table'] += 1
                self.feat[KILL]['on_table'] += 1

            else:
                # Es imposible ver otra accion (y hacer una jugada)
                assert False

    def escoger_ficha(self, cabezas):
        self.feed()

        assert tuple(self.cabezas) == tuple(cabezas)

        num = np.zeros((7, 11))

        for i in range(7):
            kv = list(self.feat[i].items())
            for j in range(11):
                if 'have' == kv[j][0]:
                    # Don't use 'have' value from features
                    # but compute it again
                    continue
                num[i][j] = kv[j][1]

        for ficha in self.fichas:
            # Compute number of pieces that contains particular number
            A, B = ficha
            num[A][10] += 1

            # Don't compute double twice
            if A != B:
                num[B][10] += 1

        if -1 in cabezas:
            # This is first move
            final = None
            best_value = float('-inf')

            coef = np.array(self.coeficientes)
            mas_gorda_valor = sum(max(self.fichas, key=lambda f : sum(f)))

            for ficha in self.fichas:
                # Compute piece value
                x = np.zeros(36)
                x[0] = sum(ficha)
                x[1] = float(x[0] == mas_gorda_valor)
                x[2] = float(ficha[0] == ficha[1])

                PUT, KILL = ficha

                x[3:14] = num[KILL]
                x[14:25] = num[PUT]

                val = np.dot(x, coef)

                if val > best_value:
                    best_value = val
                    final = (ficha, 0)
        else:
            final = None
            best_value = float('-inf')

            coef = np.array(self.coeficientes)
            mas_gorda_valor = sum(max(self.fichas, key=lambda f : sum(f)))

            for ficha in self.fichas:
                # Compute piece value
                for cabeza in range(2):
                    if self.cabezas[cabeza] not in ficha:
                        continue

                    x = np.zeros(36)
                    x[0] = sum(ficha)
                    x[1] = float(sum(ficha) == mas_gorda_valor)
                    x[2] = float(ficha[0] == ficha[1])

                    PUT, KILL = ficha
                    if self.cabezas[cabeza] != KILL:
                        PUT, KILL = KILL, PUT

                    assert self.cabezas[cabeza] == KILL
                    AVOID = self.cabezas[cabeza ^ 1]

                    x[3:14] = num[KILL]
                    x[14:25] = num[PUT]
                    x[25:36] = num[AVOID]

                    # print(ficha, cabeza)
                    # print(x)

                    val = np.dot(x, coef)

                    if val > best_value:
                        best_value = val
                        final = (ficha, cabeza)

        # print(final)
        # exit(0)
        return final
