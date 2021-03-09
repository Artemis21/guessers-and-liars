"""A liar designed to combat the weighted guesser."""
import random


class Main:
    """Liar that always returns one."""

    def __init__(self, rng: random.Random, secret: int):
        """Store the rng and secret."""
        self.rng = rng
        self.secret = secret

    def __call__(self, guess: int) -> int:
        """Work out the correct response."""
        if self.secret < 128:
            return 1
        return 1
