# Property namespace

Deployable Semantic MediaWiki `Property:*` definitions.

Properties are BITwiki's **durable semantic assertion vocabulary**. A Property page defines the contract for graph state: datatype/meaning, intended subjects and values, relationship direction, constraints/usage notes, and examples where useful. Canonical pages/templates must then emit and query that property consistently.

```text
canonical page / Template
        ↓ asserts
SMW Property + value
        ↓ stores durable graph state
Lua / #ask / Concept / navigation
        ↓ projects or diagnoses that state
MediaWiki / BIThub-facing views
```

The projection layer does not become the graph authority. Lua may normalize a relationship, choose an inverse **display label**, or report an invalid shape without silently storing a second assertion.

## Relationship to the Lua runtime schema

`bitwiki-runtime-schema.json` contains compiler-facing controlled vocabulary and deterministic display metadata required by Lua. It is **not a replacement for Property pages or SMW state**.

For example, relationship metadata such as an inverse display phrase can tell Lua how to render a stored `Depends on` edge from the opposite direction. The actual semantic assertion remains an SMW property/value emitted by canonical wiki state.

```text
Property:Depends on          semantic meaning + SMW datatype/contract
bitwiki-runtime-schema.json  compiler-facing deterministic metadata
SMW page assertion           durable fact/relationship state
Lua                          validation/projection/diagnostic behavior
```

These layers should agree but must not be conflated.

## V2-native properties

Current V2 properties cover identity, lifecycle, epistemics, provenance, and relationships, including `Domain`, `Entity type`, `Epistemic status`, `Provenance`, `Part of`, `Depends on`, `Implements`, `Supports`, `Contradicts`, `Refines`, `Derived from`, and `Related to`.

The self-model pages for BITwiki's own stack now exercise these relationships directly, giving future Lua/query/navigation work real graph state rather than demo-only data.

## Recovered imported vocabulary

The live V1 Property namespace also contains imported-vocabulary properties preserved because they are part of the public semantic substrate:

- `Foaf%3Ahomepage.mediawiki` → `Property:Foaf:homepage`
- `Foaf%3Aknows.mediawiki` → `Property:Foaf:knows`
- `Foaf%3Aname.mediawiki` → `Property:Foaf:name`
- `Owl%3AdifferentFrom.mediawiki` → `Property:Owl:differentFrom`

`%3A` is used in filenames for cross-platform compatibility and decodes to a colon in the namespace-local MediaWiki title.

Imported vocabulary should not be mixed casually into V2-native semantics. Preserve explicit mapping meaning and trace imports through the corresponding `MediaWiki:Smw import ...` pages and `BITwiki:Interoperability` rules.

## Invariants

```text
Property definition
≠ assertion by itself

Lua relationship metadata
≠ SMW assertion

inverse display
≠ automatically persisted inverse fact

BIThub projection/cache
≠ second semantic source of truth
```

When a semantic contract changes, update the Property page, the relevant `BITwiki:*` semantic/relationship standard, compiler schema metadata when actually required by runtime behavior, and the corresponding validation.

See `BITwiki/Semantic properties.mediawiki`, `BITwiki/Relationships.mediawiki`, `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Lua architecture.mediawiki`, and `BITwiki/Interoperability.mediawiki`.
