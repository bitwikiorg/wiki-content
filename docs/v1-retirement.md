# V1 retirement status

**Retirement is not currently authorized or complete.**

PR #155 removed `archive-v1/` prematurely and closed issue #152 before the issue's content-level reconciliation gate was satisfied. Issue #152 has been reopened and the archive is restored as an active migration source.

The immutable V1 snapshot remains commit `3100db1d7807b752e41b6ccf7f88498982cfb2d4`, but immutable recoverability is only provenance. It does not prove that useful V1 knowledge/design was migrated.

Use:

- `docs/v1-reconciliation.md` for the corrected migration standard;
- `docs/v1-reconciliation-ledger.json` for current per-source status;
- `docs/v1-retirement-disposition.json` only as a record of the invalidated PR #155 disposition logic.

Final retirement requires a separate reviewable change after all issue #152 acceptance criteria are actually satisfied.
