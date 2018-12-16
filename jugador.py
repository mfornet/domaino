import random


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.fichas = []
        self.historia = []

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
        """
        Esta función contiene la lógica del jugador
        """
        raise NotImplementedError()

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
        mayor_suma = 0
        gordas = []

        for ficha in self.fichas:
            # Pregunta si la ficha se puede poner
            if extremo1 == -1 or \
                ficha[0] in (extremo1, extremo2) or \
                ficha[1] in (extremo1, extremo2):

                suma = ficha[0] + ficha[1]

                # Si la ficha es la de mayor valor hasta ahora
                # reinicia el conjunto de fichas gordas y actualiza
                # la mayor suma.
                if suma > mayor_suma:
                    gordas = []
                    mayor_suma = suma

                # Si la ficha tiene el mismo valor que la mayor vista
                # añadela al conjunto de fichas gordas
                if suma == mayor_suma:
                    gordas.append(ficha)

        assert len(gordas) > 0

        # Escoge una de las fichas gordas de forma aleatoria
        return random.choice(gordas)


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

        return random.choice(viables)


class Cantidad(Jugador):
    """
    Este jugador escoge de entre las posibles jugadas,
    la ficha que, entre las dos partes de ella, tenga
    mayor cantidad de fichas iguales en la mano
    """
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
