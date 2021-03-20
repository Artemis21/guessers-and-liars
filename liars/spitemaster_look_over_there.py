class Main:
    """Liar that picks a number 64 off from the actual target and pretends that's the correct answer."""

    def __init__(self, rng, secret: int):
        """Pick a new secret."""
        self.secret = secret + 63.5 if secret < 128 else secret - 63.5

    def __call__(self, guess: int) -> int:
        """Return the 'correct' answer."""
        if guess < self.secret:
            return 1
        elif guess > self.secret:
            return -1
        # Should never happen
        return 0
