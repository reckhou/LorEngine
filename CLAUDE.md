# LorEngine — Claude Code Context

This file documents the **LorEngine engine** (upstream). It is owned by the upstream
repo and should never be edited in a downstream fork.

Project-specific context lives in `pages/brief.md` in the downstream repo.
Claude Code reads both files. Start there for content-specific instructions.

---

## What this repo is

**LorEngine** is a reusable, self-hosted wiki system designed for game design
documentation (or any markdown-based knowledge base). It provides:

- A static wiki site served via GitHub Pages — zero ops, zero cost
- Full-text client-side search via Lunr.js
- An AI drafting sidebar powered by the Claude API
- A visual markdown editor (`/admin/`) powered by Decap CMS
- Automatic rebuild on push, daily cron, or manual trigger via GitHub Actions

The engine is content-agnostic. All actual documentation lives in the downstream fork.

---

## Repo structure (upstream — LorEngine only)

```
/
├── CLAUDE.md                  ← you are here (engine docs, do not edit downstream)
├── wiki/
│   ├── index.html             ← doc index / entry point
│   ├── page.html              ← individual doc viewer
│   ├── search.html            ← full-text search page
│   ├── style.css              ← theming, light/dark mode
│   ├── wiki.js                ← search, routing, AI sidebar logic
│   └── admin/
│       ├── index.html         ← Decap CMS editor UI
│       └── tree.html          ← drag-and-drop hierarchy manager
├── build_wiki.py              ← parses /pages → generates search_index.json
├── decap.yml                  ← Decap CMS collection config (template, injected at build)
├── config.yml                 ← fork-editable configuration (title, AI model, OAuth, etc.)
├── search_index.json          ← generated artifact, committed to repo
├── content_hashes.json        ← tracks page body hashes for auto-timestamp detection
├── .github/
│   └── workflows/
│       ├── build.yml          ← rebuild + auto-timestamp commit + deploy
│       └── sync-upstream.yml  ← opens PR when upstream has new commits
├── pages/
│   ├── brief.md               ← downstream project identity + AI system prompt (template)
│   ├── brief-example.md       ← filled-in example for reference
│   └── getting-started/       ← example docs (delete after fork)
└── README.md                  ← setup instructions for forkers
```

---

## Separation of concerns — what lives where

| Layer | Owned by | Location | Editable downstream? |
|---|---|---|---|
| Wiki engine (HTML/CSS/JS) | Upstream | `wiki/` | No |
| Build script | Upstream | `build_wiki.py` | No |
| Decap CMS config template | Upstream | `decap.yml` | No |
| GitHub Actions | Upstream | `.github/workflows/build.yml` | No |
| Upstream sync action | Upstream | `.github/workflows/sync-upstream.yml` | No |
| LorEngine docs | Upstream | `CLAUDE.md` | No |
| Example docs | Upstream | `pages/getting-started/`, `pages/brief-example.md` | No (delete after fork) |
| Project pages | Downstream | `pages/*.md` | Yes — this is the point |
| Project context | Downstream | `pages/brief.md` | Yes — this is the point |
| Fork configuration | Downstream | `config.yml` | Yes |

**Rule:** if a file is in this table as "No", a downstream fork must never commit
changes to it. Upstream PRs will conflict otherwise. The only exception is
`config.yml` — see Configuration below.

---

## Configuration (the one file forks are meant to edit)

Downstream forks customise behaviour via `config.yml` in the repo root.
This file IS meant to be edited and will not be touched by upstream updates.

```yaml
# config.yml — edit this in your fork, not in upstream

github:
  repo: "YOUR_USERNAME/YOUR_REPO"   # required for Decap CMS editor
  oauth_app_id: ""                   # GitHub OAuth App Client ID — see README

pages_dir: "pages"                   # folder scanned for wiki pages (relative to repo root)

wiki:
  title: "My Wiki"
  description: "A short description shown in the header"
  accent_color: "#7F77DD"            # hex, used for link highlights

ai:
  model: "claude-sonnet-4-6"         # or claude-haiku-4-5-20251001 for lower cost
  max_tokens: 1024
  enable_prompt_caching: true

search:
  max_results: 20
  excerpt_length: 160                # chars shown in search result snippets

github_pages:
  base_url: ""                       # set only if serving from a custom subdirectory path

branding:
  favicon: ""                        # path to favicon file (relative to repo root)
  logo: ""                           # path to logo image (relative to repo root)
```

`build_wiki.py` reads `config.yml` at build time and injects values into the
generated HTML and Decap config. The AI sidebar reads `model` and `max_tokens`
at runtime via JS constants injected during build.

---

## How build_wiki.py works

Runs on every push, daily at 06:00 UTC, or on manual workflow dispatch. Steps:

1. Reads `config.yml` for wiki metadata
2. Walks `pages/` recursively (or whichever dir `pages_dir` specifies), reads every `.md` file
3. Parses frontmatter (title, tags, status, last-updated, slug, sort_order, parent)
4. Hard-fails on duplicate slugs; soft-warns on duplicate titles
5. Extracts `##` and `###` headings as section structure
6. Generates a plain-text excerpt for search (first 300 chars of body)
7. Auto-updates `last-updated` in source files whose body hash changed (writes back via git commit in CI)
8. Resolves `parent: slug` references to full page IDs (`compute_hierarchy`)
9. Computes backlinks (which pages link to each page) (`compute_backlinks`)
10. Writes `search_index.json` — consumed by the wiki UI at load time
11. Injects `config.yml` values into `wiki/*.html` templates → outputs to `_site/`
12. Copies and injects `decap.yml` → `_site/admin/config.yml`

Output directory `_site/` is what GitHub Pages serves. It is gitignored;
`search_index.json` and `content_hashes.json` are committed directly to root.

### search_index.json schema

```json
[
  {
    "id": "pages/rivals.md",
    "slug": "rivals",
    "title": "Rivals system",
    "tags": ["rivals", "mechanics"],
    "status": "draft",
    "last_updated": "2026-03-29",
    "sort_order": 20,
    "parent": "pages/design.md",
    "children": ["pages/rivals/megacorp.md"],
    "backlinks": ["pages/overview.md"],
    "headings": ["Overview", "MegaCorp", "OpenRival", "StealthLab"],
    "excerpt": "Three AI labs compete in parallel, each with a distinct...",
    "body": "full plain-text content for Lunr indexing"
  }
]
```

---

## Frontmatter format (required in all pages)

```yaml
---
title: "Rivals System"
tags: ["rivals", "mechanics", "ai-labs"]
status: draft          # draft | review | final
last-updated: 2026-03-29
sort_order: 20         # integer; lower = earlier in sidebar; default 100
parent: design         # slug (filename stem) of parent page; omit for root-level
---
```

`build_wiki.py` skips any `.md` file missing a `title` field and logs a warning.
All other fields are optional but recommended. `last-updated` is auto-managed by the
build script — you rarely need to set it manually.

**Slug** is derived automatically from the filename stem (e.g. `rivals.md` → slug `rivals`).
It is immutable after creation — changing a filename breaks all `parent:` references pointing to it.

---

## Visual editor — Decap CMS (`/admin/`)

The wiki ships a visual markdown editor at `<site>/admin/`. It is powered by
[Decap CMS](https://decapcms.org/) and commits directly to the GitHub repo.

### Authentication

Decap CMS uses **PKCE OAuth** (client-side only, no backend required). Setup:

1. Create a GitHub OAuth App (Settings → Developer Settings → OAuth Apps)
2. Set the callback URL to `https://<your-site>/admin/`
3. Copy the **Client ID** into `config.yml` → `github.oauth_app_id`
4. Commit — the next build wires it in automatically

The Client ID is not a secret and is safe to commit. No client secret is needed.

### decap.yml

`decap.yml` in the repo root is the collection config template. It defines the
`pages` collection with all frontmatter fields as widgets. `build_wiki.py` injects
`{{GITHUB_REPO}}` and `{{GITHUB_OAUTH_APP_ID}}` from `config.yml` at build time,
outputting the resolved config to `_site/admin/config.yml`.

### Tree manager (`/admin/tree.html`)

A separate page for drag-and-drop hierarchy management. Lets you reorder pages
(`sort_order`) and reparent them (`parent` slug) visually, then commits all
changes in a single GitHub API call. Requires being logged into Decap first
(reuses the token from `localStorage`).

---

## AI sidebar — API call design

The sidebar fires a Claude API call when the user submits a question or drafting
request. Cost is kept minimal by design.

**Every call includes:**
1. System prompt — the `## System prompt` section of `pages/brief.md` (cached)
2. Project context — all other sections of `pages/brief.md` (key decisions, glossary, conventions — cached)
3. Doc index — titles, tags, one-line excerpts of every doc (~500 tokens, cached)
4. Current page full content — the markdown of the page being viewed (omitted when viewing `pages/brief.md` itself)
5. Conversation history — last 4 turns only (prevents runaway context growth)
6. User's new message

**Never included:** full content of other docs. Cross-doc queries are handled
by instructing Claude to reference the index and ask the user to navigate there.

**Prompt caching:** system prompt + doc index are marked as cacheable. On
repeated calls this cuts input token cost by ~80%.

**API key:** users enter their Anthropic API key via a modal on first use; it is
stored in `localStorage` and never sent to any server other than `api.anthropic.com`.
Optionally, a fork owner can set `ANTHROPIC_API_KEY` as a GitHub Actions secret —
if present it is injected at build time as a JS constant, pre-loading the key for
all visitors without requiring individual sign-in.

---

## GitHub Actions workflows

### build.yml

```yaml
on:
  push:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

permissions:
  contents: write    # needed for auto-timestamp commit
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - name: Build wiki
        run: python build_wiki.py
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}   # optional
      - name: Commit auto-updated timestamps
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add pages/ content_hashes.json
          git diff --staged --quiet || (git commit -m "chore: auto-update last-updated timestamps [skip ci]" && git pull --rebase origin master && git push)
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
          upstream_sync_repo: reckhou/lorengine
          upstream_sync_branch: main
          target_sync_branch: upstream-sync
          target_repo_token: ${{ secrets.GITHUB_TOKEN }}
          test_mode: false
```

No setup required — the workflow tracks `reckhou/lorengine` by default. Your options:

1. **Leave as-is** — track the latest LorEngine engine automatically (recommended)
2. **Delete this workflow** — stay pinned to whatever version you forked at
3. **Change `upstream_sync_repo`** — track your own engine fork instead

---

## Merge conflict prevention rules

**Upstream will never modify:**
- `pages/` (except the example docs which forks should delete after setup)
- `pages/brief.md` content (ships as a template; forks fill it in)
- `config.yml`
- `content_hashes.json`

**Downstream forks must never modify:**
- `wiki/` — any change here will conflict on the next upstream PR
- `build_wiki.py` — same
- `decap.yml` — same
- `.github/workflows/build.yml` — same
- `CLAUDE.md` — same

If a downstream fork needs to extend build behaviour, add a `build_local.py`
that imports and wraps `build_wiki.py`, and call it instead. LorEngine will
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
2. Enable GitHub Pages → source: **GitHub Actions**
3. Enable all Actions in the repo
4. Edit `config.yml` — set `github.repo`, wiki title, and other settings. Committing triggers the first build.
5. Fill in `pages/brief.md` with your project identity and AI system prompt (see `pages/brief-example.md`)
6. Delete the example docs under `pages/getting-started/` and `pages/brief-example.md`
7. Push a page to `pages/` and watch the wiki build

**To enable the visual editor:**

8. Create a GitHub OAuth App and set `github.oauth_app_id` in `config.yml` (see *Visual editor* section above)

**To pre-load the AI API key for all visitors (optional):**

9. Add `ANTHROPIC_API_KEY` to GitHub Actions secrets — otherwise users enter their own key via the in-page modal

---

## Notes for Claude Code

- Read `CLAUDE.md` (this file) then `pages/brief.md` before any task
- LorEngine and content are strictly separated — never mix them
- Pages live in `pages/`, not `docs/`. `docs/` is reserved for plans and decision logs
- `config.yml` is the only intentional customisation point for forks; if a
  downstream need cannot be met via config, consider adding a config option
  to LorEngine upstream rather than letting the fork patch engine files
- Prefer stdlib over pip in `build_wiki.py` — the zero-dep constraint is load-bearing
- When in doubt, favour the simpler implementation
