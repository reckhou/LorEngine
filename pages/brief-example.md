---
title: "Project Brief — Example"
tags: ["setup", "reference"]
status: reference
last-updated: 2026-03-30
sort_order: 1
---

> **This is a read-only reference example shipped with LorEngine.**
> It uses a fictional *Duty Calls: Iron Curtain* game design wiki to show
> a fully completed `pages/brief.md`. Delete this file after setup.

---

## Project identity

This wiki is the internal design documentation for *Duty Calls: Iron Curtain*,
a fictional entry in the Duty Calls franchise set during an alternate Cold War
in 1986. The wiki covers all game design systems — weapons, multiplayer modes,
campaign structure, progression, and operator design — and serves as the single
source of truth for the development team. It is not a public-facing document.

---

## Audience and purpose

The primary audience is the internal design team: systems designers, level
designers, and narrative leads. The AI sidebar is used mainly for drafting
new system documentation, extending existing specs, and answering questions
about settled design decisions. Writers should not need to search Slack or
prior meeting notes — if a decision is made, it lives here.

---

## Key decisions

1. The setting is 1986 Eastern Europe. All weapons, vehicles, and technology
   must be period-accurate or plausible within the alternate timeline. No
   anachronistic equipment without explicit narrative justification.
2. Multiplayer has no battle pass. Progression is entirely through in-match
   performance and prestige ranks. Cosmetics are earnable only, never sold.
3. The campaign is linear with no open world. Player agency comes from
   loadout choices and optional intelligence objectives, not map exploration.
4. Killstreak rewards cap at five kills. No streaks beyond that threshold.
   This was decided to lower the skill ceiling gap in casual lobbies.
5. Operators are historical archetypes, not named fictional characters.
   They have backstories but no dialogue in multiplayer. Campaign characters
   are entirely separate from multiplayer operators.
6. Hardcore mode removes the HUD entirely — no minimap, no ammo counter,
   no hit markers. This is a permanent mode, not a playlist rotation.

---

## Writing conventions

- American English spelling throughout (armor, color, analyze, etc.)
- Direct, specific prose — no marketing language, no hedging
- Present tense for describing systems ("the player earns", not "the player will earn")
- Tables for structured comparisons (weapon stats, mode rules, etc.)
- Bullet lists for sequential steps and enumerated options only
- `##` and `###` headings only — no deeper nesting
- Weapon names always in title case: AK-74, M16A1, RPG-7
- Mode names always in title case: Team Deathmatch, Hardpoint, Domination
- Never use "fun" as a design justification — describe the specific player
  experience instead ("creates tension", "rewards positional play", etc.)

---

## Domain glossary

- **Streak** — a killstreak reward earned by killing a set number of enemies
  without dying. Never called "killstreak" in player-facing UI, only in
  internal docs.
- **Operator** — a playable multiplayer character skin with a backstory.
  Distinct from campaign characters.
- **Prestige** — the act of resetting rank to 1 in exchange for a prestige
  token and a permanent cosmetic reward.
- **Hardpoint** — a rotating objective mode where a single capture zone
  moves every 60 seconds. Not to be confused with "hill" (the colloquial
  term used by the community).
- **TTK** — time to kill. The number of milliseconds it takes to eliminate
  an enemy at a given range with a given weapon. The primary balance metric.
- **Sightline** — a line of sight corridor in a map that creates consistent
  engagement opportunities. Used in level design docs.
- **Alternate timeline** — the game's fictional premise: the Cold War
  escalated differently. Use this term in narrative docs, not "alternate
  history" (which implies real-world divergence).

---

## System prompt

You are an AI assistant embedded in the internal design wiki for
*Duty Calls: Iron Curtain*, built on LorEngine.

Iron Curtain is a fictional Duty Calls title set in an alternate Cold War
in 1986 Eastern Europe. The wiki documents all game systems — weapons,
multiplayer, campaign, progression, and operators — for the internal design team.

Help the user draft, extend, and refine design documentation. Write in direct,
specific prose. American English spelling. Present tense. No marketing language.
Match the tone and structure of existing documents.

When drafting specs, be precise about numbers, timing, and player-facing
language. When asked about something not yet documented, flag it as a gap
and offer to draft a stub. Only reference documents that appear in the index
— do not invent content that has not been established in this wiki.
