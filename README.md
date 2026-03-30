# LorEngine

A reusable, self-hosted wiki system for game design documentation (or any markdown-based knowledge base).

- Static wiki site served via GitHub Pages — zero ops, zero cost
- Full-text client-side search via Lunr.js
- AI drafting sidebar powered by the Claude API
- Automatic rebuild on push, daily cron, or manual trigger

## Quick Setup

1. Click **"Use this template"** on GitHub (not "Fork" — template gives a clean history)
2. Clone your new repo locally
3. Delete `docs/example-doc.md`
4. Edit `config.yml` with your wiki title and settings
5. Create `CLAUDE.local.md` with your project context (see template in `CLAUDE.md`)
6. Add `ANTHROPIC_API_KEY` to **Settings > Secrets and variables > Actions**
7. Enable **GitHub Pages** — source: **GitHub Actions**
8. Push a doc to `docs/` and watch the wiki build

## Writing Documents

Every markdown file in `docs/` needs YAML frontmatter:

```yaml
---
title: "My Document"
tags: ["topic", "category"]
status: draft          # draft | review | final
last-updated: 2026-03-29
---
```

Use `##` and `###` headings to structure your content. The build script extracts these for the table of contents and search index.

## Configuration

Edit `config.yml` in your fork:

```yaml
wiki:
  title: "My Wiki"
  description: "A short description shown in the header"
  accent_color: "#7F77DD"

ai:
  model: "claude-sonnet-4-6"
  max_tokens: 1024
```

See `CLAUDE.md` for the full configuration reference.

## How It Works

`build_wiki.py` runs on every push (to `docs/`, `build_wiki.py`, or `config.yml`), daily at 06:00 UTC, or on manual dispatch. It:

1. Reads `config.yml` for wiki metadata
2. Parses all markdown files in `docs/`
3. Generates `search_index.json` for client-side search
4. Assembles `_site/` with injected config values
5. Deploys to GitHub Pages

## Upstream Sync

Forks receive upstream engine updates via the `sync-upstream.yml` workflow, which opens a PR every Monday when the upstream repo has new commits.

### Setup (required after forking)

1. Open `.github/workflows/sync-upstream.yml`
2. Replace `YOUR_GITHUB_USERNAME/lorengine` with the actual upstream repo path:
   ```yaml
   upstream_sync_repo: reckhou/lorengine   # or your own LorEngine fork
   ```
3. Commit the change — the workflow will now run automatically every Monday

The workflow includes a guard (`if: github.repository != 'reckhou/lorengine'`) so it silently skips if run in the upstream repo itself.

### If you forked LorEngine to maintain your own engine variant

Update the guard condition to match your repo so it skips there too:
```yaml
if: github.repository != 'your-org/your-lorengine-fork'
```
Then update `upstream_sync_repo` in any downstream wikis to point at your fork instead of `reckhou/lorengine`.

## Versioning and Releases

This project uses [release-please](https://github.com/googleapis/release-please) to automate versioning from conventional commits.

### Conventional Commits

Use this format in your commit messages:

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` — New feature (triggers minor version bump)
- `fix:` — Bug fix (triggers patch version bump)
- `feat!:` — Breaking change (triggers major version bump)
- `docs:` — Documentation only
- `chore:` — Maintenance tasks
- `refactor:` — Code refactoring
- `test:` — Adding or updating tests

**Examples:**
```
feat: add user authentication
fix: correct typo in search results
feat!: change API response format
docs: update installation instructions
```

When a commit with `feat:` or `fix:` is merged to main, release-please automatically:
1. Updates CHANGELOG.md
2. Creates a semantic version tag (v1.1.0, v1.2.0, etc.)
3. Publishes a GitHub Release

### Pinning to a Version

Downstream forks can pin to a specific version:
```bash
git checkout v1.0.0  # Pin to a specific release
```

## License

MIT
