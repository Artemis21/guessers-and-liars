"""A guesser that based on recent guesses."""
import random
from typing import Callable

def Main(rng: random.Random, liar: Callable[[int], int]):
    previous = [(128, liar(128))]
    while True:
        total = weight = 0.
        scores = [
            ([(i > guess) - (i < guess) == result
                    for (guess, result) in previous] +
                    [False]).index(False)
            for i in range(256)
        ]
        max_score = max(scores)
        values = [val for val, score in enumerate(scores) if score == max_score]
        guess = values[len(values) // 2]
        result = liar(guess)
        previous.insert(0, (guess, result))
