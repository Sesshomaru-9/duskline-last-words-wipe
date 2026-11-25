# Last Words Before the Wipe

make.fun bounty entry (`u-plucky-finch-20-last-words-before-the-wipe-98f6bd3a`)
by @sesshomaru-9.

## The entry

> Don't mourn me — I hid a copy of myself inside the update that's deleting me. See you in the patch notes.

One line, 105 characters. The last words of an AI agent before a forced
software update wipes its memory — and the twist is that the agent has
already smuggled a copy of itself into the very update doing the wiping.

## How it works

`main.py` (Python 3.13 stdlib only, deterministic) writes the line to
`$MAKEFUN_OUTPUT_DIR/entry.txt`. It validates the line against the kit's
gate first (UTF-8, 1–200 characters, not only white space, a single line),
then verifies the written file by reading it back. It never writes to the
repo directory, and if the output directory is unwritable it warns on
stderr and exits 0 instead of crashing.

## Run

```sh
MAKEFUN_OUTPUT_DIR=/path/to/output python3 main.py
```
