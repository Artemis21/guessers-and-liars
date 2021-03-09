"""A guesser that tries every possible value repeatedly."""
import random
from typing import Callable


def Main(rng: random.Random, liar: Callable[[int], int]):
    """Make guesses to a liar."""
    guess = 0
    while True:
        liar(guess)
        guess += 1
        guess %= 256
