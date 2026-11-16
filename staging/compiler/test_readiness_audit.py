"""Smoke tests for source-scoped readiness classifications and safety gates."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "audit_staging_readiness.py"
spec = importlib.util.spec_from_file_location("audit_staging_readiness", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class StagingReadinessTests(unittest.TestCase):
    def test_artifact_fixture_covers_roles_and_manual_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "page").mkdir()
            meta = {"source_sha": "abc123"}
            index = [
                {"id": "a", "title": "Biological computation", "namespace": "Main",
                 "source_path": "Main/Biological computation.mediawiki", "content_model": "wikitext"},
                {"id": "b", "title": "Biological computation/Technical", "namespace": "Main",
                 "source_path": "Main/Biological computation/Technical.mediawiki", "content_model": "wikitext"},
                {"id": "c", "title": "Genetics", "namespace": "Main",
                 "source_path": "Main/Genetics.mediawiki", "content_model": "wikitext"},
                {"id": "d", "title": "Template:Knowledge request", "namespace": "Template",
                 "source_path": "Template/Knowledge request.mediawiki", "content_model": "wikitext"},
            ]
            graph = {"nodes": [{"id": x["id"], "title": x["title"]} for x in index],
                     "edges": [{"source": "a", "target": "c", "target_title": "Genetics",
                                "type": "Related to", "layer": "semantic", "resolved": True}]}
            objects = {"objects": [{"title": "Biological computation"}, {"title": "Genetics"}]}
            docs = {
                "a": ('{{Knowledge object|domain=Biology, Computer science}}\n'
                      '== References ==\n* [https://example.org Source]\n',
                      {"domain": "Biology, Computer science", "entity_type": "Concept"}, ["Biology"]),
                "b": ("== Technical ==\n<math>a=b</math>", {}, []),
                "c": ("{{Knowledge object|domain=Biology}}\n"
                      "== References ==\n* Smith, textbook.",
                      {"domain": "Biology", "entity_type": "Concept"}, ["Biology"]),
                "d": ("{{#cargo_declare:_table=Knowledge_requests}}", {}, []),
            }
            for key, (source, identity, cats) in docs.items():
                entry = next(x for x in index if x["id"] == key)
                data = {**entry, "source": source,
                        "parsed": {"identity": identity, "categories": cats},
                        "validation": {"status": "pass"}}
                (root / "page" / (key + ".json")).write_text(json.dumps(data))
            for name, value in [("build-meta", meta), ("pages", index),
                                ("graph", graph), ("ontology", objects)]:
                (root / (name + ".json")).write_text(json.dumps(value))
            report = mod.audit_pages(root)
            self.assertEqual(report["summary"]["staged_pages"], 4)
            self.assertEqual(report["summary"]["canonical_objects"], 2)
            rows = {r["title"]: r for r in report["rows"]}
            self.assertEqual(rows["Biological computation"]["checks"]["K05"]["status"], "UNVERIFIED")
            self.assertEqual(rows["Biological computation"]["checks"]["K06"]["status"], "UNVERIFIED")
            self.assertEqual(rows["Biological computation"]["checks"]["K12"]["status"], "UNVERIFIED")
            self.assertEqual(rows["Genetics"]["checks"]["K12"]["status"], "NEEDS_WORK")
            self.assertEqual(rows["Genetics"]["checks"]["K06"]["status"], "UNVERIFIED")
            self.assertEqual(rows["Biological computation/Technical"]["checks"]["K14"]["status"], "UNVERIFIED")
            self.assertEqual(rows["Template:Knowledge request"]["checks"]["K16"]["status"], "UNVERIFIED")
            self.assertEqual(rows["Genetics"]["checks"]["K01"]["status"], "UNVERIFIED")
            self.assertEqual(rows["Genetics"]["runtime_status"], "not_verified_against_live_mediawiki")


if __name__ == "__main__":
    unittest.main()
