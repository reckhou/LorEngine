---
title: "Economy & Progression"
tags: ["design", "economy", "balance", "progression"]
status: review
last-updated: 2026-03-30
sort_order: 2
parent: design
---

## Resource Economy

Every faction manages three **core resources**:

| Resource | Generation | Max Storage | Purpose |
|----------|------------|------------|---------|
| **Production** | Per turn from territory; boosted by buildings | Unlimited | Build units, structures, upgrades |
| **Influence** | Per turn from cities and diplomacy | 100 | Unlock tech, diplomacy, special actions |
| **Morale** | Per turn from victory; lost from defeat | 100 | Army effectiveness; morale breaks cause retreat |

### Territory Control

Units gain production income from friendly territory. Territory types:

- **City** (4 prod/turn) — core resource hub; can be fortified
- **Farm** (1 prod/turn) — rural, easily captured
- **Mine** (2 prod/turn) — defensible, rare; multiple exist on map
- **Ruin** (0 prod/turn) — neutral; grants vision and XP to units stationed there

Territory is held as long as a unit occupies it. Losing all units in a territory reverts it to neutral.

> **Economy Design:** Early game rewards map control; late game is about tech advantage. A player who hoards resources without expanding falls behind in tech.

## Tech Tree & Progression

### Tech Costs

All techs cost **Influence**, measured in "tech points" (TP):

- **Tier 1** (early): 5–10 TP each
- **Tier 2** (mid): 15–25 TP each
- **Tier 3** (late): 30–50 TP each
- **Tier 4** (endgame): 60+ TP each

### Unlocks by Type

**Unit Unlocks** (new unit type becomes available):
```
Scout → Ranger → Sentinel
  └─ Costs: 5 TP → 15 TP → 30 TP
  └ Unlocks improved movement, stealth, abilities
```

**Ability Unlocks** (existing units gain new abilities):
```
Infantry "Shield Wall" (tier 2)
  └─ Costs 10 TP
  └─ Effect: Unit and adjacent allies gain +2 armor next turn
  └─ Cooldown: 2 turns
```

**Faction Unlocks** (faction-specific bonuses):
```
Adaptors "Rapid Evolution" (trait)
  └─ Costs 20 TP
  └─ Effect: Units morph faster; reduce morph cooldown by 1 turn
```

### Tech Tree Structure

Each faction has **3 independent trees** (balanced in total cost):

1. **Military** — units, combat abilities, weapons
2. **Economic** — resource production, storage, trade
3. **Civic** — morale, diplomacy, special abilities

Trees are **not branching** — every tech in a tier can be accessed independently once the tier is unlocked.

```
Tier 1 Unlocked
  ├─ Military: Scout, Spearman, Archer
  ├─ Economic: Granary, Trade Post
  └─ Civic: Morale Recovery, Basic Diplomacy

[Player must spend 30 TP total in Tier 1 to unlock Tier 2]

Tier 2 Unlocked
  ├─ Military: Ranger, Cavalry, Mage
  ├─ Economic: Farm Infrastructure, Supply Lines
  └─ Civic: Propaganda, Alliance System
```

## Unit Progression

### Unit Experience & Leveling

Units earn **XP** from:
- Defeating enemies (+XP = enemy level × 1.5)
- Surviving battle (+1 XP per turn in combat)
- Capturing territory (+5 XP per capture)

Every 20 XP, a unit gains 1 level (max level 10).

### Level-Up Benefits

At each level-up, units improve:

| Stat | Gain per Level |
|------|----------------|
| Health | +5% |
| Damage | +3% |
| Armor | +2% |
| Accuracy | +1.5% |

Additionally, units unlock **1 ability point per 3 levels**. Spend on:
- Increase existing ability effectiveness (+1 damage, -1 cooldown turn, etc.)
- Unlock new tier 1/2 abilities (if tech tree allows)

> **Example:** A level 3 Scout with 1 ability point spends it to unlock "Evasion Stance" (tier 1 passive: +2 evasion when moving).

## Difficulty Scaling

Campaign difficulty affects:

1. **Enemy unit quality:** Higher levels, better abilities unlocked
2. **Resource generation:** Enemies gain resource multipliers
   - Easy: ×0.5 (enemies gain half normal production)
   - Normal: ×1.0
   - Hard: ×1.5 (enemies gain 50% bonus)
   - Legendary: ×2.0

3. **AI behavior:** Different decision-making and aggressiveness
   - Easy: AI makes tactical mistakes
   - Normal: AI plays well but not optimally
   - Hard: AI optimizes, focuses on player weakness
   - Legendary: AI behaves like experienced player

4. **Mission modifier:** Some battles have difficulty-locked modifiers
   - Hard: "All enemy units have +1 armor"
   - Legendary: "All enemy units regenerate 2 HP per turn"

---

> **Design Note:** Resources should feel scarce but not punishing. A player making suboptimal choices should still progress, just slower. Save resource generation for Legendary difficulty.

