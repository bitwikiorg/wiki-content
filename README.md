# BITwiki V2 — Content Map

This README is the **navigation substrate for the public BITwiki corpus**. It explains what exists, where it belongs, and how repository paths map to MediaWiki pages.

**Live `bitwiki.org` remains the authority for inherited V1 public content. This repository is the canonical V2 working corpus.** V2 preserves useful public substance and continuity while refactoring organization, semantics, transclusion, and presentation.

## Start here

| Need | Go to |
|---|---|
| Public wiki entry | [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki) |
| What BITwiki is | [`BITwiki/Manifesto.mediawiki`](BITwiki/Manifesto.mediawiki) |
| Full V2 map | [`BITwiki/Index.mediawiki`](BITwiki/Index.mediawiki) |
| How knowledge is organized | [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki) |
| How a knowledge page is built | [`BITwiki/Content model.mediawiki`](BITwiki/Content%20model.mediawiki) |
| Book Matter / reusable sections | [`BITwiki/Book matter.mediawiki`](BITwiki/Book%20matter.mediawiki) |
| Semantic schema | [`BITwiki/Schema.mediawiki`](BITwiki/Schema.mediawiki) |
| Evidence and knowledge status | [`BITwiki/Epistemics.mediawiki`](BITwiki/Epistemics.mediawiki) |
| Navigation / portals | [`BITwiki/Navigation.mediawiki`](BITwiki/Navigation.mediawiki) |
| V1 → V2 continuity | [`BITwiki/V1 public title ledger.mediawiki`](BITwiki/V1%20public%20title%20ledger.mediawiki) |
| What historical material was consolidated | [`BITwiki/Source consolidation.mediawiki`](BITwiki/Source%20consolidation.mediawiki) |

## Corpus structure

Repository directories represent **MediaWiki namespaces**, not topical folders.

```text
wiki-content/
├── Main/       ordinary public knowledge + Main Page + Book Matter subpages
├── BITwiki/    public documentation about BITwiki itself
├── Portal/     reader-facing navigation and query surfaces
├── Template/   reusable/transcluded wikicode and presentation components
├── Property/   Semantic MediaWiki properties and relationships
├── Category/   human classification and navigation groups
├── README.md   this corpus map
└── manifest.json  machine-readable repository declaration
```

### Namespace map

| Repository path | MediaWiki title | Purpose |
|---|---|---|
| `Main/Foo.mediawiki` | `Foo` | Ordinary knowledge |
| `Main/Foo/Overview.mediawiki` | `Foo/Overview` | Reusable Book Matter / subpage |
| `BITwiki/Foo.mediawiki` | `BITwiki:Foo` | Public meta, policy, architecture, documentation |
| `Portal/Foo.mediawiki` | `Portal:Foo` | Curated/dynamic navigation surface |
| `Template/Foo.mediawiki` | `Template:Foo` | Transcluded reusable content or interface |
| `Property/Foo.mediawiki` | `Property:Foo` | Typed semantic field or relationship |
| `Category/Foo.mediawiki` | `Category:Foo` | Classification/navigation category |

**Directories are transport structure for MediaWiki namespaces. They are not the knowledge taxonomy.** Domain, entity type, scope, Book Matter, epistemic status, and relationships remain separate dimensions.

## The public reading surface

The intended navigation flow is:

```text
Main Page
  ↓
Start Here / Portals / Categories
  ↓
Canonical knowledge pages
  ├── semantic relationships → other knowledge
  └── Book Matter → reusable sections
```

### Foundations

- [`BITwiki:Manifesto`](BITwiki/Manifesto.mediawiki) — why BITwiki exists.
- [`BITwiki:Charter`](BITwiki/Charter.mediawiki) — editorial commitments and operating principles.
- [`BITwiki:Constitution`](BITwiki/Constitution.mediawiki) — durable system-level invariants.
- [`BITwiki:Foundational triad`](BITwiki/Foundational%20triad.mediawiki) — ontology, epistemology, axiology.
- [`BITwiki:Glossary`](BITwiki/Glossary.mediawiki) — canonical ecosystem terminology.

### Knowledge architecture

Read this sequence when changing structure:

1. [`MediaWiki primitives`](BITwiki/MediaWiki%20primitives.mediawiki)
2. [`Architecture`](BITwiki/Architecture.mediawiki)
3. [`Organization`](BITwiki/Organization.mediawiki)
4. [`Content model`](BITwiki/Content%20model.mediawiki)
5. [`Book Matter`](BITwiki/Book%20matter.mediawiki)
6. [`Transclusion`](BITwiki/Transclusion.mediawiki)
7. [`Classification`](BITwiki/Classification.mediawiki)
8. [`Schema`](BITwiki/Schema.mediawiki)

### Knowledge quality

- [`Epistemics`](BITwiki/Epistemics.mediawiki) — evidence, confidence, uncertainty, verification.
- [`Provenance`](BITwiki/Provenance.mediawiki) — where content came from and how it changed.
- [`Quality standards`](BITwiki/Quality%20standards.mediawiki) — minimum quality expectations.
- [`Governance`](BITwiki/Governance.mediawiki) — stewardship and policy.

### Navigation

- [`BITwiki:Start here`](BITwiki/Start%20here.mediawiki)
- [`BITwiki:Index`](BITwiki/Index.mediawiki)
- [`Portal:Systems science`](Portal/Systems%20science.mediawiki)
- [`Portal:Biology`](Portal/Biology.mediawiki)
- [`Portal:Technology`](Portal/Technology.mediawiki)
- [`Portal:Philosophy`](Portal/Philosophy.mediawiki)

Portals and indexes are **views over the knowledge model**. They do not define the ontology.

## Book Matter and transclusion

A canonical knowledge page may be composed from reusable semantic parts.

Example:

```text
Bioluminescent Organisms
├── Overview
├── Biochemical Mechanism
├── Examples
├── Applications
├── Related Theories
└── References
```

The parent remains the canonical knowledge object. Its subpages can be transcluded independently when a reader, portal, agent, or another page needs only that portion.

Main Page presentation follows the same principle through real templates such as `Template:Main page/Notice`, `Template:Main page/Live stats`, and `Template:Main page/Featured knowledge`.

## How to interpret a file

V2 uses four important states:

**Canonical page** — the current V2 page for that subject or system concept.

**Meta page** — public documentation *about BITwiki*. These belong in `BITwiki:` and use `{{BITwiki meta}}` where applicable.

**Reusable/transcluded page** — Book Matter or a Template intended to be composed into another page.

**Redirect** — a V1 title, alias, revision-era name, or superseded structural page retained for continuity but pointing to its canonical V2 destination.

Some pages were reconstructed from accessible public V1 material rather than exact exported raw wikitext. Those use `{{Source status|...}}`. **A preserved title or redirect does not imply that every historical sentence has been recovered.**

## V1 continuity and provenance

V2 does not reproduce V1's duplicate architecture merely to preserve old names.

- The [`V1 public title ledger`](BITwiki/V1%20public%20title%20ledger.mediawiki) accounts for the 162 visible V1 Main-namespace titles used in the reconstruction.
- [`Source consolidation`](BITwiki/Source%20consolidation.mediawiki) records how major V1 and historical Notion families were distilled into the smaller canonical V2 set.
- MediaWiki redirects preserve old public links where a title was renamed, merged, or moved.
- Exact historical prose/history still belongs to MediaWiki revision/export reconciliation when raw source was not available during reconstruction.

Historical Notion material is **design archaeology**, not current authority.

## Where new material belongs

Use the narrowest native MediaWiki primitive:

- Durable subject knowledge → `Main/`
- Documentation about BITwiki → `BITwiki/`
- Navigation over knowledge → `Portal/`
- Reusable rendering/content → `Template/`
- Semantic attribute/relationship → `Property/`
- Human grouping/classification → `Category/`
- Reusable semantic portion of an article → usually a Main subpage / Book Matter

Do not create a category when a property is the real requirement. Do not create a namespace when an entity type is the real requirement. Do not create a separate page when a section or template is sufficient.

## Boundary

This repository contains **public BITwiki content only**. Protected/private memory, credentials, private identity data, queues, access-control internals, and non-public operational material do not belong here.

`manifest.json` is the machine-readable companion to this map.