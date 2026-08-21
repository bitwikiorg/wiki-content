# `Main/` — canonical public knowledge namespace

This directory is the repository transport mirror of MediaWiki's Main namespace. It is **not** a curated alphabetical article list and the filesystem path is not the ontology.

Start with:

- [`Main Page.mediawiki`](Main%20Page.mediawiki)
- [`../Portal/`](../Portal/) for subject orientation
- [`../BITwiki/Navigation.mediawiki`](../BITwiki/Navigation.mediawiki) for the navigation model
- [`../BITwiki/Programmable knowledge substrate.mediawiki`](../BITwiki/Programmable%20knowledge%20substrate.mediawiki) for the execution model

## What Main owns

Main space is the canonical home for durable subject knowledge. Files may have several transport roles:

| Role | Meaning |
|---|---|
| canonical knowledge object | substantive subject knowledge intended for durable reading/reuse |
| domain exemplar | substantive page proving a controlled Domain works end-to-end |
| self-model knowledge object | general knowledge about a consequential technology/project used by BITwiki itself |
| V1 compatibility redirect | preserves an old public title while routing to its canonical home |
| Book Matter / subpage | reusable/compositional subject matter when independent retrieval is justified |
| Main Page | public landing page |
| review candidate | non-redirect content still requiring human evaluation/canonicalization |

Project-specific architecture belongs in `BITwiki:*`, even when Main contains a general page about the same system. `Lua` explains the language; `BITwiki:Lua architecture` explains BITwiki's use of it.

## Main as structured knowledge

A canonical page can participate in several layers at once:

```text
authored page / Book Matter
        +
Knowledge object identity
        +
SMW properties / relationships
        ↓
canonical durable knowledge state
        ↓
Lua / queries / navigation project that state into views
```

Lua does not own the page's truth. It can normalize, type-check, derive bounded presentation, and diagnose explicit state. Semantic assertions remain in pages/SMW; repeated operational records remain in Cargo.

## Self-modeling substrate

BITwiki now dogfoods its own knowledge architecture with Main-space objects for:

- `BITwiki`
- `BIThub`
- `MediaWiki`
- `Discourse`
- `Semantic MediaWiki`
- `Cargo (MediaWiki extension)`
- `Scribunto`
- `Lua`

These are real knowledge objects, not hidden implementation notes. Conservative SMW `Depends on` / `Related to` assertions make the operating stack queryable as part of the graph. The matching `BITwiki:*` architecture pages describe local implementation policy.

## Redirects are not stubs

Tiny files may intentionally preserve old public titles, for example:

```mediawiki
#REDIRECT [[BITwiki:BITCORE Manifesto]]
```

Do not evaluate a compatibility redirect as an unfinished article.

## Do not create empty/generic shells

Missing knowledge should remain an explicit coverage/request signal until there is enough evidence for coherent canonical content.

Prefer:

1. add or refine a requested-knowledge record;
2. research and create a minimum coherent sourced page;
3. expose the gap in navigation/coverage views;
4. preserve a redirect when a better canonical home already exists.

A canonical subject page should explain what the subject is, why it matters, its core mechanisms/concepts, representative examples/applications, relevant uncertainty/context, and source lineage.

See [`../BITwiki/Page format.mediawiki`](../BITwiki/Page%20format.mediawiki), [`../BITwiki/Readable depth and localization.mediawiki`](../BITwiki/Readable%20depth%20and%20localization.mediawiki), and [`../BITwiki/Requested knowledge.mediawiki`](../BITwiki/Requested%20knowledge.mediawiki).

## Navigation is a projection

The actual reading experience should be driven by links, semantic relationships, categories, portals, contents, outlines, lists, glossaries, queries, graph views, and search—not by the repository directory order.

```text
canonical Main knowledge
        ↓
Category / Concept / Portal / query / Lua projection
        ↓
contextual reading and exploration interfaces
```

Those interfaces should project canonical state rather than become competing copies of it.

## Machine audit

```bash
python scripts/audit_mainspace.py
python scripts/validate_v2.py
```

`audit_mainspace.py` distinguishes redirects, exemplars, knowledge objects, subpages, other content, and short review candidates. **Length is descriptive, not a quality score.**

## Invariants

```text
filesystem path
≠ article quality
≠ entity type
≠ Domain
≠ navigation hierarchy
≠ epistemic standing

rendered/derived view
≠ new canonical assertion
```
