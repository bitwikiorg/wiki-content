# `Main/` — public knowledge namespace

This directory is **not a curated article list**. It is the repository transport mirror of MediaWiki's main namespace.

If you are trying to understand BITwiki, do **not** browse this folder alphabetically first.

Start with:

- [`Main Page.mediawiki`](Main%20Page.mediawiki)
- [`../Portal/`](../Portal/) for subject navigation
- [`../BITwiki/Navigation.mediawiki`](../BITwiki/Navigation.mediawiki) for the navigation model
- [`../BITwiki/Organization.mediawiki`](../BITwiki/Organization.mediawiki) for the system architecture

## What is in this directory?

`Main/` currently mixes several **different transport roles** that MediaWiki needs in the same namespace:

| Role | Meaning |
|---|---|
| canonical knowledge object | actual subject knowledge intended for reading/research |
| domain exemplar | a substantive V2 page used to prove each controlled Domain works end-to-end |
| V1 compatibility redirect | tiny file preserving an old public title while sending readers to the mature canonical V2 page |
| Book Matter / subpage | reusable or compositional subject material where independent retrieval/reuse is justified |
| Main Page | the public landing page |
| review candidate | non-redirect content that still needs human evaluation/canonicalization |

### Important: tiny files are often redirects, not stubs

For example, files such as `BITCORE Manifesto.mediawiki` exist only to preserve old public titles:

```mediawiki
#REDIRECT [[BITwiki:BITCORE Manifesto]]
```

The substantive page lives in the `BITwiki:` namespace. Do not evaluate a compatibility redirect as if it were an unfinished article.

## Current substantive exemplars

The V2 domain exemplars are intentionally compact but real sourced knowledge pages. Examples include:

- [`System boundary.mediawiki`](System%20boundary.mediawiki)
- [`Hypothesis.mediawiki`](Hypothesis.mediawiki)
- [`Cell membrane.mediawiki`](Cell%20membrane.mediawiki)
- [`Prime number.mediawiki`](Prime%20number.mediawiki)
- [`Causality.mediawiki`](Causality.mediawiki)
- [`Version control.mediawiki`](Version%20control.mediawiki)
- [`Resistor.mediawiki`](Resistor.mediawiki)
- [`Energy efficiency.mediawiki`](Energy%20efficiency.mediawiki)
- [`Safety factor.mediawiki`](Safety%20factor.mediawiki)
- [`pH.mediawiki`](pH.mediawiki)
- [`Momentum.mediawiki`](Momentum.mediawiki)
- [`Pulse.mediawiki`](Pulse.mediawiki)

The Computer science expansion adds a thirteenth substantive exemplar once that Domain is accepted by validation.

## Do not create empty/generic article shells

A missing topic should not automatically become a low-information file just so the title exists.

Prefer one of these instead:

1. add it to a requested-knowledge / coverage queue;
2. research and create a minimum coherent sourced page;
3. add it to a portal/category/outline as a planned gap;
4. preserve a redirect when the knowledge already has a better canonical home.

A canonical subject page should have enough signal to answer at least:

- What is it?
- Why does it matter?
- What are its core mechanisms/concepts?
- What are representative examples or applications?
- What is uncertain or context-dependent?
- Where did the information come from?

See [`../BITwiki/Page format.mediawiki`](../BITwiki/Page%20format.mediawiki) and [`../BITwiki/Readable depth and localization.mediawiki`](../BITwiki/Readable%20depth%20and%20localization.mediawiki).

## Machine audit

Run:

```bash
python scripts/audit_mainspace.py
```

It generates `v2-mainspace-audit.json`, separating redirects, domain exemplars, knowledge objects, subpages, other content, and very-short non-redirect review candidates.

**Length is not quality.** The audit uses size only as a review signal; it does not label short pages as bad automatically.

## Design invariant

```text
filesystem path
≠ article quality
≠ entity type
≠ domain
≠ navigation hierarchy
≠ epistemic standing
```

`Main/` is where MediaWiki main-namespace files travel through Git. The actual reading experience should be driven by portals, contents, categories, outlines, links, semantic queries, and search.
