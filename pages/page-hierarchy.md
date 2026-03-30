---
title: "Page Hierarchy"
tags: ["docs", "guide", "structure"]
status: final
last-updated: 2026-03-30
sort_order: 3
parent: getting-started
---

## How the Tree Sidebar Works

The sidebar on the left is a **navigable page tree**. Pages can be:

- **Root pages** — top-level entries, no parent
- **Section roots** — pages that have children nested under them
- **Leaf pages** — pages with a parent but no children of their own

The tree is built from two sources working together:

1. **The `parent:` frontmatter field** — explicitly declares which page is the parent
2. **File modification time** — determines sort order when `last-updated` dates are equal

---

## Declaring a Parent

To nest a page under another, set `parent:` to the parent page's **slug** (its filename without `.md`):

```yaml
# pages/design/combat-system.md
---
title: "Combat System"
parent: design
---
```

This makes "Combat System" appear as a child of whatever page has the slug `design` — which would be `pages/design.md`.

### How Slugs Work

A slug is the filename stem — everything before the `.md`. It must be **unique across the entire wiki** (not just within a folder):

```
pages/design.md                      → slug: design
pages/design/combat-system.md        → slug: combat-system
pages/world/lore.md                  → slug: lore
```

> **Warning:** Two pages with the same filename in different folders will collide. The build exits with an error: `ERROR: Duplicate slug 'lore' in ...`

---

## Folder Structure Convention

You don't *have* to use subfolders — you could put all pages flat in `pages/` and rely entirely on `parent:` declarations. However, using matching folder names keeps things tidy and makes the structure obvious at a glance.

### Recommended Pattern

Place a page's children in a folder named after it:

```
pages/
  design.md                          ← section root (slug: design)
  design/
    gameplay-systems.md              ← parent: design
    economy-progression.md           ← parent: design
    combat-system.md                 ← parent: design
  world-story.md                     ← section root (slug: world-story)
  world-story/
    factions.md                      ← parent: world-story
    lore-timeline.md                 ← parent: world-story
```

### Flat Pattern (No Subfolders)

Works fine for small wikis. All `parent:` declarations must still be correct slugs:

```
pages/
  design.md                          ← slug: design
  gameplay-systems.md                ← parent: design
  economy-progression.md             ← parent: design
  world-story.md                     ← slug: world-story
  factions.md                        ← parent: world-story
```

### Deep Nesting

The wiki supports **one level of nesting** in the sidebar. A page can be a child of a parent, but grandchildren (children of children) are **not** displayed as nested — they appear as children of the grandparent's section.

```
design.md                            ← root
  └── gameplay-systems.md            ← child of design (shows in sidebar)
        └── combat-rules.md          ← child of gameplay-systems
                                        (shows as child of design in sidebar,
                                         not indented further)
```

> For deeply hierarchical content, consider flattening the structure and using in-page links to connect related pages.

---

## Visual Result

Given this file layout and frontmatter:

```
pages/
  getting-started.md                 sort_order: 1
  getting-started/
    quickstart.md                    sort_order: 1, parent: getting-started
    frontmatter-reference.md         sort_order: 2, parent: getting-started
    page-hierarchy.md                sort_order: 3, parent: getting-started
  markdown-showcase.md               sort_order: 2
  markdown-showcase/
    text-formatting.md               sort_order: 1, parent: markdown-showcase
    tables-and-lists.md              sort_order: 2, parent: markdown-showcase
```

The sidebar (Custom order) renders as:

```
▼ Getting Started
    Quickstart
    Frontmatter Reference
    Page Hierarchy
▼ Markdown Showcase
    Text Formatting
    Tables & Lists
```

---

## Moving Pages

To move a page to a different section:

1. Change its `parent:` field to the new parent's slug
2. Optionally move the file to a matching subfolder (not required but keeps things tidy)
3. Run `python build_wiki.py` to rebuild

The tree sidebar updates immediately after rebuild. No other pages need to change unless you had inline links pointing to the page's old path.

---

## Sidebar Sort Options

The sidebar supports multiple sort modes, selectable from the dropdown at the top:

| Mode | Behaviour |
|------|-----------|
| **Custom order** | Uses `sort_order` field ascending; ties broken by title A–Z |
| **A–Z** | Alphabetical by title |
| **Z–A** | Reverse alphabetical |
| **Oldest first** | Ascending `last-updated` date |
| **Newest first** | Descending `last-updated` date |

The selected sort applies to all tree nodes simultaneously. Children within a parent section sort independently from other sections.

