# V1 governance, quality, and validation-receipt reconciliation

Issue #152 reconciliation for:
- 6 `quality_governance_stewardship` sources;
- 6 `maintenance_validation_test` sources.

Current comparison targets include `BITwiki:Constitution`, `BITwiki:Editorial protocol`, `BITwiki:Epistemic audit`, `BITwiki:Page format`, `BITwiki:Templates and categories`, `BITwiki:Lua architecture`, `BITwiki:Semantic properties`, and the current repository validators/tests.

## Reconciled sources

| V1 source | Disposition | Durable substance / explicit non-adoption |
|---|---|---|
| BITwiki Governance Framework | deprecated | Transparent, attributable, reviewable decisions and revisable governance survive in the Constitution/Editorial protocol. Distributed consensus, weighted convergence, fixed steward councils, voting thresholds, reputation weights, quarterly governance metrics and a claim that no entity has veto power are not current governance. |
| BITwiki Quality Bar | superseded | The durable “guardrails rather than opaque scores” idea survives in Epistemic audit, Page format and current validators. Mandatory epistemic status on every claim, Axiomatic/Verified tiers, fixed workflow stages and blanket rejection for missing metadata are not current rules. |
| BITwiki Quality Standards | superseded | Multi-dimensional review—evidence, structure, clarity, semantic correctness and maintenance—is current. Historical weighted quality scores, Flesch targets, YAML requirements, source-count minima, universal template requirements and automatic confidence thresholds are not current standards. |
| BITwiki Steward Handbook | superseded | Current Constitution preserves accountable stewardship and current Editorial protocol requires attributable/reviewable/reversible decisions. The historical four steward classes, appointment process, indefinite terms, fixed escalation ladder and authority to numerically adjust confidence are not constituted current offices/processes. |
| Governance Integration Coraline | deprecated | Provenance-tracked decisions, uncertainty transparency and governance revisability survive. Weighted steward reputation, confidence-weighted governance, meta-stewards, fixed review metrics and “distributed intelligence arbitration” are not adopted current mechanisms. |
| Quality Validation Framework | deprecated | Layered source/runtime/editorial auditing survives in current validation and Epistemic audit. Universal automated quality scoring, community confidence voting, fixed reviewer panels, quality classes and numeric dashboards are not current epistemic or governance authority. |
| PHASE3 DEPLOYMENT AUDIT | historical-only | This is a dated readiness receipt over a 2026-02 source state. Its “ready for full production deployment” conclusion cannot establish current deployment. Current deployment requires current source planning plus observed runtime verification. |
| Template Improvement Recommendations | incorporated | The durable recommendations—centralize reusable validation in Lua, prevent invalid semantic emission, centralize controlled vocabulary, avoid duplicated template logic, test missing/invalid inputs, and regression-test changes—are reflected in the current BITwiki Lua compiler/runtime schema and validation suite. Historical field vocabularies and proposed module names are obsolete. |
| Template Validation Implementation | superseded | The historical ParserFunction/TemplateStyles implementation targeted obsolete infoboxes, required numeric confidence, and old status vocabularies. Current compiler/schema architecture preserves validation-before-emission and visible diagnostics without those assumptions. |
| Template Validation Lua Module | superseded | The proposed ValidatorBase/EpistemicValidator/InfoboxValidator architecture matured into `Module:BITwiki/Core`, `Module:BITwiki/Compiler`, `Module:Structure`, and the runtime-schema projection. Old required confidence/source-count fields and old vocabularies are not retained. |
| Template Validation Report | historical-only | This is an audit of the old template implementation. Its valuable findings—duplicated logic, weak validation, invalid property emission risk, uncontrolled vocabularies, need for shared Lua logic and tests—are represented in current Lua/template architecture. The old per-template scores and implementation state are historical only. |
| Test Page | historical-only | A one-line pywikibot test artifact contains no durable knowledge or design requirement. |

## Durable V1 signal confirmed in current canon

- quality checks should expose specific failure modes rather than collapse quality into one score;
- provenance, uncertainty and review decisions must remain inspectable;
- editorial/governance decisions should be attributable, reviewable and reversible;
- automation can enforce source/schema contracts but cannot certify factual truth;
- semantic assertions should not be emitted from invalid inputs;
- shared validation logic belongs in reusable tested code rather than copied parser-function branches;
- controlled vocabularies require one authority and drift checks;
- repository validation, staging and live runtime verification establish different facts;
- deployment/readiness claims are version- and environment-specific.

## Explicitly deprecated/superseded mechanisms

- distributed-consensus governance as current BITwiki authority;
- weighted steward reputation/voting and fixed steward councils;
- universal numeric epistemic/quality/confidence scores;
- fixed source-count thresholds and quality classes;
- mandatory metadata on every claim/page regardless of context;
- historical five-tier/Axiomatic/Verified vocabularies;
- old YAML-frontmatter/template contracts;
- old infobox validator module names/interfaces;
- a dated audit authorizing current production deployment.

## Result

All 12 V1 governance/quality/maintenance-test sources are content-reconciled for issue #152.

This does not close issue #152 or authorize archive retirement.
