#!/usr/bin/env bash
# check_status.sh
# Checks Claude Code CLI installation, version, and authentication status.
# Usage: bash check_status.sh
# Exits 0 if Claude Code is ready, non-zero otherwise.

set -euo pipefail

PASS="[OK]"
FAIL="[FAIL]"
WARN="[WARN]"

echo "=== Claude Code Status Check ==="
ALL_OK=true

# ── 1. Node.js ────────────────────────────────────────────────────────────────
if command -v node &>/dev/null; then
  NODE_VER=$(node --version)
  NODE_MAJOR=$(echo "$NODE_VER" | sed 's/v//' | cut -d. -f1)
  if [ "$NODE_MAJOR" -ge 18 ]; then
    echo "$PASS Node.js $NODE_VER"
  else
    echo "$FAIL Node.js $NODE_VER (need 18+)"
    ALL_OK=false
  fi
else
  echo "$FAIL Node.js not found"
  ALL_OK=false
fi

# ── 2. Claude Code binary ────────────────────────────────────────────────────
if command -v claude &>/dev/null; then
  CLAUDE_VER=$(claude --version 2>/dev/null || echo "unknown")
  CLAUDE_PATH=$(command -v claude)
  echo "$PASS Claude Code $CLAUDE_VER ($CLAUDE_PATH)"
else
  echo "$FAIL 'claude' command not found in PATH"
  echo "       Run: npm install -g @anthropic-ai/claude-code"
  ALL_OK=false
fi

# ── 3. API key / auth ─────────────────────────────────────────────────────────
if [ -n "${ANTHROPIC_API_KEY:-}" ]; then
  # Mask key for display
  MASKED="${ANTHROPIC_API_KEY:0:10}...${ANTHROPIC_API_KEY: -4}"
  echo "$PASS ANTHROPIC_API_KEY is set ($MASKED)"
else
  echo "$WARN ANTHROPIC_API_KEY is not set"
  echo "       Non-interactive (headless) use requires an API key."
  echo "       Export it with: export ANTHROPIC_API_KEY='sk-ant-...'"
  # Not a hard failure — interactive login may still work
fi

# ── 4. Summary ────────────────────────────────────────────────────────────────
echo ""
if $ALL_OK; then
  echo "=== Claude Code is ready to use ==="
  exit 0
else
  echo "=== Issues detected — see above ==="
  exit 1
fi
