---
title: "Examples"
tags: ["examples", "navigation"]
status: final
last-updated: 2026-03-29
---

## Overview

This section contains example pages that demonstrate how the tree sidebar organises docs.

Pages placed directly inside a folder become children of the file named after that folder.
For example, `simple-page.md` and `another-page.md` are siblings here because both live in
`docs/pages/examples/` and this file is named `examples.md` — matching the folder name.

## Key rule

A file named the same as its containing folder becomes the **section root** for that folder.
Every other `.md` file in that folder is a direct child of the root.

```
docs/pages/examples/
  examples.md        ← section root (this file)
  simple-page.md     ← child
  another-page.md    ← child
  subsection/
    subsection.md    ← independent section root for the subsection folder
    child-one.md     ← child of subsection.md
    child-two.md     ← child of subsection.md
```

## Subsections

Subfolder roots (e.g. `subsection/subsection.md`) appear as independent top-level nodes in the
tree — they are **not** children of this page. The tree only tracks one level of folder nesting
per section root.
