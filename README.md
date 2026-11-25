# BITwiki V2

**BITwiki V2 is the source-controlled knowledge architecture and public corpus for BITwiki.**

**Editorial scope:** BITwiki documents knowledge across disciplines without imposing a computation- or information-centered admission gate. Canonical subjects must have defensible identity, appropriate sources, meaningful qualifications and relations. Editorial quality is evaluated on the substance; CI does not certify scientific or philosophical validity. See [page format](BITwiki/Page%20format.mediawiki) and [editorial protocol](BITwiki/Editorial%20protocol.mediawiki).

This repository includes the reviewed deployment projection for BITwiki's public MediaWiki knowledge substrate, as well as separate non-deployable validation, historical and operational files. Repository visibility is public; internal-only records should ultimately live in a separately access-controlled system.

- **BITwiki:** https://bitwiki.org/
- **GitHub Pages staging:** https://bitwikiorg.github.io/wiki-content/
- **BIThub:** https://hub.bitwiki.org/
- **Canonical branch:** `main`
- **V1 migration source:** content reconciliation is complete; `archive-v1/` remains read-only pending the separate retirement operation. See [`docs/v1-reconciliation.md`](docs/v1-reconciliation.md) and [`docs/v1-retirement-dependency-audit.md`](docs/v1-retirement-dependency-audit.md).

> `main` is the integrated repository source of truth. Filesystem folders project MediaWiki/runtime surfaces; they are not themselves the ontology.

---

## System model

BITwiki is not only a collection of pages. It is a programmable knowledge substrate.

```text
authored wikitext / Templates
            +
Semantic MediaWiki graph state
            +
Cargo operational state
            ↓
MediaWiki parser + Scribunto/Lua
            ↓
normalize → type-check → resolve → bounded derive → project → diagnose
            ↓
page · navigation · graph · comparison · maintenance · machine-facing views
            ↕
authenticated API / plugin / service / agent boundary
            ↕
BIThub / Discourse
            ↕
humans · agents · workflows
```

The layers intentionally keep different authority:

| Layer | Responsibility |
|---|---|
| Main-space pages / Book Matter | canonical durable knowledge and authored explanation |
| Semantic MediaWiki | durable typed properties and semantic relationships |
| Cargo | repeated structured operational/workflow records |
| Templates | declarative authoring, transclusion, semantic emission, and stable public invocation |
| Scribunto/Lua | deterministic compiler/type-system/bounded-inference/projection/diagnostics layer |
| MediaWiki | parsing, revisions, namespaces, permissions, caching, APIs, and execution environment |
| BIThub/Discourse | conversation, coordination, active inference, contribution workflow, and user/agent interaction |
| BITCORE/agents | external research, synthesis, orchestration, tools, and proposed structured changes |

**BIThub is an interface/workflow plane over BITwiki knowledge, not a second semantic authority.** Cross-service transport belongs to authenticated APIs, plugins, services, or agents; Scribunto is not the network bridge.

Detailed architecture: [`BITwiki/Programmable knowledge substrate.mediawiki`](BITwiki/Programmable%20knowledge%20substrate.mediawiki) and [`BITwiki/Lua architecture.mediawiki`](BITwiki/Lua%20architecture.mediawiki).

---

## Compiler/runtime architecture

Lua is an architectural layer, not merely a template helper.

```text
bitwiki-runtime-schema.json            repository authority
        ↓
Module:BITwiki/Data/Schema             Scribunto runtime projection
        ↓
Module:BITwiki/Core
        ↓
Module:BITwiki/Compiler
        ↓
Module:Structure                       public compatibility wrapper
        ↓
Template:Knowledge object
```

`bitwiki-runtime-schema.json` owns compiler-facing controlled vocabularies and deterministic relationship-display metadata. `scripts/validate_v2.py` consumes that authority directly. Scribunto cannot read arbitrary repository JSON, so `Module:BITwiki/Data/Schema` is the necessary runtime projection; `scripts/audit_runtime_schema.py` detects drift between them.

Compiler derivation is deliberately bounded:

```text
stored assertion
≠ derived display
≠ derived diagnostic
≠ proposed persistent assertion
```

Lua may normalize, validate, derive safe deterministic views, and diagnose state. It must not silently manufacture canonical facts or become an autonomous/background runtime.

---

## Self-modeling stack

BITwiki should describe consequential systems that make BITwiki possible. Main space therefore includes canonical knowledge objects for BITwiki, BIThub, MediaWiki, Discourse, Semantic MediaWiki, Cargo, Scribunto, and Lua.

These pages also emit conservative SMW relationships so the platform can inspect its own substrate as graph state. For example, BITwiki depends on MediaWiki, Semantic MediaWiki, Scribunto, and Cargo, while BIThub depends on Discourse and remains explicitly related to BITwiki.

Project-specific implementation standards remain in `BITwiki:*`; Main-space pages explain the technology/project itself. This prevents project architecture from replacing general knowledge while still allowing the system to dogfood its own semantic model.

---

## Repository structure

```text
wiki-content/
├── Main/          canonical Main-namespace knowledge, self-model objects, redirects, Book Matter
├── archive-v1/    read-only V1 migration/provenance source
├── BITwiki/       public project architecture, editorial standards, governance, epistemics
├── Template/      declarative authoring/invocation and recovered compatibility templates
├── Module/        Scribunto/Lua compiler, transformation, projection, diagnostics
├── Property/      Semantic MediaWiki assertion vocabulary
├── Concept/       reusable computed SMW sets
├── SMWSchema/     native smw/schema namespace payloads
├── Category/      browse/classification/navigation surfaces
├── MediaWiki/     public runtime/interface configuration pages
├── Help/          stable user-facing workflow documentation
├── Portal/        Portal:* navigation title projection; not a confirmed namespace
├── scripts/       archival, validation, audit, inventory, and migration tooling
├── docs/          non-deployable maintainer deployment runbook
├── ops/           non-deployable operational records (still visible in public GitHub)
├── .github/       CI and repository automation
├── bitwiki-runtime-schema.json  compiler-facing schema authority
└── manifest.json  explicit runtime/source mappings and architecture invariants
```

Each major directory README is **living architecture text**: it states what that surface owns, what it does not own, how it connects to adjacent layers, and which deeper `BITwiki:*` standards govern it.

---

## Native primitive rule

Use the smallest native layer whose semantics match the job.

| Need | Primitive |
|---|---|
| canonical independent knowledge | page / knowledge object |
| authored reusable matter | transclusion / Book Matter |
| declarative rendering or semantic emission | Template |
| reusable normalization, validation, bounded inference, computation, semantic presentation | Scribunto `Module:` |
| durable graph assertion | SMW `Property:` |
| reusable computed semantic set | SMW `Concept:` |
| qualified/nested semantic fact | SMW subobject when justified |
| repeated operational records | Cargo |
| browse hierarchy | Category |
| subject orientation | Portal / contents / outline / list / glossary |
| cross-service BIThub interaction | authenticated API/plugin/service/agent integration |

A view is not the database. A discussion is not canon. A Lua derivation is not automatically a stored assertion.

---

## Knowledge-request lifecycle

Missing coverage is represented as operational state rather than empty Main-space shells.

```text
requested → researching → drafting → review → satisfied
                                      ↘ declined
```

The critical invariant is:

```text
active request
≠ canonical Main page
```

The prior public Cargo-backed queue has been retired from source-controlled MediaWiki publication. Existing 51 request records are preserved in `ops/knowledge-requests.json`, validated by `scripts/audit_workflow.py`, and **not** a public wiki page or Cargo table. This public GitHub repository is not a private operations database; a confidential workflow requires a separate private migration.

---

## Canonical entry points

| Need | Source |
|---|---|
| Public wiki entry | [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki) |
| Programmable substrate | [`BITwiki/Programmable knowledge substrate.mediawiki`](BITwiki/Programmable%20knowledge%20substrate.mediawiki) |
| Lua/compiler standard | [`BITwiki/Lua architecture.mediawiki`](BITwiki/Lua%20architecture.mediawiki) |
| MediaWiki/runtime mapping | [`BITwiki/MediaWiki substrate.mediawiki`](BITwiki/MediaWiki%20substrate.mediawiki) |
| Ecosystem / BIThub boundary | [`BITwiki/Ecosystem.mediawiki`](BITwiki/Ecosystem.mediawiki) |
| Interoperability | [`BITwiki/Interoperability.mediawiki`](BITwiki/Interoperability.mediawiki) |
| Organization | [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki) |
| Page/content standard | [`BITwiki/Page format.mediawiki`](BITwiki/Page%20format.mediawiki) |
| Semantic properties | [`BITwiki/Semantic properties.mediawiki`](BITwiki/Semantic%20properties.mediawiki) |
| Navigation | [`BITwiki/Navigation.mediawiki`](BITwiki/Navigation.mediawiki) |
| Operational request records (not wiki source) | [`ops/knowledge-requests.json`](ops/knowledge-requests.json) |
| Deployment runbook (not wiki source) | [`docs/deployment.md`](docs/deployment.md) |
| Runtime mapping manifest | [`manifest.json`](manifest.json) |
| V1 reconciliation | [`docs/v1-reconciliation.md`](docs/v1-reconciliation.md) · source `archive-v1/` · immutable snapshot `3100db1d7807b752e41b6ccf7f88498982cfb2d4` |

---

## Validation and executable governance

Run the architecture checks locally with:

```bash
python scripts/validate_v2.py
python scripts/audit_runtime_schema.py
python scripts/audit_substrate.py
python scripts/audit_workflow.py
python scripts/audit_mainspace.py
python scripts/inventory_corpus.py
python scripts/classify_v1_page_roles.py
python scripts/classify_v1_architecture_families.py
find Module -type f -name '*.lua' -print0 | xargs -0 -n1 luac5.1 -p
```

CI treats these checks as executable architecture evidence. Generated JSON reports are run-specific evidence and are not committed as mutable canonical source.

Repository validation does not prove the remote MediaWiki deployment. Runtime deployment must still verify module dependency order, Scribunto behavior, relevant SMW state and any supported integration contract. Cargo must be checked if a future reviewed feature actually uses it. Native `mw.smw` access is not assumed; it requires an explicitly deployed and compatible SemanticScribunto capability.

---

## V1 → V2

V2 preserves V1 as design and provenance evidence rather than treating it as disposable scaffolding.

```text
V1
→ preserve
→ understand
→ identify signal
→ mature primitive
→ enhance
→ integrate into V2
```

`archive-v1/` is a read-only migration/provenance source retained after completion of the content-level reconciliation. It is not deployable V2 source or current architecture. The remaining retirement work is documented in `docs/v1-retirement-dependency-audit.md`; Git recoverability alone was not treated as proof of successful migration.

---

## Living-text rule

Architecture changes are incomplete when only code or one specification knows about them.

When a reviewed change alters a directory's responsibility, source-of-truth boundary, dependency, deployment order, or connection to another subsystem:

1. update the implementation;
2. update the authoritative `BITwiki:*` architecture/standard where applicable;
3. update the nearest README so a repository reader encounters the current model locally;
4. update `manifest.json` or executable validation when the invariant is machine-checkable;
5. preserve historical descriptions as history rather than silently rewriting archival evidence.

READMEs should summarize the current operational contract rather than duplicate entire standards. Detailed semantics belong in canonical wiki architecture pages; READMEs explain how the repository surface participates in them.

---

## Branch and contribution policy

**`main` is the only canonical integrated repository state.** Working branches are review surfaces, not alternate BITwiki versions.

Before changing content or architecture, determine whether the change is canonical knowledge, project architecture, graph state, operational state, navigation, interface configuration, executable logic, or provenance. Use the corresponding native primitive, preserve evidence, run the relevant audits, and integrate accepted work into `main`.

See [`BITwiki/Contributing.mediawiki`](BITwiki/Contributing.mediawiki) and the maintainer [`docs/deployment.md`](docs/deployment.md).
