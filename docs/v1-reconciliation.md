# V1 reconciliation — issue #152

This is the active migration/reconciliation control document for `archive-v1/`.

## Governing rule

A V1 source is not retirement-ready merely because a current BITwiki page exists in the same architectural family.

A source becomes retirement-ready only when its useful, non-deprecated substance has one of these evidenced outcomes:

1. **incorporated** — the useful claims, distinctions, mechanisms, examples, relationships, citations or architecture decisions are present in current canonical BITwiki;
2. **already represented** — direct comparison shows the current canonical corpus already contains the durable substance;
3. **superseded** — a newer design explicitly replaces the old mechanism and preserves the useful intent;
4. **deprecated/rejected** — the old mechanism or claim was evaluated and deliberately not adopted, with the reason recorded;
5. **deliberately excluded/test-only** — the material was experimental, irrelevant to current scope, or otherwise intentionally excluded with evidence;
6. **historical-only** — the source has no remaining current knowledge/design value beyond provenance, after direct review.

Anything else remains **open reconciliation**.

A family-level target such as “Ontology” or “Epistemics” is not evidence that every V1 source in that family was actually incorporated.

## Correction of PR #155

PR #155 removed the working-tree V1 archive after generating a 162-page disposition ledger. That ledger overreached: it treated broad current family targets as proof of incorporation even though the earlier V1 maturation work explicitly left major areas at **Research** or **Candidate** status.

Issue #152 was therefore reopened. The archive is restored as the active migration source while reconciliation continues.

The valid parts of PR #155 remain valid:

- `Holobiont`, `Holobiome`, and `Systems analysis` are independently researched current articles;
- the old coral/bioluminescence project material is test/prototype content and is not a current BITwiki project;
- current runtime validation must not treat a historical V1 siteinfo snapshot as current runtime truth.

## Evidence already available

The earlier V1 maturation pass classified all 162 V1 Main pages by artifact role:

- 83 architecture/system sources;
- 52 Book Matter/reusable composition artifacts;
- 19 navigation/interface surfaces;
- 6 maintenance/validation/test artifacts;
- 2 historical subject/test candidates;
- 0 role-classification unknowns.

That role classification is useful evidence, but it is not the final content disposition.

The maturation register itself left these areas incomplete:

- epistemics / confidence trails — Research;
- semantic properties — Research;
- relationships / graph semantics — Research;
- categories — Research;
- knowledge graphs — Research;
- modules / schema machinery — Research;
- research objects — Research;
- templates — Candidate;
- Book Matter — Candidate;
- transclusion — Candidate;
- portals — Candidate;
- human–AI knowledge-production details — Candidate.

These areas must be reconciled source-by-source or mechanism-by-mechanism before retirement.

## Reconciliation result

The source-by-source/content-level pass is now complete:

- 162 / 162 V1 Main sources have an evidenced disposition;
- 0 sources remain open;
- 21 prototype/test sources are deliberately excluded;
- 29 sources have useful substance explicitly incorporated;
- 5 are already represented by current canon;
- 83 are superseded by current canonical structures after direct comparison;
- 12 obsolete mechanisms/sources are explicitly deprecated;
- 12 are historical-only after direct review.

Family reports under `docs/v1-reconciliation-*.md` preserve the comparison rationale. This completion means the '''knowledge-recovery gate''' is satisfied; it does not itself authorize deleting `archive-v1/`.

## Current ledger

`docs/v1-reconciliation-ledger.json` is authoritative for issue #152.

The prior `docs/v1-retirement-disposition.json` is retained only as evidence of the premature PR #155 decision and must not be used as a deletion gate.

The corrected ledger now records the completed content-level outcomes. No source is retirement-ready merely because of a family label; each final disposition is backed by a source-level family report or explicit test/historical rationale.

## Working method

For every open V1 source:

1. read the exact V1 body and relevant revision lineage;
2. identify durable claims, distinctions, mechanisms, examples, relationships, citations, authored formulations and architecture decisions;
3. compare those items against current canonical BITwiki, not merely page titles;
4. verify any factual or technical claims that would become current canon;
5. merge useful material into the best current page/primitive, or create a new canonical object only when justified;
6. explicitly record deprecated/rejected/superseded/test-only material and why;
7. update the reconciliation ledger with exact destination/evidence;
8. validate links, semantics, transclusion/runtime behavior and staging as applicable.

## Retirement gate

Content reconciliation is complete, but `archive-v1/` stays in the working tree until:

- every V1 source is retirement-ready under the rule above;
- no useful non-deprecated signal remains only in the archive;
- dependency and reference audits pass;
- the live/repository distinction is documented;
- the owner explicitly accepts the completed reconciliation;
- archive retirement is proposed as a separate reviewable change.

The immutable snapshot remains commit `3100db1d7807b752e41b6ccf7f88498982cfb2d4`, but Git recoverability is provenance, not a substitute for successful migration.
