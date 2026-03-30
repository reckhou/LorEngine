---
title: "Frontmatter Reference"
tags: ["docs", "reference", "frontmatter"]
status: final
last-updated: 2026-03-30
sort_order: 2
parent: getting-started
---

## What Is Frontmatter?

Every wiki page starts with a **YAML frontmatter block** — metadata enclosed in triple-dash delimiters:

```yaml
---
title: "My Page Title"
tags: ["tag-one", "tag-two"]
status: draft
last-updated: 2026-03-30
sort_order: 10
parent: my-section
---

Page content starts here.
```

The frontmatter is never shown as raw text in the wiki. Fields are used by the build system and the UI to organise, display, and search pages.

---

## Fields Reference

### `title` *(required)*

**Type:** String

The display name of the page. Shown in the sidebar, search results, and page heading.

```yaml
title: "Combat System"
```

> **Required:** The build will skip any page without a `title` and log a warning. All other fields are optional.

---

### `tags` *(optional)*

**Type:** Array of strings

Used for categorisation and filtering. Tags appear as small chips in search results and on the index page. Choose lowercase, hyphen-separated values.

```yaml
tags: ["design", "combat", "mechanics"]
```

**Conventions:**
- Use short, reusable tags (`design`, `art`, `audio`, `lore`, `reference`)
- Don't use tags that duplicate the title (`tags: ["combat-system"]` on a page titled "Combat System" adds no value)
- Be consistent — `mechanics` and `mechanic` are different tags to the search engine

---

### `status` *(optional)*

**Type:** One of `draft`, `review`, or `final`

Shown as a coloured badge on index cards and search results.

```yaml
status: draft     # 🟠 orange — work in progress
status: review    # 🔵 blue — needs sign-off
status: final     # 🟢 green — approved, stable
```

Omitting `status` defaults to no badge shown.

---

### `last-updated` *(optional, auto-managed)*

**Type:** Date string in `YYYY-MM-DD` format

Records when the page content was last changed. Used to sort the **Recent Pages** list on the home screen (newest first).

```yaml
last-updated: 2026-03-30
```

> **Auto-update:** The build script (`build_wiki.py`) tracks a content hash of each page. When the page body changes between builds, `last-updated` is automatically rewritten to today's date. You rarely need to set this manually.

---

### `sort_order` *(optional)*

**Type:** Integer (default: `100`)

Controls a page's position within its section when the sidebar sort is set to **Custom order**. Lower numbers appear first.

```yaml
sort_order: 10    # appears near top
sort_order: 50    # appears in middle
sort_order: 100   # default; appears near bottom
sort_order: 999   # always last
```

**Suggested numbering:**
- Leave gaps (10, 20, 30...) so you can insert pages later without renumbering everything
- Root/overview pages typically get `sort_order: 1` or `sort_order: 10`
- Appendix or reference pages get `sort_order: 90` or higher

---

### `parent` *(optional)*

**Type:** Slug string (filename stem of the parent page)

Places this page as a **child** of another page in the tree sidebar. The value must be the exact slug (filename without `.md`) of the parent.

```yaml
parent: design             # parent is pages/design.md
parent: getting-started    # parent is pages/getting-started.md
parent: world-story        # parent is pages/world-story.md
```

> **Important:** The parent page must exist. If the slug doesn't match any page, the build logs a warning and the page is placed at the root level instead.

See [Page Hierarchy](page-hierarchy.md) for the full picture of how parent/child relationships work with folder structure.

---

## Complete Example

A fully populated frontmatter block:

```yaml
---
title: "Faction Design: Harmonists"
tags: ["design", "factions", "narrative"]
status: review
last-updated: 2026-04-15
sort_order: 20
parent: world-story
---
```

This page would:
- Show as **"Faction Design: Harmonists"** everywhere in the UI
- Display a **REVIEW** badge (blue)
- Appear in search results filtered by `design`, `factions`, or `narrative`
- Sort at position **20** within its section
- Appear **nested under** the "World & Story" page in the sidebar

---

## Frontmatter Gotchas

### Strings with Special Characters

Wrap titles in quotes if they contain colons, brackets, or other YAML special characters:

```yaml
# ✓ Safe
title: "Faction: Harmonists"
title: "Chapter 1 — The Awakening"

# ✗ Breaks YAML parsing
title: Faction: Harmonists
title: Chapter 1 — The Awakening
```

### Dates Must Be Quoted or Bare ISO Format

```yaml
# ✓ Both valid
last-updated: 2026-03-30
last-updated: "2026-03-30"

# ✗ Invalid — YAML interprets this as a number
last-updated: 2026/03/30
```

### Tags Must Be an Array

```yaml
# ✓ Correct
tags: ["design", "combat"]
tags:
  - design
  - combat

# ✗ Wrong — this is a string, not an array
tags: "design, combat"
```

