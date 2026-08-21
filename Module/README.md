# Module namespace

Source for MediaWiki `Module:*` pages executed by Scribunto/Lua.

The captured live V1 corpus had the Module namespace configured but **zero live Module pages**. V1 nevertheless contains substantial Lua design specifications under `archive-v1/pages/Main/`. Those documents are design lineage, not proof that the proposed modules were deployed.

## V2 role

Lua is BITwiki's deterministic **compiler / domain type-system / bounded-inference / transformation / projection / diagnostics layer** inside MediaWiki.

```text
wikitext / Template inputs
          +
SMW semantic state
          +
Cargo operational state
          ↓
Module:BITwiki/*
normalize → type-check → resolve → bounded derive → project → diagnose
          ↓
structured view model / rendered output / maintenance signal
```

- Wikitext/templates remain authoring and public invocation syntax.
- Semantic MediaWiki remains the durable page/property/relationship graph.
- Cargo remains repeated structured operational state.
- Lua computes deterministically over permitted wiki state; it does not own an independent database.
- MediaWiki remains the parser, revision, permission, cache, API, and execution substrate.
- BIThub/Discourse remains the interactive conversation/workflow plane and connects through explicit authenticated APIs/plugins/services/agents rather than Scribunto network access.

## Current dependency chain

```text
bitwiki-runtime-schema.json             repository authority
        ↓
Module:BITwiki/Data/Schema              mw.loadData() runtime projection
        ↓
Module:BITwiki/Core                     shared deterministic utilities
        ↓
Module:BITwiki/Compiler                 normalization/type checking/diagnostics
        ↓
Module:Structure                        public compatibility wrapper
        ↓
Template:Knowledge object               wikitext-facing consumer
```

`Module:Structure` is therefore a public adapter, not the whole runtime architecture.

## Compiler contract

Internal module APIs should prefer structured results over presentation-only strings, conceptually:

```lua
{
  ok = true,
  schema_version = "...",
  record = normalized_state,
  diagnostics = {...},
  derived = {...}
}
```

Presentation adapters can then choose MediaWiki rendering, a graph payload, maintenance output, or a BIThub-facing integration projection without creating multiple semantic models.

## State and inference boundaries

```text
stored assertion
≠ derived display
≠ derived diagnostic
≠ proposed persistent assertion
```

Safe Lua work includes normalization, explicit type contracts, deterministic inverse display labels, bounded structural diagnostics, and reusable view models. Persistent derived facts require an explicit provenance/governance/write path outside incidental rendering.

## Structured-data access

Cargo exposes native Scribunto access through `mw.ext.cargo`; modules may query and normalize Cargo state while Cargo remains its owner.

Native structured SMW access through `mw.smw` is **not assumed** from SMW + Scribunto alone. It requires an explicitly deployed compatible SemanticScribunto capability. Until that is verified, higher-level module design must not depend on `mw.smw` as though it were part of the captured runtime.

## Runtime/security boundaries

Scribunto is sandboxed and resource-bounded. Modules must not be designed as:

- arbitrary filesystem/process workers;
- general outbound HTTP clients;
- secret stores;
- long-running daemons or background schedulers;
- autonomous AI/LLM runtimes;
- a second persistent semantic database.

Those responsibilities belong to explicit MediaWiki/Discourse extensions, backend services, authenticated integration APIs, or BITCORE/agent workflows.

## V2 policy

- Use Lua for non-trivial reusable normalization, validation, bounded inference, computation, semantic presentation, or diagnostics.
- Prefer interface-neutral normalized state when several consumers need the same semantics.
- Keep simple declarative presentation/semantic emission in templates when wikitext remains clearer.
- Do not turn parse-time rendering into surprising writes merely because an extension exposes storage functions.
- Keep graph semantics in Property/SMW state and operational records in Cargo.
- Do not resurrect obsolete V1 numeric-confidence logic; V2 uses the current epistemic-status model.
- A module should have real consumers or remove demonstrated duplication rather than exist as architectural ornament.

## Validation and deployment

Repository CI checks all `Module/**/*.lua` with a Lua 5.1 parser and audits the JSON→Lua schema projection. Deployment must still import module dependencies before consumers and test the actual Scribunto runtime with valid and deliberately invalid invocations.

MediaWiki's canonical runtime title for `Structure.lua` is `Module:Structure`; nested repository paths under `Module/` map to corresponding Module subpage titles.

When module responsibilities, dependency order, schema contracts, or state-access assumptions change, update this README, the affected nested README, and `BITwiki/Lua architecture.mediawiki` together.

See `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Lua architecture.mediawiki`, `BITwiki/MediaWiki substrate.mediawiki`, and `BITwiki/Deployment prerequisites.mediawiki`.
