# Graphify In-Depth Reference

Graphify v0.9.x · package `graphifyy` (PyPI) · commands `graphify`, `graphify-mcp` · MIT · Python ≥ 3.10

> Organized reference for every command area. The beginner walkthrough is `README.md`; the printable one-pager is `graphify-cheatsheet.html`. Upstream: https://github.com/safishamsi/graphify

---

## Table of Contents

1. [Core concepts](#1-core-concepts)
2. [Installation & platforms](#2-installation--platforms)
3. [Optional extras](#3-optional-extras)
4. [Building a graph (`/graphify`, flags)](#4-building-a-graph)
5. [Querying (`query`, `path`, `explain`)](#5-querying)
6. [Headless extraction (`extract`, backends)](#6-headless-extraction)
7. [Exports (HTML, wiki, Obsidian, Neo4j, SVG…)](#7-exports)
8. [Git hooks & team workflow](#8-git-hooks--team-workflow)
9. [MCP server (`graphify-mcp` / `serve`)](#9-mcp-server)
10. [PR dashboard (`prs`)](#10-pr-dashboard)
11. [Global graph & misc commands](#11-global-graph--misc-commands)
12. [Ignoring files](#12-ignoring-files)
13. [Environment variables](#13-environment-variables)
14. [File types handled](#14-file-types-handled)
15. [Privacy model](#15-privacy-model)
16. [Troubleshooting](#16-troubleshooting)

---

## 1. Core concepts

```
corpus (folder)  ──►  extraction  ──►  graph  ──►  outputs
                       │                            ├─ graph.html      (interactive viz)
   code → tree-sitter AST (local, free)             ├─ GRAPH_REPORT.md (highlights)
   docs/PDFs/images → LLM (via skill or API)        ├─ graph.json      (source of truth)
   video/audio → faster-whisper (local)             └─ optional: wiki, Obsidian, Neo4j…
```

- **Node** — a function, class, file, concept, document, comment-rationale, package…
- **Edge** — calls, imports, references, explains, depends_on… Each tagged `EXTRACTED` / `INFERRED` / `AMBIGUOUS`.
- **Community** — clusters found by community detection (Leiden/Louvain); the report is organized around them.
- **God node** — unusually high-degree node; architectural hotspot.
- Two front doors: the **skill** (`/graphify` inside an AI assistant — uses your assistant's model for semantic work) and the **CLI** (`graphify …` — local AST always; LLM only with a configured backend).

## 2. Installation & platforms

```bash
uv tool install graphifyy      # recommended (then: uv tool update-shell if not found)
pipx install graphifyy         # alternative (then: pipx ensurepath)
pip install graphifyy          # last resort; python3 -m graphify always works
uv tool upgrade graphifyy      # update
```

> `uvx` note: name the package — `uvx --from graphifyy graphify install`. Plain `uvx graphify` fails because the package is `graphifyy`.

**Register the skill** (user-global) or per-repo (`--project`):

```bash
graphify install                     # Claude Code (default platform)
graphify install --project           # into ./.claude/skills/ of current repo
graphify install --platform codex    # other platforms: codebuddy, opencode, kilo,
                                     # copilot, aider, claw, droid, trae, gemini,
                                     # hermes, kimi, pi, agents (cross-framework)…
graphify cursor install              # some platforms use subcommand form:
graphify vscode install              #   cursor, vscode, kiro, devin, amp, antigravity
```

**Always-on graph-first behavior** (per project, after building a graph): `graphify claude install` writes a CLAUDE.md section + PreToolUse hook that nudges Claude Code to `graphify query` instead of grep/read. Equivalents: `graphify codex|opencode|cursor|gemini|kilo|… install`.

**Remove:** `graphify uninstall` (all platforms), `--purge` also deletes `graphify-out/`, or per-platform `graphify claude uninstall`.

## 3. Optional extras

`uv tool install "graphifyy[extra]"` — or `[all]` for everything:

| Extra | Adds |
|---|---|
| `pdf` | PDF extraction |
| `office` | `.docx` / `.xlsx` |
| `google` | Google Sheets rendering (`.gsheet` via `gws` CLI) |
| `video` | video/audio transcription (faster-whisper + yt-dlp) |
| `mcp` | MCP server |
| `svg` | `graph.svg` export |
| `neo4j` / `falkordb` | push to graph databases |
| `leiden` | Leiden clustering (Python < 3.13) |
| `sql` / `postgres` | SQL schema / live PostgreSQL introspection |
| `terraform` | `.tf` / `.hcl` extraction |
| `anthropic` / `openai` / `gemini` / `ollama` / `bedrock` / `kimi` | headless LLM backends |
| `chinese` | jieba query segmentation |

## 4. Building a graph

Inside an assistant, `/graphify` (Codex: `$graphify`; PowerShell: `graphify`, no slash):

```
/graphify                       # current directory
/graphify ./docs                # specific folder
/graphify . --update            # re-extract only changed files
/graphify . --mode deep         # more aggressive relationship extraction
/graphify . --directed          # preserve edge direction
/graphify . --cluster-only      # recluster without re-extracting
/graphify . --cluster-only --resolution 1.5    # finer-grained communities
/graphify . --cluster-only --exclude-hubs 99   # hide utility super-hubs from rankings
/graphify . --no-viz            # skip graph.html (big repos)
/graphify . --watch             # auto-sync as files change ([watch] extra)
/graphify . --force             # overwrite even if new graph has fewer nodes
```

Add external content:

```
/graphify add https://arxiv.org/abs/1706.03762
/graphify add <video-or-youtube-url>            # [video] extra
/graphify add https://... --author "Name"
```

## 5. Querying

```bash
graphify query "what connects auth to the database?"
graphify query "..." --graph path/to/graph.json    # non-default graph
graphify query "..." --dfs --budget 1500           # deeper traversal, bigger answer budget
graphify path "DigestAuth" "Response"              # shortest path between two nodes
graphify explain "RateLimiter"                     # one node: neighbors, docs, rationale
```

- Queries are logged (metadata only) to `~/.cache/graphify-queries.log`; disable with `GRAPHIFY_QUERY_LOG_DISABLE=1`.
- Work memory: `graphify save-result --question "Q" --answer "A" --nodes Foo --outcome useful` records outcomes; `graphify reflect` aggregates them into `reflections/LESSONS.md` (`--if-stale` makes it a cheap no-op when current).

## 6. Headless extraction

`graphify extract` runs without an IDE (CI, cron, servers). Code-only corpora are **fully offline** — no key needed. Docs/PDFs/images need a backend:

```bash
graphify extract .                                # code-only: local, free
graphify extract ./docs --backend claude          # ANTHROPIC_API_KEY
graphify extract ./docs --backend claude-cli      # routes through Claude Code CLI — no key, uses your subscription
graphify extract ./docs --backend gemini          # GEMINI_API_KEY / GOOGLE_API_KEY
graphify extract ./docs --backend openai          # OPENAI_API_KEY (or any OpenAI-compatible server via OPENAI_BASE_URL)
graphify extract ./docs --backend ollama          # local Ollama, no key
graphify extract ./docs --backend bedrock         # AWS IAM credential chain
# also: deepseek, kimi, azure
```

Backend auto-detection priority when unset: Gemini → Kimi → Claude → OpenAI → DeepSeek → Azure → Bedrock → Ollama.

Useful knobs:

```bash
--model <name>            # per-backend model override
--mode deep               # richer semantic extraction
--token-budget 4000       # smaller chunks (local/small models)
--max-concurrency 2       # fewer parallel LLM calls
--max-workers 16          # AST thread parallelism
--api-timeout 900         # slow local models (default 600s)
--no-cluster              # raw extraction, skip clustering
--timing                  # per-stage timings to stderr
--force                   # overwrite smaller rebuilds / clear ghost duplicates
--dedup-llm               # LLM tiebreak for ambiguous entity merges
--global --as myrepo      # register into the cross-project global graph
--postgres "postgresql://…"   # introspect a live database schema
--cargo                   # introspect a Rust workspace
--google-workspace        # export .gdoc/.gsheet/.gslides via gws first
```

## 7. Exports

```bash
graphify export callflow-html                 # Mermaid architecture/call-flow page
graphify export callflow-html --max-sections 8 --output docs/arch.html

/graphify . --wiki                            # agent-crawlable markdown wiki
/graphify . --obsidian                        # Obsidian vault
/graphify . --obsidian --obsidian-dir ~/vault # into an existing vault (non-destructive)
/graphify . --svg                             # graph.svg ([svg] extra)
/graphify . --graphml                         # for Gephi / yEd
/graphify . --neo4j                           # cypher.txt
/graphify . --neo4j-push bolt://localhost:7687
/graphify . --falkordb / --falkordb-push falkordb://localhost:6379
graphify merge-graphs a.json b.json           # combine two graphs
```

## 8. Git hooks & team workflow

```bash
graphify hook install     # post-commit + post-checkout rebuild (AST only, no API cost)
graphify hook status
graphify hook uninstall
```

- Hook install also sets a **merge driver** so `graph.json` union-merges instead of conflicting.
- Hooks embed the interpreter path at install time — re-run `graphify hook install` after upgrading graphify.
- **Team pattern:** commit `graphify-out/` (it's portable); gitignore `graphify-out/cost.json`; everyone pulls a ready-made map; `--update` refreshes docs nodes.

## 9. MCP server

Structured graph access for assistants (tools: `query_graph`, `get_node`, `get_neighbors`, `shortest_path`, `list_prs`, `get_pr_impact`, `triage_prs`). Needs `[mcp]` extra.

```bash
python3 -m graphify.serve graphify-out/graph.json              # stdio (default)
python3 -m graphify.serve graph.json --transport http --port 8080          # shared team server
python3 -m graphify.serve graph.json --transport http --host 0.0.0.0 --api-key "$SECRET"
```

| Flag | Default | Purpose |
|---|---|---|
| `--transport stdio\|http` | stdio | one-per-dev vs shared HTTP (`http://host:8080/mcp`) |
| `--host` / `--port` / `--path` | 127.0.0.1 / 8080 / /mcp | bind + mount |
| `--api-key` | `$GRAPHIFY_API_KEY` | Bearer / X-API-Key auth — required if exposing beyond localhost |
| `--json-response` | off | plain JSON instead of SSE |
| `--stateless` | off | for load-balanced/CI |
| `--session-timeout` | 3600 | reap idle sessions |

## 10. PR dashboard

Requires a GitHub repo (uses `gh`-style auth):

```bash
graphify prs                 # dashboard: CI state, review status, worktrees, graph impact
graphify prs 42              # deep dive incl. graph impact of PR #42
graphify prs --triage        # AI-ranked review queue (backend auto-detected; GRAPHIFY_TRIAGE_BACKEND overrides)
graphify prs --conflicts     # PRs touching the same graph communities → merge-order risk
graphify prs --worktrees     # worktree → branch → PR mapping
graphify prs --base main --repo owner/repo
```

## 11. Global graph & misc commands

```bash
graphify global add graphify-out/graph.json --as myrepo   # cross-project graph at ~/.graphify/global-graph.json
graphify global remove myrepo
graphify global list
graphify global path
graphify clone https://github.com/karpathy/nanoGPT        # clone + graph a repo in one step
```

## 12. Ignoring files

`.graphifyignore` in project root, `.gitignore` syntax incl. `!` negation. `.gitignore` is respected automatically; the two are merged with `.graphifyignore` evaluated last (wins conflicts) but it can only exclude *more*, never re-include something git already ignores. Subdirectory scoping works like git.

```
node_modules/
dist/
# only index src/:
*
!src/
!src/**
```

## 13. Environment variables

Only needed for headless `extract` (the skill uses your IDE session's model):

| Variable | For |
|---|---|
| `ANTHROPIC_API_KEY` / `ANTHROPIC_BASE_URL` / `ANTHROPIC_MODEL` | `--backend claude` (default model `claude-sonnet-4-6`) |
| `GEMINI_API_KEY` or `GOOGLE_API_KEY` | `--backend gemini` |
| `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `OPENAI_MODEL` | `--backend openai` and any OpenAI-compatible server (llama.cpp, vLLM, LM Studio) |
| `DEEPSEEK_API_KEY` · `MOONSHOT_API_KEY` | deepseek / kimi backends |
| `AZURE_OPENAI_API_KEY` + `AZURE_OPENAI_ENDPOINT` (+ `_API_VERSION`, `_DEPLOYMENT`) | `--backend azure` |
| `OLLAMA_BASE_URL` / `OLLAMA_MODEL` / `GRAPHIFY_OLLAMA_NUM_CTX` / `GRAPHIFY_OLLAMA_KEEP_ALIVE` | `--backend ollama` |
| AWS credential chain | `--backend bedrock` (no key, IAM) |
| `GRAPHIFY_MAX_WORKERS` · `GRAPHIFY_MAX_OUTPUT_TOKENS` · `GRAPHIFY_API_TIMEOUT` · `GRAPHIFY_MAX_RETRIES` | performance/limits |
| `GRAPHIFY_FORCE` | same as `--force` |
| `GRAPHIFY_GOOGLE_WORKSPACE=1` | auto-enable Workspace export |
| `GRAPHIFY_TRIAGE_BACKEND` / `GRAPHIFY_TRIAGE_MODEL` | `prs --triage` |
| `GRAPHIFY_QUERY_LOG` / `GRAPHIFY_QUERY_LOG_DISABLE=1` / `GRAPHIFY_QUERY_LOG_RESPONSES=1` | query logging |
| `GRAPHIFY_MAX_GRAPH_BYTES` | raise the 512 MiB graph.json cap (`700MB`, `2GB`) |
| `GRAPHIFY_LLM_TEMPERATURE` | extraction temperature (`none` to omit) |

## 14. File types handled

| Type | Notes |
|---|---|
| Code — 36 tree-sitter grammars | py ts js jsx tsx go rs java c cpp cu metal rb cs kt scala php swift lua zig ps1 ex objc jl vue svelte astro groovy dart verilog sql fortran pascal sh json … (local, free) |
| Salesforce Apex | `.cls` `.trigger` (regex-based) |
| Terraform/HCL | `[terraform]` extra |
| MCP configs / package manifests | `.mcp.json`, `pyproject.toml`, `go.mod`, `pom.xml` → dependency hub nodes |
| Docs | `.md .mdx .html .txt .rst .yaml` — markdown links & `[[wikilinks]]` become edges |
| Office / Google | `.docx .xlsx` (`[office]`); `.gdoc .gsheet .gslides` (opt-in via `gws` + `--google-workspace`) |
| PDFs / images | `[pdf]`; `.png .jpg .webp .gif` |
| Video/audio/YouTube | `[video]` — transcribed locally |

## 15. Privacy model

- **Code** → tree-sitter, local, nothing leaves the machine; code-only extract runs fully offline.
- **Video/audio** → local faster-whisper.
- **Docs/PDFs/images** → sent to whichever model backend you configured (or your IDE session's model via the skill).
- No telemetry. Query metadata logged locally only (see §13 to disable).
- Data residency: `--backend ollama` for fully local; note `kimi` routes to Moonshot servers in China.

## 16. Troubleshooting

| Symptom | Fix |
|---|---|
| `command not found` after install | `uv tool update-shell` / `pipx ensurepath`, new terminal; or `python3 -m graphify` |
| `uvx graphify` → "no versions of graphify" | package is `graphifyy`: `uvx --from graphifyy graphify …` |
| `ModuleNotFoundError: graphify` from the skill | mixed environments — prefer `uv tool install`/`pipx` over plain pip |
| `/graphify .` breaks PowerShell | drop the slash: `graphify .` |
| Fewer nodes after refactor/`--update` | `--force` or `GRAPHIFY_FORCE=1` |
| Duplicate "ghost" nodes (pre-0.8.33 graphs) | `graphify extract . --force` |
| Ollama VRAM / context overflow | `GRAPHIFY_OLLAMA_NUM_CTX=8192 … --token-budget 4000` |
| "LLM returned invalid JSON" warnings | auto-recovered; reduce with `GRAPHIFY_MAX_OUTPUT_TOKENS=16384` or smaller `--token-budget` |
| graph.html too big (>5000 nodes) | `--no-viz`, use `graphify query` |
| `graph.json` merge conflicts | `graphify hook install` (merge driver) |
| Empty nodes for docs/PDFs | needs an LLM — set a backend key or run via the skill |
| Skill version mismatch warning | `uv tool upgrade graphifyy && graphify install` |
