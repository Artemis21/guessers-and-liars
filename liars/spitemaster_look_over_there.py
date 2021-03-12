import random


class Main:
    """Liar that picks a number 64 off from the actual target and pretends that's the correct answer."""

    def __init__(self, rng: random.Random, secret: int):
        """Store the rng even though we do nothing with it.  Pick a new secret."""
        self.rng = rng
        self.secret = secret + 63.5 if secret < 128 else secret - 63.5

    def __call__(self, guess: int) -> int:
        """Return the 'correct' answer."""
        if guess < self.secret:
            return 1
        elif guess > self.secret:
            return -1
        # Should never happen
        return 0
