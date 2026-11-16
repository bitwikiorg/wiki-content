"""Regression checks for the static, source-preserving GitHub Pages projection."""
import unittest
from build import (
    expand_static_transclusions,
    extract_section,
    inline_markup,
    render_preview,
    search_body,
    validate_identity,
)


class StagingProjectionTests(unittest.TestCase):
    def test_multidomain_values_are_validated_individually(self):
        schema = {"entity_types": ["Concept"], "domains": ["Biology", "Computer science"], "epistemic_statuses": ["Established"]}
        correct = {"entity_type": "Concept", "domain": "Biology, Computer science", "status": "Established", "provenance": "Test"}
        self.assertEqual(validate_identity(correct, schema), [])
        wrong = {**correct, "domain": "Biology, Imaginary domain"}
        issues = validate_identity(wrong, schema)
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["value"], "Imaginary domain")

    def test_read_preview_hides_metadata_and_renders_references(self):
        content = """{{Source status|status=test}}
{{Knowledge object
 |title=Example
 |entity_type=Concept
 |domain=Biology
 |status=Established
 |provenance=Test
}}
{{Reading depth|base=Example|current=Core}}
= Example =
== Overview ==
A '''bit''' <sub>2</sub> with [[Information theory]]<ref name="source">[https://doi.org/10.1002/j.1538-7305.1948.tb01338.x Shannon (1948)]</ref>.
== References ==
<references />
"""
        preview = render_preview(content, "wikitext")
        self.assertNotIn("{{Source status", preview)
        self.assertNotIn("{{Knowledge object", preview)
        self.assertNotIn("{{Reading depth", preview)
        self.assertIn("<strong>bit</strong>", preview)
        self.assertIn("<sub>2</sub>", preview)
        self.assertIn('class="citation"', preview)
        self.assertIn('class="references"', preview)
        self.assertIn("Shannon", preview)
        self.assertIn('id="section-2"', preview)

    def test_reference_reuse(self):
        source = 'Test<ref name="a">[https://example.com An example]</ref>. Again<ref name="a" />. <references />'
        html = render_preview(source, "wikitext")
        self.assertEqual(html.count('aria-label="Reference 1"'), 2)
        self.assertEqual(html.count('id="reference-1"'), 1)

    def test_transclusion_uses_source_and_skips_literal_examples(self):
        lookup = {"Book Matter/Example": "== Mechanism ==\nFactual source passage.\n== Applications ==\nAn application."}
        source = "{{:Book Matter/Example}}\n<pre>\n{{:Book Matter/Example}}\n</pre>"
        rendered = expand_static_transclusions(source, "Host", lookup)
        self.assertIn("Static preview transcluded from", rendered)
        self.assertEqual(rendered.count("Factual source passage."), 1)
        self.assertIn("<pre>\n{{:Book Matter/Example}}\n</pre>", rendered)
        selected = expand_static_transclusions("{{#lsth:Book Matter/Example|Mechanism}}", "Host", lookup)
        self.assertIn("Factual source passage.", selected)
        self.assertNotIn("An application.", selected)

    def test_transclusion_cycle_is_bounded(self):
        lookup = {"A": "{{:B}}", "B": "{{:A}}"}
        rendered = expand_static_transclusions("{{:A}}", "Host", lookup)
        self.assertIn("Preview cannot resolve transclusion", rendered)

    def test_search_indexes_body_not_only_title(self):
        content = "= Article =\nAn unusual but important biochemical oscillation."
        self.assertIn("biochemical oscillation", search_body(content))

    def test_untrusted_source_is_escaped(self):
        rendered = inline_markup('<img src=x onerror=alert(1)>')
        self.assertNotIn("<img", rendered)
        self.assertIn("&lt;img", rendered)


if __name__ == "__main__":
    unittest.main()
