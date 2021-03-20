import random

class Main:
    """A **real** liar"""

    def __init__(self, rng: random.Random, secret: int):
        """Store the rng and secret."""
        self.rng = rng
        self.secret = secret

    def __call__(self, guess: int) -> int:
        """You can trust me, really"""
        if guess > self.secret:
            return 1
        return -1
