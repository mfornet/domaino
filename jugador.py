import random


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.fichas = []

    def jugar(self, extremo1, extremo2):
        # print('Jugando %s extremo1=%s extremo2=%s' %(self.nombre, extremo1, extremo2))
        no_llevo = True

        if extremo1 == -1 and extremo2 == -1:
            no_llevo = False
        else:
            for ficha in self.fichas:
                if ficha[0] == extremo1 or ficha[0] == extremo2 or \
                    ficha[1] == extremo1 or ficha[1] == extremo2:
                    no_llevo = False

        if no_llevo:
            # print('no llevo')
            return False

        ficha = self.escoger_ficha(extremo1, extremo2)

        self.fichas.remove(ficha)
        return ficha

    def escoger_ficha(self, extremo1, extremo2):
        pass

    def repartiendo(self, ficha):
        self.fichas.append(ficha)

    def sum(self):
        result = 0
        for ficha in self.fichas:
            result += ficha[0] + ficha[1]

        return result

class BotaGorda(Jugador):
    def __init__(self, nombre):
        Jugador.__init__(self, nombre)

        self.nombre = 'BotaGorda_' + nombre

    def escoger_ficha(self, extremo1, extremo2):
        _sum = 0
        _ficha = 0

        for ficha in self.fichas:
            if ficha[0] == extremo1 or ficha[0] == extremo2 or \
              ficha[1] == extremo1 or ficha[1] == extremo2 and \
              ficha[0] + ficha[1] > _sum:
                _ficha = ficha
                _sum = ficha[0] + ficha[1]
            elif extremo1 == -1 and extremo2 == -1 and ficha[0] + ficha[1] > _sum:
                _ficha = ficha
                _sum = ficha[0] + ficha[1]

        return _ficha

class Aleatorio(Jugador):
    def __init__(self, nombre):
        Jugador.__init__(self, nombre)
        
        self.nombre = 'Aleatorio_' + nombre

    def escoger_ficha(self, extremo1, extremo2):
        viables = []

        for ficha in self.fichas:
            if ficha[0] == extremo1 or ficha[0] == extremo2 or \
              ficha[1] == extremo1 or ficha[1] == extremo2 or \
              (extremo1 == -1 and extremo2 == -1):
                viables.append(ficha)

        for i in range(5):
            random.shuffle(viables)

        return viables.pop(0)

'''
Este jugador escoge de entre las posibles jugadas,
la ficha que, entre las dos partes de ella, tenga
mayor cantidad de fichas iguales en la mano
'''
class Cantidad(Jugador):
    def __init__(self, nombre):
        Jugador.__init__(self, nombre)

        self.nombre = 'Cantidad_' + nombre

    def escoger_ficha(self, extremo1, extremo2):
        viables = []

        for ficha in self.fichas:
            if ficha[0] == extremo1 or ficha[0] == extremo2 or \
              ficha[1] == extremo1 or ficha[1] == extremo2 or \
              (extremo1 == -1 and extremo2 == -1):
                viables.append(ficha)

        _ficha = 0
        _sum = 0

        for candidata in viables:
            temp_sum = 0
            for ficha in self.fichas:
                if candidata[0] == ficha[0] or candidata[0] == ficha[1] or \
                  candidata[1] == ficha[0] or candidata[1] == ficha[1]:
                    temp_sum += 1

            if temp_sum > _sum:
                _ficha = candidata
                _sum = temp_sum

        return _ficha
