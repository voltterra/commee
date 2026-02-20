#!/usr/bin/env bash
# run_headless.sh
# Runs a single non-interactive Claude Code prompt and prints the result.
#
# Usage:
#   bash run_headless.sh "Your prompt here"
#   bash run_headless.sh "Your prompt" --output-format json
#   bash run_headless.sh "Your prompt" --cwd /path/to/project
#   bash run_headless.sh "Your prompt" --max-turns 5
#
# Environment variables:
#   ANTHROPIC_API_KEY   Required for non-interactive use
#   CLAUDE_MODEL        Optional model override (e.g. claude-opus-4-5)
#   CLAUDE_MAX_TURNS    Optional max agentic turns (default: 10)
#
# Output goes to stdout. Exit code mirrors claude's exit code.

set -euo pipefail

# ── Argument parsing ──────────────────────────────────────────────────────────
if [ $# -lt 1 ]; then
  echo "Usage: $0 <prompt> [additional claude flags]"
  echo ""
  echo "Examples:"
  echo "  $0 \"Write a hello world in Python\""
  echo "  $0 \"List files here\" --output-format json"
  echo "  $0 \"Fix bugs\" --cwd /my/project --max-turns 5"
  exit 1
fi

PROMPT="$1"
shift  # remaining args passed directly to claude

# ── Preflight checks ──────────────────────────────────────────────────────────
if ! command -v claude &>/dev/null; then
  echo "[ERROR] 'claude' command not found. Run install_claude_code.sh first." >&2
  exit 1
fi

if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  echo "[ERROR] ANTHROPIC_API_KEY is not set. Export it before running headless mode." >&2
  exit 1
fi

# ── Build claude command ──────────────────────────────────────────────────────
MAX_TURNS="${CLAUDE_MAX_TURNS:-10}"

CMD=(claude --print "$PROMPT" --max-turns "$MAX_TURNS")

# Optional model override
if [ -n "${CLAUDE_MODEL:-}" ]; then
  CMD+=(--model "$CLAUDE_MODEL")
fi

# Append any extra args passed by the caller
CMD+=("$@")

# ── Run ───────────────────────────────────────────────────────────────────────
echo "[claude-code] Running: ${CMD[*]}" >&2
echo "" >&2

"${CMD[@]}"
