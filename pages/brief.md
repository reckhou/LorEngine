---
title: "Project Brief"
tags: ["setup"]
status: draft
last-updated: 2026-03-30
sort_order: 0
---

This file configures the AI sidebar for your LorEngine wiki. Fill in each
section below — no developer tooling required. The wiki indexes this page
and the AI sidebar reads it to give the AI context for every session.

See `pages/brief-example.md` for a fully completed reference. Delete it
after setup.

Aim for under 1,000 tokens of content. A warning appears in the AI sidebar
above 1,500 tokens (~6,000 characters). The leaner and more specific each
section, the better the AI performs.

---

## Project identity

<!--
One paragraph. What is this project? What is the wiki for?
This is the first thing the AI reads — it sets the frame for every session.
-->

ProjectAii/TestWiki

---

## Audience and purpose

<!--
Who reads and writes in this wiki? What do they primarily use the AI
sidebar for — drafting new docs, answering questions, extending sections?
-->

ProjectAii/TestWiki

---

## Key decisions

<!--
Settled canon. Number each entry. One to two sentences maximum.
This prevents the AI from relitigating prior design work.
-->

1. [First settled decision.]
2. [Second settled decision.]
3. [Add as many as needed.]

---

## Writing conventions

<!--
Spelling standard, tone, preferred structure, forbidden phrases.
The AI applies these on every draft it writes.
-->

- [Convention one.]
- [Convention two.]

---

## Domain glossary

<!--
Project-specific terms the AI might misinterpret or hallucinate.
Format: **Term** — definition.
-->

- **[Term]** — [Definition specific to this project.]

---

## Inspirations and references

<!--
Works that define this project's tone and design vocabulary.
One line each. Helps the AI use apt analogies.
-->

- [Reference — why it is relevant.]

---

## Planned documents

<!--
Docs not yet written but expected. Helps the AI flag gaps and avoid
inventing content for sections that do not exist.
Format: `pages/filename.md` — brief description.
-->

- `pages/[filename].md` — [What this doc will cover.]

---

## System prompt

<!--
IMPORTANT: Do not remove or rename this section heading.
The AI sidebar extracts everything below this heading as the verbatim
system prompt sent to Claude. Keep under 400 tokens.
Write it as instructions to the AI, not a description of it.
-->

You are an AI assistant embedded in the [project name] wiki, built on Lorengine.

[One sentence describing the project for the AI's context.]

Help the user draft, extend, and refine documentation pages. Match the style
and conventions of existing documents. When asked about something not yet
documented, flag it as a gap and offer to draft a stub. Only reference
documents that appear in the index — do not invent content.
