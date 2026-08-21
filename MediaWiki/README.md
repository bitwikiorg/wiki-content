# MediaWiki namespace

Source-controlled public `MediaWiki:*` runtime/interface configuration.

These pages are **site infrastructure**, not subject knowledge. They can affect rendering, Semantic MediaWiki imports, extension behavior, and interface configuration, so deployment must preserve exact page titles/content models and should remain conservative.

Current recovered surfaces include:

- `MediaWiki:Common.css`
- `MediaWiki:KnowledgeGraphOptions`
- SMW import definitions for FOAF, OWL, Schema.org, and SKOS.

## Position in the programmable substrate

`MediaWiki:*` configuration participates below and beside authored knowledge:

```text
MediaWiki configuration + installed extensions
                 ↓
       parser / runtime capabilities
                 ↓
wikitext + Templates + SMW + Cargo + Scribunto
                 ↓
       rendered/computed BITwiki views
```

This directory does **not** become BITwiki's application backend merely because `MediaWiki:*` pages can affect runtime behavior.

Cross-service BIThub/Discourse authentication, HTTP transport, retries, secrets, queues, and background processing belong to explicit plugins, APIs, services, or agents. Scribunto/Lua remains sandboxed parse-time computation; `MediaWiki:*` pages should not be used to smuggle secret-bearing integration state into public wiki source.

## Relationship to semantic imports

SMW import pages define mappings to external vocabularies. Imported labels are not automatically equivalent to V2-native semantics. Mapping meaning and semantic loss are governed by `BITwiki:Interoperability` and the relevant Property contracts.

## Evidence and deployment

Some files originate from the verified V1 snapshot; evidence lives under `archive-v1/pages/MediaWiki/` and `archive-v1/history/MediaWiki/`. File extensions here reflect repository/source shape for readability; deployment must preserve the actual MediaWiki title and content model.

Repository source cannot by itself prove the target installation has the required extension/version/configuration. Reconcile against `Special:Version`, `Special:NamespaceInfo`, captured siteinfo, and `BITwiki/Deployment prerequisites.mediawiki` before deployment.

See `BITwiki/MediaWiki substrate.mediawiki`, `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Interoperability.mediawiki`, and `BITwiki/Deployment prerequisites.mediawiki`.
