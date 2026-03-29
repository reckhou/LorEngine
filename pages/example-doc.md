---
title: "Example Document"
tags: ["example", "getting-started"]
status: draft
last-updated: 2026-03-29
---

## Overview

This is an example document demonstrating the required frontmatter format for
Lorengine. Every markdown file in `docs/` needs a `title` field in its YAML
frontmatter — all other fields are optional but recommended.

Delete this file after setting up your fork and replace it with your own content.

## Frontmatter Fields

- **title** (required): The display name of the document
- **tags**: A list of tags for categorisation and search filtering
- **status**: One of `draft`, `review`, or `final`
- **last-updated**: The date this document was last modified (YYYY-MM-DD)

## Writing Guidelines

Use `##` and `###` headings to structure your documents. These headings are
extracted by the build script for the table of contents and search index.

### Markdown Features

Standard markdown is supported:

- **Bold** and *italic* text
- `Inline code` and fenced code blocks
- Links, images, and lists
- Tables and blockquotes

```python
# Code blocks are syntax-highlighted via highlight.js
def hello():
    print("Hello from Lorengine!")
```

### Tips

- Keep documents focused on a single topic
- Use descriptive titles and relevant tags
- Update the `last-updated` field when making changes
- Set `status` to `final` when the document is ready for reference
