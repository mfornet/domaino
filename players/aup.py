""" Scripted agent
"""
from player import BasePlayer
from domino import Event

import numpy as np

class AuP(BasePlayer):
    def __init__(self, name):
        super().__init__(f"AuP::{name}")
        self.history_pointer = 0

    def my_init(self):
        self.ontable = [0] * 7
        self.pieces_on_hand = [7] * 4

    def feed(self):
        if self.history_pointer == 0:
            self.my_init()

        # Game simulation
        team = self.position % 2

        while self.history_pointer < len(self.history):
            # Read and proc next event
            event, *args = self.history[self.history_pointer]
            self.history_pointer += 1

            if event == Event.MOVE:
                position, piece, _ = args
                for i in range(7):
                    if i in piece:
                        self.ontable[i] += 1

                self.pieces_on_hand[position] -= 1

    def choice(self):
        """
            Ideas
                + Play doubles
                + Kill number that my partner don't have
                + [META] Avoid numbers that let enemy play a number that me or my partner don't have
                    Prioritize my partner, since he is playing first

                + Try to put my partner number
                    Or a number such that my partner can put his data
                    (How can I know what is my partner number)

                + Avoid killing our numbers
        """
        self.feed()

        me = self.me
        partner = self.partner

        if self.pieces_on_hand[me] <= self.pieces_on_hand[partner]:
            # What is my number
            pass
        else:
            pass

        raise NotImplementedError()
