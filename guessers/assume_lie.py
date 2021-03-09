"""A guesser that always assumes the liar is lying."""
import random
from typing import Callable


def Main(rng: random.Random, liar: Callable[[int], int]):
    """Make guesses to a liar."""
    guess = 128
    abs_delta = 64
    guesses = []
    while abs_delta >= 0.25:
        guesses.append(guess)
        delta = abs_delta * liar(min(255, round(guess)))
        guess -= delta
        abs_delta /= 2
    for guess in guesses:
        for _ in range(8):
            liar(min(255, round(guess)))
    # Our assumption was incorrect!
    Main(rng, liar)
