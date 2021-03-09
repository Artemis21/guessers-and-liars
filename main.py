"""The entrypoint that runs the submissions."""
import argparse
import contextlib
import itertools
import logging
import random
import string
from collections import defaultdict
from typing import Any, Callable

import guessers
from guessers import *    # noqa:F401,F403 - Needed to load guessers, not used.

import liars
from liars import *    # noqa:F401,F403 - Needed to load liars, not used.


logger = logging.getLogger('guesser_liar')

LIES_ALLOWED = 8
SECRET_RANGE = 256


class GameOver(Exception):
    """An exception that is raised when a game is over."""

    def __init__(self, guesses: int):
        """Store the number of guesses that were taken."""
        self.guesses = guesses

    def __str__(self) -> str:
        """Display the error (shouldn't need to be called)."""
        return f'Game over after {self.guesses} guesses.'


class SubmissionError(Exception):
    """An error indicating a bug in a submission."""

    def __init__(self, message: str, submission: str):
        """Store the submission that caused the error."""
        self.submission = submission
        super().__init__(message)


class SubmissionInterface:
    """Base class for interfacing with submissions."""

    def __init__(self, package: Any, name: str, *init_args: tuple[Any]):
        """Load the submission."""
        self.name = name
        module = getattr(package, name)
        if not hasattr(module, 'Main'):
            raise SubmissionError(
                f'Submission {name} has no Main class.', self.name
            )
        with self.handle_submission_errors():
            self.submission = module.Main(*init_args)

    @contextlib.contextmanager
    def handle_submission_errors(self):
        """Catch any errors and raise them as SubmissionErrors."""
        try:
            yield
        except Exception as e:
            if isinstance(e, SubmissionError):
                # Don't catch our opponent's errors
                raise e
            if isinstance(e, GameOver):
                raise e
            raise SubmissionError(
                f'Submission {self.name} raised a {type(e).__name__} error: '
                f'{e}', self.name
            ) from e


class LiarInterface(SubmissionInterface):
    """Manages the interface with the liar program."""

    def __init__(self, name: str, rng: random.Random, secret: int):
        """Initialise the liar."""
        super().__init__(liars, name, rng, secret)

    def __call__(self, guess: int) -> int:
        """Ask the liar to respond to a guess."""
        with self.handle_submission_errors():
            response = self.submission(guess)
        if response not in (-1, 0, 1):
            raise SubmissionError(
                f'Liar {self.name} returned an invalid value: {response}.',
                self.name
            )
        return response


class GuesserInterface(SubmissionInterface):
    """Manages the interface with the guesser program."""

    def __init__(
            self, name: str, rng: random.Random,
            liar_callback: Callable[[int], int]):
        """Initialise the guesser with their guess callback."""
        self.liar_callback = liar_callback
        super().__init__(guessers, name, rng, self.callback)

    def callback(self, guess: int) -> int:
        """Respond to the guesser's guess."""
        if (not isinstance(guess, int)) or guess < 0 or guess >= SECRET_RANGE:
            raise SubmissionError(
                f'Guesser {self.name} guessed invalid value: {guess}',
                self.name
            )
        return self.liar_callback(guess)


class GameManager:
    """Manager for a single game."""

    def __init__(
            self, rng: random.Random, secret: int, liar: str, guesser: str):
        """Set up the game manager."""
        self.secret = secret
        liar_rng = random.Random()
        liar_rng.seed(rng.randbytes(255))
        guesser_rng = random.Random()
        guesser_rng.seed(rng.randbytes(255))
        self.guesses_taken = 0
        self.lies_remaining = LIES_ALLOWED
        self.liar = LiarInterface(liar, liar_rng, self.secret)
        self.guesser = GuesserInterface(guesser, guesser_rng, self.callback)
        # GuesserInterface __init__ should never return, just raise GameOver,
        # so if we've got this far, the guesser exited early.
        raise GameOver(SECRET_RANGE * (LIES_ALLOWED + 1))

    def get_guess_response(self, guess: int) -> int:
        """Get the response from the liar."""
        self.guesses_taken += 1
        if self.guesses_taken > SECRET_RANGE * (LIES_ALLOWED + 1):
            return 0
        if guess == self.secret:
            actual = 0
        elif guess < self.secret:
            actual = 1
        else:
            actual = -1
        if not self.lies_remaining:
            return actual
        response = self.liar(guess)
        if response != actual:
            self.lies_remaining -= 1
        return response

    def callback(self, guess: int) -> int:
        """Respond to a guess from the guesser."""
        response = self.get_guess_response(guess)
        if response == 0:
            raise GameOver(self.guesses_taken)
        else:
            return response


class TourneyManager:
    """Manager for an entire tournament."""

    def __init__(self, seed: Any, repetitions: int = 10):
        """Set up and run the tournament."""
        self.repetitions = repetitions
        self.seed = seed
        self.rng = random.Random()
        self.rng.seed(seed)
        self.game_scores = defaultdict(int)
        self.liar_scores = defaultdict(int)
        self.guesser_scores = defaultdict(int)
        self.disqualified = []
        self.run_games()
        self.calculate_scores()

    def run_games(self):
        """Run all the games in the tournament."""
        for liar, guesser, secret, _ in itertools.product(
                liars.SUBMISSIONS, guessers.SUBMISSIONS, range(SECRET_RANGE),
                range(self.repetitions)):
            if guesser in self.disqualified:
                continue
            if liar in self.disqualified:
                continue
            self.run_game(secret, liar, guesser)

    def run_game(self, secret: int, liar: str, guesser: str):
        """Run a game between two submissions."""
        try:
            GameManager(self.rng, secret, liar, guesser)
        except GameOver as game_over:
            self.game_scores[liar, guesser] += game_over.guesses
        except SubmissionError as submission_error:
            logger.warning(str(submission_error))
            self.disqualified.append(submission_error.submission)

    def calculate_scores(self):
        """Calculate each submission's scores for the tournament."""
        game_counts = defaultdict(int)
        for (liar, guesser), guesses in self.game_scores.items():
            if (liar in self.disqualified) or (guesser in self.disqualified):
                continue
            game_counts[liar] += self.repetitions * SECRET_RANGE
            game_counts[guesser] += self.repetitions * SECRET_RANGE
            self.liar_scores[liar] += guesses
            self.guesser_scores[guesser] += guesses
        for liar, score in self.liar_scores.items():
            self.liar_scores[liar] = round(score / game_counts[liar])
        for guesser, score in self.guesser_scores.items():
            self.guesser_scores[guesser] = round(score / game_counts[guesser])

    def print_results(self):
        """Print the results to stdout."""
        top_liars = sorted(
            self.liar_scores,
            key=lambda liar: self.liar_scores[liar],
            reverse=True
        )[:10]
        top_guessers = sorted(
            self.guesser_scores,
            key=lambda guesser: self.guesser_scores[guesser]
        )[:10]
        print(f'{self.repetitions} repetitions with seed {self.seed}:')
        print('\nTop 10 liars:\n' + '-' * 37)
        for liar in top_liars:
            print(f'{liar:<32} {self.liar_scores[liar]:>4}')
        print('\nTop 10 guessers:\n' + '-' * 37)
        for guesser in top_guessers:
            print(f'{guesser:<32} {self.guesser_scores[guesser]:>4}')
        print(f'\n{len(self.disqualified)} submissions were disqualified.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Run a guesser/liar tournament'
    )
    parser.add_argument('-s', '--seed', dest='seed')
    parser.add_argument(
        '-r', '--repetitions', type=int, default=10, dest='repetitions'
    )
    args = parser.parse_args()
    seed = args.seed
    if not seed:
        letters = string.ascii_uppercase + string.digits
        seed = ''.join(random.choices(letters, k=6))
    TourneyManager(seed, args.repetitions).print_results()
