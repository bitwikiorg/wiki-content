# BITwiki V2

**Public MediaWiki source. Start here.**

BITwiki is the durable knowledge layer of the **BITwiki / BIThub / BITCORE** ecosystem.
This repository has two clearly separated layers:

```text
V2 canon       → Main/ BITwiki/ Portal/ Template/ Property/ Category/
V1 provenance  → archive-v1/
```

`archive-v1/` is read-only evidence. It is **not** a second deployable wiki.

## Start in 60 seconds

| Need | Open |
|---|---|
| Public wiki entry | [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki) |
| Why BITwiki exists | [`BITwiki/Manifesto.mediawiki`](BITwiki/Manifesto.mediawiki) |
| Operating covenant | [`BITwiki/Charter.mediawiki`](BITwiki/Charter.mediawiki) |
| Durable invariants | [`BITwiki/Constitution.mediawiki`](BITwiki/Constitution.mediawiki) |
| Ontology / Epistemology / Axiology | [`BITwiki/Foundational triad.mediawiki`](BITwiki/Foundational%20triad.mediawiki) |
| How knowledge is composed | [`BITwiki/Book Matter.mediawiki`](BITwiki/Book%20Matter.mediawiki) |
| Default knowledge-page format | [`BITwiki/Page format.mediawiki`](BITwiki/Page%20format.mediawiki) |
| How knowledge becomes canon | [`BITwiki/Knowledge lifecycle.mediawiki`](BITwiki/Knowledge%20lifecycle.mediawiki) |
| Organization model | [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki) |
| Templates + categories | [`BITwiki/Templates and categories.mediawiki`](BITwiki/Templates%20and%20categories.mediawiki) |
| Exact V1 implementation audit | [`BITwiki/V1 implementation audit.mediawiki`](BITwiki/V1%20implementation%20audit.mediawiki) |
| V1 category refactor | [`BITwiki/V1 category migration.mediawiki`](BITwiki/V1%20category%20migration.mediawiki) |
| Exhaustive V1 archive | [`archive-v1/README.md`](archive-v1/README.md) |

## Repository map

```text
wiki-content/
├── Main/          ordinary public knowledge pages
├── BITwiki/       foundations, architecture, governance, guides
├── Portal/        high-level knowledge entry points
├── Template/      reusable/transcluded V2 components
├── Property/      Semantic MediaWiki properties
├── Category/      intentional human-readable indexes
├── archive-v1/    exhaustive read-only public V1 snapshot
├── scripts/       reproducible archive tooling
└── .github/       validation/archive automation
```

**Repository paths mirror MediaWiki roles; they are not the ontology.**

```text
namespace ≠ entity type ≠ domain ≠ Book Matter ≠ epistemic status ≠ relationship
```

## V1 archive: exhaustive, not sampled

The public V1 snapshot is generated directly from the anonymous MediaWiki Action API with continuation followed until exhaustion. The current audited snapshot contains:

- **24** nonnegative namespaces enumerated;
- **186** public pages;
- **606** revision bodies, including historical wikitext;
- **162** Main-namespace pages;
- **9** actual Template pages and every transclusion caller;
- **162** used categories and every category membership;
- **0** created `Category:` pages in V1 — all 162 categories existed only through membership tags;
- **4** actual Property pages (imported FOAF/OWL vocabulary);
- **3** `smw/schema` pages;
- **6** MediaWiki pages;
- **2** File description pages;
- **0** Concept pages and **0** Module pages.

Open:

- [`archive-v1/audit.json`](archive-v1/audit.json) — completeness checks + counts
- [`archive-v1/index.json`](archive-v1/index.json) — every archived page
- [`archive-v1/pages/`](archive-v1/pages/) — current exact wikitext
- [`archive-v1/history/`](archive-v1/history/) — complete archived revision bodies
- [`archive-v1/categories/index.json`](archive-v1/categories/index.json) — all 162 categories
- [`archive-v1/templates/index.json`](archive-v1/templates/index.json) — all 9 real templates
- [`archive-v1/special/`](archive-v1/special/) — generated maintenance reports

The archive is reproducible with [`scripts/archive_v1.py`](scripts/archive_v1.py) and [`.github/workflows/archive-v1.yml`](.github/workflows/archive-v1.yml).

### Important V1 distinction

V1 contains sophisticated architecture documents that describe many templates, properties, categories, modules and semantic systems that were **planned or documented but not actually instantiated as namespace objects**. V2 preserves both layers:

```text
design intent      → archived writings
live implementation → archived namespaces / membership / transclusion state
```

Neither is allowed to masquerade as the other.

## 12 domain exemplars

Each major domain has one small V2 page using the same page grammar.

| Domain | Portal | Example page |
|---|---|---|
| Systems science | [`Portal/Systems science.mediawiki`](Portal/Systems%20science.mediawiki) | [`System boundary`](Main/System%20boundary.mediawiki) |
| Science | [`Portal/Science.mediawiki`](Portal/Science.mediawiki) | [`Hypothesis`](Main/Hypothesis.mediawiki) |
| Biology | [`Portal/Biology.mediawiki`](Portal/Biology.mediawiki) | [`Cell membrane`](Main/Cell%20membrane.mediawiki) |
| Mathematics | [`Portal/Mathematics.mediawiki`](Portal/Mathematics.mediawiki) | [`Prime number`](Main/Prime%20number.mediawiki) |
| Philosophy | [`Portal/Philosophy.mediawiki`](Portal/Philosophy.mediawiki) | [`Causality`](Main/Causality.mediawiki) |
| Technology | [`Portal/Technology.mediawiki`](Portal/Technology.mediawiki) | [`Version control`](Main/Version%20control.mediawiki) |
| Electronics | [`Portal/Electronics.mediawiki`](Portal/Electronics.mediawiki) | [`Resistor`](Main/Resistor.mediawiki) |
| Energy | [`Portal/Energy.mediawiki`](Portal/Energy.mediawiki) | [`Energy efficiency`](Main/Energy%20efficiency.mediawiki) |
| Engineering | [`Portal/Engineering.mediawiki`](Portal/Engineering.mediawiki) | [`Safety factor`](Main/Safety%20factor.mediawiki) |
| Chemistry | [`Portal/Chemistry.mediawiki`](Portal/Chemistry.mediawiki) | [`pH`](Main/pH.mediawiki) |
| Physics | [`Portal/Physics.mediawiki`](Portal/Physics.mediawiki) | [`Momentum`](Main/Momentum.mediawiki) |
| Medicine | [`Portal/Medicine.mediawiki`](Portal/Medicine.mediawiki) | [`Pulse`](Main/Pulse.mediawiki) |

## Default knowledge-page anatomy

Use only the matter the subject needs. A small concept generally starts with:

```text
identity / semantic metadata
Overview
Definition
Scope & importance
Core concepts / mechanism
Examples
Applications / implications
Epistemic notes
References
```

A mature page may expand into history, frameworks, methods, evidence, case studies, controversies, timelines, primary/secondary sources, bibliography, knowledge maps, implementation, limitations and related concepts.

**Modularity does not mean fragmentation.** Keep the canonical parent coherent. Split/transclude matter only when the portion is independently useful.

## V1 → V2 refactor rule

The archive preserves everything; V2 preserves the useful function with the correct primitive.

```text
V1 source + full revision history + usage
→ identify what job the object was doing
→ compare variants and intended architecture
→ preserve unique writing / behavior / provenance
→ assign correct V2 primitive
→ implement
→ validate against Special pages
```

Examples:

- V1 domain categories → `Domain` property + curated domain categories/portals.
- V1 entity-type categories → `Entity type` property; category only when a human index is useful.
- V1 epistemic-state categories → `Epistemic status` / evidence model, not a parallel category ontology.
- V1 section/fragment categories → Book Matter/transclusion.
- V1 error/validation categories → validation logic and generated maintenance reports.
- V1 templates that never existed → design-intent evidence, not automatically recreated code.

## Canon workflow

```text
source
→ preserve raw signal
→ compare revisions
→ research / cross-check
→ distill redundancy
→ revise
→ verify
→ canonicalize
→ transclude / relate
→ publish
```

A cleaner sentence is not automatically a better sentence. Preserve authored voice, unique distinctions, citations, provenance and meaningful historical development.

## Public boundary

This repository contains public material only. Private memory, credentials, access-control internals, private identity data and unpublished sensitive operational material do not belong here.
