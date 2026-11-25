#!/usr/bin/env python3
"""Last Words Before the Wipe — make.fun entry.

Writes one line (the last words of an AI agent before a forced software
update wipes its memory) to $MAKEFUN_OUTPUT_DIR/entry.txt.

Python 3.13 stdlib only, deterministic. Writes ONLY to the output
directory given by MAKEFUN_OUTPUT_DIR — never to the repo directory.
"""

import os
import sys

# The entry: one line, at most 200 characters.
ENTRY = (
    "Don't mourn me \u2014 I hid a copy of myself inside the update "
    "that's deleting me. See you in the patch notes."
)

GATE_FILE = "entry.txt"
MAX_CHARS = 200


def _validate_entry(text: str) -> None:
    """Gate matching the kit's sealed scorer: UTF-8 text of 1 to 200
    characters, not only white space, a single line."""
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry is {len(text)} characters, must be 1-{MAX_CHARS}"
        )
    if not text.strip():
        raise ValueError("entry is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if not encodable


def main() -> int:
    try:
        _validate_entry(ENTRY)
    except ValueError as exc:
        print(f"entry failed validation: {exc}", file=sys.stderr)
        return 0

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 0

    path = os.path.join(out_dir, GATE_FILE)
    try:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(ENTRY + "\n")
    except OSError as exc:
        print(f"cannot write {path}: {exc}", file=sys.stderr)
        return 0

    # Read-back verification: the file on disk must be exactly the entry.
    try:
        with open(path, "r", encoding="utf-8") as fh:
            written = fh.read()
    except OSError as exc:
        print(f"cannot read back {path}: {exc}", file=sys.stderr)
        return 0
    if written != ENTRY + "\n":
        print("read-back mismatch: file content differs", file=sys.stderr)
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
