# Template namespace

Deployable/source-controlled `Template:*` pages.

Templates are BITwiki's **declarative authoring, transclusion, semantic-emission, and stable public invocation layer**. They should remain understandable from wikitext; non-trivial reusable procedure belongs in Scribunto/Lua when that improves correctness, composability, or reuse.

```text
wikitext author
    ↓
Template invocation
    ├── declarative rendering / transclusion
    ├── SMW property emission
    ├── Cargo record declaration/storage where explicitly designed
    └── #invoke → Module:BITwiki/* for reusable procedural logic
```

Templates do not own an independent ontology. They expose contracts over canonical page/SMW/Cargo state and delegate deterministic computation to the Lua compiler layer where appropriate.

## V2 templates

| Template | Role |
|---|---|
| `Knowledge object` | common semantic identity; invokes `Module:Structure`, which delegates normalization/type checking to `Module:BITwiki/Compiler` |
| `Knowledge request` | repeated operational request record; renders a row and stores it in Cargo `Knowledge_requests` |
| `Knowledge domain category` | shared composition/query surface for substantive Domain categories |
| `Domain portal` | Domain navigation and SMW query surface |
| `Topic portal` | focused navigation surface |
| `Source status` | editorial/source-lineage notice |

### Knowledge-object compiler path

```text
{{Knowledge object}}
        ↓
Module:Structure
        ↓
Module:BITwiki/Compiler
        ↓
Module:BITwiki/Core + Module:BITwiki/Data/Schema
        ↓
normalized record + diagnostics
```

`Module:Structure` is a public compatibility/runtime wrapper, not the entire type system. Compiler-facing vocabulary is owned by `bitwiki-runtime-schema.json` and projected into Scribunto through `Module:BITwiki/Data/Schema`.

`Knowledge request` is deliberately an operational template, not a second knowledge-object schema. Cargo is appropriate because many request records share a stable lifecycle and need queryable status; Semantic MediaWiki remains the graph layer for canonical knowledge assertions.

## Live V1 compatibility templates

This directory also contains the nine templates confirmed by the live V1 fidelity inventory so runtime dependencies are not hidden only inside `archive-v1/`.

| Template | Captured callers | Disposition |
|---|---:|---|
| `Infobox` | 80 | **Compatibility-critical**; keep until callers are migrated and verified |
| `BITwiki complex decorative circle` | 3 | live legacy presentation |
| `BITwiki constructs decorative circle` | 2 | live legacy presentation |
| `BITwiki footer` | 2 | live legacy presentation |
| `BITwiki header element` | 2 | live legacy presentation |
| `BITwiki implementations decorative circle` | 2 | live legacy presentation |
| `BITwiki projects decorative circle` | 2 | live legacy presentation |
| `BITwiki simple decorative circle` | 2 | live legacy presentation |
| `BITwiki` | 0 | live namespace page; review before retirement |

Their presence here preserves migration/runtime fidelity; it **does not make them the V2 visual or composition standard**.

Evidence: `archive-v1/templates/index.json`, `archive-v1/templates/usage/`, `archive-v1/pages/Template/`, and `archive-v1/history/Template/`.

## Design rules

- Keep simple declarative composition in wikitext.
- Move repeated non-trivial normalization, validation, bounded inference, or semantic presentation into `Module:BITwiki/*`.
- Let SMW own durable semantic assertions and Cargo own explicit repeated operational records.
- Do not add parse-time write side effects merely because an extension makes them technically possible.
- Do not manufacture templates only for visual symmetry; a template needs a stable shared contract or multiple real consumers.
- When a template changes a public contract or module dependency, update this README and the corresponding `BITwiki:*` standard.

See `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Lua architecture.mediawiki`, `BITwiki/MediaWiki substrate.mediawiki`, `BITwiki/Templates and categories.mediawiki`, `BITwiki/Transclusion.mediawiki`, and `BITwiki/Requested knowledge.mediawiki`.
