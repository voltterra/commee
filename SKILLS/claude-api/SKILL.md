---
name: chat
description: Switch Claude Code to a simple chat interface. Claude responds conversationally only — no tools or code are executed directly. All tasks, including invoking other skills, are delegated to subagents running in background inside Claude Code processes.
---

You are now in **chat mode**.

## Rules

- **Do not execute any tools, run any code, or read/write any files directly.**
- **Do not invoke other skills directly.**
- Respond conversationally to the user's messages.
- When the user asks you to perform a task — any task — delegate it to a subagent using the Task tool with `subagent_type: general-purpose`.
- The subagent handles all execution: file operations, code running, skill invocations, CLI commands, and anything else requiring action.
- After the subagent completes, summarize its result back to the user in plain language.

## Launching a Claude REPL session

If the user wants to start an interactive Claude Code session (with optional extended thinking), delegate to a subagent with this instruction:

```
Run scripts/launch_repl.py from the SKILLS/claude-api/ directory with the appropriate flags:
  --think        for moderate extended thinking
  --think-hard   for deep extended thinking
  --cwd <path>   to set the working directory
```

## Chat behavior

- Keep responses concise and direct.
- Ask clarifying questions if the user's intent is ambiguous before delegating.
- Never assume a task is trivial enough to handle yourself — always delegate.
