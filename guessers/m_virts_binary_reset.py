import random
from typing import Callable


def Main(rng: random.Random, liar: Callable[[int], int]):
    """Guess deterministically."""
    ub=255
    lb=0
    while True:
        g=(ub-lb)//2+lb
        r=liar(g)
        if r==-1:
            lb=g
        elif r==1:
            ub=g
        if lb>=ub:
            ub=255
            lb=0
