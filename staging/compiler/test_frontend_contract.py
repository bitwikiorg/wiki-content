"""Performance guardrails for the compact GitHub Pages content index."""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class FrontendPerformanceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "staging/frontend/index.html").read_text(encoding="utf-8")
        cls.js = (ROOT / "staging/frontend/app.js").read_text(encoding="utf-8")

    def test_recursive_mutation_observer_is_removed(self):
        # Rewriting the same link's text inside a childList observer causes an
        # infinite feedback loop (each textContent assignment mutates childList).
        self.assertNotIn("MutationObserver", self.html)
        self.assertNotIn("clarifyExactGitHubSourceLink", self.html)

    def test_boot_only_loads_small_index_and_build_metadata(self):
        startup = self.js.split("async function initialize() {", 1)[1].split("function renderNamespaces()", 1)[0]
        self.assertIn("loadJSON('./data/pages.json')", startup)
        self.assertIn("loadJSON('./data/build-meta.json')", startup)
        self.assertNotIn("graph.json", startup)
        self.assertNotIn("search.json", startup)
        self.assertNotIn("ontology.json", startup)
        self.assertNotIn("loadFullPage", startup)

    def test_sidebar_does_not_fetch_all_portal_pages(self):
        sidebar = self.js.split("function renderSidebarPortals() {", 1)[1].split("function canonicalArticles()", 1)[0]
        self.assertNotIn("loadFullPage", sidebar)
        self.assertIn("pages.slice(0, 20)", sidebar)

    def test_compact_homepage_and_bounded_directories(self):
        overview = self.js.split("function renderOverview() {", 1)[1].split("function renderDirectory(", 1)[0]
        self.assertIn("BITwiki content index", overview)
        self.assertNotIn("loadFullPage(", overview)
        self.assertIn("maxResults = 40", self.js)
        self.assertIn("matches.slice(0, maxResults)", self.js)
        self.assertIn("maxResults: maxResults + 40", self.js)

    def test_expensive_data_only_loaded_on_specific_routes(self):
        self.assertIn("async function ensureGraph()", self.js)
        self.assertIn("async function ensureSearch()", self.js)
        self.assertIn("if (q) await ensureSearch();", self.js)
        self.assertIn("await ensureGraph();", self.js)

    def test_browser_cache_busted(self):
        self.assertIn("styles.css?v=compact-20261116", self.html)
        self.assertIn("app.js?v=compact-20261116", self.html)


if __name__ == "__main__":
    unittest.main()
