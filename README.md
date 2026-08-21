# BITwiki V2

**BITwiki V2 is the source-controlled knowledge architecture and public corpus for BITwiki.**

This repository is the reviewed source and deployment projection for BITwiki's MediaWiki knowledge substrate: canonical knowledge, semantic graph state, operational records, programmable computation, navigation, project standards, migration evidence, and executable validation.

- **BITwiki:** https://bitwiki.org/
- **BIThub:** https://hub.bitwiki.org/
- **Canonical branch:** `main`
- **V1 lineage:** preserved under `archive-v1/`

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
├── BITwiki/       project architecture, standards, governance, epistemics, operations
├── Template/      declarative authoring/invocation and recovered compatibility templates
├── Module/        Scribunto/Lua compiler, transformation, projection, diagnostics
├── Property/      Semantic MediaWiki assertion vocabulary
├── Concept/       reusable computed SMW sets
├── SMWSchema/     native smw/schema namespace payloads
├── Category/      browse/classification/navigation surfaces
├── MediaWiki/     public runtime/interface configuration pages
├── Help/          stable user-facing workflow documentation
├── Portal/        Portal:* navigation title projection; not a confirmed namespace
├── archive-v1/    preserved public V1 provenance and migration evidence
├── scripts/       archival, validation, audit, inventory, and migration tooling
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

`Template:Knowledge request` stores repeated workflow state in Cargo table `Knowledge_requests`; `BITwiki:Requested knowledge` remains the authored queue and computed operational view.

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
| Knowledge requests | [`BITwiki/Requested knowledge.mediawiki`](BITwiki/Requested%20knowledge.mediawiki) |
| V1 → V2 maturation | [`BITwiki/V1 to V2 maturation.mediawiki`](BITwiki/V1%20to%20V2%20maturation.mediawiki) |
| Deployment | [`BITwiki/Deployment prerequisites.mediawiki`](BITwiki/Deployment%20prerequisites.mediawiki) |
| Runtime mapping manifest | [`manifest.json`](manifest.json) |
| V1 archive | [`archive-v1/README.md`](archive-v1/README.md) |

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

Repository validation does not prove the remote MediaWiki deployment. Runtime deployment must still verify module dependency order, Scribunto behavior, Cargo tables, SMW state, and any BIThub integration contract. Native `mw.smw` access is not assumed; it requires an explicitly deployed and compatible SemanticScribunto capability.

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

`archive-v1/` is read-only historical evidence, not deployable V2 source and not an alternate current architecture.

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

See [`BITwiki/Contributing.mediawiki`](BITwiki/Contributing.mediawiki) and [`BITwiki/Deployment prerequisites.mediawiki`](BITwiki/Deployment%20prerequisites.mediawiki).
