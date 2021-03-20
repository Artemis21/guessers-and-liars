import random
from collections import defaultdict


class Main:
    """Liar that tries to foil binary searchers and repeat guesses"""
    from collections import defaultdict

    def __init__(self, rng: random.Random, secret: int):
        self.rng = rng
        self.secret = secret
        self.lies = 0
        self.low = 0
        self.high = 255
        self.prev_guess = defaultdict(int)

    def __call__(self, guess: int) -> int:
        """Return 1"""
        if self.prev_guess[guess] > 0:
            if guess != self.secret:
                if self.rng.randint(0,self.prev_guess[guess]-1) == 0:
                    self.lies += 1
                    answer = -1 if guess > self.secret else 1
                else:
                    answer = 1 if guess > self.secret else -1

        if guess == self.secret:
            self.lies += 1
            return self.rng.choice((-1, 1))

        self.prev_guess[guess] += 1

        if not (self.low <= guess <= self.high):
            self.low = 0
            self.high = 255
            self.prev_guess = defaultdict(int)

        if self.low <= self.secret <= self.high: 
            if self.rng.randint(1,self.lies+1) == 1:
                self.lies += 1
                if not (guess <= self.secret <= self.high):
                    self.low = guess + 1
                    return 1
                else:
                    self.high = guess - 1
                    return -1

        answer = -1 if self.secret < guess else 1
        if answer < 0:
            self.low = guess + 1
        else:
            self.high = guess - 1
        return answer
