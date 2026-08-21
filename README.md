# BITwiki V2

**BITwiki V2 is the source-controlled knowledge architecture and public corpus for BITwiki.**

This repository contains the deployable MediaWiki content, semantic model, composition layer, runtime-facing configuration, migration evidence, and validation tooling used to develop V2 from the preserved V1 system.

- **BITwiki:** https://bitwiki.org/
- **BIThub:** https://hub.bitwiki.org/
- **Canonical branch:** `main`
- **Repository status:** V2 architecture/substrate under active development; V1 preserved as provenance evidence

> `main` is the integrated source of truth. Working branches are temporary implementation surfaces and should be merged or retired once their work is resolved.

---

## What this repository owns

BITwiki is not just a directory of articles. V2 treats the wiki as a composable knowledge system built from native MediaWiki primitives.

```text
knowledge       → pages / knowledge objects
composition     → templates / transclusion / Lua
semantics       → SMW properties / concepts / queries
operations      → Cargo workflows where repeated records justify tables
navigation      → categories / portal titles / indexes / semantic views
provenance      → preserved V1 archive + migration evidence
validation      → structural, semantic, workflow and substrate audits
```

The repository is the review and transport surface for those layers. **Filesystem folders are mappings to wiki/runtime surfaces; they are not themselves the ontology.**

---

## Current integrated state

The current `main` branch includes:

- preserved public V1 provenance in `archive-v1/`;
- the V2 foundations, charter, ontology, epistemics and governance corpus;
- controlled knowledge-object identity and Domain vocabulary;
- 13 Domain exemplars plus the approved first Computer-science foundation wave;
- all 9 templates captured from the public V1 runtime, including compatibility-critical `Template:Infobox`;
- V2 templates for knowledge objects, Domain portals/categories and request records;
- `Module:Structure` as a Scribunto validation primitive;
- Semantic MediaWiki Property, Concept and `smw/schema` source surfaces;
- composed Category and Portal-title navigation;
- an executable Cargo-backed `Knowledge_requests` lifecycle;
- read-only CI that regenerates validation evidence instead of writing generated reports back into canonical source.

The V2 architecture is intentionally being exercised with real consumers before broad corpus expansion.

---

## V1 → V2

V2 is an evolution of BITwiki, not a clean-room rewrite.

```text
V1
↓ preserve
↓ understand
↓ identify signal
↓ mature primitive
↓ enhance
↓ integrate
V2
```

V1 supplied much of the imagination: ontology, epistemics, modularity, transclusion, semantic organization, relationships, portals, templates, schema, confidence systems, graphs and composable knowledge structures.

V2 keeps that ambition while grounding it in a clearer executable substrate.

`archive-v1/` is therefore **evidence**, not deployable V2 content and not a second active tree.

See:

- [`BITwiki/V1 to V2 maturation.mediawiki`](BITwiki/V1%20to%20V2%20maturation.mediawiki)
- [`archive-v1/README.md`](archive-v1/README.md)

---

## Repository map

```text
wiki-content/
├── Main/          Main namespace: canonical knowledge + compatibility redirects
├── BITwiki/       Project namespace: architecture, governance, standards, research
├── Template/      Template namespace: V2 composition + preserved compatibility templates
├── Module/        Scribunto/Lua reusable logic
├── Property/      Semantic MediaWiki Property namespace
├── Concept/       Semantic MediaWiki Concept namespace
├── SMWSchema/     smw/schema namespace source
├── Category/      human browse/classification surfaces
├── MediaWiki/     runtime/interface configuration source
├── Help/          Help namespace source mapping
├── Portal/        `Portal:*` title projection; not a configured namespace in captured siteinfo
├── archive-v1/    preserved public V1 provenance snapshot
├── scripts/       archive, inventory, audit and validation tooling
├── .github/       read-only CI / evidence generation
└── manifest.json  explicit runtime/source-control mapping
```

Every repository directory carries its own README for local orientation.

### Runtime mapping rule

```text
filesystem path
≠ MediaWiki namespace unless explicitly mapped
≠ entity type
≠ knowledge Domain
≠ Book Matter
≠ epistemic standing
≠ lifecycle
≠ semantic relationship
≠ navigation view
```

The authoritative mapping is documented in [`manifest.json`](manifest.json) and [`BITwiki/MediaWiki substrate.mediawiki`](BITwiki/MediaWiki%20substrate.mediawiki).

---

## Architecture

### Knowledge objects

Canonical subject pages use `Template:Knowledge object` to expose explicit identity:

```text
Knowledge object
├── Entity type
├── Domain
├── Epistemic status
├── Provenance
└── authored content / references / relationships
```

`Module:Structure` provides a runtime validation backstop. Missing identity remains missing; templates must not manufacture certainty with defaults.

### Semantic MediaWiki

SMW remains the canonical semantic graph layer:

- `Property/` defines graph assertions;
- `Concept/` defines reusable semantic sets;
- `#ask` powers dynamic semantic views;
- `SMWSchema/` source-controls `smw/schema` surfaces.

Subobjects are intentionally not used until a real qualified/nested-fact requirement justifies them.

### Cargo

Cargo is reserved for repeated operational records rather than canonical graph assertions.

The first bounded implementation is the knowledge-request lifecycle:

```text
Template:Knowledge request
        ↓ stores
Knowledge_requests
        ↓ queried by
BITwiki:Requested knowledge
```

Requests progress through:

```text
requested → researching → drafting → review → satisfied
                                      ↘ declined
```

The repository audit enforces:

```text
active request ≠ canonical Main page
```

A satisfied request must point to its canonical page.

### Categories and portals

Categories are human browse/classification surfaces and may be composed from templates and semantic queries rather than duplicated prose.

`Portal/` is a filesystem projection for public titles such as `Portal:Physics`. The captured MediaWiki runtime does **not** expose a dedicated Portal namespace.

---

## Start here

| Need | Canonical source |
|---|---|
| Public wiki entry | [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki) |
| System architecture | [`BITwiki/System architecture.mediawiki`](BITwiki/System%20architecture.mediawiki) |
| MediaWiki/runtime substrate | [`BITwiki/MediaWiki substrate.mediawiki`](BITwiki/MediaWiki%20substrate.mediawiki) |
| V1 → V2 maturation | [`BITwiki/V1 to V2 maturation.mediawiki`](BITwiki/V1%20to%20V2%20maturation.mediawiki) |
| Organization | [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki) |
| Ontology | [`BITwiki/Ontology.mediawiki`](BITwiki/Ontology.mediawiki) |
| Entity types | [`BITwiki/Entity types.mediawiki`](BITwiki/Entity%20types.mediawiki) |
| Epistemics | [`BITwiki/Epistemics.mediawiki`](BITwiki/Epistemics.mediawiki) |
| Semantic properties | [`BITwiki/Semantic properties.mediawiki`](BITwiki/Semantic%20properties.mediawiki) |
| Templates/categories | [`BITwiki/Templates and categories.mediawiki`](BITwiki/Templates%20and%20categories.mediawiki) |
| Transclusion | [`BITwiki/Transclusion.mediawiki`](BITwiki/Transclusion.mediawiki) |
| Navigation | [`BITwiki/Navigation.mediawiki`](BITwiki/Navigation.mediawiki) |
| Requested knowledge | [`BITwiki/Requested knowledge.mediawiki`](BITwiki/Requested%20knowledge.mediawiki) |
| Deployment prerequisites | [`BITwiki/Deployment prerequisites.mediawiki`](BITwiki/Deployment%20prerequisites.mediawiki) |
| V1 provenance | [`archive-v1/README.md`](archive-v1/README.md) |

---

## Validation

Run the same core audit family used by CI:

```bash
python scripts/validate_v2.py
python scripts/audit_substrate.py
python scripts/audit_workflow.py
python scripts/audit_mainspace.py
python scripts/inventory_corpus.py
python scripts/classify_v1_page_roles.py
python scripts/classify_v1_architecture_families.py
```

These checks cover:

- deployable wikitext structure and references;
- controlled entity/Domain/epistemic vocabularies;
- knowledge-object completeness;
- namespace/source mappings;
- actual SMW, Lua, Cargo and transclusion usage;
- request lifecycle integrity;
- Main-namespace role classification;
- empirical V1/V2 migration inventories.

Generated `v2-*.json` and other run reports are **commit-specific evidence**, not canonical source. GitHub Actions regenerates and uploads them as artifacts with read-only repository permissions.

---

## Deployment

Repository validity and MediaWiki runtime state are different things.

Before deploying, follow [`BITwiki/Deployment prerequisites.mediawiki`](BITwiki/Deployment%20prerequisites.mediawiki).

Important runtime steps include:

1. verify namespace/extension reality against the target MediaWiki installation;
2. deploy namespace-native source using the mappings in `manifest.json`;
3. deploy Modules before templates that invoke them;
4. rebuild/verify Semantic MediaWiki data after semantic changes;
5. create or recreate Cargo tables when their declaration changes;
6. verify rendered pages, semantic queries, Cargo queries and compatibility dependencies.

For the current request workflow, the runtime table is `Knowledge_requests`.

---

## Branch policy

`main` is the canonical integrated state.

Branches are temporary and should exist only while a coherent change is actively being prepared or reviewed.

```text
create focused branch
→ implement
→ validate
→ review / merge into main
→ retire branch
```

Do not maintain alternative architectural states on long-lived branches. Historical decisions belong in Git/PR history and preserved evidence—not in parallel active branches.

---

## Contribution principles

1. **Preserve before replacing.** V1 is evidence and lineage.
2. **Use native primitives deliberately.** Templates, Lua, SMW, Cargo, Categories and transclusion have different jobs.
3. **Do not invent schema to satisfy aesthetics or metrics.** New structure requires a real consumer.
4. **Prefer composition over duplication.** Small source files can render rich objects through reusable primitives.
5. **Keep requests distinct from canonical knowledge.** Missing coverage is not a stub article.
6. **Keep `main` coherent.** Experimental branches are temporary; integrated architecture belongs on `main`.
7. **Validate behavior, not prose claims.** Architecture is real only when exercised and auditable.

---

## Project principle

> **V1 gave us the imagination. V2 gives that imagination a coherent substrate.**
