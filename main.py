#!/usr/bin/env python3
"""Entry program: write this repository's front page image to /output/entry.png.

The image ships with the repository, so the program only copies it. No network,
no dependencies beyond the standard library, and the same bytes on every run.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def target_dir():
    for candidate in ("/output", os.path.join(HERE, "output")):
        try:
            os.makedirs(candidate, exist_ok=True)
            if os.access(candidate, os.W_OK):
                return candidate
        except OSError:
            continue
    raise SystemExit("no writable output directory")


def main():
    out = os.path.join(target_dir(), "entry.png")
    shutil.copyfile(SOURCE, out)
    with open(out, "rb") as fh:
        data = fh.read()
    if len(data) > 1048576:
        raise SystemExit("image exceeds 1 MiB")
    sys.stdout.write("wrote %s (%d bytes)\n" % (out, len(data)))


if __name__ == "__main__":
    main()
