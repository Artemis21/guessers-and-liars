"""A guesser that based on recent guesses."""
import random
from typing import Callable

def Main(rng: random.Random, liar: Callable[[int], int]):
    scores, current = [0] * 256, 0
    while True:
        max_score = max(scores)
        values = [val for val, score in enumerate(scores) if score == max_score]
        guess = values[len(values) // 2]
        result = liar(guess)
        current -= 1
        if result > 0:
            scores[:guess + 1] = [current] * (guess + 1)
        else:
            scores[guess:] = [current] * (256 - guess)
