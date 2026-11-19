# Deployment documentation (repository-only)

This directory contains **non-deployable maintainer runbooks**, not MediaWiki content. Public wiki pages document the intellectual architecture and editorial norms; the repository tooling and this runbook document execution details.

- [Deployment and recovery](deployment.md) — source preflight, dry-run/execute safeguards, module and semantic dependency ordering, rollback and post-import verification.

The GitHub repository is **public**. Do not place credentials, private request payloads, privileged access tokens or confidential operational state here. Removing an article from the deployable `BITwiki/` tree does not delete any existing page on the live wiki.
