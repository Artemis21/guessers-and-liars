import random
from typing import Callable


def Main(rng: random.Random, liar: Callable[[int], int]):
    i = 0

    while i < 9:
        low = j = 0
        high = 255

        while j < 8:
            guess = (low + high) // 2
            res = liar( guess )
            if res > 0:
                low = guess + 1
            else:
                high = guess - 1
            j += 1

        i += 1
