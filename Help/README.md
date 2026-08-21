# Help namespace

Source-control mapping for `Help:*`.

Help pages explain **stable user-facing workflows** for interacting with BITwiki. They are not project architecture specifications, canonical subject knowledge, or a place to duplicate every README.

The namespace exists in the BITwiki MediaWiki installation, but the captured public V1 namespace is empty. V2 does **not** create filler Help pages merely to populate it.

Add Help content when a real workflow becomes stable enough that a wiki user needs operational guidance, for example:

- creating or reviewing a knowledge request;
- authoring a valid knowledge object;
- understanding semantic/navigation interfaces;
- moving between BIThub interaction and BITwiki canonical publication;
- using a contribution or research workflow exposed by the programmable substrate.

## Documentation boundary

```text
README                repository-local operational orientation
BITwiki:*             project architecture / standards / governance
Help:*                stable end-user workflow guidance
Main:*                canonical subject knowledge
BIThub                 interactive/conversational workflow surface
```

Help should explain the user's path through those systems without becoming a second specification. When behavior changes, update the authoritative architecture/implementation first and then revise Help if the user workflow changed.

See `BITwiki/Contributing.mediawiki`, `BITwiki/Programmable knowledge substrate.mediawiki`, and `BITwiki/Ecosystem.mediawiki`.
