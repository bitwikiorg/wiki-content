# Repository scripts

Audit, archival, inventory, classification, fidelity, migration, deployment, and V2 validation utilities.

These scripts are **executable governance over repository source**: they make architecture claims falsifiable, detect drift between representations, generate review evidence, and turn reviewed source into an explicit deployment plan. They are tooling, not wiki content and not a parallel semantic authority.

## Current validation and deployment layers

| Script | Contract |
|---|---|
| `validate_v2.py` | deployable structure, references, knowledge-object identity, controlled vocabularies, Domain coverage |
| `audit_runtime_schema.py` | canonical `bitwiki-runtime-schema.json` ↔ Scribunto `Module:BITwiki/Data/Schema` projection agreement |
| `audit_substrate.py` | MediaWiki/SMW/Lua/Cargo substrate usage and source/runtime mappings |
| `deployment_plan.py` | complete recursive deployable-page inventory, MediaWiki titles/content models, dependency ordering, and manual runtime checkpoints derived from `manifest.json` |
| `deploy_mediawiki.py` | non-destructive-by-default MediaWiki API importer over the validated deployment plan |
| `audit_workflow.py` | Cargo `Knowledge_requests` schema/storage/query and request lifecycle invariants |
| `audit_mainspace.py` | Main-namespace role inventory without equating file length with quality |
| `audit_staging_readiness.py` | Per-page, source-SHA-anchored staging checks K01–K18 with explicit editorial and live-runtime unknowns; emits untracked CI artifact |
| `inventory_corpus.py` | semantic/content corpus and V1 classification evidence; **not** the deployment manifest |
| `classify_v1_page_roles.py` | V1 page-role evidence before migration/ontology decisions |
| `classify_v1_architecture_families.py` | V1 architecture-source maturation classification |

The V1 inventory/classification chain is now historical migration tooling: content reconciliation is complete, and these scripts remain only while `archive-v1/` is retained pending the separate retirement change. They are not current runtime/deployment authority.

GitHub Actions also parses every source-controlled `Module/**/*.lua` with a Lua 5.1 compiler before accepting the module source as syntactically valid Scribunto-era Lua.

## Deployment contract

`manifest.json` is the source for namespace/title-projection mappings. `deployment_plan.py` recursively discovers every deployable source file under those mappings, including nested Module subpages, derives its MediaWiki title and content model, verifies the required Lua compiler chain is strictly ordered, and exposes runtime checkpoints that cannot be satisfied by page import alone.

```text
manifest.json source_control_mappings
        ↓ recursive discovery
scripts/deployment_plan.py
        ↓ validated ordered plan + checkpoints
v2-deployment-plan.json        CI/run evidence; untracked
        ↓
scripts/deploy_mediawiki.py
        ↓ explicit --execute only
MediaWiki API
```

The currently required compiler path is checked as:

```text
Module:BITwiki/Data/Schema
→ Module:BITwiki/Core
→ Module:BITwiki/Compiler
→ Module:Structure
→ Template:Knowledge object
```

Generate/validate the plan locally with:

```bash
python scripts/deployment_plan.py --check
python scripts/deploy_mediawiki.py
```

The second command is a dry run. Live writes require `--execute` plus `BITWIKI_BOT_USER` and `BITWIKI_BOT_PASSWORD`. Existing differing pages are refused unless `--overwrite-existing` is also supplied. Existing content-model mismatches are always refused instead of being silently converted. New pages use `createonly`; updates use the queried base revision to detect races. This prevents a repository import from silently becoming destructive or overwriting an intervening edit.

### Cargo checkpoint

`Template:Knowledge request` declares/stores the `Knowledge_requests` Cargo table, but saving the template does not itself complete table creation/recreation. The deployment plan therefore places an explicit checkpoint before `BITwiki:Requested knowledge`:

```text
Template:Knowledge request
        ↓
CHECKPOINT cargo:Knowledge_requests
create/recreate + verify Cargo table
        ↓
BITwiki:Requested knowledge
```

A full execution without acknowledgement stops at that boundary. A safe two-stage run is:

```bash
# Stage 1: deploy through the Knowledge request template.
python scripts/deploy_mediawiki.py --execute --max-priority 402

# Then create/recreate and verify Knowledge_requests in MediaWiki/Cargo.

# Stage 2: resume only after that runtime step is actually complete.
python scripts/deploy_mediawiki.py --execute \
  --ack-checkpoint cargo:Knowledge_requests
```

The acknowledgement is deliberately explicit; the repository cannot prove a remote Cargo table was created merely because its template source exists.

`inventory_corpus.py` remains a semantic/content evidence tool. Its counts must not be used as a deployment manifest; runtime surfaces such as Module, MediaWiki and SMW schema are governed by the deployment plan instead.

## Schema authority

The Python validator reads `bitwiki-runtime-schema.json` directly instead of maintaining its own copy of compiler-facing controlled vocabulary.

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

The readiness audit reads the existing GitHub Pages staging projection; it does not inspect publication state, use the separate Library comparator catalogs as article targets, or automatically make editorial judgments. Its coverage and reference counts are triage signals, not quality scores. Run `python staging/compiler/build.py` then `python scripts/audit_staging_readiness.py`.

A clean repository audit still does not prove the remote MediaWiki instance has the expected namespaces, extension versions, Cargo tables, Scribunto behavior, or BIThub integration. Deployment validation remains a separate runtime responsibility.

## Pending semantic validation — not implemented by this extraction

The completed V2 architecture evaluation identified additional tests which should be implemented as adopted vocabulary and runtime features permit:

- semantic relationship target resolution and documented relation meaning;
- canonical redirect and duplicate-target integrity, including retiring historical BITwiki project pages;
- transclusion caller/cycle safety;
- property domain/range checks where domain and range are actually defined;
- graph/query regression against reviewed sample knowledge objects;
- review/lifecycle and research-object schema validation after their semantics are accepted.

These remain distinct from the current source-level validators and from live MediaWiki/Cargo/Lua verification. A passing CI check is not confirmation of deployment or editorial correctness. See <code>BITwiki/Deployment prerequisites.mediawiki</code> and <code>scripts/audit_staging_readiness.py</code>.

## Design rules

- Reflect actual MediaWiki/SMW/Cargo/Scribunto semantics rather than inventing a parallel schema in Python.
- Derive deployable surfaces recursively from `manifest.json`; do not maintain a second partial root list and call it deployable.
- Encode runtime steps that page import cannot satisfy as explicit checkpoints rather than implicit prose.
- Prefer invariant checks over brittle snapshots of incidental counts.
- Keep historical classifiers/audits distinguishable from current-state validators and deployment tooling.
- Do not let automation rewrite canonical content merely to make its own report green.
- When an architecture invariant becomes machine-checkable, add/update the validator and describe the contract in the nearest README plus relevant `BITwiki:*` standard.

See `README.md`, `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Deployment prerequisites.mediawiki`, and `.github/workflows/`.
