# Graphify — beginner tutorial

Graphify v0.9.x · pip package **`graphifyy`** (double-y!) · CLI command **`graphify`**

Last updated: 2026-07-04

---

## What Graphify is for

Graphify turns a folder — code, markdown docs, PDFs, images, even videos — into a **knowledge graph**: a web of nodes (functions, classes, concepts, documents) connected by edges (calls, imports, references, "explains"). Then, instead of you (or your AI assistant) grepping through files, you *query the graph*:

```bash
graphify query "what connects auth to the database?"
```

It's built primarily as a **skill for AI coding assistants** (Claude Code, Codex, Cursor, Gemini CLI, …). Once installed, you type `/graphify .` inside Claude Code and it maps your whole project. Your assistant then answers architecture questions from the graph instead of re-reading every file — faster and cheaper.

Key facts:

- **Code parsing is 100% local** (tree-sitter AST — 36 languages). No API calls, no code leaves your machine.
- Docs/PDFs/images go through your AI assistant's model for semantic extraction.
- Made by Graphify Labs (YC S26), MIT licensed. Repo: https://github.com/safishamsi/graphify

---

## Install

> ⚠️ The PyPI package is **`graphifyy`** with a double y. The command it installs is still `graphify`. Other `graphify*` packages on PyPI are unaffiliated.

```bash
# recommended — isolated install:
uv tool install graphifyy
# or:
pipx install graphifyy
# or plain pip (may need ~/.local/bin on PATH):
pip install graphifyy
```

Then register the skill with Claude Code:

```bash
graphify install
```

If `graphify: command not found` afterwards: run `uv tool update-shell` (or `pipx ensurepath`), open a new terminal. Worst case, `python3 -m graphify` always works.

---

## First graph — 60-second tour

In Claude Code, inside a project:

```
/graphify .
```

Or straight from the shell for a code-only project (no API key needed — code is parsed locally):

```bash
graphify extract .
```

You get a `graphify-out/` folder:

| File | What it is |
|------|-----------|
| `graph.html` | interactive graph in your browser — click nodes, filter, search |
| `GRAPH_REPORT.md` | the highlights: key concepts, surprising connections, suggested questions |
| `graph.json` | the full graph — what `graphify query` reads |

Open `graph.html` in a browser and click around. The report is the guided tour; the HTML is the map.

For a readable architecture page with call-flow diagrams:

```bash
graphify export callflow-html
```

---

## Asking the graph questions

This is the payoff. All of these work from the shell (and your assistant uses them too):

```bash
graphify query "show the auth flow"
graphify query "what connects RateLimiter to the config loader?"
graphify path "UserService" "DatabasePool"     # shortest path between two things
graphify explain "RateLimiter"                 # everything about one node
```

`query` returns the relevant subgraph — the nodes and relationships that answer the question — not a wall of source code.

---

## What's in the report

- **God nodes** — the most-connected concepts. Everything flows through these.
- **Surprising connections** — links between things in different files/modules, ranked by how unexpected.
- **The "why"** — `# NOTE:` / `# HACK:` comments, docstrings, and design rationale become their own nodes, linked to the code they explain.
- **Suggested questions** — 4–5 questions the graph is well positioned to answer.
- **Confidence tags** — every relationship is marked `EXTRACTED`, `INFERRED`, or `AMBIGUOUS`, so you know what was found vs guessed.

---

## Keeping the graph fresh

```bash
/graphify . --update        # re-extract only changed files (fast)
graphify hook install       # auto-rebuild on every git commit (AST only, free)
```

The git hook also installs a merge driver so `graph.json` never gets conflict markers when two people commit at once.

---

## Ignoring files

Create `.graphifyignore` in the project root — same syntax as `.gitignore` (your `.gitignore` is already respected automatically; this only ever excludes *more*):

```
node_modules/
dist/
*.generated.py
```

---

## Making your assistant graph-first

One more optional step per project:

```bash
graphify claude install
```

This writes a CLAUDE.md section + a hook so Claude Code automatically reaches for `graphify query` instead of grepping when you ask codebase questions.

Remove everything later with `graphify uninstall` (add `--purge` to also delete `graphify-out/`).

---

## Adding non-code things

```bash
/graphify add https://arxiv.org/abs/1706.03762   # fetch a paper into the graph
/graphify add <youtube-url>                       # transcribe a video into it (needs [video] extra)
```

Extras are opt-in installs: `uv tool install "graphifyy[pdf]"` for PDFs, `[office]` for .docx/.xlsx, `[video]` for transcription, `[all]` for everything. See REFERENCE.md.

---

## Mental model

```
your folder
  ├─ code      ──(tree-sitter, local)──►  nodes: functions/classes  edges: calls/imports
  ├─ docs/PDFs ──(LLM extraction)─────►  nodes: concepts           edges: references/explains
  └─ media     ──(local whisper)──────►  transcripts → concepts
                                │
                                ▼
                        graphify-out/graph.json
                                │
              ┌─────────────────┼──────────────────┐
              ▼                 ▼                  ▼
         graph.html      GRAPH_REPORT.md    graphify query / MCP
         (explore)       (read)             (ask questions)
```

---

## Troubleshooting quickies

- **`command not found`** → `uv tool update-shell` or `pipx ensurepath`, new terminal.
- **`uvx graphify` fails** → the *package* is `graphifyy`: `uvx --from graphifyy graphify …`
- **Empty nodes for docs/PDFs** → those need an LLM; run via the `/graphify` skill or set an API key for `graphify extract`.
- **Graph shrank after a refactor** → `graphify extract . --force`
- **Huge repo, HTML won't open** → build with `--no-viz` and use `graphify query` instead.

---

## Further reading

- `REFERENCE.md` in this folder — full command/flag/env-var reference
- `graphify-cheatsheet.html` in this folder — printable one-pager
- https://github.com/safishamsi/graphify — upstream README (very thorough)
