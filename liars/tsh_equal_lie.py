"""A liar that only lies when equal."""
import random


class Main:

    def __init__(self, rng: random.Random, secret: int):
        """Store the rng and secret."""
        self.rng = rng
        self.secret = secret

    def __call__(self, guess: int) -> int:
        """Work out the correct response. mostly."""
        if guess == self.secret:
            if guess % 2:
                return -1
            return 1
        if guess < self.secret:
            return 1
        return -1
