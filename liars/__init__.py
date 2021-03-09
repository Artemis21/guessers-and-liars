"""Load all submissions from this folder."""
import os
import pathlib


__all__ = []
SUBMISSIONS = []
THIS_DIR = pathlib.Path(__file__).parent.absolute()

for filename in os.listdir(THIS_DIR):
    if filename.endswith('.py') and filename != '__init__.py':
        __all__.append(filename[:-3])
        SUBMISSIONS.append(filename[:-3])
