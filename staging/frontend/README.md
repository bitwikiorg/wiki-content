# Staging frontend

This directory contains the static inspection UI for the BITwiki staging workbench.

The frontend deliberately starts from MediaWiki/BITwiki visual grammar and adds capabilities that are awkward to express in the live MediaWiki runtime: source inspection, derived structure, layered local graphs, and promotion previews.

The frontend reads only generated artifacts from `build/staging/site/data/`. It does not write repository source or MediaWiki runtime state.

Primary modes:

- Read
- Source
- Structure
- Graph
- Promote

`MediaWiki/Common.css` is copied into the generated site at build time so MediaWiki-side styling remains inspectable without duplicating or relocating that source into staging.
