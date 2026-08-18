# BITwiki V2 — Canon Map

This file is the navigation substrate for the public BITwiki corpus. It is not a conventional repository README.

BITwiki is the durable MediaWiki / Semantic MediaWiki knowledge layer of the wider BITwiki–BIThub–BITCORE ecosystem. This repository mirrors public wiki source in a form that can be reviewed, versioned, transcluded, and deployed.

## Read the corpus in this order

### 1. Foundations — why the system exists

- [`BITwiki/Manifesto.mediawiki`](BITwiki/Manifesto.mediawiki)
- [`BITwiki/Charter.mediawiki`](BITwiki/Charter.mediawiki)
- [`BITwiki/Constitution.mediawiki`](BITwiki/Constitution.mediawiki)
- [`BITwiki/Foundational triad.mediawiki`](BITwiki/Foundational%20triad.mediawiki)

These are authored foundations. They are not generic documentation. Their wording is preserved from the strongest recoverable public/historical formulations, with source lineage stated on-page.

### 2. Knowledge architecture — what a BITwiki page is made of

- [`BITwiki/Book Matter.mediawiki`](BITwiki/Book%20Matter.mediawiki)
- [`BITwiki/Organization.mediawiki`](BITwiki/Organization.mediawiki)
- [`BITwiki/Epistemics.mediawiki`](BITwiki/Epistemics.mediawiki)
- [`BITwiki/Navigation.mediawiki`](BITwiki/Navigation.mediawiki)

### 3. Knowledge process — how signal becomes durable memory

- [`BITwiki/Knowledge lifecycle.mediawiki`](BITwiki/Knowledge%20lifecycle.mediawiki)
- [`BITwiki/Ecosystem.mediawiki`](BITwiki/Ecosystem.mediawiki)

### 4. Public reading surface

- [`Main/Main Page.mediawiki`](Main/Main%20Page.mediawiki)
- [`Portal/Systems science.mediawiki`](Portal/Systems%20science.mediawiki)
- `Portal/` — major knowledge entry points

### 5. Provenance and migration

- [`BITwiki/Source lineage.mediawiki`](BITwiki/Source%20lineage.mediawiki)
- [`BITwiki/V1 public corpus inventory.mediawiki`](BITwiki/V1%20public%20corpus%20inventory.mediawiki)

The inventory preserves visible V1 titles without pretending that unrecovered bodies have already been merged or redirected correctly.

---

## Repository path → MediaWiki title

| Repository path | MediaWiki title | Role |
|---|---|---|
| `Main/Foo.mediawiki` | `Foo` | ordinary knowledge object |
| `Main/Foo/Overview.mediawiki` | `Foo/Overview` | independently addressable Book Matter when justified |
| `BITwiki/Foo.mediawiki` | `BITwiki:Foo` | public project/meta/foundational documentation |
| `Portal/Foo.mediawiki` | `Portal:Foo` | reader-facing knowledge entry point |
| `Template/Foo.mediawiki` | `Template:Foo` | reusable/transcluded wiki component |
| `Property/Foo.mediawiki` | `Property:Foo` | Semantic MediaWiki property |
| `Category/Foo.mediawiki` | `Category:Foo` | human-readable classification/navigation |

**The repository directories mirror MediaWiki namespaces. They are transport structure, not the ontology.**

## Core distinction

```text
Namespace ≠ entity type ≠ domain ≠ Book Matter ≠ epistemic status ≠ relationship
```

A page can simultaneously have a MediaWiki identity, an entity type, one or more knowledge domains, semantic relationships, reusable Book Matter, and sources/evidence/provenance.

Do not collapse those dimensions into one category tree.

## Book Matter

BITwiki was designed around *fluid modularized content*. A coherent page may expose useful semantic parts—overview, concepts, frameworks, applications, timelines, references, and other matter—so humans and agents can retrieve or transclude exactly the required depth.

Progressive disclosure is intentional:

```text
orientation
→ intermediate structure
→ advanced depth
→ source / evidence layer
```

Transclusion is an implementation of modularity, not permission to fragment every paragraph into a page.

## Canon rule

```text
source
→ preserve exact signal
→ compare revisions
→ research and cross-check
→ distill redundancy
→ revise
→ verify
→ canonicalize
→ transclude / relate
→ publish
```

A cleaner sentence is not automatically a better sentence. Authored voice, unique distinctions, historical development, citations, and provenance are part of the knowledge.

## Source authority

For inherited public BITwiki material:

1. live `bitwiki.org` page + revision history;
2. current first-party public BIThub / GitHub material;
3. older public writings and captured historical versions;
4. historical design material used as provenance, not as automatic current state.

If a V1 title is known but its complete body has not been recovered, it remains **unreconciled** in the inventory. It must not be silently rewritten, merged, or redirected.

## Public boundary

Only public material belongs here. Private memory, credentials, access-control internals, private identity data, non-public operations, and unpublished sensitive material stay outside the repository.
