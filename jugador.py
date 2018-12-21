import random


class Jugador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.puesto = None
        self.fichas = []
        self.historia = []

    def jugar(self, cabezas):
        no_llevo = True

        if -1 in cabezas:
            # Principio del juego
            no_llevo = False
        else:
            for ficha in self.fichas:
                if ficha[0] in cabezas or ficha[1] in cabezas:
                    no_llevo = False
                    break

        if no_llevo:
            return False

        ficha, cabeza = self.escoger_ficha(cabezas)

        assert ficha in self.fichas
        self.fichas.remove(ficha)

        return ficha, cabeza

    def empieza_partida(self, puesto):
        self.puesto = puesto
        self.historia.clear()
        self.fichas.clear()

    def log(self, data):
        self.historia.append(data)

    def escoger_ficha(self, cabezas):
        """
        Esta función contiene la lógica del jugador para elegir la ficha.
        Note que esta función solo se va a llamar cuando el jugador posee
        al menos una ficha para jugar

        Return: (ficha, cabeza)
            ficha: La ficha que el jugador desea jugar (aún la debe poseer)
            cabeza: Un entero entre 0 y 1 para elegir porque cabeza desea jugar
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

    def escoger_ficha(self, cabezas):
        mayor_suma = 0
        gordas = []

        for ficha in self.fichas:
            # Pregunta si la ficha se puede poner
            if -1 in cabezas or \
                ficha[0] in cabezas or \
                ficha[1] in cabezas:

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
        ficha = random.choice(gordas)

        # Porque cabeza?
        cabeza = 0 if cabezas[0] in ficha else 1

        return ficha, cabeza


class Aleatorio(Jugador):
    def __init__(self, nombre):
        Jugador.__init__(self, nombre)

        self.nombre = 'Aleatorio_' + nombre

    def escoger_ficha(self, cabezas):
        # Lista de pares (ficha, cabeza) válidos para jugar
        viables = []

        if -1 in cabezas:
            # Principio del juego. Solo se añaden las fichas por
            # la cabeza 0 pues por la cabeza 1 es equivalente
            viables = [(ficha, 0) for ficha in self.fichas]

        else:
            for ficha in self.fichas:
                if cabezas[0] in ficha:
                    viables.append((ficha, 0))

                if cabezas[1] in ficha:
                    viables.append((ficha, 1))

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

    def escoger_ficha(self, cabezas):
        # Lista de pares (ficha, cabeza) válidos para jugar
        viables = []

        if -1 in cabezas:
            # Principio del juego. Solo se añaden las fichas por
            # la cabeza 0 pues por la cabeza 1 es equivalente
            viables = [(ficha, 0) for ficha in self.fichas]

        else:
            for ficha in self.fichas:
                if cabezas[0] in ficha:
                    viables.append((ficha, 0))

                if cabezas[1] in ficha:
                    viables.append((ficha, 1))

        fichas = []
        mejor_frecuencia = -1

        for (candidata, cabeza) in viables:
            frecuencia = 0

            for ficha in self.fichas:
                if ficha[0] in candidata or ficha[1] in candidata:
                    frecuencia += 1

            if frecuencia > mejor_frecuencia:
                mejor_frecuencia = frecuencia
                fichas = []

            if frecuencia == mejor_frecuencia:
                fichas.append((candidata, cabeza))

        return random.choice(fichas)
