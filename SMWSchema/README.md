# Semantic MediaWiki schema namespace

Source-control projection of MediaWiki's configured `smw/schema:*` namespace.

The runtime namespace name contains `/`, so the repository uses `SMWSchema/` instead of pretending `smw/` and `schema/` are independent architectural directories. Namespace-local colons are URL-encoded as `%3A` in filenames for cross-platform compatibility.

The current public schema/profile pages are recovered from the verified V1 snapshot. They use the native `smw/schema` content model and should not be edited as ordinary wikitext without understanding Semantic MediaWiki schema semantics.

## Two different kinds of schema

`SMWSchema/` and `bitwiki-runtime-schema.json` are deliberately **not the same layer**.

| Surface | Role |
|---|---|
| `SMWSchema/` | native Semantic MediaWiki schema/profile payloads interpreted by SMW |
| `Property/` | human-visible contracts for semantic predicates and datatypes |
| `bitwiki-runtime-schema.json` | repository authority for compiler-facing controlled vocabularies and deterministic runtime metadata |
| `Module:BITwiki/Data/Schema` | Scribunto projection of the JSON compiler schema |

```text
SMWSchema + Property + page assertions
               ↓
       durable SMW semantic state
               ↓
Lua compiler/runtime metadata
               ↓
validation / deterministic projection / diagnostics
```

The Lua schema must not become a shadow replacement for SMW's own schema model, and SMW schema pages should not be used as an arbitrary configuration store for compiler-only concerns.

## Deployment mapping

- `Group%3APredefined properties.mediawiki` → `smw/schema:Group:Predefined properties`
- `Group%3ASchema properties.mediawiki` → `smw/schema:Group:Schema properties`
- `Profile%3AFacetedsearch default profile.mediawiki` → `smw/schema:Profile:Facetedsearch default profile`

Deployment must preserve the exact MediaWiki title and `smw/schema` content model.

See `BITwiki/MediaWiki substrate.mediawiki`, `BITwiki/Semantic properties.mediawiki`, `BITwiki/Lua architecture.mediawiki`, and `Module/BITwiki/Data/README.md`.
