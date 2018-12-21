from jugador import Jugador

import numpy as np

# precomputation
ficha2ix = {}
pointer = 0
for i in range(7):
    for j in range(i + 1):
        ficha2ix[(i, j)] = pointer
        ficha2ix[(j, i)] = pointer
        pointer += 1


class Flat(Jugador):
    def __init__(self, nombre, coeficientes):
        Jugador.__init__(self, nombre)
        self.nombre = 'Flat_' + nombre

        assert len(coeficientes) == 29 * 28
        self.coeficientes = coeficientes

    def escoger_ficha(self, cabezas):
        M = np.reshape(self.coeficientes, (28, 29))

        x = np.zeros(29)
        x[28] = 1. # bias
        pnt = 0

        for ficha in self.fichas:
            p = ficha2ix[ficha]
            x[p] = 1.

        y = M @ x

        ficha_final = None
        best_value = float('-inf')

        for ficha in self.fichas:
            if -1 in cabezas or \
                ficha[0] in cabezas or \
                ficha[1] in cabezas:

                p = ficha2ix[ficha]
                v = y[p]

                if v > best_value:
                    best_value = v
                    ficha_final = ficha

        # Porque cabeza? (Hacer algo más inteligente cuando es capicua)
        cabeza = 0 if cabezas[0] in ficha_final else 1
        return ficha_final, cabeza
