# V1 system architecture and deployment reconciliation

Issue #152 reconciliation for:
- 4 `system_architecture_boundary` sources;
- 5 `deployment_integration_migration_operations` sources.

Current comparison targets include `BITwiki:Organization`, `BITwiki:Ecosystem`, `BITwiki:MediaWiki substrate`, `BITwiki:Programmable knowledge substrate`, `BITwiki:Interoperability`, `BITwiki:Lua architecture`, `BITwiki:Contributing`, and `docs/deployment.md`.

## Reconciled sources

| V1 source | Disposition | Durable substance / explicit non-adoption |
|---|---|---|
| BITwiki Architecture Overview | superseded | Current MediaWiki substrate/Organization preserve MediaWiki + SMW + templates/modules, source/runtime separation, validation and performance concerns. Historical version numbers, Redis/Varnish/Cloudflare/MySQL layouts, OAuth, custom BITwiki extensions, permission groups and scaling/monitoring claims were design examples or unsupported deployment assertions, not current facts. |
| BITwiki BITHUB Boundary Specification | superseded | Current Ecosystem/Organization preserve the durable three-plane separation: BITwiki canonical durable knowledge, BIThub interaction/workflow, BITCORE cognition/orchestration; cross-system writes require explicit authenticated integration. Historical A2A, filesystem/memory protocols, fixed agent capability matrices and forbidden-crossing rules are not current verified contracts. |
| System Architecture | superseded | Current Ecosystem preserves the useful BIThub/BITwiki/BITCORE architecture and durable-publication loop. Historical claims that n8n, GitHub canonical specifications, PM-agent routes or specific automated refinement pipelines constitute deployed architecture are not assumed. |
| Wiki Organization Guidelines | incorporated | The durable goal—organized semantic knowledge with explicit relationships, reusable composition and navigable views—is directly represented in current Organization, Ontology, Navigation, Book Matter and Transclusion standards. |
| BITwiki Deployment Guide | superseded | Current repository deployment tooling and `docs/deployment.md` replace the historical guide with source-derived dependency planning, dry-run-by-default writes, revision-race checks, explicit checkpoints and runtime verification. Historical fixed versions, commands, old templates, cache configuration and production assumptions are not authoritative. |
| BITwiki Integration Guide | superseded | Current Interoperability/Ecosystem preserve API/integration principles, authentication boundaries, provenance, mapping semantics, retries/failure handling and canonical-authority rules. Historical OAuth server, API-key tiers, webhooks, RDF endpoints, rate limits and integration SDK examples are not claimed deployed. |
| BITwiki Performance Budgets | superseded | Current Lua architecture/MediaWiki substrate preserve parser-limit inspection, shallow composition, query reuse, cache-aware design and explicit traversal limits. Historical “recommended” numeric budgets and assumed cache/query infrastructure are not current limits without runtime measurement. |
| BITwiki User Guide | superseded | Current Contributing, Page format, Help surfaces, Semantic properties and Epistemic standards replace the old guide. YAML-frontmatter requirements, numeric confidence scores, old templates/statuses and assumed open editing workflows are not current rules. |
| Content Migration Guide | incorporated | Its durable requirements—license compatibility, attribution/provenance, source assessment, careful transformation and post-migration validation—are now explicitly incorporated into `BITwiki:Contributing`. Historical mechanical category/template conversion, automatic epistemic mapping and unverified migration scripts are not adopted. |

## New incorporation from this audit

`BITwiki:Contributing` now has an explicit **Importing or adapting external material** section requiring:

- license/copyright/reuse verification before import;
- attribution and transformation provenance;
- independent factual/citation revalidation;
- deliberate rather than mechanical schema/template/category conversion;
- post-transformation validation;
- small representative tests before bulk migration.

## Result

All 9 V1 system-boundary/deployment/integration sources are content-reconciled for issue #152.

This closes only these two architecture families. It does not close issue #152 or authorize archive retirement.
