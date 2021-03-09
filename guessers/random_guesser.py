"""Guesser that always guesses a random number."""
import random
from typing import Callable


def Main(rng: random.Random, liar: Callable[[int], int]):
    """Make guesses to a liar."""
    while True:
        liar(rng.randrange(256))
