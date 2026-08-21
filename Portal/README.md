# Portal title projection

Files representing `Portal:*` titles used by V2 navigation.

Important: the archived 2026-08-18 MediaWiki namespace configuration does **not** list a dedicated Portal namespace. Until live `Special:NamespaceInfo` proves otherwise, this directory is a repository/title projection rather than evidence that `Portal` is a configured namespace.

Portals are **subject-orientation interfaces over canonical knowledge**. They are not ontology, semantic authority, or substitutes for contents, outlines, lists, glossaries, categories, Concepts, or explicit relationships.

```text
canonical pages + SMW relationships + authored navigation
                         ↓
             query / Template / Lua projection
                         ↓
                    Portal view
```

A portal may combine authored orientation with computed semantic/query views. If Lua is used, it should transform existing state deterministically rather than maintain an independent membership database.

## Relationship to BIThub

The same underlying BITwiki state may be projected differently in BIThub/Discourse—for example as entity cards, graph neighborhoods, contribution tasks, or contextual navigation. A BIThub-native interface and a Portal page can therefore be two presentations of the same canonical knowledge without needing duplicate semantic truth.

## Design rules

- Keep portals useful for orientation rather than recursively mirroring every taxonomy level.
- Prefer canonical focused portal titles; retain legacy slash paths only as redirects where required.
- Use categories, Concepts, explicit relationships, contents, outlines, lists, and glossaries for the jobs they model better.
- Treat portal hierarchy as navigation, not automatically as ontology.
- Update this README when the portal execution/interface model changes.

See `BITwiki/Navigation.mediawiki`, `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Ecosystem.mediawiki`, and `Template/README.md`.
