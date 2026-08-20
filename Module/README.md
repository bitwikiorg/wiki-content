# Module namespace

Source for MediaWiki `Module:*` pages executed by Scribunto/Lua.

The captured live V1 corpus had the Module namespace configured but **zero live Module pages**. V1 nevertheless contains substantial Lua design specifications under `archive-v1/pages/Main/`. Those documents are design lineage, not proof that the proposed modules were deployed.

## V2 policy

- Use Lua for non-trivial reusable logic, validation, normalization, or computation.
- Keep declarative presentation/semantic emission in templates when wikitext remains clearer.
- Do not resurrect V1 numeric-confidence logic; V2 uses the current epistemic-status model.
- A module should have real template/page consumers rather than existing as an architectural ornament.

`Structure.lua` is the first V2 runtime module. `Template:Knowledge object` invokes it as a bounded identity-validation backstop for direct wiki edits.

MediaWiki's canonical runtime title for `Structure.lua` is `Module:Structure`.
