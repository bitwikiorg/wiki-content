# BITwiki namespace

Deployable project/governance/architecture pages corresponding to `BITwiki:*` titles.

This namespace is the **living specification layer for BITwiki itself**. It explains how the knowledge system is organized, how native MediaWiki/SMW/Cargo/Scribunto primitives are used, where authority boundaries sit, and how humans, BIThub, and agents interact with the durable wiki.

## What belongs here

`BITwiki:*` pages own project-specific standards and system behavior such as:

- architecture and MediaWiki runtime mapping;
- ontology, semantic properties, relationships, provenance, and epistemics;
- Book Matter, transclusion, page format, and composition;
- navigation, portals, categories, contents, outlines, and coverage;
- contribution/review/request workflows;
- deployment and migration protocol;
- interoperability and BIThub/Discourse integration boundaries.

General knowledge about a technology belongs in Main space. For example, `Main/Lua.mediawiki` explains Lua; `BITwiki/Lua architecture.mediawiki` explains **how BITwiki uses Lua**.

## Programmable substrate

The current architecture is:

```text
wikitext / Templates + SMW graph + Cargo operational state
                         ↓
                MediaWiki + Scribunto/Lua
                         ↓
 normalize → type-check → resolve → bounded derive → project → diagnose
                         ↓
        wiki / graph / diagnostic / machine-facing views
                         ↕
          authenticated integration boundary
                         ↕
                  BIThub / Discourse
```

Key standards:

- `Programmable knowledge substrate.mediawiki` — system-level execution and authority model;
- `Lua architecture.mediawiki` — compiler/module/data-access/runtime rules;
- `MediaWiki substrate.mediawiki` — namespace/extension/runtime reconciliation;
- `Ecosystem.mediawiki` — BITwiki ↔ BIThub ↔ BITCORE roles;
- `Interoperability.mediawiki` — external and BIThub interface contracts;
- `Deployment prerequisites.mediawiki` — repository-to-live-runtime deployment requirements.

## Authority boundary

These pages can specify intended behavior, but prose does not make an implementation true. A standard is operational only when the repository/runtime actually implements it and relevant validation or deployment evidence agrees.

Likewise:

```text
BITwiki architecture prose
≠ canonical subject knowledge
≠ SMW graph assertion by itself
≠ Cargo record
≠ Lua runtime behavior by itself
≠ BIThub discussion
```

The specification, implementation, structured state, and interface projections should agree without being collapsed into one layer.

## Living-text rule

When architecture changes, update the canonical `BITwiki:*` standard **and** the nearest repository README that a maintainer will encounter while working in the affected surface. READMEs summarize local operational consequences; these wiki pages carry the deeper project semantics and rationale.

Historical V1 material is evidence under `archive-v1/` and should not be silently rewritten to match current V2 behavior.
