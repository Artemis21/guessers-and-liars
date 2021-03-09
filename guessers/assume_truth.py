"""A guesser that always assumes the liar is telling the truth."""
import random
from typing import Callable


def Main(rng: random.Random, liar: Callable[[int], int]):
    """Make guesses to a liar."""
    guess = 128
    delta = 64
    while True:
        guess += delta * liar(min(round(guess), 255))
        delta /= 2
