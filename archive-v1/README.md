# archive-v1 — public V1 source archive

**Read-only provenance. Do not deploy this directory as V2 pages.**

This directory gives every visible public V1 Main-namespace page one stable archival record before V2 decides to keep, revise, merge, split, redirect, or retire anything.

## Start here

- [`manifest.json`](manifest.json) — all **162** public V1 Main-namespace titles, their live source URL, and recovery state.
- [`raw-snapshots-1.md`](raw-snapshots-1.md) and [`raw-snapshots-2.md`](raw-snapshots-2.md) — exact public `View source` wikitext already recovered during reconstruction.

Current checkpoint: **162 / 162 titles are accounted for**. Exact raw source is already stored for 21 Main-namespace pages; the remaining records keep their authoritative live source URL until their raw source and revision history are captured.

A `reference-only` record does **not** mean lost or safe to rewrite. It means the title and authoritative live source are accounted for here, but its exact source/revision history must still be captured before a migration decision is made.

## Migration rule

```text
archive V1 source
→ compare revisions / related pages
→ preserve unique writing, citations, properties and transclusions
→ separate durable ideas from obsolete implementation
→ decide V2 disposition
→ publish
```

Similarity of titles is never sufficient evidence for a merge.

## Authority

The live public wiki and its revision history remain authoritative for inherited V1 content. This directory is the Git-side preservation and lookup surface.
