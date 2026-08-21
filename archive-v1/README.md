# archive-v1 — exhaustive public BITwiki V1 snapshot

**Read-only provenance. Do not deploy this directory as V2 pages.**

Generated from the anonymous MediaWiki Action API with continuation followed until exhaustion.

This archive preserves what V1 actually contained—content, revision history, namespaces, template usage, semantic/runtime evidence, and historical design language. It is deliberately **not rewritten when V2 architecture changes**.

For the current living V2 model, start with the repository root `README.md`, `BITwiki/Programmable knowledge substrate.mediawiki`, `BITwiki/Lua architecture.mediawiki`, and `manifest.json`.

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
- Created `Category:` pages: **0**
- Used categories lacking `Category:` pages: **162**

These counts describe this preserved snapshot, not current V2 corpus/runtime state.

## Files

`siteinfo.json` site model; `index.json` every page; `namespaces/*` exhaustive title lists; `pages/*` captured wikitext; `history/*` complete revision histories with bodies; `files/*` uploaded-file revisions and metadata; `categories/*` category graph; `templates/*` templates and transclusion callers; `special/*` maintenance reports; `audit.json` completeness checks.

## How V2 uses the archive

```text
archive exact V1 source + history + usage
→ compare related versions
→ preserve unique writing / citations / semantics / behavior
→ distinguish documented design from deployed implementation
→ identify durable signal
→ KEEP / REWRITE / MERGE / SPLIT / REDIRECT / RETIRE
→ implement/mature the primitive in V2
→ verify repository + runtime consequences
```

The current Lua compiler architecture illustrates this rule. V1 contained substantial Lua/module specifications but the captured live Module namespace had zero deployed Module pages. V2 therefore treats those specifications as **design lineage**, not proof of deployed behavior, and matures the reusable-runtime idea into the current `Module:BITwiki/*` implementation without pretending the historical implementation already existed.

## Authority boundary

```text
archive-v1 historical evidence
≠ current V2 architecture
≠ deployable V2 content
≠ current MediaWiki runtime state
```

Special pages are generated reports, not deployable content pages. Similar titles are never sufficient evidence for a merge. When current architecture changes, update living V2 documentation; preserve this archive as historical evidence unless a new verified snapshot is intentionally generated.
