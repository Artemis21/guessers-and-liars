import random
from typing import Callable

def Main(rng: random.Random, liar: Callable[[int], int]):
    while liar(0) == -1: pass
    previous = {0:1}
    lb = 0
    ub = 255
    while True:
        while lb <= ub:
            g = (lb+ub)//2
            if g in previous:
                r = previous[g]
            else:
                r = liar(g)
            if r == 1:
                lb = g+1
            elif r == -1:
                ub = g-1
            previous[g] = r
        k = g == ub
        n = 0
        while True:
            n += 1
            g = min(max(ub+k,0),255)
            k = 1-k
            r = liar(g)
            if previous[g] != r:
                previous[g] = r
                break
        lb = 0
        ub = 255
