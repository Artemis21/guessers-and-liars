# Guessers and Liars

This is a King-of-the-Hill style challenge for [CGCC](https://codegolf.stackexchange.com/).

## Rules

You have probably played, and may even have written a program to play, a simple number guessing game. If so, this probably looks familiar:
```
Try to guess my number (1 to 100)!
Please enter a guess: 50
Too small, guess again!
Please enter a guess: 75
Too big, guess again!
Please enter a guess: 63
Correct!
```
(Obviously, it usually takes a little longer.)

But what if your opponent *lied*? Or, to be more generous, isn't very good at comparing numbers.

There are two parts to this challenge.

### 1: The liar

- Your program will be passed a number between 0 and 255 inclusive.
- Your program will be passed a guess, within the same bounds.
- Your program should return one of -1 (the guess is smaller than your number), 0 (the guess *is* your number) or 1 (the guess is greater than your number).
- You may store state for the duration of a single game.
- You may return an inaccurate result (lie!) up to `X` times in a game.
- If you return 0 when the guess is not equal to your number, your opponent will win anyway. However, you may chose not to return 0 even when the guess *is* equal to your number (this counts as one of your allotted lies).
- Your aim is to delay returning 0 for as long as possible ("long" as in most calls to the program, not length of time, obviously).

### 2: The guesser

- Your program will be passed a function to call. You should pass this function a guess, between 0 and 255. It will return -1 (indicating that you should guess lower), 0 (indicating that your guess was correct) or 1 (indicating that you should guess higher).
- The function may return an inaccurate result up to `X` times in a single invocation of your program.
- Your aim is to receive output of 0 from the function after calling it the fewest possible times.

### General notes

- Once the liar has used up their allotted lies, the function passed to the guesser (henceforth "guess function") will simply begin returning the correct answer without invoking the liar.
- The maximum number of guesses is `256 * (X + 1)`. After this, the guess function will return 0 and end the game.
- Practically, the guess function will never return 0, it will just end the game. So the guesser only needs to handle a return of -1 or 1.

## Implementation

Guessers should be added as Python files to the `guessers` folder. Their name should be unique among both the liars and guessers. The should define a single callable, called `Main` (capitalised even if it just a function). This should accept two arguments: an instance of `random.Random`, which it should use for all non-determinism, and a function (the guess function). The guess function will take a single number between 0 and 255, and return either -1 or 1.

Guessers functions need never return - indeed, if they do, they will get the worst possible score.

Liars should be added as Python files to the `liars` folder. Their name should be unique among both the liars and guessers. They should define a single class, called `Main`. The `__init__` function for this class should accept two parameters: an instance of `random.Random`, which it should use for all non-determinism, and an `int`, which is the secret it should protect.

Liar classes should additionally define a `__call__` function, which should accept one parameter (a guess), and return -1 or 1. It may also return 0, but this is never advantageous.

A tournament can be run by executing the `main.py` file. It has two options: `--seed`, which can be any text to use as the RNG seed, and `--repetitions` which is the number of times each guesser should face each liar (default 10).

See the `guesser` and `liar` folders for example guessers and liars.
