# BITwiki V2 — Content Map

This README is the **navigation substrate for the public BITwiki corpus**, not a conventional repository README.

```text
V2 canon       → Main/ · BITwiki/ · Portal/ · Template/ · Property/ · Category/
V1 provenance  → archive-v1/
```

`archive-v1/` is read-only source evidence. **Do not deploy it as V2.**

## Start here

| Need | Canonical surface |
|---|---|
| Public wiki entry | [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki) |
| Subject navigation | [`Portal/`](Portal/) |
| Why `Main/` looks strange on GitHub | [`Main/README.md`](Main/README.md) |
| How BITwiki is organized | [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki) |
| Navigation model | [`BITwiki/Navigation.mediawiki`](BITwiki/Navigation.mediawiki) |
| Simple → technical reading model | [`BITwiki/Readable depth and localization.mediawiki`](BITwiki/Readable%20depth%20and%20localization.mediawiki) |
| Contribute | [`BITwiki/Contributing.mediawiki`](BITwiki/Contributing.mediawiki) |
| Missing / requested knowledge | [`BITwiki/Requested knowledge.mediawiki`](BITwiki/Requested%20knowledge.mediawiki) |
| External research references | [`BITwiki/Research references.mediawiki`](BITwiki/Research%20references.mediawiki) |
| Comparative wiki research | [`BITwiki/Comparative wiki research register.mediawiki`](BITwiki/Comparative%20wiki%20research%20register.mediawiki) |
| Navigation / coverage research | [`BITwiki/Navigation and coverage research.mediawiki`](BITwiki/Navigation%20and%20coverage%20research.mediawiki) |
| Sensitive-topic scope research | [`BITwiki/Sensitive topic scope research.mediawiki`](BITwiki/Sensitive%20topic%20scope%20research.mediawiki) |
| Foundations | [`BITwiki/Foundations.mediawiki`](BITwiki/Foundations.mediawiki) |
| Ontology | [`BITwiki/Ontology.mediawiki`](BITwiki/Ontology.mediawiki) |
| Entity vocabulary | [`BITwiki/Entity types.mediawiki`](BITwiki/Entity%20types.mediawiki) |
| Relationships | [`BITwiki/Relationships.mediawiki`](BITwiki/Relationships.mediawiki) |
| Epistemics | [`BITwiki/Epistemics.mediawiki`](BITwiki/Epistemics.mediawiki) |
| Provenance | [`BITwiki/Provenance.mediawiki`](BITwiki/Provenance.mediawiki) |
| V1 → V2 maturation | [`BITwiki/V1 to V2 maturation.mediawiki`](BITwiki/V1%20to%20V2%20maturation.mediawiki) |
| Exact current-public V1 archive | [`archive-v1/README.md`](archive-v1/README.md) |
| V2 validation | [`v2-validation.json`](v2-validation.json) |

## Corpus structure

```text
wiki-content/
├── Main/          MediaWiki main namespace: knowledge + compatibility redirects + Book Matter
├── BITwiki/       foundations, architecture, epistemics, governance, guides, research/admin
├── Portal/        reader-facing Domain and focused/subportal entry points
├── Template/      reusable content/interface behavior
├── Property/      Semantic MediaWiki properties and relations
├── Category/      intentional human browse/index surfaces
├── archive-v1/    exhaustive current-public V1 provenance snapshot
├── scripts/       archive, fidelity, inventory, audit, and validation tooling
└── .github/       reproducible automation
```

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

## `Main/` is not an article directory

Many tiny files in `Main/` are V1 compatibility redirects preserving old public titles. They are **not generic stubs**. The substantive canonical page may live in `BITwiki:` or elsewhere.

Run:

```bash
python scripts/audit_mainspace.py
```

to generate `v2-mainspace-audit.json`, which separates redirects, domain exemplars, knowledge objects, subpages, other content, and short non-redirect review candidates.

Missing knowledge should normally go to [`BITwiki/Requested knowledge.mediawiki`](BITwiki/Requested%20knowledge.mediawiki) rather than becoming an empty article shell.

## Navigation architecture

BITwiki intentionally uses several complementary views:

```text
Contents / Main Page
Portal / focused portal
Category / subcategory
Outline
List / registry
Glossary / index
Core/Vital coverage set
Semantic query / graph
Search / links
```

No single one is the ontology.

Focused portals use canonical titles such as:

- `Portal:Bioinformatics` — navigational parents Biology + Computer science
- `Portal:Python` — navigational parent Computer science

Older slash paths may redirect for continuity, but filesystem-like portal paths do not define ontology inheritance.

## Reader-depth localization

The preferred presentation model is:

```text
Simple orientation
→ Core understanding
→ Technical depth
→ Frontier / research
```

The goal is **one coherent canonical knowledge graph with progressive disclosure**, rather than separate disconnected “simple” and “technical” encyclopedias. Language translation is a separate dimension.

See [`BITwiki/Readable depth and localization.mediawiki`](BITwiki/Readable%20depth%20and%20localization.mediawiki).

## Current controlled Domain surfaces

| Domain | Portal | Exemplar |
|---|---|---|
| Systems science | `Portal:Systems science` | `System boundary` |
| Science | `Portal:Science` | `Hypothesis` |
| Biology | `Portal:Biology` | `Cell membrane` |
| **Computer science** | `Portal:Computer science` | `Algorithm` |
| Mathematics | `Portal:Mathematics` | `Prime number` |
| Philosophy | `Portal:Philosophy` | `Causality` |
| Technology | `Portal:Technology` | `Version control` |
| Electronics | `Portal:Electronics` | `Resistor` |
| Energy | `Portal:Energy` | `Energy efficiency` |
| Engineering | `Portal:Engineering` | `Safety factor` |
| Chemistry | `Portal:Chemistry` | `pH` |
| Physics | `Portal:Physics` | `Momentum` |
| Medicine | `Portal:Medicine` | `Pulse` |

These **13 Domains are a controlled working vocabulary, not a claim that all knowledge fits into thirteen exclusive branches**. Expansion is evidence-driven; current candidates are tracked in `BITwiki:Requested knowledge` and navigation research.

## Knowledge-object model

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
            Portal · Category · Outline · Index · Query · Graph
```

Use semantic properties deliberately. Missing identity remains missing; templates must not manufacture certainty through defaults.

## Default page grammar

Use only the matter the subject needs:

```text
semantic identity
Overview / understandable lead
Definition
Scope & importance
Core concepts / mechanism
Examples
Applications / implications
Technical depth when useful
Epistemic notes / frontier questions
References
```

**Modularity does not mean fragmentation.** Keep the canonical parent coherent. Split or transclude only when a portion has an independent reuse/retrieval/provenance job.

## Contribution rule

Before creating a new page, ask whether an existing page section, relation, category, portal, outline, request, query, or Book Matter unit already performs the job.

Prefer:

```text
read
→ identify gap
→ source/research
→ improve existing knowledge or record request
→ create coherent page only when justified
→ validate
→ canonicalize
```

See [`BITwiki/Contributing.mediawiki`](BITwiki/Contributing.mediawiki).

## V1 source integrity

The current-public V1 archive remains independently verified:

- **186 / 186** current public pages archived;
- **606 / 606** public revision bodies compared;
- all current page/revision IDs and SHA-1s match;
- all **162** category names and memberships match;
- all **9** implemented templates and callers match;
- independent audit: `content_fidelity_pass: true`.

Historical deleted bodies that are not anonymously retrievable remain outside the completeness claim. Detailed evidence lives in the audit files and `archive-v1/`.

## V1 → V2 editorial rule

```text
V1
→ preserve
→ understand
→ identify signal
→ mature primitive
→ enhance
→ integrate into V2
→ validate
```

**V1 gave us the imagination. V2 gives that imagination a coherent substrate.**

Canonicalization is not permission to replace authored work with generic summaries. Preserve meaningful voice, unusual thinking, experiments, and provenance while refactoring implementation mistakes.

## Validation

`v2-validation.json` checks the deployable V2 structure and semantic identity. Every controlled Domain must have its Category, Portal, and at least one Domain exemplar; the validator no longer relies on a hard-coded exemplar count.

`v2-mainspace-audit.json` is generated separately to make the Main namespace legible without confusing redirects or file length with article quality.

Source fidelity is a separate question from structural validity; both matter.

## Public boundary

This repository contains public material only. Private memory, credentials, access-control internals, identity-bound private state, and unpublished sensitive operational material do not belong here.
