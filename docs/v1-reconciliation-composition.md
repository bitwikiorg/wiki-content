# V1 composition / templates / transclusion reconciliation

Issue #152 family reconciliation for the 10 V1 `composition_templates_transclusion` architecture sources.

Current comparison targets include `BITwiki:Transclusion`, `Help:Transclusion`, `BITwiki:Book Matter`, `BITwiki:Templates and categories`, `BITwiki:Lua architecture`, `BITwiki:Semantic properties`, and `Template:Knowledge object`.

## Reconciled sources

| V1 source | Disposition | Durable substance / explicit non-adoption |
|---|---|---|
| BITwiki Transclusion Rules | superseded | Current Transclusion preserves canonical-source reuse, provenance, context, downstream dependency review, cycle/performance hygiene and source/host semantic caution. It corrects several V1 overclaims: `{{:Page#Section}}` is not universal core section transclusion; slash titles do not prove Main subpages; semantic properties do not safely “belong to the source” after expansion; no deployed universal DAG/fragment registry is assumed. |
| Doc | superseded | This is documentation for the historical Infobox Project contract. Its durable idea—project pages may need goal/status/lead/domain/deliverable information—is design evidence, not proof those fields require one universal template/property schema. Current Page format + Knowledge object carry common identity; specialized structured fields require demonstrated repeated query/use. |
| Infobox Concept | superseded | Concept remains a current Entity type, but the V1 template's mandatory definition/status/numeric-confidence/source-count contract and TemplateStyles implementation are obsolete. Current Knowledge object provides the minimal common identity contract; concept-specific prose/relations are modeled where needed. |
| Infobox Idea | deprecated | V1 Idea has matured broadly into current Concept. A separate Idea infobox, numeric confidence/source-count contract and Idea-specific schema are not current architecture. |
| Infobox Implementation | superseded | Implementation remains a current Entity type. Historical implementation-language/interface/status/stability/confidence fields are useful design candidates only when recurring corpus/query needs justify them; they are not automatically global properties. |
| Infobox Project | superseded | Project remains a current Entity type. Goal/lead/status/deliverable fields are useful project-description candidates, but the historical template contract is not current schema without repeated project consumers and validated semantics. |
| SMW Template System | incorporated | Current Templates and categories + Lua architecture preserve the mature separation: Template is the declarative invocation/rendering surface; Lua handles reusable procedural validation/transformation; SMW owns durable graph assertions; Cargo owns separately justified operational records. |
| Template Catalog | superseded | Current Templates and categories explicitly distinguishes the 9 implemented V1 templates from the much larger wanted/design catalog. Missing/wanted templates are design evidence, not an implementation backlog; current template families must emerge from real callers. |
| Template System Validation Framework | superseded | Current Lua architecture, Semantic properties, Epistemic audit and tests preserve semantic integrity, validation-before-emission, transclusion hygiene, documentation, integration tests and deprecation/release checks. Mandatory confidence/status display, automatic semantic contribution from every template and recursive self-reference tests are not universal rules. |
| Template Usage Guide | superseded | Current Contributing, Templates and categories, Semantic properties and Help pages replace the old guide. The durable principle is “consistent pattern without rigidity”; obsolete Idea templates, confidence systems, source counts and assumed template families are not current requirements. |

## Reconciliation decision for specialized infobox fields

V1's four Main-space infobox designs contain useful field ideas, but issue #152 does not turn every historical field into a current Property merely to preserve it.

Current rule:

1. keep the common semantic identity contract small;
2. write domain/entity-specific descriptive material in coherent article prose where no structured consumer exists;
3. add a specialized Property/template field only after repeated articles or queries demonstrate a stable semantic job;
4. define type, meaning, cardinality/target/value behavior and validation before adoption.

This preserves V1's useful design signal without recreating schema bloat.

`BITwiki:Templates and categories` is updated to record that these four infobox design pages and the two template-system documents are now reconciled.

## Explicit V1 corrections

Not current behavior:

- core section transclusion through `{{:Page#Heading}}`;
- treating slash titles as proof that Main subpages are enabled;
- assuming transcluded SMW annotations remain attached to the source rather than potentially asserting against the host;
- a universally maintained transclusion DAG/adjacency matrix;
- mandatory fragment suffixes such as `/def`, `/cite`, `/nav`, `/box`;
- mandatory confidence/status/source-count fields in every infobox;
- separate Idea template/schema;
- creating all historical wanted templates;
- requiring every template invocation to emit semantic state.

## Result

All 10 V1 composition/template/transclusion architecture sources are content-reconciled for issue #152.

This does not close issue #152 or authorize archive retirement.
