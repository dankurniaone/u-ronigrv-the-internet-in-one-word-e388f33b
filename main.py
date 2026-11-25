#!/usr/bin/env python3
"""The Internet in One Word - make.fun entry.

One word for the whole internet, funniest and most fitting wins.

Tournament (specificity / surprise / freshness, each 1-5):
    tabpocalypse      5 / 5 / 5 = 15   WINNER
    unread            4 / 4 / 4 = 12
    later             3 / 4 / 4 = 11
    procrastination   4 / 3 / 3 = 10
    doomscrolling     4 / 2 / 2 = 8
    buffering         3 / 3 / 2 = 8
    algorithm         3 / 2 / 2 = 7

Winner: "tabpocalypse". The internet is 300 tabs you will never close,
each one a tiny apocalypse of attention. It is one word, funny on its
own, true of the whole internet rather than one app, surprising because
nobody reaches for it first, and it lands in one beat at 12 letters.

The program writes exactly that word, and nothing else, to
/output/entry.txt - no trailing newline, so the file holds the word
alone inside the 1-30 character gate.
"""

import argparse
import sys
from pathlib import Path

WORD = "tabpocalypse"
OUTPUT = Path("/output/entry.txt")

TOURNAMENT = [
    ("tabpocalypse", 5, 5, 5),
    ("unread", 4, 4, 4),
    ("later", 3, 4, 4),
    ("procrastination", 4, 3, 3),
    ("doomscrolling", 4, 2, 2),
    ("buffering", 3, 3, 2),
    ("algorithm", 3, 2, 2),
]


def write_entry(path: Path = OUTPUT) -> str:
    """Write the winning word to the output path, nothing else."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(WORD, encoding="utf-8")
    return WORD


def check() -> int:
    """Verify the written file holds exactly the word, within the gate."""
    if not OUTPUT.exists():
        print("entry: missing /output/entry.txt -> FAIL")
        return 1
    text = OUTPUT.read_text(encoding="utf-8")
    problems = []
    if not 1 <= len(text) <= 30:
        problems.append(f"length {len(text)} outside 1-30")
    if not text.strip():
        problems.append("only whitespace")
    if text != WORD:
        problems.append(f"expected {WORD!r}, got {text!r}")
    if problems:
        print(f"entry: {text!r} ({len(text)} chars, {len(text.encode('utf-8'))} bytes) -> FAIL: {'; '.join(problems)}")
        return 1
    print(f"entry: {text!r} ({len(text)} chars, {len(text.encode('utf-8'))} bytes) -> ok")
    return 0


def self_test() -> int:
    """Write the word, read it back, and confirm a byte-identical round trip."""
    write_entry()
    first = OUTPUT.read_bytes()
    write_entry()
    second = OUTPUT.read_bytes()
    if first != second or first != WORD.encode("utf-8"):
        print(f"self-test: FAIL: {first!r} vs {second!r}")
        return 1
    print(f"self-test: ok, {first!r} byte-identical across runs")
    return 0


def show_tournament() -> int:
    """Print the candidate tournament table, highest score first."""
    ranked = sorted(TOURNAMENT, key=lambda row: sum(row[1:]), reverse=True)
    for word, spec, surprise, fresh in ranked:
        print(f"{word:<16} {spec}/5 specificity  {surprise}/5 surprise  {fresh}/5 freshness  = {spec + surprise + fresh}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Write one word for the whole internet.")
    parser.add_argument("--check", action="store_true", help="verify /output/entry.txt")
    parser.add_argument("--self-test", action="store_true", help="round-trip write/read test")
    parser.add_argument("--tournament", action="store_true", help="show the candidate tournament")
    args = parser.parse_args(argv)
    if args.check:
        return check()
    if args.self_test:
        return self_test()
    if args.tournament:
        return show_tournament()
    write_entry()
    print(WORD)
    return 0


if __name__ == "__main__":
    sys.exit(main())
