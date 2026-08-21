# Module:BITwiki/*

Reusable Scribunto/Lua runtime for BITwiki's programmable knowledge substrate.

This module family is the deterministic compiler/type/projection layer between authored wikitext plus structured wiki state and rendered or machine-facing views.

## Boundaries

- Wikitext/templates remain the public authoring and invocation syntax.
- Semantic MediaWiki and Cargo remain structured state/data layers.
- Lua normalizes, validates, derives bounded rules, selects presentation, and emits deterministic projections.
- Lua does not become a daemon, network client, autonomous agent runtime, filesystem worker, or independent database.
- BIThub/Discourse and external agents interact with BITwiki through explicit MediaWiki/Discourse integration surfaces; they may consume Lua-produced wiki views but do not turn Scribunto into the transport layer.

## Current runtime modules

- `Module:BITwiki/Core` — shared pure utilities.
- `Module:BITwiki/Compiler` — knowledge-object normalization/type checking and diagnostics.
- `Module:BITwiki/Data/Schema` — immutable runtime projection of `bitwiki-runtime-schema.json`.

`Module:Structure` remains the compatibility/public validation wrapper consumed by `Template:Knowledge object` and delegates to this module family.

See `BITwiki:Programmable knowledge substrate` and `BITwiki:Lua architecture`.
