# BITwiki V2

**Public MediaWiki source. Start here.**

BITwiki is the durable knowledge layer of the **BITwiki / BIThub / BITCORE** ecosystem.  
This repository is organized to answer three questions quickly:

1. **What should I read?**
2. **Where does a page belong?**
3. **Where did V2 material come from?**

---

## Start in 60 seconds

| Need | Open |
|---|---|
| Public wiki entry | [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki) |
| Why BITwiki exists | [`BITwiki/Manifesto.mediawiki`](BITwiki/Manifesto.mediawiki) |
| Operating covenant | [`BITwiki/Charter.mediawiki`](BITwiki/Charter.mediawiki) |
| Durable invariants | [`BITwiki/Constitution.mediawiki`](BITwiki/Constitution.mediawiki) |
| Ontology / Epistemology / Axiology | [`BITwiki/Foundational triad.mediawiki`](BITwiki/Foundational%20triad.mediawiki) |
| How pages are composed | [`BITwiki/Book Matter.mediawiki`](BITwiki/Book%20Matter.mediawiki) |
| Default V2 page format | [`BITwiki/Page format.mediawiki`](BITwiki/Page%20format.mediawiki) |
| How knowledge becomes canon | [`BITwiki/Knowledge lifecycle.mediawiki`](BITwiki/Knowledge%20lifecycle.mediawiki) |
| How the wiki is organized | [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki) |
| Evidence / confidence / uncertainty | [`BITwiki/Epistemics.mediawiki`](BITwiki/Epistemics.mediawiki) |
| Portals and navigation | [`BITwiki/Navigation.mediawiki`](BITwiki/Navigation.mediawiki) |
| V1 source archive | [`archive-v1/README.md`](archive-v1/README.md) |

---

## Repository map

```text
wiki-content/
├── Main/          ordinary public knowledge pages
├── BITwiki/       project foundations, architecture, governance, guides
├── Portal/        high-level entry points into knowledge domains
├── Template/      reusable/transcluded wiki components
├── Property/      Semantic MediaWiki properties
└── archive-v1/    read-only V1 source/reference archive
```

**MediaWiki namespaces and repository-only archival structure are organization surfaces, not the ontology.**

```text
namespace ≠ entity type ≠ domain ≠ Book Matter ≠ epistemic status ≠ relationship
```

---

## 12 domain exemplars

Each major domain has one small page using the same V2 anatomy. These are reference implementations, not privileged topics.

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

---

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

A mature page can expand into the richer Book Matter vocabulary: history, frameworks, methods, evidence, case studies, controversies, timelines, primary/secondary sources, bibliography, knowledge maps, implementation, limitations, and related concepts.

**Modularity does not mean fragmentation.** Keep the parent page coherent. Split/transclude matter only when the portion is independently useful.

---

## V1 is preserved, not guessed away

`archive-v1/` is the repository-only source archive for the public V1 wiki.

- `archive-v1/manifest.json` accounts for every title in the 162-page V1 Main-namespace inventory.
- `archive-v1/raw-snapshots-1.md` and `raw-snapshots-2.md` preserve exact public wikitext already recovered.
- An item marked `reference-only` is known to exist but still needs a raw source/history snapshot.
- V2 pages may cite the archive while being edited.
- **Never merge, redirect, or delete a V1 page merely because two titles look similar. Recover and compare the source first.**

The live wiki and revision history remain the highest authority for inherited V1 text.

---

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

A cleaner sentence is not automatically a better sentence. Preserve authored voice, unique distinctions, citations, provenance, and meaningful historical development.

---

## Public boundary

This repository contains public material only. Private memory, credentials, access-control internals, private identity data, and unpublished sensitive operational material do not belong here.
