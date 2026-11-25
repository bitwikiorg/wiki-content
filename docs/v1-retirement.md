# V1 working-tree retirement

Issue #152 retires the redundant `archive-v1/` working-tree snapshot after extracting durable knowledge, preserving provenance, and removing active dependencies on the directory.

## Immutable historical anchors

- Public V1 snapshot captured **2026-08-18T17:20:10Z**: commit `3100db1d7807b752e41b6ccf7f88498982cfb2d4`.
- At that commit, the complete recursive tree contains **648 paths under `archive-v1/`**, including 186 public pages, 162 Main pages, and 606 revision bodies.
- Evidence-driven V1 → V2 classification/maturation: merged PR #2, merge commit `5c98cad2e5c4679d1cac0db6bd421b4167856c32`.
- Per-title final disposition: `docs/v1-retirement-disposition.json`.
- Deleted-content limits remain preserved in `v1-deleted-content-audit.json` and `v1-deleted-unresolved.json`.

The full snapshot remains retrievable from:
`https://github.com/bitwikiorg/wiki-content/tree/3100db1d7807b752e41b6ccf7f88498982cfb2d4/archive-v1`

## What was recovered

The previous exhaustive migration pass classified every V1 Main artifact before ontology:

- 83 architecture/system sources;
- 52 Book Matter/reusable composition artifacts;
- 19 navigation/interface surfaces;
- 6 maintenance/validation/test artifacts;
- 2 historical subject/test candidates;
- 0 unresolved.

The durable architecture signal was matured into the current BITwiki standards: epistemics/evidence/provenance, ontology/relationships, semantic schema, Book Matter/transclusion, navigation, governance/editorial process, interoperability/runtime architecture, and system boundaries.

High-value reusable subject fragments were dispositioned individually. Emergence, feedback, homeostasis, empirical validation, and peer review are already represented in current canonical knowledge. Systems-analysis signal is re-canonicalized as a properly sourced current article rather than preserving the old fragment.

## Test biology material

`Bioluminescent Organisms`, `Fluorescent Coral Reefs`, their subpages, and the duplicated generic topic-section fragments are treated as prototype/test material, not as historical projects or current factual canon.

They are deliberately excluded rather than restored.

The useful research direction exposed during review is host–microbiome systems. Current `Holobiont` and `Holobiome` articles are independently researched canonical knowledge; they do **not** inherit factual or project claims from the V1 tests.

## Retirement boundary

Removing `archive-v1/` from the current branch:

- does not rewrite Git history;
- does not delete content from the live MediaWiki;
- does not claim recovery of two unavailable historical file binaries;
- does not claim access to deleted pre-snapshot revision bodies that the anonymous API could not return;
- does not make old architecture or test material current policy.

The repository should not depend on the retired directory for current validation, runtime authority, or publication. Historical questions use immutable Git references; current runtime questions use current source plus live MediaWiki verification.
