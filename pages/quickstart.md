---
title: "Quickstart"
tags: ["docs", "guide", "setup"]
status: final
last-updated: 2026-03-30
sort_order: 1
parent: getting-started
---

## Your First Page in 5 Minutes

This guide gets you from zero to a live wiki page as fast as possible.

---

## Step 1: Create a Markdown File

Create a new `.md` file anywhere inside the `pages/` directory:

```
pages/
  my-first-page.md       ← your new file
```

The filename becomes the page's **slug** — a unique identifier used for linking and hierarchy. Use lowercase, hyphen-separated names.

**Good slugs:**
```
combat-system.md
art-direction.md
chapter-one.md
```

**Avoid:**
```
My First Page.md    ← spaces break links
combat_system.md    ← underscores work but aren't conventional
COMBAT.md           ← uppercase works but isn't conventional
```

---

## Step 2: Add the Required Frontmatter

Every page **must** start with a YAML frontmatter block. The only required field is `title`:

```yaml
---
title: "My First Page"
---
```

A complete, well-structured frontmatter block looks like this:

```yaml
---
title: "Combat System"
tags: ["design", "mechanics", "combat"]
status: draft
last-updated: 2026-03-30
sort_order: 10
parent: design
---
```

See [Frontmatter Reference](frontmatter-reference.md) for every available field.

---

## Step 3: Write Your Content

After the frontmatter closing `---`, write your page content in Markdown.

```markdown
---
title: "Combat System"
tags: ["design", "mechanics"]
status: draft
last-updated: 2026-03-30
---

## Overview

This page documents the turn-based combat system.

## Attack Resolution

Each attack roll uses:
- Base accuracy (weapon-dependent)
- Attacker bonuses (high ground, flanking)
- Defender evasion (cover, stance)
```

> **Heading levels:** Use `##` for top-level sections and `###` for subsections. Don't use `#` (that's the page title, already shown from your frontmatter).

---

## Step 4: Build the Wiki

Run the build script from the project root:

```bash
python build_wiki.py
```

The build:
1. Scans all `.md` files in `pages/`
2. Parses frontmatter and body text
3. Builds the search index (`search_index.json`)
4. Assembles the final site in `_site/`

**Output when successful:**

```
Lorengine build starting...
  Wiki: My Wiki
  Indexed 12 document(s)
  Computed hierarchy and backlinks
  Wrote search_index.json
  Assembled site in _site/
Build complete.
```

If a file is missing its `title` field, the build skips it with a warning:

```
Warning: skipping pages/my-file.md — missing title in frontmatter
```

---

## Step 5: View Your Page

Serve the `_site/` directory locally:

```bash
python -m http.server 8000 --directory _site
```

Then open `http://localhost:8000` in your browser.

Your new page should appear:
- In the **tree sidebar** on the left
- In **Recent Pages** on the home screen (if it's one of the 5 most recently modified)
- In **search results** when you type any word from the page

---

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| Page not in sidebar | Missing `title` in frontmatter | Add `title: "..."` and rebuild |
| Page not in search | Build not run after edit | Run `python build_wiki.py` |
| Page in wrong tree position | `parent:` slug mismatch | Check slug matches parent file's stem |
| Duplicate slug warning | Two files with same name | Rename one file; slugs must be unique |

---

## What's Next?

- **Organise your pages:** See [Page Hierarchy](page-hierarchy.md) for how to nest pages under sections
- **Add metadata:** See [Frontmatter Reference](frontmatter-reference.md) for tags, status, and ordering
- **Write richer content:** See [Markdown Showcase](../markdown-showcase.md) for tables, code blocks, and more

