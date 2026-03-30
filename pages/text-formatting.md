---
title: "Text Formatting"
tags: ["docs", "reference", "markdown"]
status: final
last-updated: 2026-03-30
sort_order: 1
parent: markdown-showcase
---

## Bold

Wrap text in double asterisks or double underscores.

```markdown
**This text is bold**
__This is also bold__
```

**This text is bold**
__This is also bold__

---

## Italic

Wrap text in single asterisks or single underscores.

```markdown
*This text is italic*
_This is also italic_
```

*This text is italic*
_This is also italic_

---

## Bold and Italic Combined

Use triple asterisks for bold-italic.

```markdown
***This is bold and italic***
```

***This is bold and italic***

---

## Strikethrough

Wrap text in double tildes.

```markdown
~~This text has a strikethrough~~
The old price was ~~$49.99~~ — now $29.99.
```

~~This text has a strikethrough~~

The old price was ~~$49.99~~ — now $29.99.

---

## Inline Code

Wrap code in single backticks. Use for file names, function names, commands, and short code snippets.

```markdown
Run `python build_wiki.py` to rebuild the site.
The function `computeHierarchy()` processes parent/child links.
Edit `pages/my-page.md` to update the content.
```

Run `python build_wiki.py` to rebuild the site.
The function `computeHierarchy()` processes parent/child links.
Edit `pages/my-page.md` to update the content.

---

## Emphasis Within Sentences

You can apply formatting to part of a word or within flowing sentences:

```markdown
The unit has un**believable** range.
Use *only* one attack per turn.
The `status` field accepts `draft`, `review`, or `final`.
```

The unit has un**believable** range.
Use *only* one attack per turn.
The `status` field accepts `draft`, `review`, or `final`.

---

## Horizontal Rule

Three or more dashes (or asterisks or underscores) on their own line create a horizontal divider.

```markdown
Section one content.

---

Section two content.
```

This is useful for separating major conceptual areas within a long page without using a new heading.

---

## Line Breaks

In standard markdown, a single newline in the source does **not** create a visible break in the output — the two lines are joined.

To create a hard line break within a paragraph, end a line with two or more spaces, or use a blank line to start a new paragraph.

```markdown
This line ends here.
This continues on the same line in the output.

This line ends here.

This starts a new paragraph.
```

This line ends here.
This continues on the same line in the output.

This line ends here.

This starts a new paragraph.

---

## Escaping Special Characters

Prefix any special markdown character with a backslash `\` to output it literally:

```markdown
\*Not italic\*
\**Not bold\**
\`Not code\`
\# Not a heading
```

\*Not italic\*

\`Not code\`

---

## Special Typography

Standard characters that render nicely in the browser:

```markdown
Em dash: —  (type directly or use &mdash;)
En dash: –  (type directly or use &ndash;)
Ellipsis: …  (type directly or use &hellip;)
Copyright: ©
Trademark: ™
Non-breaking space: use &nbsp; in HTML contexts
```

Em dash: —
En dash: –
Ellipsis: …

> **Tip:** For game design docs, em dashes (—) are common for ranges ("3–5 damage"), explanations ("Combat — the core of the game"), and asides. Type them directly rather than using `---` (which creates a horizontal rule).

---

## Combining Formats

Formats can be combined freely:

```markdown
**`config.yml`** is the only file you *should* edit in a fork.

The ~~deprecated~~ `legacy-build.py` has been **replaced** by `build_wiki.py`.

> ***Critical:*** Always back up your `pages/` directory before a major restructure.
```

**`config.yml`** is the only file you *should* edit in a fork.

The ~~deprecated~~ `legacy-build.py` has been **replaced** by `build_wiki.py`.

> ***Critical:*** Always back up your `pages/` directory before a major restructure.

