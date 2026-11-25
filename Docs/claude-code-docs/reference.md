# Claude Code — Complete Reference

> Last verified: 2026-04-27 against `claude --help` output.
> Claude Code is the Anthropic CLI at `~/.claude/` — interactive AI coding assistant in your terminal.

---

## Table of Contents

1. [Starting Claude](#1-starting-claude)
2. [CLI Flags](#2-cli-flags)
3. [Subcommands](#3-subcommands)
4. [Slash Commands (in-session)](#4-slash-commands-in-session)
5. [Keyboard Shortcuts](#5-keyboard-shortcuts)
6. [Configuration Files & Locations](#6-configuration-files--locations)
7. [Settings Reference](#7-settings-reference)
8. [Permissions System](#8-permissions-system)
9. [Hooks](#9-hooks)
10. [CLAUDE.md — Project Memory](#10-claudemd--project-memory)
11. [MCP Servers](#11-mcp-servers)
12. [Plugins](#12-plugins)
13. [Tools Claude Can Use](#13-tools-claude-can-use)
14. [Models](#14-models)
15. [Context & Usage Management](#15-context--usage-management)
16. [Automation & Scripting](#16-automation--scripting)
17. [Environment Variables](#17-environment-variables)

---

## 1. Starting Claude

```bash
claude                        # interactive session in current dir
claude "fix the login bug"    # start with an initial prompt
claude -c                     # continue most recent conversation here
claude -r                     # open resume picker (all sessions)
claude -r <session-id>        # resume a specific session
```

---

## 2. CLI Flags

### Session Control

| Flag | Short | Description |
|------|-------|-------------|
| `--continue` | `-c` | Continue the most recent conversation in current dir |
| `--resume [id]` | `-r` | Resume by session ID or open picker |
| `--fork-session` | | Create new session ID when resuming (branch off) |
| `--from-pr [num]` | | Resume session linked to a GitHub PR |
| `--name <name>` | `-n` | Display name for this session |
| `--session-id <uuid>` | | Force a specific UUID for the session |
| `--no-session-persistence` | | Don't save session to disk (print mode only) |

### Input / Output

| Flag | Short | Description |
|------|-------|-------------|
| `--print` | `-p` | Non-interactive: print response and exit |
| `--output-format <fmt>` | | `text` (default), `json`, `stream-json` |
| `--input-format <fmt>` | | `text` (default), `stream-json` |
| `--json-schema <schema>` | | Validate output against a JSON Schema |
| `--include-partial-messages` | | Stream partial chunks (with `stream-json`) |
| `--include-hook-events` | | Include hook lifecycle in output stream |
| `--replay-user-messages` | | Echo user messages back on stdout |
| `--verbose` | | Show extra debug info |
| `--no-markdown` | | Disable markdown rendering (set in config) |

### Model & Effort

| Flag | Description |
|------|-------------|
| `--model <model>` | Model alias (`sonnet`, `opus`, `haiku`) or full ID |
| `--effort <level>` | Thinking budget: `low`, `medium`, `high`, `xhigh`, `max` |
| `--fallback-model <model>` | Auto-fallback when primary is overloaded (print mode only) |

### Tools & Permissions

| Flag | Description |
|------|-------------|
| `--allowedTools <tools...>` | Whitelist specific tools, e.g. `"Bash(git *) Edit"` |
| `--disallowedTools <tools...>` | Blacklist specific tools |
| `--tools <tools...>` | Set exact tool list; `""` disables all, `"default"` = all |
| `--permission-mode <mode>` | `default`, `acceptEdits`, `auto`, `bypassPermissions`, `dontAsk`, `plan` |
| `--dangerously-skip-permissions` | Bypass all permission checks (sandboxes only) |
| `--allow-dangerously-skip-permissions` | Allow that mode to be toggled in-session |
| `--add-dir <dirs...>` | Extra directories Claude can access |

### System Prompt

| Flag | Description |
|------|-------------|
| `--system-prompt <text>` | Replace the default system prompt |
| `--append-system-prompt <text>` | Add to end of default system prompt |
| `--exclude-dynamic-system-prompt-sections` | Move machine-specific sections to first user message (better cache reuse across users) |

### Configuration

| Flag | Description |
|------|-------------|
| `--settings <file-or-json>` | Load extra settings from file path or JSON string |
| `--setting-sources <list>` | Which sources to load: `user`, `project`, `local` |
| `--mcp-config <configs...>` | Load MCP servers from JSON files or strings |
| `--strict-mcp-config` | Only use `--mcp-config` servers, ignore all other MCP config |
| `--plugin-dir <path>` | Load plugins from dir for this session only (repeatable) |
| `--agents <json>` | Define custom agents inline as JSON |
| `--agent <agent>` | Use a named agent for this session |

### Development & Debug

| Flag | Description |
|------|-------------|
| `--debug [filter]` | Debug mode; filter categories e.g. `"api,hooks"` or `"!1p,!file"` |
| `--debug-file <path>` | Write debug logs to file |
| `--bare` | Minimal mode — no hooks, no CLAUDE.md, no auto-memory, no keychain |
| `--ide` | Auto-connect to IDE if exactly one is available |
| `--chrome` | Enable Claude in Chrome integration |
| `--worktree [name]` | `-w` — Create a git worktree for this session |
| `--tmux` | Open worktree in a tmux session |
| `--betas <betas...>` | Beta feature headers (API key users only) |
| `--brief` | Enable `SendUserMessage` tool for agent-to-user comms |
| `--disable-slash-commands` | Disable all skills/slash commands |

---

## 3. Subcommands

```bash
claude <subcommand> [options]
```

### `auth`

```bash
claude auth login             # sign in to Anthropic account
claude auth logout            # sign out
claude auth status            # show current auth state
```

### `mcp`

```bash
claude mcp list                               # list configured MCP servers
claude mcp add <name> <cmd> [args...]         # add stdio server
claude mcp add --transport http <name> <url>  # add HTTP server
claude mcp add --transport sse <name> <url>   # add SSE server
claude mcp add -e KEY=val <name> <cmd>        # add with env vars
claude mcp add -s project <name> <cmd>        # scope: user|project|local
claude mcp add-json <name> '<json>'           # add from raw JSON
claude mcp add-from-claude-desktop            # import from Claude Desktop (Mac/WSL)
claude mcp get <name>                         # details for one server
claude mcp remove <name>                      # remove a server
claude mcp reset-project-choices              # reset approved/rejected .mcp.json servers
claude mcp serve                              # start Claude Code as an MCP server itself
```

### `agents`

```bash
claude agents                 # list background and configured agents
```

### `plugin` / `plugins`

```bash
claude plugin list                    # list installed plugins
claude plugin install <plugin>        # install from marketplace
claude plugin install <p>@<market>    # install from specific marketplace
claude plugin uninstall <plugin>      # remove plugin
claude plugin enable <plugin>         # enable disabled plugin
claude plugin disable <plugin>        # disable plugin
claude plugin update <plugin>         # update to latest
claude plugin validate <path>         # validate plugin manifest
claude plugin tag [path]              # create release git tag
claude plugin marketplace             # manage marketplaces
```

### `update` / `upgrade`

```bash
claude update                 # check for and install updates
```

### `install`

```bash
claude install                # install native build (stable)
claude install latest         # install latest version
claude install <version>      # install specific version
```

### `doctor`

```bash
claude doctor                 # health-check the auto-updater and MCP servers
```

### `setup-token`

```bash
claude setup-token            # set up long-lived auth token (requires subscription)
```

### `auto-mode`

```bash
claude auto-mode              # inspect auto-mode classifier configuration
```

---

## 4. Slash Commands (in-session)

Type these at the prompt during an interactive session.

### Session Management

| Command | Description |
|---------|-------------|
| `/new` | Start a fresh conversation (clears history, keeps dir) |
| `/clear` | Same as `/new` — wipes context |
| `/compact [instructions]` | Summarize and compress the conversation. Optional focus e.g. `/compact focus on the auth module` |
| `/exit` or `/quit` | End the session |

### Conversation Info

| Command | Description |
|---------|-------------|
| `/cost` | Show token usage and estimated cost for this session |
| `/status` | Show current model, context usage %, and session info |

### Configuration

| Command | Description |
|---------|-------------|
| `/config` | Open interactive config editor |
| `/model` | Switch model for current session |
| `/fast` | Toggle Fast mode (Opus 4.6 with faster output) |
| `/permissions` | View current permission rules |
| `/memory` | Edit the project's CLAUDE.md file |

### Input Modes

| Command | Description |
|---------|-------------|
| `/vim` | Enter vim-style input mode for multi-line editing |

### Account

| Command | Description |
|---------|-------------|
| `/login` | Switch Anthropic accounts |
| `/logout` | Log out |
| `/bug` | Report a bug to Anthropic |

### Skills (User-invocable)

Skills are slash commands defined by plugins or built-in:

| Command | Description |
|---------|-------------|
| `/init` | Initialize a CLAUDE.md for the current project |
| `/review` | Review current branch as a pull request |
| `/security-review` | Security review of pending branch changes |
| `/ultrareview` | Multi-agent cloud review (current branch or `/ultrareview <PR#>`) |
| `/simplify` | Review changed code for quality/efficiency and fix issues |
| `/schedule` | Create/manage scheduled remote agents |
| `/loop [interval] [cmd]` | Run a command on a recurring interval |
| `/update-config` | Modify settings.json via natural language |
| `/keybindings-help` | Customize keyboard shortcuts |
| `/fewer-permission-prompts` | Auto-add allowlist rules based on your history |
| `/claude-api` | Build/debug Claude API apps |
| `/statusline-setup` | Configure the status line |

---

## 5. Keyboard Shortcuts

In the interactive prompt:

| Key | Action |
|-----|--------|
| `Enter` | Submit message |
| `Shift+Enter` | New line (multi-line input) |
| `\` + `Enter` | New line (alternative) |
| `Up` / `Down` | Navigate message history |
| `Ctrl+C` | Cancel current operation / interrupt Claude |
| `Ctrl+D` | Exit session (EOF) |
| `Ctrl+R` | Search input history |
| `Ctrl+L` | Clear screen |
| `Escape` | Cancel / go back |
| `Tab` | Autocomplete file paths and slash commands |

Custom keybindings are stored in `~/.claude/keybindings.json`.

---

## 6. Configuration Files & Locations

### File Hierarchy (loaded in order, later overrides earlier)

```
~/.claude/settings.json              # global user settings
<project>/.claude/settings.json      # project settings (commit this)
<project>/.claude/settings.local.json # local overrides (gitignore this)
```

### Other Important Paths

```
~/.claude/CLAUDE.md                  # global memory (all sessions)
<project>/CLAUDE.md                  # project memory (auto-loaded)
<project>/.claude/                   # project Claude state dir
~/.claude/projects/<path>/           # stored conversations
~/.claude/projects/<path>/<id>.jsonl # individual session transcript
~/.claude/keybindings.json           # custom key bindings
~/.claude/cache/                     # internal cache
~/.claude/.credentials.json          # auth tokens (don't touch)
```

### MCP Config Files

```
~/.claude/mcp.json                   # global MCP servers (user scope)
<project>/.mcp.json                  # project MCP servers (commit this)
```

---

## 7. Settings Reference

Settings are JSON. All keys are optional.

### `settings.json` — Full Reference

```json
{
  "model": "claude-sonnet-4-6",
  "theme": "dark",
  "verbose": false,
  "autoUpdates": true,
  "includeCoAuthoredBy": true,

  "statusLine": {
    "type": "command",
    "command": "<shell command that reads JSON from stdin and outputs a string>"
  },

  "env": {
    "MY_VAR": "value"
  },

  "apiKeyHelper": "/path/to/script-that-prints-api-key",

  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm run *)",
      "Read(~/projects/*)",
      "Edit(~/projects/*)"
    ],
    "deny": [
      "Bash(rm -rf *)"
    ]
  },

  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "Notification": [...],
    "Stop": [...],
    "SubagentStop": [...]
  }
}
```

### Theme Options

`"dark"` | `"light"` | `"dark-daltonism"` | `"light-daltonism"` | `"system"`

---

## 8. Permissions System

Controls which tool calls Claude can make without asking.

### Permission Patterns

```
Bash(git *)           # git commands only
Bash(npm run *)       # npm run scripts only
Bash                  # all bash (no restriction)
Read(~/projects/*)    # read anywhere in projects
Edit(src/*)           # edit files in src/
Write                 # all file writes
WebFetch(https://docs.example.com/*)
```

### Permission Modes (CLI / config)

| Mode | Description |
|------|-------------|
| `default` | Ask for each new tool pattern |
| `acceptEdits` | Auto-approve file edits, ask for Bash |
| `auto` | Attempt to auto-classify risky vs. safe |
| `dontAsk` | Auto-approve everything in current session |
| `bypassPermissions` | Skip all checks (sandboxes only) |
| `plan` | Read-only mode — no writes or executes |

Set per session with `--permission-mode <mode>` or in settings:

```json
{ "defaultPermissionMode": "acceptEdits" }
```

### Scopes

Rules in `~/.claude/settings.json` apply globally.
Rules in `<project>/.claude/settings.json` apply to that project only.

---

## 9. Hooks

Shell commands that fire at lifecycle events. Defined in `settings.json`.

### Hook Events

| Event | Fires When |
|-------|-----------|
| `PreToolUse` | Before Claude calls any tool |
| `PostToolUse` | After a tool call completes |
| `Notification` | Claude wants to notify you |
| `Stop` | Claude finishes a response turn |
| `SubagentStop` | A spawned subagent finishes |

### Hook Structure

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'About to run bash' >> /tmp/claude.log"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "notify-send 'Claude is done'"
          }
        ]
      }
    ]
  }
}
```

### Hook Input (stdin JSON)

Hooks receive a JSON object on stdin with:

```json
{
  "session_id": "...",
  "tool_name": "Bash",
  "tool_input": { "command": "ls" },
  "tool_response": "...",
  "workspace": { "current_dir": "/home/you/projects/foo" },
  "model": { "display_name": "claude-sonnet-4-6" },
  "context_window": { "used_percentage": 42.1 }
}
```

### Hook Exit Codes

| Exit Code | Meaning |
|-----------|---------|
| `0` | Success, continue |
| `2` | Block the tool call (PreToolUse only) |
| other | Log warning, continue |

### Status Line Hook Example

```json
{
  "statusLine": {
    "type": "command",
    "command": "input=$(cat); cwd=$(echo \"$input\" | jq -r '.workspace.current_dir'); model=$(echo \"$input\" | jq -r '.model.display_name'); echo \"$cwd | $model\""
  }
}
```

---

## 10. CLAUDE.md — Project Memory

A markdown file Claude reads at the start of every session in that directory.

### Locations

| File | Scope |
|------|-------|
| `~/.claude/CLAUDE.md` | Global — loaded in every session |
| `<project>/CLAUDE.md` | Project — loaded when working in that dir |
| `<project>/subdir/CLAUDE.md` | Sub-directory — loaded when cwd is that subdir |

### What to Put In It

```markdown
# Project Name

## Architecture
Brief description of how the system is structured.

## Key Commands
- Build: `make build`
- Test: `pytest`
- Deploy: `./deploy.sh prod`

## Conventions
- Use snake_case for Python, camelCase for JS
- All API endpoints live in src/api/

## Gotchas
- Never call `reboot` on the prod box
- The `legacy/` dir is read-only, don't touch it
```

### Tips

- Keep it under ~100 lines — it's loaded into every context
- Put commands Claude will need to run frequently
- Put constraints and "never do X" rules here
- `/init` auto-generates one from your codebase
- `/memory` opens it for quick editing

---

## 11. MCP Servers

Model Context Protocol — plugs external tools and data sources into Claude.

### Server Scopes

| Scope | File | Who Sees It |
|-------|------|-------------|
| `user` | `~/.claude/mcp.json` | You, all projects |
| `project` | `<project>/.mcp.json` | Everyone on the project (commit this) |
| `local` | local settings | You, this project only |

### Add a Server

```bash
# stdio (subprocess)
claude mcp add my-server npx my-mcp-package

# stdio with env vars
claude mcp add -e API_KEY=abc my-server npx my-mcp-package

# HTTP
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# HTTP with auth header
claude mcp add --transport http myapi https://api.example.com/mcp \
  --header "Authorization: Bearer mytoken"

# Project scope
claude mcp add -s project my-server npx my-mcp-package

# Import from Claude Desktop
claude mcp add-from-claude-desktop
```

### `.mcp.json` Format (project file)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["my-mcp-package"],
      "env": { "API_KEY": "abc" }
    },
    "my-http-server": {
      "transport": "http",
      "url": "https://api.example.com/mcp",
      "headers": { "Authorization": "Bearer token" }
    }
  }
}
```

### Claude as an MCP Server

```bash
claude mcp serve              # expose Claude Code as an MCP server itself
```

---

## 12. Plugins

Extend Claude Code with new slash commands, skills, and tools.

```bash
claude plugin install <name>             # install from default marketplace
claude plugin install <name>@<market>    # install from specific marketplace
claude plugin list                       # list what's installed
claude plugin enable/disable <name>      # toggle without uninstalling
claude plugin update <name>              # update to latest
claude plugin uninstall <name>           # remove
claude plugin marketplace                # manage marketplaces
```

Plugins can define:
- New slash commands (skills)
- New tools Claude can call
- New agents with custom system prompts

---

## 13. Tools Claude Can Use

These are the built-in tools available to Claude in a session.

### File System

| Tool | Description |
|------|-------------|
| `Read` | Read a file (supports: text, images, PDFs, Jupyter notebooks) |
| `Write` | Write / overwrite a file |
| `Edit` | Make targeted string replacements (sends only the diff) |
| `NotebookEdit` | Edit Jupyter notebook cells |

### Shell

| Tool | Description |
|------|-------------|
| `Bash` | Run any shell command; results can be large (be careful) |

### Web

| Tool | Description |
|------|-------------|
| `WebSearch` | Search the web |
| `WebFetch` | Fetch a URL and return content; large pages become tool result files |

### Agents & Tasks

| Tool | Description |
|------|-------------|
| `Agent` | Spawn a subagent (separate context, runs a task, returns result) |
| `TaskCreate` | Create a tracked task |
| `TaskUpdate` | Update task status (in_progress, completed, etc.) |
| `TaskGet` | Get a task's details |
| `TaskList` | List all tasks |
| `TaskOutput` | Get a task's output |
| `TaskStop` | Stop a running task |

### Scheduling

| Tool | Description |
|------|-------------|
| `CronCreate` | Create a recurring scheduled job |
| `CronList` | List cron jobs |
| `CronDelete` | Delete a cron job |
| `ScheduleWakeup` | Schedule a one-shot future wakeup (for `/loop`) |
| `RemoteTrigger` | Trigger a remote agent |

### Interaction

| Tool | Description |
|------|-------------|
| `AskUserQuestion` | Ask the user a clarifying question mid-task |
| `PushNotification` | Send a push notification to your device |
| `Monitor` | Stream events from a background process |

### Planning

| Tool | Description |
|------|-------------|
| `EnterPlanMode` | Switch to plan-only mode (no writes) |
| `ExitPlanMode` | Return from plan mode |
| `EnterWorktree` | Switch to a git worktree |
| `ExitWorktree` | Exit worktree |

### Restricting Tools

```bash
# Only allow read-only tools
claude --tools "Read,WebSearch,WebFetch"

# Disable all tools
claude --tools ""

# Blacklist one tool
claude --disallowedTools Bash
```

---

## 14. Models

### Available Models

| Alias | Full Model ID | Best For |
|-------|--------------|----------|
| `opus` | `claude-opus-4-7` | Most capable, complex reasoning |
| `sonnet` | `claude-sonnet-4-6` | Default — speed/capability balance |
| `haiku` | `claude-haiku-4-5-20251001` | Fast, lightweight tasks |

### Switching Models

```bash
claude --model opus           # start with Opus
claude --model sonnet         # start with Sonnet (default)
claude --model haiku          # start with Haiku
```

In-session:
```
/model                        # open model picker
/fast                         # toggle Fast mode (Opus 4.6, faster output)
```

In settings:
```json
{ "model": "claude-opus-4-7" }
```

### Effort / Thinking Budget

Controls how much extended thinking the model does before responding.

```bash
claude --effort low           # minimal thinking
claude --effort medium        # balanced
claude --effort high          # deeper reasoning
claude --effort xhigh         # extended reasoning
claude --effort max           # maximum thinking budget
```

---

## 15. Context & Usage Management

### See Current Usage

```
/cost       # tokens used + estimated $ cost for this session
/status     # context window %, model, session info
```

### Reduce Context Bloat

| Problem | Fix |
|---------|-----|
| Long conversation | `/compact` — summarizes and compresses history |
| Unrelated task | `/clear` or `/new` — fresh context |
| Huge bash output | Pipe through `head -50` or use `-q` flags |
| git commit lists all files | Use `git commit -q` |
| `find` on large trees | Add `| head -30` or `-maxdepth 2` |
| WebFetch of big page | Ask Claude to fetch only what you need |

### Context Window at 50%? Best Practices

- `/compact` at ~40% to get a clean summarized history
- `/new` when switching to a completely different task
- Avoid `ls -R`, `find /`, `cat` on large files — use targeted reads
- Don't `git commit` without `-q` on large repos

### Session Continuity

```bash
claude -c                     # continue most recent session in this dir
claude -r                     # pick from all sessions (fuzzy search)
claude -r <session-id>        # resume exact session
claude -r --fork-session      # branch off a resumed session (new ID)
```

---

## 16. Automation & Scripting

### Non-interactive (pipe-friendly)

```bash
# Print mode — returns output and exits
echo "explain this code" | claude -p
claude -p "summarize README.md"

# JSON output
claude -p --output-format json "list 3 improvements"

# Streaming JSON
claude -p --output-format stream-json "write a test"

# Budget cap (fails if exceeded)
claude -p --max-budget-usd 0.10 "refactor this function"

# Structured output validated against schema
claude -p --json-schema '{"type":"object","properties":{"name":{"type":"string"}}}' "..."

# Pipe code in
cat myfile.py | claude -p "find bugs in this"
```

### Agents

```bash
# Define custom agents inline
claude --agents '{"reviewer": {"description": "Reviews code", "prompt": "You are a strict code reviewer."}}'

# Use a named agent
claude --agent reviewer
```

### Worktrees (isolated branches)

```bash
claude -w                     # create git worktree for this session
claude -w my-feature          # named worktree
claude -w --tmux              # open in tmux pane
```

### Scheduled / Background

Use `/schedule` in-session to set up recurring remote agents.
Use `/loop` to run a command on a repeating interval during a session.

---

## 17. Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API key (skips OAuth login) |
| `ANTHROPIC_MODEL` | Default model override |
| `ANTHROPIC_SMALL_FAST_MODEL` | Model for background/lightweight tasks |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Max tokens per response |
| `BASH_DEFAULT_TIMEOUT_MS` | Default bash command timeout (ms) |
| `BASH_MAX_TIMEOUT_MS` | Maximum allowed bash timeout |
| `MAX_MCP_OUTPUT_TOKENS` | Token limit for MCP tool results |
| `DISABLE_AUTOUPDATER` | `1` to disable auto-updates |
| `DISABLE_ERROR_REPORTING` | `1` to disable telemetry |
| `CLAUDE_CODE_SIMPLE` | Set by `--bare` mode; disables most features |
| `ANTHROPIC_BASE_URL` | Override API endpoint (Bedrock, Vertex, etc.) |

You can also set env vars per-project in settings:

```json
{
  "env": {
    "NODE_ENV": "development",
    "PYTHONDONTWRITEBYTECODE": "1"
  }
}
```

---

## Quick Reference Card

```
STARTING
  claude                        interactive
  claude "prompt"               start with message
  claude -c                     continue last session
  claude -r                     resume picker
  claude -p "prompt"            non-interactive output

IN-SESSION
  /new or /clear                fresh context
  /compact                      summarize & compress
  /cost                         token usage
  /status                       context %, model
  /model                        switch model
  /fast                         toggle fast mode
  /vim                          vim input mode
  /memory                       edit CLAUDE.md
  /init                         create CLAUDE.md
  /review                       PR review

MODELS
  --model opus                  claude-opus-4-7
  --model sonnet                claude-sonnet-4-6 (default)
  --model haiku                 claude-haiku-4-5

PERMISSIONS
  --permission-mode auto        auto-approve safe ops
  --permission-mode plan        read-only mode
  --allowedTools "Bash(git *)"  whitelist pattern

CONFIG FILES
  ~/.claude/settings.json       global settings
  .claude/settings.json         project settings
  CLAUDE.md                     project memory
  .mcp.json                     project MCP servers
```
