#!/usr/bin/env python3
"""Fix LaTeX escape sequences that were accidentally unescaped in CSV exports.

Problem:
- \t and \f inside LaTeX commands (e.g. \text, \frac) were interpreted as
  escape sequences, turning into TAB (\x09) and FORMFEED (\x0c) characters.
- In many pipelines the backslash is consumed, leaving raw control chars
  (e.g. "\x0crac" instead of "\frac", "\text" -> "\text" with \t removed).

This script fixes:
- "\\<TAB>"      -> "\\t"
- "\\<FORMFEED>" -> "\\f"
- raw <TAB>      -> "t"
- raw <FORMFEED> -> "f"
- missing command backslashes for common LaTeX commands (e.g. "frac{" -> "\\frac{")

It operates on raw bytes to avoid encoding side-effects.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
import re

TAB = b"\t"
FORMFEED = b"\x0c"
CR = b"\r"
BACKSLASH = b"\\"

PAT_TAB = BACKSLASH + TAB
PAT_FF = BACKSLASH + FORMFEED
REPL_TAB = b"\\t"
REPL_FF = b"\\f"

RAW_TAB_REPL = b"t"
RAW_FF_REPL = b"f"

# Common LaTeX commands that break when a backslash is consumed.
COMMAND_FIXES = [
    ("frac", r"\\frac{"),
    ("text", r"\\text{"),
]

# Fix common manglings of \text
MALFORMED_TEXT = [
    (b"\\textext", b"\\text"),
    (b"\\tex\\text", b"\\text"),
]

# Backslash before apostrophe often comes from escaping in CSV/JSON.
APOSTROPHE_ESC = (b"\\'", b"'")



def iter_csv_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_dir():
            for root, _dirs, filenames in os.walk(p):
                for name in filenames:
                    if name.lower().endswith(".csv"):
                        files.append(Path(root) / name)
        elif p.is_file() and p.suffix.lower() == ".csv":
            files.append(p)
    return sorted(set(files))


def fix_bytes(data: bytes) -> tuple[bytes, int, int, int, int, int]:
    esc_tab_count = data.count(PAT_TAB)
    esc_ff_count = data.count(PAT_FF)
    raw_tab_count = data.count(TAB)
    raw_ff_count = data.count(FORMFEED)
    if esc_tab_count:
        data = data.replace(PAT_TAB, REPL_TAB)
    if esc_ff_count:
        data = data.replace(PAT_FF, REPL_FF)
    if raw_tab_count:
        data = data.replace(TAB, RAW_TAB_REPL)
    if raw_ff_count:
        data = data.replace(FORMFEED, RAW_FF_REPL)
    # Normalize Windows/Mac line endings to LF.
    crlf_count = data.count(b"\r\n")
    if crlf_count:
        data = data.replace(b"\r\n", b"\n")
    raw_cr_count = data.count(CR)
    if raw_cr_count:
        data = data.replace(CR, b"\n")

    cmd_count = 0
    for name, repl in COMMAND_FIXES:
        pattern_str = r"(?<!\\){}\{{".format(name)
        pattern = re.compile(pattern_str.encode("ascii"))
        matches = pattern.findall(data)
        if matches:
            cmd_count += len(matches)
            data = pattern.sub(repl.encode("ascii"), data)

    malformed_count = 0
    for bad, good in MALFORMED_TEXT:
        hits = data.count(bad)
        if hits:
            malformed_count += hits
            data = data.replace(bad, good)

    apostrophe_count = data.count(APOSTROPHE_ESC[0])
    if apostrophe_count:
        data = data.replace(*APOSTROPHE_ESC)

    # Collapse doubled backslashes before LaTeX delimiters or commands.
    # This turns "\\frac" -> "\frac" and "\\(" -> "\(".
    dbl_count = 0
    pattern = re.compile(br"\\+(?=[A-Za-z\[\]\(\)])")
    matches = pattern.findall(data)
    if matches:
        dbl_count = len(matches)
        # Use a function to return a single backslash without replacement escaping.
        data = pattern.sub(lambda _m: b"\\", data)

    # Fix a common case where "\right" lost its "\r" and became a newline + "ight".
    right_count = data.count(b"\night")
    if right_count:
        data = data.replace(b"\night", b"\\right")

    # Undo previous CR->'r' conversion at line ends if it happened.
    stray_r_count = data.count(b"\"r\n") + (1 if data.endswith(b"\"r") else 0)
    if b"\"r\n" in data:
        data = data.replace(b"\"r\n", b"\"\n")
    if data.endswith(b"\"r"):
        data = data[:-1]

    return (
        data,
        esc_tab_count,
        esc_ff_count,
        raw_tab_count,
        raw_ff_count,
        raw_cr_count,
        cmd_count + dbl_count + right_count + stray_r_count + malformed_count + apostrophe_count,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fix LaTeX \\t/\\f escape damage in CSV files.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="CSV file(s) or directory(ies) to scan",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write fixes in-place (default is dry-run)",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create .bak backup files when writing",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with code 2 if any fixes would be applied",
    )

    args = parser.parse_args()
    files = iter_csv_files(args.paths)

    if not files:
        print("No CSV files found.")
        return 1

    any_hits = False
    total_tab = 0
    total_ff = 0
    total_cr = 0

    for path in files:
        data = path.read_bytes()
        (
            fixed,
            esc_tab_count,
            esc_ff_count,
            raw_tab_count,
            raw_ff_count,
            raw_cr_count,
            cmd_count,
        ) = fix_bytes(data)
        if (
            esc_tab_count
            or esc_ff_count
            or raw_tab_count
            or raw_ff_count
            or raw_cr_count
            or cmd_count
        ):
            any_hits = True
            total_tab += esc_tab_count + raw_tab_count
            total_ff += esc_ff_count + raw_ff_count
            total_cr += raw_cr_count
            print(
                f"{path}: \\t-> {esc_tab_count}, \\f-> {esc_ff_count}, "
                f"TAB->t: {raw_tab_count}, FF->f: {raw_ff_count}, CR->LF: {raw_cr_count}, "
                f"cmds: {cmd_count}"
            )

            if args.write:
                if not args.no_backup:
                    backup = path.with_suffix(path.suffix + ".bak")
                    if not backup.exists():
                        backup.write_bytes(data)
                path.write_bytes(fixed)

    if not any_hits:
        print("No escaped-LaTeX issues found.")
        return 0

    if args.check:
        print(f"Found {total_tab + total_ff + total_cr} issue(s).")
        return 2

    if not args.write:
        print("Dry-run only. Re-run with --write to apply fixes.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
