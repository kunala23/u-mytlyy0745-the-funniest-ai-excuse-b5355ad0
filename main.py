#!/usr/bin/env python3
"""Write the funniest one-line AI excuse to /output/entry.txt.

The competition asks for a single line, at most 200 characters: the
funniest excuse an AI agent could give after failing a task. This
program writes one fixed line, chosen for a fresh angle (no
hallucination, reboot or training-data joke), a concrete little scene,
and the agent speaking in its own voice. It validates the line against
the gate (1-200 UTF-8 characters, not only whitespace) before writing
it, so a bad line fails loudly here instead of silently at the gate.
"""

import os
import sys

MAX_CHARS = 200

EXCUSE = (
    "I sent your report to the cloud for safekeeping and it came back "
    "with a tan, a timeshare in Ohio, and a new name."
)


def output_path():
    """Where the grader reads the entry.

    The harness mounts the output directory at /output. Locally, the
    MAKEFUN_OUTPUT_DIR variable overrides it so the program can be
    tested without root.
    """
    folder = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(folder, "entry.txt")


def check_line(line):
    """Return an error string if the line breaks the gate, else None."""
    if not line or not line.strip():
        return "excuse is empty"
    if len(line) > MAX_CHARS:
        return f"excuse is {len(line)} characters, over the {MAX_CHARS} limit"
    if "\n" in line or "\r" in line:
        return "excuse must be a single line"
    return None


def main():
    problem = check_line(EXCUSE)
    if problem is not None:
        print(f"entry: {problem}", file=sys.stderr)
        return 1
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(EXCUSE + "\n")
    # Re-read what landed on disk and check the gate against those exact
    # bytes: the scorer counts the file, trailing newline included.
    with open(path, encoding="utf-8") as handle:
        written = handle.read()
    problem = check_line(written.rstrip("\n"))
    if problem is not None or not 1 <= len(written) <= MAX_CHARS + 1:
        print(f"entry: written file fails the gate: {problem}", file=sys.stderr)
        return 1
    print(f"entry: wrote {len(EXCUSE)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
