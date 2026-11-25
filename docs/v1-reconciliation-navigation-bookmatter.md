# V1 navigation, interface, and Book Matter reconciliation

Issue #152 reconciliation for:
- 4 `navigation_portals_categories_visualization` architecture sources;
- 19 `navigation_interface` sources;
- 26 remaining `book_matter_reusable` sources.

Every source below was reviewed as content. Navigation/interface classification alone is not used as the disposition rationale.

## Navigation / portal / visualization architecture

| V1 source | Disposition | Durable substance / explicit non-adoption |
|---|---|---|
| BITwiki Glossary | incorporated | The glossary function remains useful, but the V1 definitions mixed current concepts with obsolete confidence tiers, old governance, and false implementation assumptions. A new `BITwiki:Glossary` now provides current project terminology and points to canonical definitions, including Holobiont/Holobiome. |
| CATEGORY ARCHITECTURE | superseded | Current Navigation, Templates and categories, Ontology, and Navigation and coverage research preserve polyhierarchical browsing, Domain/category separation, category roles, naming discipline, and query projections. The old fixed root hierarchy, epistemic categories, agent workspaces, auto-category assumptions, and one-template-per-category plan are not current architecture. |
| Knowledge Graph Visualization | incorporated | Its durable visualization concerns—semantic fidelity, accessible encodings, text equivalents, graph/view provenance, query-derived views, bounded performance, and the distinction between rendered edges and semantic facts—are now represented in Page format and Navigation. Historical confidence-sized/colored nodes, Axiomatic layouts, D3/Graph-extension code, custom result formats, and claimed runtime support are not adopted. |
| Portal Architecture Specification | superseded | Current Navigation and Navigation and coverage research preserve progressive disclosure, cross-domain links, polyhierarchical portals, parent/related distinctions, smaller meaningful portal sets, query-supported content, and portal-maintenance failure lessons. Historical fixed portal-type taxonomy, invented portal tree, required 13-section structure, LocalSettings snippets, auto-rotation/cache variables, and unverified comparative counts are not current contracts. |

## Book Matter / reusable composition sources

| V1 source | Disposition | Durable substance / explicit non-adoption |
|---|---|---|
| BITwiki Epistemic Tiers/Confidence Levels | superseded | Historical confidence-level fragment is replaced by current Epistemic status plus explicit confidence rationale; no universal numeric/fixed confidence ladder. |
| BITwiki Epistemic Tiers/Overview | superseded | Provisionality and visible evidentiary standing survive in current Epistemics/Epistemic status; historical tier mechanics are superseded. |
| BITwiki Epistemic Tiers/Theoretical Foundations | superseded | Method pluralism and situated/contextual concerns survive in current Epistemics/Four foundations; the fragment does not define a separate current tier system. |
| BITwiki Epistemic Tiers/Tier Definitions | superseded | Hypothetical/Emerging/Established concepts survive in the current six-value vocabulary. Historical Archived-as-epistemic-tier and source-count/consensus thresholds are not current standing rules. |
| Component Implementation section | superseded | Current Organization, Navigation, Semantic properties, Transclusion and MediaWiki substrate preserve the useful implementation concerns. Historical semantic-forms, automatic graph visualization/pathfinding and broad implementation claims were not verified runtime facts. |
| Component:Implementation section | superseded | Parallel-format variant of the same implementation guidance; no independent durable signal beyond the current architecture. |
| Component Knowledge graph section | superseded | Current Ontology, Relationships and Navigation preserve explicit graph semantics and graph/query views. Old Idea/Implementation schema, pathfinding and assumed integrated visualization are not current contracts. |
| Component:Knowledge graph section | superseded | Parallel-format variant; no independent current knowledge beyond the reconciled graph/navigation principles. |
| Component Portals section | superseded | Current Navigation preserves portal orientation, scope, cross-links and maintenance while rejecting the old four-portal-domain model and compulsory portal subpage/navbox structure. |
| Component:Portals section | superseded | Parallel-format variant of the old portal component. |
| Component Semantic section | superseded | Current Semantic properties/Relationships/Navigation preserve explicit semantics and queries. Historical `Has implementation`/`Implements idea`, category-as-property syntax, automatic categorization, semantic forms and assumed graph visualization are not current standards. |
| Component:Semantic section | superseded | Parallel-format variant of the old semantic component. |
| Component Transclusion section | superseded | Current Transclusion/Book Matter preserve reuse, source ownership, context, testing and dependency review while rejecting compulsory fragmentation and unsupported automatic semantic behavior. |
| Component:Transclusion section | superseded | Parallel-format variant of the old transclusion component. |
| Constructs section | historical-only | Main-page placeholder containing decorative empty-square links rather than durable subject knowledge. |
| Emergent Properties section | historical-only | Main-page placeholder containing decorative empty-square links rather than a substantive account of emergence. |
| Featured Articles section | historical-only | A dated curation list of three links; no durable knowledge beyond historical homepage state. |
| Implementations section | historical-only | Empty-square Main-page placeholder; no substantive implementation knowledge. |
| Learn More section | superseded | Useful search/random/all-pages/GitHub/contribution routes are represented in the current Main Page and contribution surfaces; historical links/decorative template are obsolete. |
| Live Stats section | deprecated | `NUMBEROFARTICLES`/edit/user counts may be display metrics, but labeling all articles “verified” is false and raw activity is not a quality measure. Current architecture explicitly separates scale/activity from epistemic quality. |
| Main Page | superseded | Current Main Page deliberately matures the original orientation/quick-access modular homepage while correcting stale portals, opaque placeholders, “verified article” counts, and overclaims about AI/modularity. |
| Main Page styled | superseded | Byte-identical historical presentation variant of Main Page; superseded by the current Main Page. |
| Peer-review-protocol | superseded | Conflict-of-interest disclosure, methodological/evidence review, documentation and dispute handling survive across Peer review, Claim validation, Editorial protocol and Epistemic audit. Mandatory Emerging→Established board review and old confidence categories are not current rules. |
| Projects section | historical-only | Empty-square Main-page placeholder; no substantive project knowledge. |
| Start Exploring section | incorporated | The useful multi-entry-point navigation function is directly matured in the current Main Page's Start Exploring section with current portals and navigation semantics. |
| What Makes Us Different section | incorporated | The current Main Page deliberately preserves and corrects this comparison: coherent modular reuse, multiple reading depths, evidence/provenance/uncertainty, and accountable human/AI-assisted inquiry replace the simplistic V1 contrasts. |

## Navigation/interface sources

| V1 source | Disposition | Durable substance / explicit non-adoption |
|---|---|---|
| BITwiki How to Navigate | superseded | Current Navigation/Main Page preserve hierarchical, lateral, query-driven and cross-domain exploration. Historical toroidal validation, confidence trajectories, old Idea/Topic types, Verified categories and nonexistent templates are not current navigation contracts. |
| BITwiki Master Navigation | superseded | Current Main Page, Navigation, Organization and focused standards replace the old book-matter master index. Old confidence tables, Axiomatic queries, workflow statuses and workspace links are obsolete. |
| BITwiki Ontology Index | superseded | Current Ontology, Entity types, Semantic properties and Relationships preserve evolving types/properties/relations and validation. Historical Topic/Idea, confidence/source-count properties and processual “crystallization” examples are not the current contract. |
| BITwiki Start Here | superseded | Current Main Page, Contributing, Epistemics and Navigation provide onboarding. Historical “every claim has a confidence score/status,” toroidal validation, YAML markers and committee review are explicitly not current rules. |
| Category List | superseded | Current Category namespace and Navigation/Template-category rules replace the historical hard-coded list. Old entity-type and epistemic categories are not a current taxonomy. |
| Component List | superseded | The useful functions—portals, semantics, reuse, graph views and implementation—are represented by current architecture pages rather than a fixed five-component model. |
| Concept Catalog | superseded | Current canonical pages plus the new `BITwiki:Glossary` replace the old catalog. Useful terms are retained through canonical definitions; obsolete Axiomatic/numeric-confidence/decentralized-governance/swarm assumptions are not. |
| Constitutional index | superseded | Current Manifesto, Constitution, Four foundations, Epistemics and Human-AI symbiosis replace the old merged constitutional index. Its residual useful themes—knowledge situated in practices/institutions, context-dependent evidence, anti-consensus truth, self-production/autopoiesis as a real scientific concept—are represented in current Manifesto/Epistemics and the existing `Autopoiesis` article. Signal-to-noise remains an analogy, not a universal quality metric; process metaphysics and old amendment/committee machinery are not current constitutional doctrine. |
| Evidence epistemics index | superseded | Current Epistemics/Evidence/Sources/Claim validation/Provenance/Uncertainty/Epistemic status/Epistemic audit provide the substantive framework. The index's later six-status/rationale direction survives; its five-tier/numeric-confidence variants and upgrade workflow are superseded. |
| Governance index | superseded | Current Constitution and Editorial protocol preserve transparent, accountable, revisable decisions. Distributed collective-intelligence authority, Epistemic Committee, fixed review cycles, confidence-calibration governance and obsolete board/policy files are not current governance. |
| INDEX | historical-only | An ontology-expansion deliverable index whose substantive source documents have now been individually reconciled. Its file counts, version assertions and deployment examples add no independent current standard. |
| MASTER INDEX | historical-only | Hyperion/book-matter workspace inventory and phase/deployment receipt. Its source families are individually reconciled; “READY FOR DEPLOYMENT,” quality percentages, task status and workspace paths are historical process claims, not current architecture. |
| Ontology index | superseded | Current Ontology/Entity types/Relationships/Semantic properties supersede the historical EPV/composable-multi-type catalog. Event/Model/System/etc. expansions remain use-driven candidates, not automatically imported types. |
| Portal List | superseded | Current Portal namespace and Navigation are the authority. The historical list mostly names proposed portals that were never established and cannot serve as current coverage evidence. |
| Property Definitions Index | superseded | Current Property namespace and Semantic properties define the implemented floor. Historical confidence/quality/source-count/template-metadata and hierarchical-category properties are proposed design, not current schema. |
| Research Synthesis Index | incorporated | Its durable comparative-research function and source-family lineage are now preserved in the active Comparative wiki research register. Historical “36 files/34 deliverables,” token/DAO/governance recommendations, roadmap completion claims and implementation priorities are not accepted without re-verification. |
| Schema matter index | superseded | Current Entity types, Semantic properties, Templates and categories, Lua architecture, MediaWiki substrate and Navigation replace this index. The durable principle that structure should enable rather than rigidly constrain survives; obsolete six-type/property/template/query catalogs do not. |
| Site notice | incorporated | Its durable warning—human-assisted AI content can be incomplete and consequential information should be checked—is represented more precisely in the current Main Page's Read Critically/footer guidance and current epistemics standards. |
| Template List | superseded | Current Template namespace and Templates and categories are the authority. The historical list mixed nonexistent wanted templates with old section templates and obsolete confidence/Idea interfaces. |

## Concrete recovery added during this pass

### Current project glossary
`BITwiki:Glossary` is restored as a useful navigation function, but rebuilt from current canon rather than copying obsolete V1 definitions. It includes current terms such as BITCORE, BIThub, BITwiki, Book Matter, Domain, Entity type, Epistemic status, Holobiont, Holobiome, Interoperability, Provenance, Relationship, Transclusion and Uncertainty.

### Comparative-research lineage
The active `BITwiki:Comparative wiki research register` now records the V1 comparative-research lineage and clearly distinguishes research hypotheses from implemented architecture.

## Result

All 49 V1 navigation/interface/remaining-Book-Matter sources are content-reconciled for issue #152.

This does not itself authorize archive retirement.
