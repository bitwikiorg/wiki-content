# BITwiki V2 — Content Map

This README is the **navigation substrate for the public BITwiki corpus**. It is not a conventional repository README.

```text
V2 canon       → Main/ · BITwiki/ · Portal/ · Template/ · Property/ · Category/
V1 provenance  → archive-v1/
```

`archive-v1/` is read-only source evidence. **Do not deploy it as V2.**

## Start here

| Need | Canonical page |
|---|---|
| Public wiki entry | [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki) |
| Foundation map | [`BITwiki/Foundations.mediawiki`](BITwiki/Foundations.mediawiki) |
| Why BITwiki exists | [`BITwiki/Manifesto.mediawiki`](BITwiki/Manifesto.mediawiki) |
| BITCORE worldview | [`BITwiki/BITCORE Manifesto.mediawiki`](BITwiki/BITCORE%20Manifesto.mediawiki) |
| Operating covenant | [`BITwiki/Charter.mediawiki`](BITwiki/Charter.mediawiki) |
| Durable invariants | [`BITwiki/Constitution.mediawiki`](BITwiki/Constitution.mediawiki) |
| Ontology / Epistemology / Axiology | [`BITwiki/Foundational triad.mediawiki`](BITwiki/Foundational%20triad.mediawiki) |
| How the wiki is organized | [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki) |
| V1 → V2 maturation framework | [`BITwiki/V1 to V2 maturation.mediawiki`](BITwiki/V1%20to%20V2%20maturation.mediawiki) |
| Default knowledge-page grammar | [`BITwiki/Page format.mediawiki`](BITwiki/Page%20format.mediawiki) |
| Reusable content anatomy | [`BITwiki/Book Matter.mediawiki`](BITwiki/Book%20Matter.mediawiki) |
| Composition / reuse rules | [`BITwiki/Transclusion.mediawiki`](BITwiki/Transclusion.mediawiki) |
| Ontological model | [`BITwiki/Ontology.mediawiki`](BITwiki/Ontology.mediawiki) |
| Entity vocabulary | [`BITwiki/Entity types.mediawiki`](BITwiki/Entity%20types.mediawiki) |
| Relationship model | [`BITwiki/Relationships.mediawiki`](BITwiki/Relationships.mediawiki) |
| Implemented SMW properties | [`BITwiki/Semantic properties.mediawiki`](BITwiki/Semantic%20properties.mediawiki) |
| Epistemic model | [`BITwiki/Epistemics.mediawiki`](BITwiki/Epistemics.mediawiki) |
| Evidence evaluation | [`BITwiki/Evidence.mediawiki`](BITwiki/Evidence.mediawiki) |
| Provenance | [`BITwiki/Provenance.mediawiki`](BITwiki/Provenance.mediawiki) |
| Uncertainty | [`BITwiki/Uncertainty.mediawiki`](BITwiki/Uncertainty.mediawiki) |
| Navigation / portals | [`BITwiki/Navigation.mediawiki`](BITwiki/Navigation.mediawiki) |
| Knowledge lifecycle | [`BITwiki/Knowledge lifecycle.mediawiki`](BITwiki/Knowledge%20lifecycle.mediawiki) |
| Source authority / lineage | [`BITwiki/Source lineage.mediawiki`](BITwiki/Source%20lineage.mediawiki) |
| Exact current-public V1 archive | [`archive-v1/README.md`](archive-v1/README.md) |
| Independent V1 fidelity audit | [`v1-fidelity-audit.json`](v1-fidelity-audit.json) |
| V2 structural validation | [`v2-validation.json`](v2-validation.json) |

## Corpus structure

```text
wiki-content/
├── Main/          ordinary public knowledge + V1 compatibility redirects
├── BITwiki/       foundations, architecture, epistemics, governance, guides
├── Portal/        reader-facing domain entry points
├── Template/      reusable content/interface behavior
├── Property/      Semantic MediaWiki properties and relations
├── Category/      intentional human browse/index surfaces
├── archive-v1/    exhaustive snapshot of the current public V1 corpus
├── scripts/       archive, fidelity, and validation tooling
└── .github/       reproducible automation
```

### Repository path → MediaWiki title

| Repository path | MediaWiki title | Job |
|---|---|---|
| `Main/Foo.mediawiki` | `Foo` | ordinary knowledge |
| `Main/Foo/Overview.mediawiki` | `Foo/Overview` | reusable Book Matter / subpage |
| `BITwiki/Foo.mediawiki` | `BITwiki:Foo` | public project/meta architecture |
| `Portal/Foo.mediawiki` | `Portal:Foo` | reader-facing navigation |
| `Template/Foo.mediawiki` | `Template:Foo` | reusable rendering/content behavior |
| `Property/Foo.mediawiki` | `Property:Foo` | semantic attribute/relation |
| `Category/Foo.mediawiki` | `Category:Foo` | human browse/index surface |

**Directories are transport structure for MediaWiki namespaces. They are not the knowledge taxonomy.**

```text
namespace
≠ entity type
≠ domain
≠ Book Matter
≠ epistemic standing
≠ lifecycle
≠ relationship
≠ navigation view
```

## The V2 knowledge object

```text
                         KNOWLEDGE OBJECT
                               │
       ┌───────────────────────┼────────────────────────┐
       │                       │                        │
    IDENTITY                CONTENT                 EPISTEMICS
       │                       │                        │
 Entity type               Book Matter              Evidence
 Domain(s)                 Overview                 Sources
 Relationships             Theory / model           Provenance
 Scope                     Mechanism                Standing
                            Methods                  Uncertainty
                            Applications             Review
                            References               Lifecycle
       │                       │                        │
       └───────────────────────┼────────────────────────┘
                               │
                         NAVIGATION / VIEWS
                  Portal · Category · Index · Query
```

No branch is the whole knowledge model.

## Public reading path

```text
Main Page
   ↓
Portals / Categories / Search
   ↓
Canonical knowledge objects
   ├── semantic relationships → other knowledge
   ├── Book Matter → reusable portions
   ├── evidence / provenance → why it should be trusted
   └── revision history → how it changed
```

The 12 domain portals now use `Template:Domain portal`: each preserves its domain-specific orientation while the template provides a common semantic browse/query surface.

## Current domain surfaces

| Domain | Portal | Exemplar |
|---|---|---|
| Systems science | `Portal:Systems science` | `System boundary` |
| Science | `Portal:Science` | `Hypothesis` |
| Biology | `Portal:Biology` | `Cell membrane` |
| Mathematics | `Portal:Mathematics` | `Prime number` |
| Philosophy | `Portal:Philosophy` | `Causality` |
| Technology | `Portal:Technology` | `Version control` |
| Electronics | `Portal:Electronics` | `Resistor` |
| Energy | `Portal:Energy` | `Energy efficiency` |
| Engineering | `Portal:Engineering` | `Safety factor` |
| Chemistry | `Portal:Chemistry` | `pH` |
| Physics | `Portal:Physics` | `Momentum` |
| Medicine | `Portal:Medicine` | `Pulse` |

These are initial high-level views, not exclusive ontological branches.

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

Mature pages can expand into history, frameworks, methods, evidence/results, case studies, controversy, timelines, implementation, limitations, bibliography, knowledge maps, and other Book Matter.

**Modularity does not mean fragmentation.** Keep the canonical parent coherent. Split or transclude only when the portion has an actual independent reuse/retrieval/provenance job.

## Semantic rules

The V2 semantic substrate is deliberately smaller than the V1 proposed schema.

Use:

- `Entity type` for what kind of knowledge object this is;
- `Domain` for fields/bodies of knowledge;
- `Epistemic status` for present evidentiary standing;
- `Confidence rationale` for why the present evidence justifies reliance;
- `Review status` for actual review/verification state;
- `Lifecycle status` for active/superseded/deprecated/archived state;
- `Provenance` for origin/lineage;
- specific Page relations such as `Implements`, `Part of`, `Depends on`, `Supports`, `Contradicts`, `Refines`, and `Derived from` when justified.

Do not compress these jobs into one category, one status field, or a decorative numeric confidence score.

## V1 source integrity

The current public V1 archive is independently verified against live BITwiki:

- **186 / 186** current public pages archived;
- **606 / 606** public revision bodies compared;
- all current page/revision IDs and SHA-1s match;
- all **162** category names and memberships match;
- all **9** implemented templates and callers match;
- both File-page revision records match;
- namespace and required maintenance-report state match;
- independent audit: `content_fidelity_pass: true`.

Historical boundary: the public deletion log contains deleted titles whose deleted bodies are not anonymously retrievable. Therefore the archive is complete for the **current anonymous-readable V1 corpus and public histories of pages that currently exist**, not a claim of byte-for-byte recovery of every deleted revision ever created.

Detailed evidence belongs in the audit files, not in this navigation page:

- [`archive-v1/audit.json`](archive-v1/audit.json)
- [`v1-fidelity-audit.json`](v1-fidelity-audit.json)
- [`v1-deleted-content-audit.json`](v1-deleted-content-audit.json)
- [`v1-deleted-unresolved.json`](v1-deleted-unresolved.json)
- [`BITwiki/V1 implementation audit.mediawiki`](BITwiki/V1%20implementation%20audit.mediawiki)
- [`BITwiki/V1 category migration.mediawiki`](BITwiki/V1%20category%20migration.mediawiki)
- [`BITwiki/V1 maintenance baseline.mediawiki`](BITwiki/V1%20maintenance%20baseline.mediawiki)

## V1 → V2 editorial rule

```text
V1
→ preserve
→ understand
→ identify signal
→ mature primitive
→ enhance
→ integrate into V2
```

**V1 gave us the imagination. V2 gives that imagination a coherent substrate.**

This is a maturation process, not a rewrite. Design writing and implementation evidence are both authoritative for different questions: one records what BITwiki was trying to become; the other records what actually existed and ran.

Canonicalization is **not** permission to replace authored work with generic summaries. Historical implementation mistakes may be refactored. Historical thinking, unusual language, worldview, experiments, and provenance remain evidence and lineage.

The detailed framework lives in [`BITwiki/V1 to V2 maturation.mediawiki`](BITwiki/V1%20to%20V2%20maturation.mediawiki).

## Where new material belongs

| Need | Put it here |
|---|---|
| durable subject knowledge | `Main/` |
| BITwiki foundations/architecture/governance | `BITwiki/` |
| high-level reader navigation | `Portal/` |
| repeated rendering or reusable interface/content behavior | `Template/` |
| stable semantic attribute/relation | `Property/` |
| useful human browse collection | `Category/` |
| reusable subject portion | Main subpage / Book Matter |
| historical V1 evidence | `archive-v1/` only |

Before creating a new object, ask whether an existing page section, property, relation, template, query, or Book Matter unit already performs the job.

## Validation

`v2-validation.json` is the structural gate for the deployable V2 corpus. It checks category/template resolution, intentional categorization, all 12 domain portals/categories, and the exemplar set.

Source fidelity is a separate question from structural validity; both matter.

## Public boundary

This repository contains public material only. Private memory, credentials, access-control internals, identity-bound private state, and unpublished sensitive operational material do not belong here.
