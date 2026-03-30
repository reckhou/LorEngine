# LorEngine

A reusable, self-hosted wiki system for game design documentation (or any markdown-based knowledge base).

- Static wiki site served via GitHub Pages — zero ops, zero cost
- Full-text client-side search via Lunr.js
- AI drafting sidebar powered by the Claude API
- Automatic rebuild on push, daily cron, or manual trigger

## Quick Setup

1. Create a fork of this repository.
2. Enable **GitHub Pages** — source: **GitHub Actions**
3. Check **Actions** and enable all of them
4. Edit `config.yml` — set `github.repo` to `YOUR_USERNAME/YOUR_REPO`, update wiki title and settings. Committing this file triggers the first **Build and Deploy Wiki** action.
5. Check **GitHub Pages** for site address. New site might take 5–10 minutes to activate.

### Enabling the visual editor (`/admin/`)

The wiki includes a visual markdown editor powered by [Decap CMS](https://decapcms.org/). It requires a one-time GitHub OAuth App setup:

1. Go to **GitHub → Settings → Developer settings → OAuth Apps → New OAuth App**
2. Set **Authorization callback URL** to `https://YOUR_USERNAME.github.io/YOUR_REPO/admin/`
3. Copy the **Client ID** from the app's settings page
4. Paste it into `config.yml` under `github.oauth_app_id`
5. Commit — the next build wires it in automatically

The Client ID is not a secret and is safe to commit. No client secret is needed (the editor uses PKCE auth, which works entirely client-side).

## Writing Documents

Every markdown file in `pages/` needs YAML frontmatter:

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

`build_wiki.py` runs on every push (to `pages/`, `build_wiki.py`, or `config.yml`), daily at 06:00 UTC, or on manual dispatch. It:

1. Reads `config.yml` for wiki metadata
2. Parses all markdown files in `pages/`
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
