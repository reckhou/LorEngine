---
title: "Feature Roadmap Decisions"
tags: ["meta", "decisions", "roadmap"]
status: final
last-updated: 2026-03-29
---

## Context

Technical decisions agreed in a design session on 2026-03-29, covering six feature areas
for Lorengine v1.1+. These decisions are binding unless explicitly revisited.

## 1. Browser editing

- **Tool:** Decap CMS — adds `/admin` page, GitHub OAuth login
- **Editor:** Toast UI Editor embedded — WYSIWYG ↔ raw markdown toggle with preview
- **Flow:** User edits in browser → Decap commits to repo via GitHub API → build pipeline rebuilds
- **Requirement:** Editors must have a GitHub account

## 2. Tree view / page hierarchy

- **Structure:** Folder-based — `docs/combat/attacks.md` means `combat` is parent of `attacks`
- **Depth:** Arbitrary; 3 levels recommended as best practice
- **Nodes:** Every page is a node — no separate category type. Each page has at most 1 parent.
- **Sidebar:** Collapsible, visible by default, state persisted in localStorage
- **Sort:** Alphabetical or date asc/desc — user-selectable
- **Filter:** Matches page titles; unmatched ancestors remain visible to preserve structure

## 3. Visual markdown editor

- **Library:** Toast UI Editor (MIT, CDN-available)
- **Modes:** WYSIWYG and raw markdown, switchable
- **Preview:** Real rendered preview before submitting
- **Images:** In-repo (`docs/assets/`) or external URL — user responsible for accessibility
- **Principle:** Use existing library, do not build from scratch

## 4. Page references

- **Autocomplete:** Matches frontmatter titles (case-insensitive)
- **Syntax:** Standard markdown `[Title](docs/path/to/file.md)` — WYSIWYG renders as link
- **Backlinks:** Section at bottom of every page listing pages that link to it (generated at build time)
- **Wiki-links:** `[[Title]]` only if the editor natively supports it; otherwise standard links
- **GitHub issues:** Reference as standard markdown links only — no deep integration

## 5. Favicon / branding

Both optional, set per-fork in `config.yml`:

```yaml
branding:
  favicon: ""    # path relative to repo root, e.g. "favicon.svg"
  logo: ""       # image shown in header instead of text title
```

## 6. Backward compatibility

- **Template scope:** Public template, focused on game development wikis
- **Future:** May expand to GitHub issues/tasks integration
- **Versioning:** release-please Action → auto CHANGELOG.md + semver tags + GitHub Releases
- **Semver:** major = breaking, minor = new feature, patch = bugfix
- **Config:** Build script warns (non-fatal) on unknown config.yml keys

## 7. API key — two supported options

### Option A: User-supplied key
- **Blocking modal** when no saved key exists — cannot use AI sidebar without entering a key
- "Remember on this device" checkbox — defaults to `sessionStorage` (cleared on tab close)
- If "Remember" checked → stored in `localStorage` + "Delete saved key" button visible in sidebar
- User can delete the saved key at any time via the button in the sidebar

### Option B: Cloudflare Worker proxy
- Key stored in Cloudflare secret store, never exposed to browser
- Recommended for public wikis
- Free tier: 100k requests/day
- Proxy template + setup docs included in repo

### Runtime priority
1. `localStorage` saved key → use silently (show delete option in sidebar)
2. Neither → show blocking modal
