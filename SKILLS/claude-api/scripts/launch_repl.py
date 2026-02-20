#!/usr/bin/env python3
"""
launch_repl.py
--------------
Python launcher for an interactive Claude Code CLI session.

Usage (CLI):
    python3 launch_repl.py
    python3 launch_repl.py --cwd /my/project
    python3 launch_repl.py --think
    python3 launch_repl.py --think-hard --cwd /my/project
    python3 launch_repl.py --model claude-opus-4-5

Usage (imported):
    from launch_repl import launch_claude_repl
    launch_claude_repl(cwd="/my/project", think=True)
"""

import argparse
import os
import subprocess
import sys
from typing import Optional


def launch_claude_repl(
    cwd: Optional[str] = None,
    think: bool = False,
    think_hard: bool = False,
    model: Optional[str] = None,
    verbose: bool = False,
    extra_flags: Optional[list] = None,
) -> int:
    """
    Launch an interactive Claude Code CLI REPL session.

    Args:
        cwd:        Working directory for Claude Code to operate in.
        think:      Enable extended thinking (moderate budget).
        think_hard: Enable extended thinking (large budget).
        model:      Model override, e.g. 'claude-opus-4-5'.
        verbose:    Show verbose output including thinking blocks.
        extra_flags: Any additional CLI flags as a list of strings.

    Returns:
        Exit code from the claude process.

    Raises:
        FileNotFoundError: If 'claude' is not installed or not in PATH.
    """
    cmd = ["claude"]

    if think_hard:
        cmd.append("--think-hard")
    elif think:
        cmd.append("--think")

    if cwd:
        cmd += ["--cwd", cwd]

    if model:
        cmd += ["--model", model]

    if verbose:
        cmd.append("--verbose")

    if extra_flags:
        cmd += extra_flags

    try:
        proc = subprocess.run(cmd)
        return proc.returncode
    except FileNotFoundError:
        raise FileNotFoundError(
            "'claude' command not found. "
            "Install it with: npm install -g @anthropic-ai/claude-code"
        )


# ── CLI entrypoint ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Launch an interactive Claude Code CLI REPL session."
    )
    parser.add_argument("--cwd", default=None, help="Working directory")
    parser.add_argument(
        "--think",
        action="store_true",
        help="Enable extended thinking (moderate budget)",
    )
    parser.add_argument(
        "--think-hard",
        action="store_true",
        dest="think_hard",
        help="Enable extended thinking (large budget)",
    )
    parser.add_argument("--model", default=None, help="Model override")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show verbose output including thinking blocks",
    )
    args = parser.parse_args()

    try:
        code = launch_claude_repl(
            cwd=args.cwd,
            think=args.think,
            think_hard=args.think_hard,
            model=args.model,
            verbose=args.verbose,
        )
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    sys.exit(code)


if __name__ == "__main__":
    main()
