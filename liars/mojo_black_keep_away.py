"""A liar that tries to keep the guesser away from the secret"""
import random

class Main:
    def __init__(self, rng: random.Random, secret: int):
        """Store the rng and secret."""
        self.rng = rng
        self.secret = secret
        self.lb = 0
        self.ub = 255
        self.lies = 4
    def __call__(self,guess):
        r = (guess <= self.secret) - (guess > self.secret)
        a = (self.lb+self.secret)//2
        b = (self.ub+self.secret)//2
        if self.lies:
            if a <= guess < self.secret:
                self.lies -= 1
                self.lb = guess
                r = -r
            elif self.secret < guess <= b:
                self.lies -= 1
                self.ub = guess
                r = -r
        return r
