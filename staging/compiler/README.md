# Staging compiler

`build.py` is a read-only inspection compiler over the existing BITwiki repository source.

It consumes `manifest.json`, `bitwiki-runtime-schema.json`, and namespace-native MediaWiki source, then derives disposable artifacts under `build/staging/` for the staging workbench.

It does **not**:

- modify `.mediawiki`, Lua, CSS, or JS source;
- define a second ontology;
- promote content to MediaWiki;
- treat generated JSON as canonical state.

Its job is to make existing source inspectable as page models, ontology objects, graph layers, search data, validation state, and promotion metadata. Actual MediaWiki deployment remains governed by `scripts/deployment_plan.py` and `scripts/deploy_mediawiki.py`.
