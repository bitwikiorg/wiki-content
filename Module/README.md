# Module namespace

Source for MediaWiki `Module:*` pages executed by Scribunto/Lua.

The captured live V1 corpus had the Module namespace configured but **zero live Module pages**. V1 nevertheless contains substantial Lua design specifications under `archive-v1/pages/Main/`. Those documents are design lineage, not proof that the proposed modules were deployed.

## V2 role

Lua is BITwiki's deterministic compiler/type-system/inference-and-projection layer inside MediaWiki.

- Wikitext/templates remain authoring and public invocation syntax.
- Semantic MediaWiki remains the durable page/property/relationship graph.
- Cargo remains structured repeated operational state.
- Lua normalizes, type-checks, applies bounded explicit rules, transforms state into reusable view models, renders semantic interfaces, and emits diagnostics.
- MediaWiki remains the parser, revision, permission, cache, API, and execution substrate.
- BIThub/Discourse remains the interactive conversation/workflow plane and connects through explicit integration APIs/plugins/services/agents rather than through Scribunto network access.

See `BITwiki:Programmable knowledge substrate` and `BITwiki:Lua architecture`.

## V2 policy

- Use Lua for non-trivial reusable logic, validation, normalization, bounded inference, computation, or semantic presentation.
- Prefer structured internal results/view models over mixing state access, inference, and HTML in one function.
- Keep declarative presentation/semantic emission in templates when wikitext remains clearer.
- Keep persistent knowledge in pages/SMW/Cargo; do not create a second hidden state system inside modules.
- Do not turn parse-time rendering into surprising writes merely because an extension exposes storage functions to Lua.
- Keep inference rules explicit and distinguish stored assertions from derived display/diagnostics.
- Do not resurrect V1 numeric-confidence logic; V2 uses the current epistemic-status model.
- A module should have a real consumer or remove demonstrated duplicated logic rather than existing as an architectural ornament.

## Module family

BITwiki-owned runtime logic should live under `Module:BITwiki/*` as the family grows.

Current foundation:

- `Module:BITwiki/Core` — common pure utilities.
- `Module:BITwiki/Data/Schema` — immutable runtime schema projection loaded through `mw.loadData()`.
- `Module:BITwiki/Compiler` — normalization/type-checking and diagnostics for knowledge-object inputs.
- `Module:Structure` — public compatibility/runtime wrapper consumed by `Template:Knowledge object`; now delegates to the compiler family.

`bitwiki-runtime-schema.json` is the reviewed repository authority for compiler-facing controlled vocabularies. `scripts/audit_runtime_schema.py` prevents the Lua projection and repository validation layer from silently drifting from that authority.

## Runtime boundaries

Scribunto is sandboxed and resource-bounded. Modules must not be designed as filesystem workers, arbitrary network clients, secret stores, long-running daemons, background schedulers, or autonomous AI runtimes. Those responsibilities belong to explicit MediaWiki/Discourse extensions, backend integrations, APIs, or BITCORE/agent workflows.

MediaWiki's canonical runtime title for `Structure.lua` is `Module:Structure`; nested repository paths under `Module/` map to corresponding Module subpage titles.
