# Concept namespace

Source for Semantic MediaWiki `Concept:*` pages.

A Concept is a **named semantic query / dynamic set**. It is not another category tree, an entity type, or an independent store of facts. Use a Concept when the same computed set has genuine reuse value in queries, navigation, maintenance, exploration, or higher-level projections.

```text
canonical SMW assertions
        ↓
Concept query definition
        ↓
reusable dynamic set
        ├── #ask / navigation
        ├── maintenance
        └── future Lua/interface projections
```

The set changes as canonical semantic state changes; the Concept does not duplicate those assertions.

The captured live V1 Concept namespace was configured but empty. V2 therefore introduces Concepts progressively rather than manufacturing a catalog to populate the namespace. `Computer science.mediawiki` is the first proof and represents pages explicitly annotated with `Domain::Computer science`.

## Relationship to adjacent layers

```text
SMW Property/value   durable semantic assertion
Concept              reusable query over those assertions
Category             browse/classification presentation
Portal               subject orientation
Lua                   deterministic transformation/projection when needed
BIThub                interaction surface consuming canonical/query state
```

Higher-level consumers should reuse the semantic set rather than copy its membership into separate manually maintained lists unless an authored list has a distinct editorial purpose.

See `BITwiki/MediaWiki substrate.mediawiki`, `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Navigation.mediawiki`, and Semantic MediaWiki's Concepts documentation.
