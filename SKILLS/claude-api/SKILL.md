---
name: claude-code
description: Use this skill whenever the user wants to call the Claude API or interact with Claude models programmatically — by routing requests through the Claude Code CLI, which reuses the user's existing claude.ai subscription (no separate API key needed). Triggers include: calling Claude API, sending prompts to Claude programmatically, using Claude Code CLI, automating Claude interactions, running headless Claude sessions, or any task that involves invoking Claude from a script or terminal.
license: MIT. LICENSE.txt has complete terms.
---

# Claude Code CLI Skill — Claude API via Subscription

## Overview

This skill uses **Claude Code CLI** as a lightweight proxy to the Claude API, reusing the user's existing **claude.ai subscription** — no separate `ANTHROPIC_API_KEY` is needed.

Claude Code authenticates via OAuth against the user's Anthropic account. When run in headless (`-p`) mode, it sends prompts to Claude and returns responses, effectively functioning as a CLI-accessible Claude API client backed by the subscription.

This skill covers:
- Installing Claude Code
- Authenticating via claude.ai subscription (OAuth)
- Calling Claude API headlessly through the CLI
- Scripting and automation using Claude Code as the API transport

---

## Installation

Claude Code requires **Node.js 18+**.

```bash
npm install -g @anthropic-ai/claude-code
```

Verify installation:
```bash
claude --version
```

---

## Authentication — Subscription-Based (Preferred)

Claude Code authenticates via OAuth against your **claude.ai account**. This reuses your existing subscription — no API key or billing setup required.

```bash
claude  # First run opens a browser login flow; token is cached locally
```

Once logged in, all subsequent `claude` calls (including headless `-p` calls) use the cached OAuth token automatically.

### Fallback: API key (optional)

If the user has an explicit API key and prefers to use it instead:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
claude -p "Your prompt"
```

**Always prefer the subscription/OAuth path.** Only fall back to an API key if the user explicitly requests it or if OAuth login is not possible in the environment.

---

## Basic Usage — Calling Claude API via CLI

### One-shot prompt (headless) — primary pattern
```bash
claude -p "Explain what this repo does" --output-format text
```

### Pipe input from stdin
```bash
cat error.log | claude -p "What caused this error?"
```

### Work in a specific directory
```bash
claude --cwd /path/to/project -p "List all TODO comments in this codebase"
```

### Interactive REPL (for manual exploration)
```bash
claude
```

---

## Key CLI Flags

| Flag | Description |
|------|-------------|
| `-p, --print <prompt>` | Run non-interactively; send prompt to Claude API and exit |
| `--output-format` | `text` (default), `json`, or `stream-json` |
| `--cwd <path>` | Set working directory Claude Code operates in |
| `--model <model>` | Override the model (e.g. `claude-opus-4-5`) |
| `--max-turns <n>` | Limit agentic turns (default: unlimited) |
| `--no-ansi` | Disable colored output (useful for scripting) |
| `--verbose` | Show verbose output including tool calls |
| `--version` | Print version and exit |

---

## Non-Interactive (Headless) Mode — API Calls via CLI

Use `-p` to send a single prompt to the Claude API and get a response back. This is the primary way this skill calls the Claude API.

```bash
# Ask Claude a question
claude -p "What is the capital of France?" --output-format text

# Generate code
claude -p "Write a Python script that checks if a URL is reachable" --output-format text > check_url.py

# Analyze a file
claude -p "Review this Python file for bugs: $(cat myfile.py)"

# Get JSON-structured output
claude -p "List 5 sorting algorithms as JSON with name and complexity fields" --output-format json
```

---

## Common Patterns

### Ask Claude API about a codebase
```bash
cd /path/to/project
claude -p "Summarize the architecture of this project in 3 sentences"
```

### Auto-fix a failing test (agentic)
```bash
claude -p "Run the tests and fix any failures" --max-turns 10
```

### Generate and immediately run code
```bash
claude -p "Write a Python one-liner to find duplicate files in /tmp" --output-format text | python3
```

---

## Using the Helper Scripts

This skill includes ready-to-use scripts in the `scripts/` folder:

| Script | Purpose |
|--------|---------|
| `install_claude_code.sh` | Install/verify Claude Code and Node.js |
| `check_status.sh` | Check Claude Code installation, version, and auth status |
| `run_headless.sh` | Run a one-shot Claude API call via CLI and capture output |
| `pipe_prompt.py` | Python wrapper to call Claude API via CLI programmatically |

---

## Workflow for Claude (AI Assistant)

When the user wants to call the Claude API or run a prompt through Claude Code:

1. **Check if Claude Code is installed** — run `scripts/check_status.sh`
2. **Install if needed** — run `scripts/install_claude_code.sh`
3. **Ensure auth** — if not authenticated, instruct the user to run `claude` once interactively to complete OAuth login (no API key needed)
4. **Run the Claude API call** — use `scripts/run_headless.sh "prompt"` or compose a `claude -p` command directly
5. **Capture and present output** — save results to `/mnt/user-data/outputs/` if the user wants a file

### Example task flow
```
User: "Call Claude API to generate a Python function for me"
→ check_status.sh              (verify installed + authenticated)
→ run_headless.sh "Write a Python function that..."
→ save output → present to user
```

---

## Important Notes

- **Primary auth method is OAuth / claude.ai subscription** — no API key needed. Run `claude` once interactively to complete the login flow; the token is cached for all future calls.
- **API key is a fallback only** — use it only if the user explicitly requests it or if OAuth is unavailable in the environment.
- Non-interactive mode (`-p`) is preferred in automation — it exits cleanly after one task.
- Avoid `--max-turns` values higher than 20 for simple tasks; it can be slow.
- If Claude Code is not installed, always run `install_claude_code.sh` first.
- Rate limits and model access are determined by the user's claude.ai subscription tier.
