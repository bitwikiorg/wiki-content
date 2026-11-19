# BITwiki deployment and recovery runbook

**Repository-maintainer instructions, not deployable MediaWiki content.** Public wiki architecture belongs in `BITwiki/`; executable deployment policy and operational checklists belong alongside the tooling. This GitHub repository is public: never commit secrets.

## Authority and preflight

- Reconcile target wiki `Special:NamespaceInfo`, `Special:Version`, installed extensions, site state, and `archive-v1/siteinfo.json` before acting. A repository folder is a title projection, not a configured MediaWiki namespace.
- `manifest.json` owns mapped source folders; `scripts/deployment_plan.py` recursively discovers deployable files, titles, models, dependency order and explicitly declared checkpoints.
- `archive-v1/` is read-only historical provenance. Do not turn missing source files into delete operations on the live wiki.
- Source CI, generated reports, dry runs and staging previews do **not** establish a deployed or approved MediaWiki revision.

## Verify source before publication

```bash
python scripts/validate_v2.py
python scripts/test_editorial_architecture.py
python scripts/audit_runtime_schema.py
python scripts/audit_substrate.py
python scripts/audit_workflow.py
python scripts/audit_mainspace.py
python scripts/deployment_plan.py --check
python -m py_compile scripts/deployment_plan.py scripts/deploy_mediawiki.py
python scripts/deploy_mediawiki.py
```

The last command is a **dry run**. Live writes require `--execute` and separately supplied `BITWIKI_BOT_USER` / `BITWIKI_BOT_PASSWORD`. An existing page with different source must be explicitly reviewed before `--overwrite-existing` is allowed; content-model mismatches are refused. New-page writes use create-only semantics, and existing-page edits use the checked base revision to detect concurrent changes.

## Dependency and checkpoint rules

1. Verify installed runtime support: MediaWiki, Semantic MediaWiki, Scribunto and relevant parser extensions. Do not presume native `mw.smw` without a compatible SemanticScribunto deployment.
2. Deploy schema/Property dependencies before consumers. For the compiler: `Module:BITwiki/Data/Schema` → `Module:BITwiki/Core` → `Module:BITwiki/Compiler` → `Module:Structure` → `Template:Knowledge object` → articles.
3. Check nested module paths and Lua 5.1 compatibility. Validate a correct and an intentionally invalid `Template:Knowledge object` invocation in an isolated target before broad publication.
4. `scripts/deployment_plan.py` retains support for explicitly configured runtime checkpoints. **No Cargo `Knowledge_requests` checkpoint or public research-queue producer/consumer remains in the current source plan.** Do not re-create that table or deploy the former queue solely because an old runbook described it.
5. When adopting any new Cargo use case, explicitly declare its schema, create/recreate and verify the target table, and register a checkpoint when the producer/consumer dependency warrants one. Cargo remains an optional capability; it is not automatically BITwiki's operational source of truth.
6. Scribunto performs bounded parser-time computation. Cross-service BIThub/agent writes require separately authenticated and permission-bounded integration, attribution, provenance, failure handling and review.

## Publication, verification and recovery

- Treat deployments as **additive and non-destructive by default**. Explicitly review every rename, merge, redirect, overwrite or live deletion against current target revisions and incoming links.
- After import inspect rendering, actual revision IDs, `Special:AllPages`, categories, wanted templates, redirects and transclusion host pages. For semantic edits inspect `Special:Browse`, `Special:Ask`, properties/concepts and rebuilds as applicable.
- Preserve live V1 template callers (including `Template:Infobox`) and source lineage until each migration is checked. Do not infer safe deletions from missing V2 files.
- Record reviewed source SHA, deployment plan, credentials authority (not secrets), affected titles, operator, checkpoint evidence, pre/post revision IDs and a tested rollback/restore path.
- Run source checks and compare target state again after the change. A green GitHub Action does not prove the target wiki changed.

## Public/private separation

The former public `BITwiki:Requested knowledge`, `BITwiki:Computational scope` and `BITwiki:Deployment prerequisites` pages are no longer staged as deployable namespace source. Coverage records are retained in `ops/knowledge-requests.json`, **publicly visible in this GitHub repository but not published as wiki pages**. A truly private internal operations service requires a separately authorized migration and access controls.

Removing files from this repository's deployable tree does **not** remove pages or Cargo tables already present on `bitwiki.org`. Any live retirement or privacy remediation needs a separate authorized maintenance action.
