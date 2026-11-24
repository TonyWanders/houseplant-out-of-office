#!/usr/bin/env python3
"""Write the houseplant out-of-office reply to /output/entry.txt.

Deterministic: no network, no clock, no randomness. The entry is a fixed
string. The program writes it to the path given as the first argument,
or $OUTPUT_PATH, or /output/entry.txt by default, and enforces the
competition gate: 1 to 120 characters, not only white space, one line.
Use -h or --help to see the usage line.
"""

import os
import sys
from pathlib import Path

ENTRY = (
    "I am out of office. I am the cactus. "
    "I have no water, no patience, and no plans to reply."
)

MIN_CHARS = 1
MAX_CHARS = 120
DEFAULT_PATH = "/output/entry.txt"
USAGE = "usage: main.py [output-path]"


def gate_error(text: str) -> str | None:
    """Return why the entry fails the competition gate, or None if it passes."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return f"entry is {len(text)} characters, gate is {MIN_CHARS} to {MAX_CHARS}"
    if not text.strip():
        return "entry is only white space"
    if "\n" in text:
        return "entry must be one line"
    return None


def validate(text: str) -> str:
    """Return the entry when it passes the competition gate, else fail.

    Raises ValueError naming the failed gate so the caller can report it
    without a traceback.
    """
    error = gate_error(text)
    if error is not None:
        raise ValueError(error)
    return text


def resolve_output_path() -> Path:
    """Pick the output path: first argument, $OUTPUT_PATH, or the default."""
    if len(sys.argv) > 1:
        return Path(sys.argv[1])
    return Path(os.environ.get("OUTPUT_PATH", DEFAULT_PATH))


def write_entry(text: str, path: Path) -> None:
    """Write the entry, reporting a write failure instead of crashing.

    A missing parent directory is created. A write that still fails, for
    example a read-only directory, prints the reason and exits 1.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    except OSError as exc:
        print(f"cannot write {path}: {exc}", file=sys.stderr)
        raise SystemExit(1)


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(USAGE)
        return 0
    try:
        text = validate(ENTRY)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    path = resolve_output_path()
    write_entry(text, path)
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
