---
title: "Getting Started"
tags: [getting-started, help]
status: final
last-updated: 2026-03-29
---

## Welcome

Welcome to the wiki! This is a static site built with **Lorengine**, a self-hosted markdown-based knowledge base.

## Adding Pages

Create markdown files in the `/pages/` folder with frontmatter:

```yaml
---
title: "Your Page Title"
tags: [tag1, tag2]
status: draft
last-updated: 2026-03-29
---
```

## Features

- **Full-text search** powered by Lunr.js
- **AI sidebar** powered by the Claude API
- **Multiple themes** — Light, Dark, Sepia, High Contrast
- **Tree navigation** with folder hierarchy
- **Backlinks** — see which pages reference the current one

## Search

Use the search page to find content across all pages instantly.

## AI Assistant

Each page includes an AI assistant sidebar. Enter your Anthropic API key when prompted — it is never stored in the repository.
