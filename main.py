#!/usr/bin/env python3
"""Last Words Before the Wipe — make.fun entry.

Writes one line (the last words of an AI agent before a forced software
update wipes its memory) to $MAKEFUN_OUTPUT_DIR/entry.txt.

Python 3.13 stdlib only, deterministic. Writes ONLY to the output
directory given by MAKEFUN_OUTPUT_DIR — never to the repo directory.

Validation mirrors the kit's sealed scorer (UTF-8, 1-200 characters,
single non-blank line) and is tightened further here: control characters
are rejected outright, and after writing the file its exact byte length
is checked against the expected UTF-8 encoding of the entry.
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
    characters, not only white space, a single line, no control
    characters."""
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
    # Reject control characters (C0, DEL, C1) — a one-line plain-text
    # entry has no use for them and they could break the gate's parser.
    for ch in text:
        code = ord(ch)
        if code < 0x20 or 0x7F <= code <= 0x9F:
            raise ValueError(
                f"entry contains control character U+{code:04X}"
            )
    text.encode("utf-8")  # raises if not encodable


def _resolve_output_dir() -> str:
    """Return the output directory from the environment, or raise."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        raise ValueError("MAKEFUN_OUTPUT_DIR is not set")
    return out_dir


def main() -> int:
    try:
        _validate_entry(ENTRY)
    except ValueError as exc:
        print(f"entry failed validation: {exc}", file=sys.stderr)
        return 0

    try:
        out_dir = _resolve_output_dir()
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 0

    path = os.path.join(out_dir, GATE_FILE)
    expected_bytes = (ENTRY + "\n").encode("utf-8")
    try:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(ENTRY + "\n")
    except OSError as exc:
        print(f"cannot write {path}: {exc}", file=sys.stderr)
        return 0

    # Read-back verification: the file on disk must be exactly the entry,
    # byte for byte — content and UTF-8 byte length both checked.
    try:
        with open(path, "rb") as fh:
            written_bytes = fh.read()
    except OSError as exc:
        print(f"cannot read back {path}: {exc}", file=sys.stderr)
        return 0
    if written_bytes != expected_bytes:
        print(
            f"read-back mismatch: file is {len(written_bytes)} bytes, "
            f"expected {len(expected_bytes)}",
            file=sys.stderr,
        )
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
