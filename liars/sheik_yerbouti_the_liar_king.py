import random, math

class Main:

    def __init__(self, rng: random.Random, secret: int):
        self.rng = rng
        self.secret = secret

    def __call__(self, guess: int) -> int:
        timeToLie = self.rng.randint(1,16)
        if guess == self.secret:
            res = self.rng.choice([-1,1])
        elif timeToLie == 1:
            if self.secret > guess:
                res = -1
            else:
                res = 1
        elif self.secret > guess:
            res = 1
        else:
            res = -1
        return res
