# Lorengine — Claude Code Context

This file documents the **Lorengine engine** (upstream). It is owned by the upstream
repo and should never be edited in a downstream fork.

Project-specific context lives in `CLAUDE.local.md` in the downstream repo.
Claude Code reads both files. Start there for content-specific instructions.

---

## What this repo is

**Lorengine** is a reusable, self-hosted wiki system designed for game design
documentation (or any markdown-based knowledge base). It provides:

- A static wiki site served via GitHub Pages — zero ops, zero cost
- Full-text client-side search via Lunr.js
- An AI drafting sidebar powered by the Claude API
- Automatic rebuild on push, daily cron, or manual trigger via GitHub Actions

The engine is content-agnostic. All actual documentation lives in the downstream fork.

---

## Repo structure (upstream — Lorengine only)

```
/
├── CLAUDE.md                  ← you are here (engine docs, do not edit downstream)
├── wiki/
│   ├── index.html             ← doc index / entry point
│   ├── page.html              ← individual doc viewer
│   ├── search.html            ← full-text search page
│   ├── style.css              ← theming, light/dark mode
│   └── wiki.js                ← search, routing, AI sidebar logic
├── build_wiki.py              ← parses /docs → generates search_index.json
├── search_index.json          ← generated artifact, committed to repo
├── .github/
│   └── workflows/
│       ├── build.yml          ← rebuild triggers
│       └── sync-upstream.yml  ← opens PR when upstream has new commits
├── docs/
│   └── example-doc.md        ← example doc showing required frontmatter format
└── README.md                  ← setup instructions for forkers
```

---

## Separation of concerns — what lives where

| Layer | Owned by | Location | Editable downstream? |
|---|---|---|---|
| Wiki engine (HTML/CSS/JS) | Upstream | `wiki/` | No |
| Build script | Upstream | `build_wiki.py` | No |
| GitHub Actions | Upstream | `.github/workflows/build.yml` | No |
| Upstream sync action | Upstream | `.github/workflows/sync-upstream.yml` | No |
| Lorengine docs | Upstream | `CLAUDE.md` | No |
| Example doc | Upstream | `docs/example-doc.md` | No (delete after fork) |
| Project docs | Downstream | `docs/*.md` | Yes — this is the point |
| Project context | Downstream | `CLAUDE.local.md` | Yes — this is the point |
| Secrets / config | Downstream | GitHub repo secrets + `config.yml` | Yes |

**Rule:** if a file is in this table as "No", a downstream fork must never commit
changes to it. Upstream PRs will conflict otherwise. The only exception is
`config.yml` — see Configuration below.

---

## Configuration (the one file forks are meant to edit)

Downstream forks customise behaviour via `config.yml` in the repo root.
This file IS meant to be edited and will not be touched by upstream updates.

```yaml
# config.yml — edit this in your fork, not in upstream
wiki:
  title: "My Wiki"
  description: "A short description shown in the header"
  accent_color: "#7F77DD"      # hex, used for link highlights

ai:
  model: "claude-sonnet-4-6"   # or claude-haiku-4-5-20251001 for lower cost
  system_prompt_file: "CLAUDE.local.md"
  max_tokens: 1024
  enable_prompt_caching: true

search:
  max_results: 20
  excerpt_length: 160           # chars shown in search result snippets

github_pages:
  base_url: ""                  # set if serving from a subdirectory e.g. /my-wiki
```

`build_wiki.py` reads `config.yml` at build time and injects values into the
generated HTML. The AI sidebar reads `model` and `max_tokens` at runtime via
JS constants injected during build.

---

## How build_wiki.py works

Runs on every qualifying push (docs/** or build_wiki.py changed), daily at 06:00
UTC, or on manual workflow dispatch. Steps:

1. Reads `config.yml` for wiki metadata
2. Walks `/docs/` recursively, reads every `.md` file
3. Parses frontmatter (title, tags, status, last-updated)
4. Extracts `##` and `###` headings as section structure
5. Generates a plain-text excerpt for search (first 300 chars of body)
6. Writes `search_index.json` — consumed by the wiki UI at load time
7. Injects `config.yml` values into `wiki/*.html` templates → outputs to `_site/`

Output directory `_site/` is what GitHub Pages serves. It is gitignored;
`search_index.json` is committed directly to root for simplicity.

### search_index.json schema

```json
[
  {
    "id": "docs/rivals.md",
    "title": "Rivals system",
    "tags": ["rivals", "mechanics"],
    "status": "draft",
    "last_updated": "2026-03-29",
    "headings": ["Overview", "MegaCorp", "OpenRival", "StealthLab"],
    "excerpt": "Three AI labs compete in parallel, each with a distinct...",
    "body": "full plain-text content for Lunr indexing"
  }
]
```

---

## Frontmatter format (required in all docs)

```yaml
---
title: "Rivals System"
tags: ["rivals", "mechanics", "ai-labs"]
status: draft          # draft | review | final
last-updated: 2026-03-29
---
```

`build_wiki.py` skips any `.md` file missing a `title` field and logs a warning.
All other fields are optional but strongly recommended.

---

## AI sidebar — API call design

The sidebar fires a Claude API call when the user submits a question or drafting
request. Cost is kept minimal by design.

**Every call includes:**
1. System prompt — from `CLAUDE.local.md` in the downstream repo (cached)
2. Doc index — titles, tags, one-line excerpts of every doc (~500 tokens, cached)
3. Current page full content — the markdown of the page being viewed
4. Conversation history — last 4 turns only (prevents runaway context growth)
5. User's new message

**Never included:** full content of other docs. Cross-doc queries are handled
by instructing Claude to reference the index and ask the user to navigate there.

**Prompt caching:** system prompt + doc index are marked as cacheable. On
repeated calls this cuts input token cost by ~80%.

**API key:** stored as GitHub Actions secret `ANTHROPIC_API_KEY`. Injected at
build time as a JS constant. Never committed to the repo. Downstream forks
must set this secret in their own GitHub repo settings.

---

## GitHub Actions workflows

### build.yml

```yaml
on:
  push:
    paths: ['docs/**', 'build_wiki.py', 'config.yml']
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: python build_wiki.py
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with: { path: '_site' }
      - uses: actions/deploy-pages@v4
```

### sync-upstream.yml (lives in downstream fork only)

Opens a PR in the downstream fork whenever upstream has new commits.
Downstream never auto-merges — you review and merge manually.

```yaml
on:
  schedule:
    - cron: '0 9 * * 1'   # every Monday 09:00 UTC
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Sync upstream
        uses: aormsby/Fork-Sync-With-Upstream-action@v3.4
        with:
          upstream_sync_repo: reckhou/lorengine   # default — no setup required
          upstream_sync_branch: main
          target_sync_branch: upstream-sync   # PR from this branch, not direct to main
          target_repo_token: ${{ secrets.GITHUB_TOKEN }}
          test_mode: false
```

No setup required — the workflow tracks `reckhou/lorengine` by default. Your options as a wiki owner:

1. **Leave as-is** — track the latest Lorengine engine automatically (recommended)
2. **Delete this workflow** — stay pinned to whatever version you forked at
3. **Change `upstream_sync_repo`** — track your own engine fork instead

---

## Merge conflict prevention rules

**Upstream will never modify:**
- `docs/` (except `example-doc.md` which forks should delete after setup)
- `CLAUDE.local.md`
- `config.yml`

**Downstream forks must never modify:**
- `wiki/` — any change here will conflict on the next upstream PR
- `build_wiki.py` — same
- `.github/workflows/build.yml` — same
- `CLAUDE.md` — same

If a downstream fork needs to extend build behaviour, add a `build_local.py`
that imports and wraps `build_wiki.py`, and call it instead. Lorengine will
never create a file with that name — it is a reserved extension point.

---

## Coding conventions

- **Python:** 3.11+, stdlib only (`pathlib`, `json`, `re`, `datetime`, `tomllib`).
  No pip dependencies — zero-dep build is a feature, not a limitation.
- **JavaScript:** vanilla JS, ES2020+. No frameworks. CDN-loaded only:
  Lunr.js (search), marked.js (markdown rendering), highlight.js (code blocks).
- **CSS:** custom properties for all colours and spacing. Light and dark mode
  via `prefers-color-scheme`. No CSS frameworks.
- **HTML:** semantic markup. Readable without JS (JS progressively enhances).
- **Markdown:** frontmatter required. `##` and `###` headings only.

---

## Setup instructions for new forks

1. Click "Use this template" on GitHub (not "Fork" — template gives a clean history)
2. Clone your new repo locally
3. Delete `docs/example-doc.md`
4. Edit `config.yml` with your wiki title and settings
5. Create `CLAUDE.local.md` with your project context (see template below)
6. Add `ANTHROPIC_API_KEY` to GitHub Actions secrets
7. Enable GitHub Pages → source: GitHub Actions
8. Push a doc to `docs/` and watch the wiki build

---

## CLAUDE.local.md template (for Lorengine forks)

Create this file in your fork. Claude Code reads it alongside this file.
Upstream will never touch it.

```markdown
# [Your Project] — project context

## What this wiki is about
[One paragraph describing the project]

## Key decisions already made
[Decisions Claude should not relitigate]

## Doc conventions
[Any project-specific writing conventions beyond the engine defaults]

## Planned documents
[Docs not yet written but expected]

## AI sidebar system prompt
Used verbatim as the Claude API system prompt in the wiki sidebar.
Keep under 500 tokens so it fits comfortably in the cached prefix.

---
You are an AI assistant embedded in the [project] wiki.
[Project description]
[Tone and style instructions]
---
```

---

## Notes for Claude Code

- Read `CLAUDE.md` (this file) then `CLAUDE.local.md` before any task
- Lorengine and content are strictly separated — never mix them
- Test `build_wiki.py` against `docs/example-doc.md` before building the UI
- `config.yml` is the only intentional customisation point for forks; if a
  downstream need cannot be met via config, consider adding a config option
  to Lorengine upstream rather than letting the fork patch engine files
- Prefer stdlib over pip in `build_wiki.py` — the zero-dep constraint is load-bearing
- When in doubt, favour the simpler implementation
