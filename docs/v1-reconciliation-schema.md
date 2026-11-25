# V1 semantic schema / SMW / query / module reconciliation

Issue #152 family reconciliation for the 13 V1 `semantic_schema_smw_queries_modules` architecture sources.

Current comparison targets include `BITwiki:Entity types`, `BITwiki:Semantic properties`, `BITwiki:Relationships`, `BITwiki:Epistemics`, `BITwiki:Transclusion`, `BITwiki:Lua architecture`, `BITwiki:MediaWiki substrate`, `BITwiki:Interoperability`, and the current runtime schema/modules.

## Reconciled sources

| V1 source | Disposition | Durable substance / explicit non-adoption |
|---|---|---|
| BITwiki Page Types | incorporated | Current Entity types/Organization preserve the central V1 insight that useful types emerge from repeated modeling needs and provide orientation rather than metaphysical confinement. Topic is decomposed into Domain/navigation/Concept; Idea matures broadly into Concept; one primary page identity plus typed relationships replaces uncontrolled multi-type assignment. |
| BITwiki Property Dictionary | superseded | Current Semantic properties preserves explicit purpose, value/target type, examples, validation and evidence-driven property evolution. The historical 30+ property catalog is design evidence, not an implementation backlog. Numeric confidence/quality/evidence-count fields and undeployed relation/property families are not imported automatically. |
| Citation Pattern Integration Guide | deprecated | Durable citation correspondence, source diversity, independence and claim-specific source evaluation are present in Sources/Evidence/Claim validation/Page format. Historical Grokpedia sample statistics, source tiers, citation-density benchmarks and confidence-coded citation templates are not accepted as current standards without reproducible research. |
| Dependency Schema | superseded | Current Relationships includes `Depends on`; Editorial protocol requires dependency/host review for shared material; deployment tooling computes source dependencies. Historical requirements that every template persist dependency metadata or that dependency depth is universally capped at five are not current rules. |
| Epistemic Properties | superseded | Current Epistemics splits source role, evidence, verification, epistemic standing, confidence rationale, provenance and uncertainty rather than collapsing them into confidence/evidence-strength/verification fields. Attribution-traced and source-documented remain provenance conditions, not universal epistemic ranks. |
| Event Types | deprecated | Event remains a valid Entity type, but the EPV-specific Creation/Modification/Relation/Observation taxonomy and associated “Was …” property family are not current schema. Event subtypes/properties should emerge from an actual event corpus and query need. |
| Lua Module Specifications | superseded | The reusable-validation/query-helper instinct matured into the current `Module:BITwiki/*` architecture, runtime schema and compiler. Historical Axiomatic/Developing/Preliminary confidence thresholds, ValidatorBase names and string-built SMW query helpers are obsolete. |
| Property Types | superseded | SMW datatypes and constraints remain real substrate capabilities, and current Property pages declare concrete types where used. A separate V1 property-type ontology, confidence metadata on property definitions and unused specialized types are not current BITwiki schema. |
| Query Patterns | superseded | Generic `#ask` filtering/sorting/limits and query projections remain valid SMW techniques, but current queries must operate on current properties. Historical high-confidence/Verified/Axiomatic examples and obsolete Idea/Topic fields are not current query contracts. |
| README | historical-only | This Main-space README is a TEMP-001/task/workspace completion receipt and inventory. Its useful validation recommendations are reconciled elsewhere; its paths, scores and task status are historical process evidence. |
| SMW Property Definitions | superseded | Current Semantic properties documents the implemented floor and requires new predicates to earn a recurring semantic job. The historical “complete catalog,” inverse tables, event/governance/workflow properties, confidence/quality scores and external mapping assertions were largely proposed rather than deployed. |
| SMW Property Types Complete | superseded | Core SMW data types remain substrate facts; current concrete Property pages define what BITwiki actually uses. Historical custom confidence/workflow/agent property types and nonstandard declaration examples are not adopted. |
| SMW Query Patterns Reference | superseded | Useful query forms—type/domain/status filters, relationship queries, limits and projections—remain available through SMW/current navigation architecture. Historical confidence-threshold, Axiomatic/Verified, obsolete relation and unverified aggregation examples are not current canonical queries. |

## Durable V1 signal confirmed in current canon

- types and properties should arise from demonstrated use;
- semantic properties need explicit meaning, expected target/value type and validation;
- schema proposals are not evidence of deployed properties;
- controlled vocabulary has one authority and should be validated;
- dependency relationships should be explicit where they carry domain/implementation meaning;
- reusable procedural validation belongs in Lua, not duplicated template branches;
- queries are projections over canonical semantic state, not a second source of truth;
- query/traversal limits and performance must be bounded;
- external ontology mappings require explicit semantics, version/provenance and loss handling;
- old property/query catalogs must be tested against actual consumers before adoption.

## Explicitly deprecated/deferred schema

Not imported as current schema:

- universal numeric confidence/quality/evidence-count properties;
- EPV as a required schema and its Creation/Modification/Relation/Observation event taxonomy;
- mandatory “Was/Has” property naming;
- the historical full Property Dictionary as a backlog;
- automatic inverse/domain/range semantics not evidenced in the runtime;
- old Topic/Idea classification;
- confidence-threshold query families and Axiomatic/Verified filtering;
- unverified external vocabulary equivalences;
- proposed ValidatorBase/EpistemicValidator/QueryHelper interfaces.

## Result

All 13 V1 semantic-schema/SMW/query/module architecture sources are content-reconciled for issue #152.

This does not close issue #152 or authorize archive retirement.
