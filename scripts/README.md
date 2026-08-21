# Repository scripts

Audit, archival, inventory, classification, fidelity, migration, and V2 validation utilities.

These scripts are **executable governance over repository source**: they make architecture claims falsifiable, detect drift between representations, and generate review evidence. They are tooling, not wiki content and not a parallel semantic authority.

## Current validation layers

| Script | Contract |
|---|---|
| `validate_v2.py` | deployable structure, references, knowledge-object identity, controlled vocabularies, Domain coverage |
| `audit_runtime_schema.py` | canonical `bitwiki-runtime-schema.json` ↔ Scribunto `Module:BITwiki/Data/Schema` projection agreement |
| `audit_substrate.py` | MediaWiki/SMW/Lua/Cargo substrate usage and source/runtime mappings |
| `audit_workflow.py` | Cargo `Knowledge_requests` schema/storage/query and request lifecycle invariants |
| `audit_mainspace.py` | Main-namespace role inventory without equating file length with quality |
| `inventory_corpus.py` | V2 corpus and V1 classification inventories |
| `classify_v1_page_roles.py` | V1 page-role evidence before migration/ontology decisions |
| `classify_v1_architecture_families.py` | V1 architecture-source maturation classification |

GitHub Actions also parses every source-controlled `Module/**/*.lua` with a Lua 5.1 compiler before accepting the module source as syntactically valid Scribunto-era Lua.

## Schema authority

The Python validator now reads `bitwiki-runtime-schema.json` directly instead of maintaining its own copy of compiler-facing controlled vocabulary.

```text
bitwiki-runtime-schema.json
        ├── scripts/validate_v2.py consumes directly
        └── Module:BITwiki/Data/Schema projects for Scribunto
                         ↓
              audit_runtime_schema.py
                 verifies agreement
```

This is the preferred pattern: validation should consume canonical repository state where possible and audit only the representations that must exist separately for runtime reasons.

## Evidence policy

Generated `v2-*.json` reports are **run evidence**, not canonical mutable source. CI uploads them as workflow artifacts; they remain ignored by Git.

```text
reviewed source + validators
        ↓
CI execution
        ↓
run-specific evidence
```

A clean repository audit still does not prove the remote MediaWiki instance has the expected namespaces, extension versions, Cargo tables, Scribunto behavior, or BIThub integration. Deployment validation remains a separate runtime responsibility.

## Design rules

- Reflect actual MediaWiki/SMW/Cargo/Scribunto semantics rather than inventing a parallel schema in Python.
- Prefer invariant checks over brittle snapshots of incidental counts.
- Keep historical classifiers/audits distinguishable from current-state validators.
- Do not let automation rewrite canonical content merely to make its own report green.
- When an architecture invariant becomes machine-checkable, add/update the validator and describe the contract in the nearest README plus relevant `BITwiki:*` standard.

See `README.md`, `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Deployment prerequisites.mediawiki`, and `.github/workflows/`.
