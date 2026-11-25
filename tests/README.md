# Article source regression tests

This directory holds scoped article-level source and numerical regression tests. They run alongside staging compiler tests through `python -m pytest -q -p no:cacheprovider tests staging/compiler` in the V2 pull-request workflow. Passing these checks is not a substitute for claim-level source verification or live MediaWiki acceptance.
