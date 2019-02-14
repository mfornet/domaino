from player import BasePlayer
import numpy as np

# TODO: Explain how this player was implemented and how was found the set of parameters.
class SimpleHybrid(BasePlayer):
    PARAMETERS = [0.613, 0.075, 0.171, 0.562, 0.007, 2.127]

    def __init__(self, name, coef=None):
        super().__init__(f"SmartH::{name}")

        if coef is None:
            coef = SimpleHybrid.PARAMETERS

        self.coef = coef

    def __eq__(self, other):
        return self.nombre == other.nombre

    def __repr__(self):
        return self.nombre

    def eval_random(self, piece):
        return 1

    def eval_big_drop(self, piece):
        sums = []
        bigger = 0
        count = 1

        for _piece in self.pieces:
            if _piece[0] + _piece[1] > bigger:
                bigger = _piece[0] + _piece[1]
                count = 1
            if _piece[0] + _piece[1] == bigger:
                count += 1

        if piece[0] + piece[1] == bigger:
            return 1. / count
        else:
            return 0

    def eval_big_drop_soft(self, piece):
        return piece[0] + piece[1]

    def eval_frequent(self, piece):
        bigger = 0
        total = []

        for i in self.pieces:
            count = 0
            for j in self.pieces:
                if i[0] == j[0] or i[0] == j[1] or i[1] == j[0] or i[1] == j[1]:
                    count += 1
            total.append(count)

            if count > bigger:
                bigger = count

        _count = 0
        for i in total:
            if i == bigger:
                _count += 1

        index = self.pieces.index(piece)
        if total[index] == bigger:
            return 1/_count
        else:
            return 0

    def eval_frequent_soft(self, piece):
        count = 0

        for _piece in self.pieces:
            if piece[0] == _piece[0] or piece[0] == _piece[1] or \
              piece[1] == _piece[0] or piece[1] == _piece[1]:
                count += 1

        return count

    def eval_doubles(self, piece):
        if piece[0] == piece[1]:
            return 1
        else:
            return 0

    def choice(self):
        heads = self.heads
        bigger = float('-inf')
        final_piece = None

        for piece in self.pieces:
            if -1 in heads or \
                piece[0] in heads or \
                piece[1] in heads:

                valores = []

                valores.append(self.eval_random(piece))
                valores.append(self.eval_big_drop(piece))
                valores.append(self.eval_big_drop_soft(piece))
                valores.append(self.eval_frequent(piece))
                valores.append(self.eval_frequent_soft(piece))
                valores.append(self.eval_doubles(piece))

                mul = np.multiply(self.coef, valores)
                val = np.sum(mul)

                if val > bigger:
                    bigger = val
                    final_piece = piece

        # What head
        head = 0 if heads[0] in final_piece else 1

        return final_piece, head