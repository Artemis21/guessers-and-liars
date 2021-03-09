"""Liar that always returns one."""
import random


class Main:
    """Liar that always returns one."""

    def __init__(self, rng: random.Random, secret: int):
        """Store the rng and secret even though we do nothing with them."""
        self.rng = rng
        self.secret = secret

    def __call__(self, guess: int) -> int:
        """Return 1."""
        return 1
