# BITwiki staging workbench

This directory contains an **inspectable micro-staging projection for BITwiki/MediaWiki**.

It is a workshop, validator, graph explorer, and promotion preview. It is **not** a replacement wiki, not a second semantic authority, and not the final publication/runtime system.

The governing question is:

> What will this knowledge become if we promote it, what is it connected to, and how do we display it?

## Authority boundary

The existing repository structure remains the deployable MediaWiki source:

```text
Main/
BITwiki/
Template/
Property/
Concept/
Category/
Module/
MediaWiki/
SMWSchema/
manifest.json
bitwiki-runtime-schema.json
```

The staging system reads those surfaces and emits derived artifacts under `build/staging/`. It does not add frontmatter to `.mediawiki` files, write generated JSON beside source pages, or introduce a parallel ontology.

```text
MediaWiki-native source
        ↓ read only
staging/compiler/build.py
        ↓
build/staging/site/
        ↓
GitHub Pages / local static server
```

`build/` is transient generated output and must not become canonical source.

## Derived views

Each staged source object exposes five inspection modes:

- **Read** — approximate human preview using MediaWiki-like visual grammar.
- **Source** — exact repository source, kept first-class and directly inspectable.
- **Structure** — extracted identity, headings, categories, wikilinks, templates, modules, properties, and semantic relations.
- **Graph** — local graph neighborhood with semantic, structural, and runtime layers kept distinct.
- **Promote** — target MediaWiki title/content model, validation state, runtime dependencies, and deployment contract.

The static build also emits:

```text
data/pages.json
data/page/<stable-id>.json
data/ontology.json
data/graph.json
data/search.json
data/build-meta.json
```

These are inspection artifacts, not canonical facts independent of the source that generated them.

## Graph layers

The graph deliberately separates different kinds of connection:

- **semantic** — controlled SMW relationships from `bitwiki-runtime-schema.json`;
- **structural** — ordinary wiki links and category membership;
- **runtime** — template, Lua module, and property dependencies.

Unresolved targets remain visible as unresolved edges rather than silently disappearing.

## Local build

From repository root:

```bash
python staging/compiler/build.py
python -m http.server 8000 --directory build/staging/site
```

Then open `http://localhost:8000/`.

## Promotion safety

The workbench never writes to MediaWiki. Actual promotion remains governed by the existing deployment contract and tooling, including `scripts/deployment_plan.py` and `scripts/deploy_mediawiki.py`.

A successful staging build means only that the repository projection was generated successfully. It does not prove the remote MediaWiki runtime is synchronized or executable.
