# archive-v1 — exhaustive public BITwiki V1 snapshot

**Read-only provenance. Do not deploy this directory as V2 pages.**

Generated from the anonymous MediaWiki Action API with continuation followed until exhaustion.

## Snapshot
- Captured: **2026-08-18T17:20:10Z**
- API: `https://bitwiki.org/w/api.php`
- Namespaces enumerated: **24**
- Pages: **186**
- Revision bodies: **606**
- File pages: **2**
- File binary revision records: **2**
- Captured binary revisions: **0**
- Unresolved historical binary references: **2**
- Unique binary blobs: **0**
- Templates: **9**
- Categories (used ∪ created): **162**
- Used categories: **162**
- Created Category: pages: **0**
- Used categories lacking Category: pages: **162**

## Files
`siteinfo.json` site model; `index.json` every page; `namespaces/*` exhaustive title lists; `pages/*` current wikitext; `history/*` complete revision histories with bodies; `files/*` uploaded file revisions and metadata; `categories/*` complete category graph; `templates/*` every template and transclusion caller; `special/*` maintenance reports; `audit.json` completeness checks.

## Migration
```text
archive exact V1 source + history + usage
→ compare related versions
→ preserve unique writing / citations / semantics / behavior
→ separate durable ideas from obsolete implementation
→ KEEP / REWRITE / MERGE / SPLIT / REDIRECT / RETIRE
→ implement V2
→ rerun maintenance reports
```

Special pages are generated reports, not deployable content pages. Similar titles are never sufficient evidence for a merge.
