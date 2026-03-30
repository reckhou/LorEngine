---
title: "Links & Cross-References"
tags: ["docs", "reference", "markdown", "navigation"]
status: final
last-updated: 2026-03-30
sort_order: 4
parent: markdown-showcase
---

## Internal Wiki Links

Link to another page using its **relative path from the current file**.

### Linking From a Root Page

If your page is at `pages/my-page.md`, link to sibling root pages like this:

```markdown
See the [Game Overview](game-overview.md) for the full pitch.
Combat details are in [Gameplay Systems](design/gameplay-systems.md).
Check [Getting Started](getting-started.md) if you're new.
```

See the [Game Overview](../game-overview.md) for the full pitch.
Combat details are in [Gameplay Systems](../design/gameplay-systems.md).
Check [Getting Started](../getting-started.md) if you're new.

### Linking From a Child Page

If your page is at `pages/getting-started/quickstart.md` (one level deep), use `../` to navigate up:

```markdown
Return to [Getting Started](../getting-started.md).
See [Markdown Showcase](../markdown-showcase.md) for formatting help.
See [World & Story](../world-story.md) for lore pages.
```

Return to [Getting Started](../getting-started.md).
See [Markdown Showcase](../markdown-showcase.md) for formatting help.
See [World & Story](../world-story.md) for lore pages.

### Linking to a Sibling Child Page

Both pages are children of the same parent. Link using just the filename (same folder):

```markdown
<!-- From pages/getting-started/quickstart.md -->
See [Frontmatter Reference](frontmatter-reference.md) for all fields.
See [Page Hierarchy](page-hierarchy.md) for tree structure details.
See [Search & Navigation](search-and-navigation.md) for navigation tips.
```

See [Frontmatter Reference](../getting-started/frontmatter-reference.md) for all fields.
See [Page Hierarchy](../getting-started/page-hierarchy.md) for tree structure details.
See [Search & Navigation](../getting-started/search-and-navigation.md) for navigation tips.

---

## External Links

Use the full URL with protocol. External links open in the same tab by default.

```markdown
Powered by [marked.js](https://marked.js.org) for markdown rendering.
Syntax highlighting by [highlight.js](https://highlightjs.org).
Search by [Lunr.js](https://lunrjs.com).
```

Powered by [marked.js](https://marked.js.org) for markdown rendering.
Syntax highlighting by [highlight.js](https://highlightjs.org).
Search by [Lunr.js](https://lunrjs.com).

---

## Link Text Best Practices

Write link text that describes the destination, not just "click here":

```markdown
✓ Good
See [Page Hierarchy](page-hierarchy.md) for how parent/child relationships work.
The [production timeline](../production.md) covers all milestones.

✗ Avoid
Click [here](page-hierarchy.md) for more information.
See [this page](../production.md) for the timeline.
```

**Good link text:**
- Names the destination page clearly
- Works in a list of links without surrounding context
- Helps readers decide whether to follow the link

---

## Inline vs Reference-Style Links

### Inline Style (Recommended)

```markdown
[Gameplay Systems](design/gameplay-systems.md)
```

Clean and readable for most cases. Use this by default.

### Reference Style

Define the URL separately from the link text. Useful when the same URL appears multiple times, or when long URLs would clutter the prose.

```markdown
The [Gameplay Systems][gs] page covers turn structure and combat.
Unit stats are also defined in [Gameplay Systems][gs].

[gs]: design/gameplay-systems.md
```

The reference definition `[gs]: design/gameplay-systems.md` can be placed anywhere in the document — typically at the bottom.

---

## Heading Anchors

Every `##` and `###` heading generates an anchor you can link to. The anchor ID is the heading text lowercased with spaces replaced by hyphens and special characters removed.

```markdown
## Combat Resolution          → #combat-resolution
## Economy & Progression      → #economy--progression
### Attack Roll               → #attack-roll
### Faction: Harmonists       → #faction-harmonists
```

### Linking to a Heading on Another Page

```markdown
[Attack Roll formula](design/gameplay-systems.md#attack-roll)
[Economy details](design/economy-progression.md#resource-economy)
[Act I missions](world-story.md#act-i-awakening-missions-15)
```

[Attack Roll formula](../design/gameplay-systems.md#attack-roll)

### Linking to a Heading on the Same Page

```markdown
Jump to [External Links](#external-links) on this page.
See the [Heading Anchors](#heading-anchors) section above.
```

Jump to [External Links](#external-links) on this page.

---

## Displaying a URL Without Link Text

Wrap in angle brackets to render the URL as a clickable link:

```markdown
Project repository: <https://github.com/yourname/your-wiki>
Email: <design@yourstudio.com>
```

Project repository: <https://github.com/yourname/your-wiki>

---

## Link Lists

A common pattern for cross-reference sections at the bottom of a page:

```markdown
---

## Related Pages

- [Game Overview](../game-overview.md) — full project pitch and pillars
- [Economy & Progression](economy-progression.md) — resource system details
- [World & Story](../world-story.md) — faction lore and campaign structure
- [Production](../production.md) — timeline and team structure
```

---

## Related Pages

- [Game Overview](../game-overview.md) — full project pitch and pillars
- [Economy & Progression](../design/economy-progression.md) — resource system details
- [World & Story](../world-story.md) — faction lore and campaign structure
- [Production](../production.md) — timeline and team structure

---

## Common Pitfalls

| Problem | Cause | Fix |
|---------|-------|-----|
| Link shows raw text | Spaces in the path | Use hyphens: `my-page.md` not `my page.md` |
| Link goes to wrong page | Wrong relative path | Count folder levels; use `../` to go up |
| Anchor doesn't work | Heading text changed | Regenerate the anchor slug from the new heading |
| External link 404 | URL changed | Update the URL; consider linking to homepage instead |
| Circular link | A links to B, B links to A | Fine! Bidirectional links are useful in wikis |

