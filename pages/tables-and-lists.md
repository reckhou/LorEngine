---
title: "Tables & Lists"
tags: ["docs", "reference", "markdown"]
status: final
last-updated: 2026-03-30
sort_order: 2
parent: markdown-showcase
---

## Unordered Lists

Use `-`, `*`, or `+` for bullet points. The character doesn't matter — be consistent within a file.

```markdown
- First item
- Second item
- Third item
```

- First item
- Second item
- Third item

---

## Ordered Lists

Use numbers followed by a period. The actual numbers don't matter — they auto-increment.

```markdown
1. First step
2. Second step
3. Third step
```

1. First step
2. Second step
3. Third step

> **Tip:** Some authors write `1.` for every item. This makes reordering easier since you never need to renumber.

---

## Nested Lists

Indent by 2–4 spaces to create sub-items. Mix ordered and unordered freely.

```markdown
- Factions
  - Harmonists
    - Philosophy: cooperation
    - Strength: group buffs
  - Isolationists
    - Philosophy: self-sufficiency
    - Strength: individual power
- Systems
  - Combat
  - Economy
```

- Factions
  - Harmonists
    - Philosophy: cooperation
    - Strength: group buffs
  - Isolationists
    - Philosophy: self-sufficiency
    - Strength: individual power
- Systems
  - Combat
  - Economy

---

## Mixed Ordered/Unordered Nesting

```markdown
1. Preproduction
   - Write design document
   - Create art style guide
   - Build prototype
2. Production
   - Implement core systems
   - Create all unit sprites
   - Compose soundtrack
3. Polish
   - Bug fixing
   - Balance tuning
   - Playtesting
```

1. Preproduction
   - Write design document
   - Create art style guide
   - Build prototype
2. Production
   - Implement core systems
   - Create all unit sprites
   - Compose soundtrack
3. Polish
   - Bug fixing
   - Balance tuning
   - Playtesting

---

## Lists with Multiple Paragraphs

Add a blank line between items and indent continuation content by 4 spaces:

```markdown
- **Combat System**

    The core interaction loop. Handles turn order, attack resolution,
    damage calculation, and special abilities.

- **Economy System**

    Manages resource production, spending, and storage across all
    faction types.
```

- **Combat System**

    The core interaction loop. Handles turn order, attack resolution,
    damage calculation, and special abilities.

- **Economy System**

    Manages resource production, spending, and storage across all
    faction types.

---

## Basic Table

Tables use pipe `|` separators with a header separator row of dashes.

```markdown
| Unit | HP | Damage | Range |
|------|-----|--------|-------|
| Scout | 30 | 8 | 5 |
| Warrior | 60 | 15 | 1 |
| Mage | 25 | 25 | 4 |
| Archer | 35 | 12 | 6 |
```

| Unit | HP | Damage | Range |
|------|-----|--------|-------|
| Scout | 30 | 8 | 5 |
| Warrior | 60 | 15 | 1 |
| Mage | 25 | 25 | 4 |
| Archer | 35 | 12 | 6 |

---

## Column Alignment

Add `:` to the separator row to align columns.

```markdown
| Left-aligned | Centered | Right-aligned |
|:-------------|:--------:|--------------:|
| Text | Text | Text |
| 1234 | 5678 | 9012 |
| Short | A much longer value | 1 |
```

| Left-aligned | Centered | Right-aligned |
|:-------------|:--------:|--------------:|
| Text | Text | Text |
| 1234 | 5678 | 9012 |
| Short | A much longer value | 1 |

Default (no colon) is left-aligned.

---

## Tables with Inline Formatting

Cell content can include any inline markdown:

```markdown
| System | Status | Owner |
|--------|--------|-------|
| **Combat** | ✓ Complete | `combat.py` |
| **Economy** | ⚠ In progress | `economy.py` |
| *Pathfinding* | ✗ Not started | — |
| ~~Old AI~~ | Deprecated | — |
```

| System | Status | Owner |
|--------|--------|-------|
| **Combat** | ✓ Complete | `combat.py` |
| **Economy** | ⚠ In progress | `economy.py` |
| *Pathfinding* | ✗ Not started | — |
| ~~Old AI~~ | Deprecated | — |

---

## Tables with Multiple Lines of Data

For readability, align your pipe characters:

```markdown
| Faction       | Production | Influence | Morale |
|---------------|:----------:|:---------:|:------:|
| Harmonists    | 4/turn     | 3/turn    | 5/turn |
| Isolationists | 3/turn     | 2/turn    | 3/turn |
| Adaptors      | 2/turn     | 4/turn    | 4/turn |
| Archivists    | 2/turn     | 6/turn    | 2/turn |
```

| Faction       | Production | Influence | Morale |
|---------------|:----------:|:---------:|:------:|
| Harmonists    | 4/turn     | 3/turn    | 5/turn |
| Isolationists | 3/turn     | 2/turn    | 3/turn |
| Adaptors      | 2/turn     | 4/turn    | 4/turn |
| Archivists    | 2/turn     | 6/turn    | 2/turn |

---

## Large Reference Tables

Tables work well for spec sheets and reference data. Example from a unit roster:

| Unit | Faction | HP | Dmg | Armor | AP | Range | Special |
|------|---------|:--:|:---:|:-----:|:--:|:-----:|---------|
| Spearman | Harmonists | 50 | 12 | 4 | 2 | 1 | Formation bonus |
| Shield Wall | Harmonists | 80 | 8 | 8 | 1.5 | 1 | Blocks for adjacent |
| Loner | Isolationists | 70 | 18 | 5 | 2 | 1 | Solo strength bonus |
| Sniper | Isolationists | 30 | 22 | 1 | 1.5 | 8 | No movement penalty |
| Morph Scout | Adaptors | 40 | 10 | 3 | 2 | 5 | Can morph into 3 forms |
| Archivist | Archivists | 35 | 14 | 2 | 2 | 4 | Copies enemy abilities |

---

## When Tables vs Lists

Use a **table** when:
- You have 2+ attributes per item
- You want to compare values across items side by side
- Data is structured and consistent

Use a **list** when:
- Each item is a standalone point with no parallel attributes
- Items have very different lengths (cells would need wrapping)
- You're describing a sequence of steps

