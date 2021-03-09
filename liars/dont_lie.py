"""A liar that doesn't lie."""
import random


class Main:
    """Liar that always returns one."""

    def __init__(self, rng: random.Random, secret: int):
        """Store the rng and secret."""
        self.rng = rng
        self.secret = secret

    def __call__(self, guess: int) -> int:
        """Work out the correct response."""
        if guess == self.secret:
            return 0
        if guess < self.secret:
            return 1
        return -1
