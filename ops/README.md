# BITwiki operational records (not MediaWiki content)

This directory is **outside** every `manifest.json` MediaWiki source mapping. Files here must never be treated as `BITwiki:`, `Main:`, `Template:` or other publishable wiki pages.

- `knowledge-requests.json` preserves 51 structured research/coverage records (32 satisfied, 17 requested, 2 researching) migrated from the former `BITwiki:Requested knowledge` source. It preserves the recorded reasons, sources, statuses and canonical links; it is not a scientific validity audit.
- `scripts/audit_workflow.py` checks source record integrity, controlled domains, and consistency between active requests and canonical Main article filenames.
- No request submission, access control, Cargo table, or autonomous publication backend is implemented by this file.

**Visibility:** This GitHub repository is **public**. Moving a record here removes it from the deployable/public wiki namespace but does **not** make it confidential. If the research queue must become access-controlled, transfer its current records to an authorized **private** system before treating it as private. Do not put credentials or sensitive operational information in this repository.

The historical MediaWiki source remains in Git history for provenance; Git source removal does not delete any already-published MediaWiki revision, template or Cargo table. Live retirement requires a separately authorized, audited migration.

## Historical article production ledgers

- `bitwiki-new-article-execution-queue.json` — original article drafting execution ledger, preserved unchanged from `automation/bitwiki-new-article-queue-v1`.
- `bitwiki-two-depth-review-queue.json` — original two-depth editorial review and integration ledger, preserved unchanged from `automation/bitwiki-two-depth-review-v1`.

These are historical operational records, not instructions to restart an automation. Their recorded branch names, statuses and checkpoints are retained as provenance. They are outside the wiki deployment mappings. The original Git branch histories are retained by the consolidation merge.
