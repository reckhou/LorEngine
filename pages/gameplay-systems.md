---
title: "Gameplay Systems"
tags: ["design", "systems", "mechanics"]
status: review
last-updated: 2026-03-30
sort_order: 1
parent: design
---

## Turn Structure

Each turn follows this sequence:

1. **Start Phase** (automatic)
   - Passive abilities trigger (e.g., regeneration)
   - Buffs/debuffs decrement by 1 turn
   - Resource production calculates

2. **Action Phase** (player)
   - Move units, execute actions, use abilities
   - Any number of actions in any order
   - Cannot repeat an action on the same unit in one turn

3. **End Phase** (player triggers)
   - Confirm all changes
   - Pass turn to opponent (in multiplayer) or AI
   - Automatic save checkpoint

### Action Economy

Units have **2 action points (AP)** per turn. Actions cost:

| Action | Cost | Notes |
|--------|------|-------|
| Move (1 square) | 0.5 AP | Diagonal = same cost; movement range varies by unit |
| Standard Attack | 1 AP | Can move + attack in one turn |
| Ability (tier 1) | 0.5–1 AP | Faction and unit-specific |
| Ability (tier 2) | 1–1.5 AP | More powerful, longer cooldown |
| Interact (object) | 1 AP | Capture, defend, interact with environment |

> **Design Intent:** 2 AP allows flexible play. Move + attack + something else creates interesting tradeoffs.

## Movement System

### Pathing & Terrain

- Units pathfind around obstacles automatically
- **Terrain Costs:**
  - Grass, stone: 1 movement cost per square
  - Forest, rubble: 1.5 movement cost
  - Water, cliffs: impassable (unless unit has special trait)

### Elevation

Heights are crucial:

```
Height 2: +1 to all attack rolls from this unit
          -1 to all attacks against this unit (range attacks only)
Height 1: normal
Height 0: normal
Height -1: -1 to all attack rolls; +1 defense vs. range
```

Units can move down any height freely. Moving up requires spending extra movement (0.5 per height level).

### Visibility & Fog of War

- Each unit has a **line of sight (LOS)** radius (typically 5–7 squares)
- Terrain blocks LOS (forest, hills, buildings)
- Attacking reveals position even in fog
- Stealthed units have reduced LOS radius

## Combat Resolution

### Attack Roll

```
Hit Chance = Base Accuracy + Attacker Bonuses - Defender Evasion

Base Accuracy (by weapon):
  - Melee: 85%
  - Ranged: 75%
  - Magic: 70%
```

> **Modifier Examples:**
> - Flanked unit: -15% accuracy (defender bonus)
> - High ground: +10% accuracy (attacker bonus)
> - In heavy cover: -20% accuracy (defender evasion)

### Damage Calculation

```
Damage = (Base Weapon Damage + Attacker Stat Bonus) × Type Modifier
         - (Defender Armor + Faction Resistance)

Type Modifiers (vs. unit type):
  Physical vs. Light Unit: ×1.2
  Physical vs. Heavy Unit: ×0.8
  Magic vs. Construct: ×1.5
  Magic vs. Living: ×1.0
```

### Special Outcomes

**Critical Hit** (10% chance on any hit):
- Doubles damage
- Bypasses cover bonuses
- Some units have abilities that increase crit chance

**Glancing Blow** (15% of misses):
- 30% of normal damage dealt
- Still triggers on-hit effects

## Ability System

### Ability Tiers

**Tier 1 (Passive):**
- Always active, no AP cost
- Examples: "Infantry +10% armor", "Mage: gain 1 mana per kill"

**Tier 2 (Active, Low Cost):**
- 0.5 AP cost, 1–3 turn cooldown
- Examples: "Sprint" (move again), "Heal nearby ally"

**Tier 3 (Active, High Impact):**
- 1 AP cost, 3–5 turn cooldown
- Examples: "Fireball" (area damage), "Rally" (buff entire army)

**Tier 4 (Ultimate):**
- 1.5 AP cost, 5+ turn cooldown
- Examples: "Summon creature", "Mass teleport"

### Cooldowns

- Cooldowns trigger on use, not on the unit
- Can have multiple copies of the same unit to use the same ability
- Some abilities have "charges" instead of cooldowns (e.g., "use 3 times per battle")

---

> **Playtester Note:** Combat feels slow if players overthink every move. Consider adding an "auto-resolve" option for low-difficulty battles.

