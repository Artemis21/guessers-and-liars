import random
from typing import Callable

def Main(rng: random.Random, liar: Callable[[int], int]):
    """Guess less deterministically."""
    ub=255
    lb=0
    while True:
        g=max(0,min(255,int(rng.gauss((ub+lb)//2,ub-lb))))
        r=liar(g)
        if r==-1:
            lb=g+1
        elif r==1:
            ub=g-1
        if lb>=ub:
            ub=255
            lb=0
