#!/usr/bin/env python3
"""
pipe_prompt.py
--------------
Python wrapper to call Claude Code CLI non-interactively.

Usage (CLI):
    python3 pipe_prompt.py "Write a Python function to reverse a string"
    python3 pipe_prompt.py "Explain this code" --cwd /my/project
    python3 pipe_prompt.py "List files" --output-format json --max-turns 5

Usage (imported):
    from pipe_prompt import run_claude_code
    result = run_claude_code("Write a hello world in Go")
    print(result.stdout)
"""

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class ClaudeResult:
    stdout: str
    stderr: str
    returncode: int
    success: bool


def run_claude_code(
    prompt: str,
    cwd: Optional[str] = None,
    output_format: str = "text",
    max_turns: int = 10,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    extra_flags: Optional[list] = None,
) -> ClaudeResult:
    """
    Run Claude Code CLI in headless (non-interactive) mode.

    Args:
        prompt:        The instruction/question to send to Claude Code.
        cwd:           Working directory for Claude Code to operate in.
        output_format: 'text' (default), 'json', or 'stream-json'.
        max_turns:     Max agentic turns before stopping (default 10).
        model:         Model override, e.g. 'claude-opus-4-5'.
        api_key:       Anthropic API key. Falls back to ANTHROPIC_API_KEY env var.
        extra_flags:   Any additional CLI flags as a list of strings.

    Returns:
        ClaudeResult with stdout, stderr, returncode, and success flag.

    Raises:
        FileNotFoundError: If 'claude' is not installed or not in PATH.
        EnvironmentError:  If ANTHROPIC_API_KEY is not available.
    """
    # Resolve API key
    resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not resolved_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Export it or pass api_key= to run_claude_code()."
        )

    # Build command
    cmd = [
        "claude",
        "--print", prompt,
        "--output-format", output_format,
        "--max-turns", str(max_turns),
        "--no-ansi",          # clean output for programmatic use
    ]

    if model:
        cmd += ["--model", model]

    if cwd:
        cmd += ["--cwd", cwd]

    if extra_flags:
        cmd += extra_flags

    env = os.environ.copy()
    env["ANTHROPIC_API_KEY"] = resolved_key

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env=env,
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            "'claude' command not found. "
            "Install it with: npm install -g @anthropic-ai/claude-code"
        )

    return ClaudeResult(
        stdout=proc.stdout,
        stderr=proc.stderr,
        returncode=proc.returncode,
        success=proc.returncode == 0,
    )


# ── CLI entrypoint ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Run a Claude Code CLI prompt non-interactively."
    )
    parser.add_argument("prompt", help="The prompt/instruction to send to Claude Code")
    parser.add_argument("--cwd", default=None, help="Working directory")
    parser.add_argument(
        "--output-format",
        default="text",
        choices=["text", "json", "stream-json"],
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--max-turns",
        type=int,
        default=10,
        help="Maximum agentic turns (default: 10)",
    )
    parser.add_argument("--model", default=None, help="Model override")
    parser.add_argument("--api-key", default=None, help="Anthropic API key")
    args = parser.parse_args()

    try:
        result = run_claude_code(
            prompt=args.prompt,
            cwd=args.cwd,
            output_format=args.output_format,
            max_turns=args.max_turns,
            model=args.model,
            api_key=args.api_key,
        )
    except (FileNotFoundError, EnvironmentError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)

    if result.stderr:
        print(result.stderr, file=sys.stderr)

    print(result.stdout, end="")
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
