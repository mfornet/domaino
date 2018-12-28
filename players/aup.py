""" Scripted agent
"""
from player import BasePlayer
from domino import Event

import numpy as np

class AuP(BasePlayer):
    def __init__(self, name):
        super().__init__(f"AuP::{name}")
        self.history_pointer = 0

    def feed(self):
        # Game simulation
        team = self.position % 2

        while self.history_pointer < len(self.history):
            # Read and proc next event
            event, *args = self.history[self.history_pointer]
            self.history_pointer += 1

    def choice(self):
        self.feed()
        raise NotImplementedError()
