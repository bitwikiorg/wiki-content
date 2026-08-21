# `Module:BITwiki/Data/*` — immutable runtime projections

Data-only Scribunto modules loaded with `mw.loadData()`.

These files are **runtime projections of reviewed repository authority**, not an independent ontology, database, or place for executable behavior.

## Current schema projection

```text
bitwiki-runtime-schema.json
        │
        │ canonical repository authority
        ↓
Module:BITwiki/Data/Schema.lua
        │
        │ mw.loadData()
        ↓
Module:BITwiki/Compiler and other runtime consumers
```

Scribunto cannot read arbitrary repository JSON files, so this duplication exists for a concrete runtime reason. `scripts/audit_runtime_schema.py` must detect drift between the JSON authority and the Lua projection.

The Python repository validator consumes `bitwiki-runtime-schema.json` directly; it should not maintain another hand-copied vocabulary.

## What belongs in data modules

Appropriate:

- immutable controlled vocabulary required by runtime behavior;
- deterministic display/rule metadata required by several modules;
- reviewed lookup tables whose source of truth is explicitly documented.

Not appropriate:

- executable functions;
- mutable/persistent state;
- SMW assertions or Cargo records copied into Lua;
- secrets or integration credentials;
- user-specific/private state;
- data added only because a future architecture might need it.

Executable behavior belongs in `Module:BITwiki/*`. Durable semantic state belongs in pages/SMW; operational repeated state belongs in Cargo.

## Schema change procedure

When compiler-facing schema changes:

1. change `bitwiki-runtime-schema.json` first;
2. update the necessary `Module:BITwiki/Data/Schema.lua` projection;
3. update Property/SMW contracts if the semantic assertion model itself changed;
4. update compiler consumers and architecture text where behavior changed;
5. run `scripts/validate_v2.py` and `scripts/audit_runtime_schema.py`.

Do not add fields to the runtime schema merely to mirror the entire ontology. It should contain only data actually needed by deterministic runtime behavior.

See `Module/README.md`, `Module/BITwiki/README.md`, `Property/README.md`, `SMWSchema/README.md`, and `BITwiki/Lua architecture.mediawiki`.
