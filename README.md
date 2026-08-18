# BITwiki V2

**Public MediaWiki source. Start here.**

BITwiki is the durable knowledge layer of the **BITwiki / BIThub / BITCORE** ecosystem.

```text
V2 canon       → Main/ BITwiki/ Portal/ Template/ Property/ Category/
V1 provenance  → archive-v1/
```

`archive-v1/` is read-only evidence. **Do not deploy it as V2.**

## Start here

| Need | Open |
|---|---|
| Public entry | [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki) |
| Why BITwiki exists | [`BITwiki/Manifesto.mediawiki`](BITwiki/Manifesto.mediawiki) |
| Charter | [`BITwiki/Charter.mediawiki`](BITwiki/Charter.mediawiki) |
| Constitution | [`BITwiki/Constitution.mediawiki`](BITwiki/Constitution.mediawiki) |
| Ontology / Epistemology / Axiology | [`BITwiki/Foundational triad.mediawiki`](BITwiki/Foundational%20triad.mediawiki) |
| Book Matter / transclusion | [`BITwiki/Book Matter.mediawiki`](BITwiki/Book%20Matter.mediawiki) |
| Default page format | [`BITwiki/Page format.mediawiki`](BITwiki/Page%20format.mediawiki) |
| Knowledge lifecycle | [`BITwiki/Knowledge lifecycle.mediawiki`](BITwiki/Knowledge%20lifecycle.mediawiki) |
| Organization | [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki) |
| Templates + categories | [`BITwiki/Templates and categories.mediawiki`](BITwiki/Templates%20and%20categories.mediawiki) |
| Exact V1 implementation | [`BITwiki/V1 implementation audit.mediawiki`](BITwiki/V1%20implementation%20audit.mediawiki) |
| V1 category refactor | [`BITwiki/V1 category migration.mediawiki`](BITwiki/V1%20category%20migration.mediawiki) |
| V1 Special-page baseline | [`BITwiki/V1 maintenance baseline.mediawiki`](BITwiki/V1%20maintenance%20baseline.mediawiki) |
| Current-live V1 fidelity audit | [`v1-fidelity-audit.json`](v1-fidelity-audit.json) |
| Deleted-history boundary | [`v1-deleted-content-audit.json`](v1-deleted-content-audit.json) |
| Unresolved deleted titles | [`v1-deleted-unresolved.json`](v1-deleted-unresolved.json) |
| Exhaustive current-public V1 archive | [`archive-v1/README.md`](archive-v1/README.md) |
| V2 structural validation | [`v2-validation.json`](v2-validation.json) |

## Repository map

```text
wiki-content/
├── Main/          ordinary public knowledge pages
├── BITwiki/       foundations, architecture, governance, guides
├── Portal/        high-level knowledge entry points
├── Template/      reusable/transcluded V2 components
├── Property/      Semantic MediaWiki properties
├── Category/      intentional human-readable indexes
├── archive-v1/    exhaustive current-public V1 snapshot
├── scripts/       archive + validation tooling
└── .github/       reproducible automation
```

**Repository paths are organization surfaces, not the ontology.**

```text
namespace ≠ entity type ≠ domain ≠ Book Matter ≠ epistemic status ≠ relationship
```

## V1 archive — independently verified current-public fidelity

Latest archive snapshot: **2026-08-18T17:20:10Z**.

An independent live-vs-archive audit subsequently compared the archive back against the live anonymous-readable wiki rather than trusting the harvester's own assertions.

### Verified complete scope

For the **currently existing public V1 corpus**, verification is complete:

- **186 / 186** live pages are archived;
- **606 / 606** public revision bodies were independently compared;
- page IDs and current revision IDs match;
- complete revision-ID sets and revision SHA-1 values match;
- current wikitext matches;
- all revisions use only the `main` MediaWiki revision slot — no auxiliary slot content was omitted;
- all **162** categories and every membership match;
- all **9** Template pages and every current transclusion caller match;
- both File-page revision records match;
- namespace inventory matches;
- required maintenance/Special-page reports show no drift.

The independent audit reports `content_fidelity_pass: true` with no page, revision, category, template, file, namespace or maintenance mismatches.

| Surface | Exact archived state |
|---|---:|
| Nonnegative namespaces | 24 |
| Public pages | 186 |
| Revision bodies | 606 |
| Main pages | 162 |
| Actual Template pages | 9 |
| Used category names | 162 |
| Created `Category:` pages | 0 |
| Property pages | 4 |
| `smw/schema` pages | 3 |
| MediaWiki pages | 6 |
| File description pages | 2 |
| File binary revision records | 2 |
| Retrievable file binaries | 0 |
| Historical binary references now unavailable | 2 |
| Concept pages | 0 |
| Module pages | 0 |

The two historical PNG upload records are preserved with timestamps, dimensions, size, SHA-1, original API URLs, and failed-resolution evidence. The files themselves now return 404 and are **not fabricated or silently omitted**.

### Historical deletion boundary

This is the important qualification to “all V1 content.”

The public deletion log contains **165 delete actions affecting 164 unique titles**. Anonymous API access cannot return deleted revision bodies for those titles; the deleted-revision API returns permission errors.

The deletion audit classifies:

- **140** deleted titles with obvious surviving clean-name counterparts, largely `... final` duplicates intentionally removed;
- **5** deleted titles that currently exist again under the exact same title;
- **19** deleted titles without an obvious current counterpart.

Those 19 include a mixture of obvious throwaway/spam/system material and potentially useful historical BITwiki artifacts such as old Main-page components/templates, `BITwiki modularization demo`, `Main page styled`, and old audit pages. Some deletion log comments preserve partial historical source snippets, but the exact full deleted bodies are not anonymously retrievable.

Therefore the precise completeness statement is:

> **The repository contains the complete current anonymous-readable V1 corpus and the complete public histories of every page that currently exists. It does not yet prove byte-for-byte recovery of revisions/pages deleted before the archive snapshot.**

Proving complete historical V1 recovery beyond this boundary requires a privileged MediaWiki deleted-revision export, database/backup source, or another preserved copy of the deleted bodies.

Open the evidence directly:

- [`archive-v1/audit.json`](archive-v1/audit.json) — archive assertions and exact counts
- [`v1-fidelity-audit.json`](v1-fidelity-audit.json) — independent live-vs-archive comparison
- [`v1-deleted-content-audit.json`](v1-deleted-content-audit.json) — all public deletion-log events and deleted-revision recoverability
- [`v1-deleted-unresolved.json`](v1-deleted-unresolved.json) — the 19 unresolved deleted titles
- [`archive-v1/index.json`](archive-v1/index.json) — every current public page
- [`archive-v1/pages/`](archive-v1/pages/) — exact current wikitext
- [`archive-v1/history/`](archive-v1/history/) — complete public histories for current pages
- [`archive-v1/templates/index.json`](archive-v1/templates/index.json) — all 9 implemented templates
- [`archive-v1/categories/index.json`](archive-v1/categories/index.json) — all 162 categories + membership graph
- [`archive-v1/special/`](archive-v1/special/) — maintenance-report snapshots
- [`archive-v1/files/index.json`](archive-v1/files/index.json) — file revision/binary availability records

### Design intent ≠ deployed implementation

V1 contains sophisticated architecture documents describing templates, categories, properties, concepts, modules and validation systems that were not all instantiated as namespace objects.

```text
design intent       → archived writings and references
live implementation → archived namespaces, revisions, memberships, transclusions
```

Both are preserved. Neither is allowed to masquerade as the other.

Examples:

- `Template:Infobox` is real and has **80 callers**.
- V1 has **59 wanted templates** that were referenced but never created.
- `Category:BITwiki Templates` had **7 Main-namespace documentation members**; it was not the inventory of the 9 actual Template pages.
- V1 had **162 used category names but zero authored Category pages**.

## 12 domain exemplars

| Domain | Portal | Example |
|---|---|---|
| Systems science | [`Portal:Systems science`](Portal/Systems%20science.mediawiki) | [`System boundary`](Main/System%20boundary.mediawiki) |
| Science | [`Portal:Science`](Portal/Science.mediawiki) | [`Hypothesis`](Main/Hypothesis.mediawiki) |
| Biology | [`Portal:Biology`](Portal/Biology.mediawiki) | [`Cell membrane`](Main/Cell%20membrane.mediawiki) |
| Mathematics | [`Portal:Mathematics`](Portal/Mathematics.mediawiki) | [`Prime number`](Main/Prime%20number.mediawiki) |
| Philosophy | [`Portal:Philosophy`](Portal/Philosophy.mediawiki) | [`Causality`](Main/Causality.mediawiki) |
| Technology | [`Portal:Technology`](Portal/Technology.mediawiki) | [`Version control`](Main/Version%20control.mediawiki) |
| Electronics | [`Portal:Electronics`](Portal/Electronics.mediawiki) | [`Resistor`](Main/Resistor.mediawiki) |
| Energy | [`Portal:Energy`](Portal/Energy.mediawiki) | [`Energy efficiency`](Main/Energy%20efficiency.mediawiki) |
| Engineering | [`Portal:Engineering`](Portal/Engineering.mediawiki) | [`Safety factor`](Main/Safety%20factor.mediawiki) |
| Chemistry | [`Portal:Chemistry`](Portal/Chemistry.mediawiki) | [`pH`](Main/pH.mediawiki) |
| Physics | [`Portal:Physics`](Portal/Physics.mediawiki) | [`Momentum`](Main/Momentum.mediawiki) |
| Medicine | [`Portal:Medicine`](Portal/Medicine.mediawiki) | [`Pulse`](Main/Pulse.mediawiki) |

## Default page grammar

Use only the matter the subject needs:

```text
semantic identity
Overview
Definition
Scope & importance
Core concepts / mechanism
Examples
Applications / implications
Epistemic notes
References
```

Mature pages may expand into history, frameworks, methods, evidence, case studies, controversies, timelines, bibliography, knowledge maps, implementation and limitations.

**Modularity does not mean fragmentation.** Keep the canonical parent coherent; split/transclude only when a portion is independently useful.

## V1 → V2 rule

```text
exact V1 source + revisions + usage
→ determine what job the object was doing
→ compare variants + intended architecture
→ preserve unique writing / behavior / provenance
→ choose the correct V2 primitive
→ implement
→ validate against Special pages
```

Typical refactors:

- domain category → `Domain` property + curated category/portal;
- entity-type category → `Entity type` property;
- epistemic category → epistemic/evidence model;
- section/fragment category → Book Matter/transclusion;
- temporary workflow/provenance category → provenance/revision metadata;
- error category → generated validation/maintenance surface;
- referenced-but-never-created template → design-intent evidence, not automatic V2 code.

## Validation

Current V2 validation is **green**: all category references resolve to documented `Category/` pages, all template transclusions resolve, no deployable Main/BITwiki/Portal/Template pages are uncategorized, all 12 domain portals/categories exist, and exactly 12 domain exemplars are present.

## Public boundary

This repository contains public material only. Private memory, credentials, access-control internals, private identity data and unpublished sensitive operational material do not belong here.
