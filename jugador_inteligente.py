import numpy as np
from jugador import Jugador


class Inteligente(Jugador):
    def __init__(self, nombre, coeficientes):
        Jugador.__init__(self, nombre)

        self.nombre = 'Inteligente_' + nombre
        self.coeficientes = coeficientes

    def __eq__(self, other):
        return self.nombre == other.nombre

    def __repr__(self):
        return self.nombre

    def eval_aleatorio(self, ficha):
        return 1

    def eval_bota_gorda(self, ficha):
        sums = []
        mayor = 0
        count = 1

        for _ficha in self.fichas:
            if _ficha[0] + _ficha[1] > mayor:
                mayor = _ficha[0] + _ficha[1]
                count = 1
            if _ficha[0] + _ficha[1] == mayor:
                count += 1

        if ficha[0] + ficha[1] == mayor:
            return 1. / count
        else:
            return 0

    def eval_bota_gorda_suave(self, ficha):
        return ficha[0] + ficha[1]

    def eval_no_pase(self, ficha):
        mayor = 0
        cantidad = []

        for i in self.fichas:
            count = 0
            for j in self.fichas:
                if i[0] == j[0] or i[0] == j[1] or i[1] == j[0] or i[1] == j[1]:
                    count += 1
            cantidad.append(count)

            if count > mayor:
                mayor = count

        _count = 0
        for i in cantidad:
            if i == mayor:
                _count += 1

        index = self.fichas.index(ficha)
        if cantidad[index] == mayor:
            return 1/_count
        else:
            return 0

    def eval_no_pase_suave(self, ficha):
        count = 0

        for _ficha in self.fichas:
            if ficha[0] == _ficha[0] or ficha[0] == _ficha[1] or \
              ficha[1] == _ficha[0] or ficha[1] == _ficha[1]:
                count += 1

        return count

    def eval_dobles(self, ficha):
        if ficha[0] == ficha[1]:
            return 1
        else:
            return 0

    def escoger_ficha(self, cabezas):
        mayor = 0
        ficha_final = 0

        for ficha in self.fichas:
            if -1 in cabezas or \
                ficha[0] in cabezas or \
                ficha[1] in cabezas:

                valores = []

                valores.append(self.eval_aleatorio(ficha))
                valores.append(self.eval_bota_gorda(ficha))
                valores.append(self.eval_bota_gorda_suave(ficha))
                valores.append(self.eval_no_pase(ficha))
                valores.append(self.eval_no_pase_suave(ficha))
                valores.append(self.eval_dobles(ficha))

                mul = np.multiply(self.coeficientes, valores)
                val = np.sum(mul)

                if val > mayor:
                    mayor = val
                    ficha_final = ficha

        # Porque cabeza?
        cabeza = 0 if cabezas[0] in ficha_final else 1

        return ficha_final, cabeza