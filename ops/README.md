# BITwiki operational records (not MediaWiki content)

This directory is **outside** every `manifest.json` MediaWiki source mapping. Files here must never be treated as `BITwiki:`, `Main:`, `Template:` or other publishable wiki pages.

- `knowledge-requests.json` preserves 51 structured research/coverage records (32 satisfied, 17 requested, 2 researching) migrated from the former `BITwiki:Requested knowledge` source. It preserves the recorded reasons, sources, statuses and canonical links; it is not a scientific validity audit.
- `scripts/audit_workflow.py` checks source record integrity, controlled domains, and consistency between active requests and canonical Main article filenames.
- No request submission, access control, Cargo table, or autonomous publication backend is implemented by this file.

**Visibility:** This GitHub repository is **public**. Moving a record here removes it from the deployable/public wiki namespace but does **not** make it confidential. If the research queue must become access-controlled, transfer its current records to an authorized **private** system before treating it as private. Do not put credentials or sensitive operational information in this repository.

The historical MediaWiki source remains in Git history for provenance; Git source removal does not delete any already-published MediaWiki revision, template or Cargo table. Live retirement requires a separately authorized, audited migration.
