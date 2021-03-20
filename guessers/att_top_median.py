import random
from typing import Callable

def Main(rng: random.Random, liar: Callable[[int], int]):
    poss=[0]*256
    while True:
        height = max(poss)
        top = [i for i in range(256) if poss[i]==height]
        guess = top[len(top)//2]

        i = liar(guess)
        for j in [range(guess+1), range(guess,256)][i<0]:
            poss[j] -= 1
