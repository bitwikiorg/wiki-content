# Category namespace

Deployable `Category:*` pages.

Categories are **browse/classification/navigation surfaces over canonical knowledge**. They are useful when they help readers understand scope and move through related material; they are not the ontology, an entity type system, or a substitute for explicit SMW relationships.

```text
canonical pages + semantic state
          ↓
Category membership / SMW query / shared category template
          ↓
substantive browse and orientation surface
```

Substantive categories may define:

- scope and inclusion/exclusion boundaries;
- relationships to adjacent fields;
- semantic/query surfaces;
- related portals, contents, outlines, lists, or concepts;
- contextual explanatory text that improves navigation.

Administrative categories should remain concise and operational. Do not pad every category to achieve visual symmetry.

## Relationship to the programmable substrate

A category may consume declarative templates, SMW queries, and eventually Lua-produced deterministic projections when transformation is genuinely useful. Those mechanisms project existing knowledge state; they do not create hidden semantic authority inside the category view.

A controlled Domain can participate simultaneously in several distinct layers:

```text
Domain property value       semantic classification
Category:<Domain>           browse/navigation surface
Concept:<Domain>            reusable computed semantic set
Portal:<Domain>             subject-orientation view
Lua/query projection        contextual computed presentation
```

These surfaces should reinforce one another without being treated as equivalent.

See `BITwiki/Templates and categories.mediawiki`, `BITwiki/Navigation.mediawiki`, `BITwiki/Programmable knowledge substrate.mediawiki`, and `Template/README.md`.
