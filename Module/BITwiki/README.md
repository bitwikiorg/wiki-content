# `Module:BITwiki/*` — BITwiki runtime family

Reusable Scribunto/Lua runtime for BITwiki's programmable knowledge substrate.

This module family is the deterministic compiler/type/projection layer between authored wikitext plus wiki-resident structured state and reusable view models, diagnostics, and rendered interfaces.

## Dataflow

```text
wikitext / Template arguments
          +
SMW / Cargo / MediaWiki-readable state
          ↓
Module:BITwiki/Core
          ↓
normalization utilities / diagnostic primitives
          ↓
Module:BITwiki/Compiler and future focused modules
          ↓
normalized record + diagnostics + bounded derived state
          ↓
public wrapper / Template / page / integration projection
```

The runtime should grow as **small composable modules with demonstrated consumers**, not as a checklist of architecture names.

## Current runtime modules

- `Module:BITwiki/Core` — shared deterministic normalization/diagnostic utilities.
- `Module:BITwiki/Compiler` — knowledge-object normalization, type checking, and structured diagnostics.
- `Module:BITwiki/Data/Schema` — immutable Scribunto projection of `bitwiki-runtime-schema.json`.

`Module:Structure` remains the public compatibility/runtime wrapper consumed by `Template:Knowledge object` and delegates to this family.

## Authority boundaries

- **Wikitext/Templates** own public authoring/invocation.
- **SMW** owns durable semantic properties and relationships.
- **Cargo** owns explicitly modeled repeated operational records.
- **Lua** transforms, validates, derives bounded rules, selects projections, and diagnoses state.
- **MediaWiki** owns parser/revision/cache/API/runtime semantics.
- **BIThub/Discourse** provides interaction/workflow interfaces through authenticated integration infrastructure.

Lua must not become a daemon, general network client, autonomous agent runtime, filesystem worker, secret store, or independent database.

## Interface-neutral outputs

When a result has more than one consumer, modules should prefer a normalized intermediate model before rendering:

```text
canonical wiki state
        ↓
normalized BITwiki model
        ├── MediaWiki rendering
        ├── graph projection
        ├── maintenance/diagnostic view
        └── BIThub/agent-facing integration view
```

This is how multiple interfaces share semantics without duplicating truth.

## Inference discipline

```text
stored assertion
≠ derived display
≠ derived diagnostic
≠ proposed persistent assertion
```

Inference rules must be explicit, deterministic, bounded, and justified for the relationship/data type. Do not silently persist parser-time derivations.

## Runtime schema

`bitwiki-runtime-schema.json` is the reviewed repository authority for compiler-facing controlled vocabulary and deterministic relationship-display metadata. Scribunto cannot read that repository JSON directly, so `Module:BITwiki/Data/Schema` is the required runtime projection loaded by `mw.loadData()`.

`scripts/audit_runtime_schema.py` verifies that projection. `scripts/validate_v2.py` consumes the JSON authority directly.

## Structured-state access

Cargo can be queried natively from Lua with `mw.ext.cargo`. Native structured SMW access via `mw.smw` requires SemanticScribunto and is not assumed until the deployed runtime explicitly provides a compatible version.

Higher-level modules should eventually hide state-access mechanics behind focused adapters instead of leaking query implementation details into every renderer.

## Living contract

When a module changes responsibility, dependency order, schema requirement, state-access assumption, or output contract, update:

1. its implementation;
2. this README or the closest nested README;
3. `Module/README.md` if the family-level model changed;
4. `BITwiki/Lua architecture.mediawiki` / programmable-substrate architecture where semantics changed;
5. executable validation where the invariant can be checked.

See `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Lua architecture.mediawiki`, and `Module/README.md`.
