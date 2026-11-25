# V1 archive retirement dependency audit

Issue #152 retirement preflight after completion of the content-level reconciliation.

## Result

**No current BITwiki runtime, deployment, current-corpus validation, workflow, Main-space audit, staging audit, or staging compiler requires `archive-v1/`.**

The working-tree archive is still consumed by the **historical migration-classification chain** and referenced by migration/provenance documentation. Those dependencies are intentional while the archive is retained; they must be removed or retargeted in the separate retirement change.

## Executable dependency classification

### Migration-only consumers

| Surface | Dependency | Retirement action |
|---|---|---|
| `scripts/inventory_corpus.py` | Reads `archive-v1/index.json` and `archive-v1/pages/Main/` to regenerate V1 classification evidence alongside the V2 corpus inventory. | Return the script to current-V2-only inventory behavior after retirement; the final reconciliation ledger/reports become the durable V1 disposition evidence. |
| `scripts/classify_v1_page_roles.py` | Consumes generated `v1-classification-usage.json`. | Retire with the migration analysis after final archive removal. |
| `scripts/classify_v1_architecture_families.py` | Consumes generated `v1-page-role-matrix.json`. | Retire with the migration analysis after final archive removal. |
| `.github/workflows/validate-v2.yml` | Watches `archive-v1/**`, runs both V1 classifiers, uploads three V1 generated matrices. | Remove V1 path trigger/classifier steps/artifacts while retaining all current V2 checks. |
| `.github/workflows/validate-v2-pr.yml` | Same migration-evidence checks on PRs. | Remove the V1-only steps/artifacts while retaining current V2/article/staging tests. |

These consumers exist to verify the historical migration source. They are not runtime or deployment dependencies.

### Verified independent current mechanisms

Direct source inspection found no `archive-v1` / V1-classifier dependency in:

- `scripts/validate_v2.py`;
- `scripts/audit_runtime_schema.py`;
- `scripts/deployment_plan.py`;
- `scripts/deploy_mediawiki.py`;
- `scripts/audit_workflow.py`;
- `scripts/audit_mainspace.py`;
- `scripts/audit_staging_readiness.py`;
- `staging/compiler/build.py`;
- `scripts/test_editorial_architecture.py`;
- `scripts/test_semantic_entry.lua`.

`scripts/audit_substrate.py` contains only a comment explaining why `archive-v1` is outside its current-source directory-documentation scope. It does not read the archive. Current runtime authority is the live MediaWiki plus current source, not the historical V1 siteinfo snapshot.

## Documentation/provenance references

Current documentation intentionally points to `archive-v1/` while it remains the active migration source. At final retirement these should be converted where necessary to:

- the immutable V1 snapshot commit `3100db1d7807b752e41b6ccf7f88498982cfb2d4`;
- `docs/v1-reconciliation-ledger.json`;
- the family reports under `docs/v1-reconciliation-*.md`;
- the preserved deleted-content limitation records.

Historical links already pinned to the immutable snapshot can remain unchanged.

## Evidence that must remain after retirement

Do not delete with the archive:

- `docs/v1-reconciliation-ledger.json`;
- all `docs/v1-reconciliation-*.md` family reports;
- `v1-deleted-content-audit.json`;
- `v1-deleted-unresolved.json`;
- issue/PR history documenting the premature PR #155 retirement and corrected PR #156 reconciliation;
- current canonical pages containing recovered material.

The two unavailable historical file binaries remain an explicit known limitation, as do deleted pre-snapshot revision bodies that anonymous access could not recover.

## Live-wiki boundary

Removing `archive-v1/` from the repository in a future retirement PR does **not** itself delete, undeploy, or alter MediaWiki pages on `bitwiki.org`.

Any live-wiki retirement or deletion remains a separate authorized maintenance action.

## Retirement readiness

The **content-recovery gate is satisfied**: 162 / 162 V1 Main sources have an evidenced final disposition and 0 remain open.

The **technical dependency gate is understood and removable**: only migration-only tooling/CI and documentation still depend on the working-tree archive.

Archive deletion is therefore technically feasible as a separate change, but remains unexecuted until the owner accepts the final retirement operation.
