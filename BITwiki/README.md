# BITwiki namespace

Deployable project/governance/architecture pages corresponding to `BITwiki:*` titles.

This namespace is the **public specification and governance layer for BITwiki itself**. It explains how knowledge is organized, represented, sourced and connected, how authoritative decisions are bounded, and how humans and agents can contribute. Private/internal work queues and deployment runbooks are not project-namespace articles.

## What belongs here

`BITwiki:*` pages own project-specific standards and system behavior such as:

- architecture and MediaWiki runtime mapping;
- ontology, semantic properties, relationships, provenance, and epistemics;
- Book Matter, transclusion, page format, and composition;
- navigation, portals, categories, contents, outlines, and coverage;
- editorial principles and public contribution guidance;
- public architectural interfaces and publication authority boundaries;
- interoperability and BIThub/Discourse integration boundaries;
- public project research, comparative analyses, and reference registers that inform BITwiki's architecture or editorial standards.

Historical internal process receipts are not current public standards; their provenance can be preserved in Git history.

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
- `Page format.mediawiki` — subject clarity, evidence and editorial scope without disciplinary admission gates;
- `Editorial protocol.mediawiki` — source-grounded research and accountable editing.

The non-deployable deployment runbook is in `docs/deployment.md`. The operational request records are in `ops/knowledge-requests.json`; both are in a **public GitHub repository**, not a private service, and neither is a public wiki article.

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
