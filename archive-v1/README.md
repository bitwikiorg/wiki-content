# archive-v1 — public V1 source archive

**Read-only provenance. Do not deploy this directory as V2 pages.**

The archive now distinguishes the **Main-namespace corpus** from the rest of the wiki surface.

## Coverage map

- [`manifest.json`](manifest.json) — **162 / 162 Main-namespace titles accounted for**.
- [`wiki-surface-manifest.json`](wiki-surface-manifest.json) — public namespaces and maintenance/source surfaces beyond Main.
- [`templates/manifest.json`](templates/manifest.json) — V1 Template titles observed during reconstruction; raw-body verification is tracked per record.
- [`categories/manifest.json`](categories/manifest.json) — category-index snapshot and category-page state.
- [`special/README.md`](special/README.md) — Special pages used to enumerate/validate the corpus.
- [`raw-snapshots-1.md`](raw-snapshots-1.md) and [`raw-snapshots-2.md`](raw-snapshots-2.md) — exact public View-source wikitext already captured.

## Four states

| State | Meaning |
|---|---|
| accounted | title/surface + authoritative source reference are recorded |
| archived | exact raw source/revision material is stored in Git |
| reconciled | related versions were compared and unique content understood |
| refactored | a deliberate V2 implementation exists |

**Accounted does not mean archived. Archived does not mean reconciled. Reconciled does not automatically mean merged.**

## Main namespace

Current checkpoint: all 162 visible Main-namespace titles are accounted for in `manifest.json`. Exact raw source has been captured for a subset and continues to accumulate in `raw-snapshots-*.md`.

## Other namespaces

The live `Special:AllPages` surface exposes Main, Talk, User, User talk, BITwiki, BITwiki talk, File, File talk, MediaWiki, MediaWiki talk, Template, Template talk, Help, Help talk, Category, Category talk, Property, Property talk, Concept, Concept talk, smw/schema, smw/schema talk, Module, and Module talk.

Those namespaces are now explicitly archive targets in `wiki-surface-manifest.json`. Do not assume the 162-page Main manifest covers them.

## Migration rule

```text
archive V1 source
→ map transclusions / categories / semantic dependencies
→ compare revisions / related pages
→ preserve unique writing, citations, properties and behavior
→ separate durable ideas from obsolete implementation
→ decide V2 disposition
→ publish
```

Similarity of titles is never sufficient evidence for a merge.

## Authority

The live public wiki and its revision history remain authoritative for inherited V1 content. This directory is the Git-side preservation and lookup surface.
