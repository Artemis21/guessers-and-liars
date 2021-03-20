"""A liar that lies once at the very beginning"""
import random

class Main:
    def __init__(self, rng: random.Random, secret: int):
        """Store the rng and secret."""
        self.rng = rng
        self.secret = secret
        self.lied = False
    def __call__(self,guess):
        r = (guess <= self.secret) - (guess > self.secret)
        if not self.lied:
            self.lied = True
            r = -r
        return r
