# Property namespace

Deployable Semantic MediaWiki `Property:*` definitions.

Property pages are contracts for the semantic graph: define datatype/meaning, intended subjects and values, relationship direction, constraints or usage notes, and examples where useful. Defining a property is insufficient; canonical pages/templates must actually emit and query it consistently.

## V2-native properties

The unencoded filenames in this directory are the current V2 identity, lifecycle, epistemic, and relationship predicates such as `Domain`, `Entity type`, `Epistemic status`, `Provenance`, `Part of`, `Depends on`, `Implements`, `Supports`, and `Contradicts`.

## Recovered imported vocabulary

The live V1 Property namespace also contains four imported-vocabulary properties. They are source-controlled here because they are part of the current public semantic substrate:

- `Foaf%3Ahomepage.mediawiki` → `Property:Foaf:homepage`
- `Foaf%3Aknows.mediawiki` → `Property:Foaf:knows`
- `Foaf%3Aname.mediawiki` → `Property:Foaf:name`
- `Owl%3AdifferentFrom.mediawiki` → `Property:Owl:differentFrom`

`%3A` is used in filenames for cross-platform compatibility; it decodes to a colon in the namespace-local MediaWiki title.

Imported vocabulary should not be mixed casually into V2-native semantics. Keep it when interoperable meaning is required and trace its mapping through the corresponding `MediaWiki:Smw import ...` pages.

See `BITwiki/Semantic properties.mediawiki` and `BITwiki/MediaWiki substrate.mediawiki`.
