# Semantic MediaWiki schema namespace

Source-control projection of MediaWiki's configured `smw/schema:*` namespace.

The runtime namespace name contains `/`, so the repository uses `SMWSchema/` instead of pretending `smw/` and `schema/` are independent architectural directories. Namespace-local colons are URL-encoded as `%3A` in filenames for cross-platform compatibility.

The three current public schema/profile pages are recovered from the verified V1 snapshot. They use the `smw/schema` content model and should not be edited as ordinary wikitext without understanding Semantic MediaWiki schema semantics.

Deployment mapping:

- `Group%3APredefined properties.mediawiki` → `smw/schema:Group:Predefined properties`
- `Group%3ASchema properties.mediawiki` → `smw/schema:Group:Schema properties`
- `Profile%3AFacetedsearch default profile.mediawiki` → `smw/schema:Profile:Facetedsearch default profile`
