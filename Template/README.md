# Template namespace

Deployable/source-controlled `Template:*` pages.

This directory now contains **both** V2 canonical templates and the nine templates confirmed by the live V1 fidelity inventory. The point is discoverability and dependency fidelity: a template that exists on the wiki should not be hidden only inside `archive-v1/`.

## V2 templates

| Template | Role |
|---|---|
| `Knowledge object` | Common semantic identity; runtime-validated by `Module:Structure` |
| `Knowledge domain category` | Shared composition/query surface for substantive Domain categories |
| `Domain portal` | Domain navigation and SMW query surface |
| `Topic portal` | Focused navigation surface |
| `Source status` | Editorial/source-lineage notice |

## Live V1 compatibility templates

| Template | Captured callers | Disposition |
|---|---:|---|
| `Infobox` | 80 | **Compatibility-critical**; keep until callers are migrated and verified |
| `BITwiki complex decorative circle` | 1 | live legacy presentation |
| `BITwiki constructs decorative circle` | 1 | live legacy presentation |
| `BITwiki footer` | 1 | live legacy presentation |
| `BITwiki header element` | 1 | live legacy presentation |
| `BITwiki implementations decorative circle` | 1 | live legacy presentation |
| `BITwiki projects decorative circle` | 1 | live legacy presentation |
| `BITwiki simple decorative circle` | 1 | live legacy presentation |
| `BITwiki` | 0 | live namespace page; review before retirement |

The compatibility files are recovered from the current-public V1 snapshot and remain migration dependencies. Their presence here **does not make them the V2 visual/template standard**.

Evidence:
- `archive-v1/templates/index.json`
- `archive-v1/templates/usage/`
- `archive-v1/pages/Template/`
- `archive-v1/history/Template/`

## Design rule

Templates should provide reusable declarative composition, rendering, and semantic emission. Repeated non-trivial logic belongs in `Module/` when Lua improves correctness or maintainability.

Do not manufacture templates merely to make every page look structurally identical. A template earns its place when multiple consumers share a stable behavior or contract.

See `BITwiki/MediaWiki substrate.mediawiki`, `BITwiki/Templates and categories.mediawiki`, and `BITwiki/Transclusion.mediawiki`.
