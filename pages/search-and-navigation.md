---
title: "Search & Navigation"
tags: ["docs", "guide", "search", "navigation"]
status: final
last-updated: 2026-03-30
sort_order: 4
parent: getting-started
---

## The Tree Sidebar

The collapsible tree on the left of every page is the primary navigation tool.

### Expanding and Collapsing Sections

- Click the **▶ arrow** beside a section name to expand its children
- Click the **▼ arrow** to collapse it again
- Use **Expand all** / **Collapse all** buttons at the top to control all sections at once

### Filtering the Sidebar

Type in the **Filter pages...** input to narrow the tree to matching page titles:

```
Filter: "combat"
→ Shows only pages with "combat" in their title
→ Parent sections remain visible if any child matches
→ Clears the filter on empty input
```

The filter is **case-insensitive** and matches any substring of the title.

### Sort Order

Use the **dropdown** below the filter input to change how pages are ordered:

| Option | Description |
|--------|-------------|
| Custom order | Uses `sort_order` frontmatter field (recommended) |
| A–Z | Alphabetical title sort |
| Z–A | Reverse alphabetical |
| Oldest first | By `last-updated` ascending |
| Newest first | By `last-updated` descending |

The selected sort persists until you change it — it's remembered across page navigations.

---

## The Home Page

`index.html` shows **Recent Pages** — the 5 most recently modified pages, displayed as cards.

Each card shows:
- **Title** (links to the page)
- **Status badge** (DRAFT / REVIEW / FINAL) if set
- **Tags** as clickable chips
- **Last updated date** right-aligned
- **Excerpt** — the first ~300 characters of page body text

Pages are sorted by `last-updated` descending, with file modification time as a tiebreaker. The most recently changed page always appears first.

---

## Full-Text Search

Click **Search** in the top navigation bar to open the search page.

### How Search Works

Search is powered by **Lunr.js** — a client-side full-text search library. The entire search index is loaded in the browser; no server is involved.

Every word in every page's body, title, and tags is indexed at build time. Searching is instant.

### Search Query Syntax

| Query | Finds |
|-------|-------|
| `combat` | Pages containing the word "combat" |
| `combat system` | Pages containing both words (AND logic) |
| `combat*` | Pages containing words starting with "combat" (wildcard) |
| `+combat -magic` | Must contain "combat", must not contain "magic" |
| `title:combat` | Pages with "combat" in the title only |

### Search Result Cards

Each result shows:
- **Title** with a link to the page
- **Status badge** and **tags**
- **Excerpt snippet** showing the first ~160 characters of body text

Results are sorted by **relevance score** (Lunr.js tf-idf weighting). Exact title matches rank higher than body text matches.

---

## The AI Sidebar

On individual page views (`page.html`), an **AI assistant panel** is available via a button in the top bar.

### What It Can Do

- Answer questions about the **current page**
- Summarise sections or the whole page
- Help draft new content based on the page's context
- Reference the **doc index** (all page titles and excerpts) to point you toward relevant pages

### What It Can't Do

The AI assistant does **not** read the full content of all pages — only the current page and a one-line summary of every other page. For questions requiring deep knowledge of another page, navigate to that page first and ask from there.

### Usage

1. Click the **AI** button in the top right of a page
2. Type your question in the input box
3. The response appears in the sidebar panel
4. Conversation history is kept for the last 4 turns

> **Cost note:** Each AI response uses the Claude API. The system prompt and doc index are cached, so repeated questions on the same page are cheaper than the first call.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `/` | Focus the sidebar filter input |
| `Escape` | Clear the filter / close a modal |

---

## Tips for Navigating Large Wikis

1. **Use the filter box** — typing 2–3 characters narrows a 100-page wiki to the relevant section instantly
2. **Bookmark deep pages** — browser bookmarks work; the URL includes the full doc path as a query parameter
3. **Use search for cross-cutting queries** — "show me everything tagged `lore`" is faster in search than browsing
4. **sort_order is your friend** — assign low numbers (10, 20, 30...) to the pages you visit most so they appear at the top of their section in Custom order mode

