"""Liar that just choses an answer randomly."""
import random


class Main:
    """Liar that just choses an answer randomly."""

    def __init__(self, rng: random.Random, secret: int):
        """Store the rng and secret."""
        self.rng = rng
        self.secret = secret

    def __call__(self, guess: int) -> int:
        """Chose a random answer."""
        return self.rng.choices((-1, 0, 1), (100, 1, 100), k=1)[0]
