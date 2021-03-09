"""A guesser that assumes the opponent usually tells the truth."""
import random
from typing import Callable


def Main(rng: random.Random, liar: Callable[[int], int]):
    """Make guesses to a liar."""
    total = 128
    guesses = 1
    while True:
        total += 128 + 128 * liar(round(total / guesses))
        guesses += 1
