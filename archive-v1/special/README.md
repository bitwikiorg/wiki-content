# V1 Special-page / maintenance surfaces

**These are generated operational reports, not ordinary pages to copy into V2.**

They are part of the archive because they reveal inventory, categorization, transclusion, redirect, and maintenance state that page bodies alone do not preserve.

| Surface | What it tells us | V2 use |
|---|---|---|
| `Special:AllPages` | page inventory by namespace | enumerate/archive every public namespace before migration |
| `Special:Categories` | categories with members + counts | recover category graph and naming drift |
| `Special:UncategorizedPages` | pages with no category tags | identify missing classification or intentional exceptions |
| `Special:UncategorizedTemplates` | templates with no category tags | template documentation/organization audit |
| `Special:UnusedTemplates` | templates not currently transcluded | review candidates; never auto-delete |
| `Special:WantedCategories` | categories with members but no created category page | distinguish membership from category-page source |
| `Special:UnusedCategories` | created category pages with no members | cleanup/reconciliation signal |
| `Special:BrokenRedirects` | redirects to missing targets | migration integrity |
| `Special:DoubleRedirects` | redirect chains | migration integrity |

## Requested V1 surfaces

- https://bitwiki.org/Special:AllPages
- https://bitwiki.org/Special:UncategorizedTemplates
- https://bitwiki.org/Special:UnusedTemplates
- https://bitwiki.org/Special:UncategorizedPages
- https://bitwiki.org/Special:Categories
- https://bitwiki.org/Category:BITwiki_Templates
- https://bitwiki.org/Category_List

`Category:BITwiki Templates` and `Category List` are not interchangeable with `Special:Categories`: the first is a category page/title, the second is a V1 Main-namespace page, and the Special page is a generated index.

## Archive rule

When a Special-page result changes during migration, capture the result/observation if it matters to provenance. Preserve the actual Template:/Category:/Property:/Module: page source separately.
