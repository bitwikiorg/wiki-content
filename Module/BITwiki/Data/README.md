# Module:BITwiki/Data/*

Immutable data modules loaded with Scribunto `mw.loadData()`.

These files are runtime projections of reviewed repository data, not an independent ontology. `Schema.lua` mirrors `bitwiki-runtime-schema.json`; repository validation must detect drift between the JSON authority and the deployed Lua projection.

Data modules must return data tables only. Executable behavior belongs in `Module:BITwiki/*` modules.
