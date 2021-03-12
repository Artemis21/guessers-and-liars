"""A guesser that based number of correct times."""
import random
from typing import Callable


def Main(rng: random.Random, liar: Callable[[int], int]):
    previous = [(128, liar(128))]
    while True:
        total = weight = 0.
        scores = [
            1 << sum((i > guess) - (i < guess) == result
                    for (guess, result) in previous)
            for i in range(256)
        ]
        mid_score, index = sum(scores) // 2, 0
        while mid_score > 0:
            mid_score, index = mid_score - scores[index], index + 1
        guess = max(0, index - 1)
        result = liar(guess)
        previous.insert(0, (guess, result))
