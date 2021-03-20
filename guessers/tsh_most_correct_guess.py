"""A guesser that based number of correct times."""
import random
from typing import Callable

def Main(rng: random.Random, liar: Callable[[int], int]):
    scores = [1] * 256
    while True:
        index, mid_score = 0, sum(scores) >> 1
        while mid_score > 0:
            mid_score, index = mid_score - scores[index], index + 1
        guess = max(0, index - 1)
        result = liar(guess)
        for index in (range(guess + 1, 256) if result > 0 else range(guess)):
            scores[index] <<= 1
