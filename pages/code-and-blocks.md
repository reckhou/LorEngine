---
title: "Code & Blocks"
tags: ["docs", "reference", "markdown"]
status: final
last-updated: 2026-03-30
sort_order: 3
parent: markdown-showcase
---

## Fenced Code Blocks

Use triple backticks to create a code block. Add a language name after the opening backticks to enable syntax highlighting.

````markdown
```python
def compute_damage(base, attacker_bonus, type_modifier, armor):
    raw = (base + attacker_bonus) * type_modifier
    return max(0, raw - armor)
```
````

```python
def compute_damage(base, attacker_bonus, type_modifier, armor):
    raw = (base + attacker_bonus) * type_modifier
    return max(0, raw - armor)
```

---

## Supported Languages

The wiki uses **highlight.js** for syntax highlighting. Common supported languages:

### Python

```python
# Turn structure
class Turn:
    def __init__(self, faction):
        self.faction = faction
        self.action_points = 2.0
        self.phase = "start"

    def spend_ap(self, cost: float) -> bool:
        if self.action_points >= cost:
            self.action_points -= cost
            return True
        return False
```

### JavaScript

```javascript
// Render a doc card on the index page
function renderCard(doc) {
  const excerpt = doc.excerpt.slice(0, 160);
  return `
    <article class="doc-card">
      <h2>${escapeHtml(doc.title)}</h2>
      <p>${escapeHtml(excerpt)}</p>
    </article>
  `;
}
```

### JSON

```json
{
  "id": "pages/combat-system.md",
  "slug": "combat-system",
  "title": "Combat System",
  "tags": ["design", "mechanics"],
  "status": "review",
  "last_updated": "2026-03-30",
  "parent": "pages/design.md",
  "children": []
}
```

### YAML

```yaml
---
title: "Combat System"
tags: ["design", "mechanics", "combat"]
status: review
last-updated: 2026-03-30
sort_order: 10
parent: design
---
```

### Bash / Shell

```bash
# Full rebuild and restart sequence
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8000 \
  -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }"

python build_wiki.py

python -m http.server 8000 --directory _site
```

### CSS

```css
.doc-card {
  border: 1px solid var(--border);
  border-radius: 0.5rem;
  padding: var(--space-lg);
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.15s ease;
}

.doc-card:hover {
  box-shadow: 0 2px 8px var(--shadow);
}
```

### HTML

```html
<article class="doc-card">
  <h2 class="doc-card-title">
    <a href="page.html?doc=pages/combat-system.md">Combat System</a>
  </h2>
  <div class="doc-card-meta">
    <span class="badge badge-review">review</span>
    <span class="tag">design</span>
    <span class="doc-card-date">2026-03-30</span>
  </div>
  <p class="doc-card-excerpt">The core interaction loop...</p>
</article>
```

### Plain Text / No Language

Use `text` or omit the language name for plain monospace blocks — useful for file trees, pseudocode, and diagrams:

```text
pages/
  getting-started.md
  getting-started/
    quickstart.md
    frontmatter-reference.md
  markdown-showcase.md
  markdown-showcase/
    text-formatting.md
    tables-and-lists.md
```

---

## Inline Code in Sentences

Use single backticks for code within flowing prose:

```markdown
Set `status: final` once the page has been reviewed.
The `parent:` field takes a slug, not a full path.
Run `python build_wiki.py` after every content change.
The build outputs to `_site/` — never edit this directory directly.
```

Set `status: final` once the page has been reviewed.
The `parent:` field takes a slug, not a full path.
Run `python build_wiki.py` after every content change.
The build outputs to `_site/` — never edit this directory directly.

---

## Blockquotes

Use `>` to create a blockquote. Blockquotes are ideal for design notes, warnings, callouts, and attributed quotes.

```markdown
> This is a blockquote. It renders with a left border and indented text.
```

> This is a blockquote. It renders with a left border and indented text.

### Multi-line Blockquotes

```markdown
> The Cataclysm wasn't a natural disaster.
> It was engineered by a faction that history forgot.
> That's the secret at the heart of the Archivists' campaign.
```

> The Cataclysm wasn't a natural disaster.
> It was engineered by a faction that history forgot.
> That's the secret at the heart of the Archivists' campaign.

### Nested Blockquotes

```markdown
> **Design Note:** Always justify balance changes in writing.
>
> > *"Numbers without context are just noise. Document the reasoning
> > or the next designer will revert it."*
> >
> > — Internal playtesting guide
```

> **Design Note:** Always justify balance changes in writing.
>
> > *"Numbers without context are just noise. Document the reasoning
> > or the next designer will revert it."*
> >
> > — Internal playtesting guide

### Blockquotes with Other Formatting

Blockquotes can contain any markdown:

```markdown
> ### Playtesting Checklist
>
> - [ ] Mission completable on all 4 difficulty levels
> - [ ] No unit can one-shot a full-HP enemy on Normal
> - [ ] At least 2 winning strategies per mission
>
> **Sign-off required from:** Lead Designer + QA Lead
```

> ### Playtesting Checklist
>
> - Mission completable on all 4 difficulty levels
> - No unit can one-shot a full-HP enemy on Normal
> - At least 2 winning strategies per mission
>
> **Sign-off required from:** Lead Designer + QA Lead

---

## Callout Conventions

The wiki doesn't have a built-in callout component, but blockquotes with a **bold label** work well as informal callouts:

```markdown
> **Note:** This behaviour changed in build 0.4.0.

> **Warning:** Renaming a page's file changes its slug and breaks existing links.

> **Tip:** Leave gaps in `sort_order` values (10, 20, 30) so you can insert pages later.

> **Example:** `parent: design` nests the page under `pages/design.md`.
```

> **Note:** This behaviour changed in build 0.4.0.

> **Warning:** Renaming a page's file changes its slug and breaks existing links.

> **Tip:** Leave gaps in `sort_order` values (10, 20, 30) so you can insert pages later.

> **Example:** `parent: design` nests the page under `pages/design.md`.

---

## Code Blocks in Lists

You can include code blocks inside list items with 4-space indentation:

````markdown
1. Create the file:

    ```bash
    touch pages/my-new-page.md
    ```

2. Add frontmatter:

    ```yaml
    ---
    title: "My New Page"
    status: draft
    ---
    ```

3. Run the build:

    ```bash
    python build_wiki.py
    ```
````

1. Create the file:

    ```bash
    touch pages/my-new-page.md
    ```

2. Add frontmatter:

    ```yaml
    ---
    title: "My New Page"
    status: draft
    ---
    ```

3. Run the build:

    ```bash
    python build_wiki.py
    ```

