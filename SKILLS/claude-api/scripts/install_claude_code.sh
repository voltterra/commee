#!/usr/bin/env bash
# install_claude_code.sh
# Installs Claude Code CLI if not already installed.
# Usage: bash install_claude_code.sh

set -euo pipefail

echo "=== Claude Code CLI Installer ==="

# ── 1. Check Node.js ──────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
  echo "[ERROR] Node.js is not installed. Claude Code requires Node.js 18+."
  echo "Install Node.js via: https://nodejs.org or your system package manager."
  exit 1
fi

NODE_VERSION=$(node --version | sed 's/v//')
NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)

if [ "$NODE_MAJOR" -lt 18 ]; then
  echo "[ERROR] Node.js $NODE_VERSION is too old. Claude Code requires Node.js 18+."
  exit 1
fi

echo "[OK] Node.js $NODE_VERSION detected."

# ── 2. Check npm ──────────────────────────────────────────────────────────────
if ! command -v npm &>/dev/null; then
  echo "[ERROR] npm is not found. Please install npm."
  exit 1
fi
echo "[OK] npm $(npm --version) detected."

# ── 3. Check if Claude Code is already installed ───────────────────────────────
if command -v claude &>/dev/null; then
  CURRENT_VERSION=$(claude --version 2>/dev/null || echo "unknown")
  echo "[OK] Claude Code already installed: $CURRENT_VERSION"
  echo "To update: npm update -g @anthropic-ai/claude-code"
  exit 0
fi

# ── 4. Install Claude Code ────────────────────────────────────────────────────
echo "Installing @anthropic-ai/claude-code globally..."
npm install -g @anthropic-ai/claude-code

# ── 5. Verify ─────────────────────────────────────────────────────────────────
if command -v claude &>/dev/null; then
  echo "[SUCCESS] Claude Code installed: $(claude --version)"
else
  echo "[ERROR] Installation completed but 'claude' command not found in PATH."
  echo "You may need to add npm global bin to your PATH:"
  echo "  export PATH=\"\$(npm root -g)/../bin:\$PATH\""
  exit 1
fi
