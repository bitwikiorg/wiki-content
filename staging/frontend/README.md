# Staging frontend

This directory contains the static inspection UI for the BITwiki staging workbench.

The frontend deliberately uses the existing MediaWiki/BITwiki navigation model instead of inventing a parallel documentation hierarchy. The repository's `Main Page`, `Portal:*`, `Category:*`, namespace titles, and source templates remain the reader-facing concepts. Staging adds inspection capabilities that are awkward to express in the live MediaWiki runtime: exact source inspection, derived structure, layered local graphs, and promotion previews.

The frontend reads only generated artifacts from `build/staging/site/data/`. It does not write repository source or MediaWiki runtime state.

## Reader navigation

- `/` renders the repository-backed `Main Page`.
- `#/wiki/<MediaWiki title>` is the normal title-oriented route.
- `#/portals` derives a portal index from existing `Portal:*` source pages.
- `#/categories` derives category membership from staged MediaWiki relations.
- `#/all-pages` and namespace filters act as staging equivalents of MediaWiki browse/special-page surfaces.
- `#/random` selects a typed Main-namespace knowledge object.
- `#/graph` is an additional inspection surface, not a replacement for portal/category navigation.

`Template:Domain portal` and `Template:Topic portal` source parameters are interpreted in the staging read view so portal pages remain recognizable as MediaWiki portals while gaining richer staged semantic browsing.

## Inspection modes

Every staged repository-backed title keeps the same five workbench modes:

- Read
- Source
- Structure
- Graph
- Promote

The normal Read surface should stay close to what the MediaWiki title is intended to become. The other four modes expose staging-only information around that title.

`MediaWiki/Common.css` is copied into the generated site at build time so MediaWiki-side styling remains inspectable without duplicating or relocating that source into staging.
