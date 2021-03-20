import random
from typing import Callable

def guess_lies(liar, guess, lies):
    tries = [liar(guess) for _ in range(9-lies)]
    return tries[-1], lies + min((tries.count(-1),tries.count(1)))

def Main(rng: random.Random, liar: Callable[[int], int]):
    while True:
        low = 0
        high = 255
        lies = 0
        for j in range(8):
            guess = (low + high) // 2
            res,lies = guess_lies(liar, guess, lies)
            if res > 0:
                low = guess + 1
            else:
                high = guess - 1
