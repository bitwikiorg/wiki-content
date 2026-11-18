#!/usr/bin/env python3
"""Read-only, source-anchored BITwiki staging readiness audit.

Consumes derived staging files from staging/compiler/build.py. It does not read
or write the live wiki and does not certify factual/editorial correctness.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

SCHEMA_VERSION = "0.1.0"
RE_URL = re.compile(r"https?://[^\s<>\]\|}]+", re.I)
RE_INLINE_CITATION = re.compile(r"<ref\b|\{\{\s*(?:cite|citation|sfn)\b", re.I)
RE_REFERENCE_HEADING = re.compile(r"^={2,6}\s*(references|sources|bibliography)\s*={2,6}\s*$", re.I | re.M)
RE_REDIRECT = re.compile(r"^\s*#redirect\b", re.I)


def status(value: str, detail: str = "") -> dict[str, str]:
    return {"status": value, "detail": detail}


def classify(page: dict) -> str:
    title = page["title"]
    ns = page["namespace"]
    src = page.get("source", "")
    if RE_REDIRECT.match(src):
        return "redirect"
    if ns == "Main" and (title.endswith("/Simple") or title.endswith("/Technical")):
        return "reading_depth"
    if ns == "Main" and page.get("parsed", {}).get("identity"):
        return "knowledge_object"
    if ns == "Main":
        return "main_other"
    return "runtime_or_project"


def audit_pages(root: Path) -> dict:
    meta = json.loads((root / "build-meta.json").read_text(encoding="utf-8"))
    index = json.loads((root / "pages.json").read_text(encoding="utf-8"))
    graph = json.loads((root / "graph.json").read_text(encoding="utf-8"))
    ontology = json.loads((root / "ontology.json").read_text(encoding="utf-8"))
    object_titles = {obj["title"] for obj in ontology["objects"]}
    id_titles = {page["id"]: page["title"] for page in index}
    known_titles = {page["title"] for page in index}
    in_edges = Counter()
    out_edges = Counter()
    unresolved_links = defaultdict(list)
    unresolved_runtime = defaultdict(list)
    semantic_edges = defaultdict(list)
    graph_layer_counts = Counter()
    for edge in graph["edges"]:
        source = id_titles.get(edge["source"], edge["source"])
        target = id_titles.get(edge["target"], edge.get("target_title", edge["target"]))
        layer = edge.get("layer", "unspecified")
        graph_layer_counts[layer] += 1
        if layer == "semantic":
            out_edges[source] += 1
            in_edges[target] += 1
            semantic_edges[source].append({
                "property": edge["type"], "target": target,
                "resolved": bool(edge.get("resolved"))
            })
        elif not edge.get("resolved"):
            if layer == "runtime":
                unresolved_runtime[source].append(target)
            elif layer == "structural":
                unresolved_links[source].append(target)

    rows = []
    for entry in sorted(index, key=lambda x: (x["namespace"], x["title"].casefold())):
        source_file = root / "page" / (entry["id"] + ".json")
        if not source_file.is_file():
            raise FileNotFoundError(f"Missing staged source projection: {source_file}")
        page = json.loads(source_file.read_text(encoding="utf-8"))
        source = page.get("source", "")
        role = classify(page)
        is_obj = role == "knowledge_object"
        title = page["title"]
        parsed = page.get("parsed", {})
        identity = parsed.get("identity", {})
        domains = [d.strip() for d in identity.get("domain", "").split(",") if d.strip()]
        links = sorted(set(unresolved_links.get(title, [])))
        runtime = sorted(set(unresolved_runtime.get(title, [])))
        refs = bool(RE_REFERENCE_HEADING.search(source))
        external_urls = RE_URL.findall(source)
        inline = len(RE_INLINE_CITATION.findall(source))
        simple = f"{title}/Simple" in known_titles
        technical = f"{title}/Technical" in known_titles
        validation = page.get("validation", {}).get("status", "unknown")
        checks = {
            "K01": status("UNVERIFIED", "Interdisciplinary editorial purpose, factual quality, canonical identity and source relevance require human review; explicit computation is not required for subject admission") if is_obj else status("NOT_APPLICABLE"),
            "K02": status("PASS" if validation == "pass" else "NEEDS_WORK", "Static title/identity validation only"),
            "K03": status("UNVERIFIED", "Wikitext/content model represented in staging; live parser execution not established"),
            "K04": status("PASS" if validation == "pass" else "NEEDS_WORK", "Static identity/schema projection") if is_obj else status("NOT_APPLICABLE"),
            "K05": status("NEEDS_WORK", "No parsed Domain/Category; inspect before adding") if is_obj and (not domains or not parsed.get("categories")) else (status("UNVERIFIED", "Multi-Domain parser/SMW emission requires target verification") if is_obj and len(domains)>1 else (status("PASS", "Source-level Domain and Category found") if is_obj else status("NOT_APPLICABLE"))),
            "K06": status("NEEDS_WORK", "No source-projected incoming/outgoing typed SMW edge; review, do not fabricate") if is_obj and not (in_edges[title] + out_edges[title]) else (status("UNVERIFIED", "Source-projected typed edge(s); semantic correctness still requires review") if is_obj else status("NOT_APPLICABLE")),
            "K07": status("UNVERIFIED", "Review direction, scope, range and cited justification of typed edges") if is_obj and (in_edges[title]+out_edges[title]) else status("NOT_APPLICABLE"),
            "K08": status("NEEDS_WORK", f"{len(links)} unresolved structural reference(s) in static projection; may be wanted links") if links else (status("PASS", "No unresolved structural edges extracted") if is_obj else status("NOT_APPLICABLE")),
            "K09": status("UNVERIFIED", "Book Matter role, section reuse and source qualifications require review") if is_obj else status("NOT_APPLICABLE"),
            "K10": status("NEEDS_WORK", "Review whether missing Simple/Technical depth is warranted") if is_obj and not(simple and technical) else (status("PASS", "Both staged reading depths exist") if is_obj else status("NOT_APPLICABLE")),
            "K11": status("UNVERIFIED", "English authorship and any translations require editorial/version review") if is_obj else status("NOT_APPLICABLE"),
            "K12": status("NEEDS_WORK", "No machine-resolvable external URL or inline citation markup; named references may exist") if is_obj and not (external_urls or inline) else (status("UNVERIFIED", "Citation presence detected; claim-to-source accuracy not reviewed") if is_obj else status("NOT_APPLICABLE")),
            "K13": status("UNVERIFIED", "Public factual accuracy, licensing and responsible-use review not performed") if is_obj else status("NOT_APPLICABLE"),
            "K14": status("UNVERIFIED", "Technical/formal claims require domain-specific review") if (title.endswith("/Technical") or "<math" in source.lower() or "<syntaxhighlight" in source.lower()) else status("NOT_APPLICABLE"),
            "K15": status("UNVERIFIED", "Bounded agent-context retrieval contract not yet deployed") if is_obj else status("NOT_APPLICABLE"),
            "K16": status("UNVERIFIED", "Cargo runtime declaration/store/query must be tested separately") if "#cargo_" in source.lower() else status("NOT_APPLICABLE", "Cargo not required for ordinary knowledge objects"),
            "K17": status("UNVERIFIED", "Static source-title projection exists; live namespace/extension state unverified"),
            "K18": status("NEEDS_WORK", f"{len(runtime)} unresolved runtime dependency edge(s) in static projection") if runtime else status("UNVERIFIED", "Static dependencies extracted; target execution unverified"),
        }
        rows.append({
            "title": title,
            "source_path": entry["source_path"],
            "source_sha": meta["source_sha"],
            "namespace": entry["namespace"],
            "content_model": entry["content_model"],
            "role": role,
            "domain": domains,
            "entity_type": identity.get("entity_type", ""),
            "source_words_approx": len(re.findall(r"\b[\w-]+\b", source)),
            "source_ref_heading": refs,
            "external_url_count": len(external_urls),
            "inline_citation_markup_count": inline,
            "simple_present": simple if is_obj else None,
            "technical_present": technical if is_obj else None,
            "typed_edges_incoming": in_edges[title],
            "typed_edges_outgoing": out_edges[title],
            "typed_edges": semantic_edges.get(title, []),
            "unresolved_structural_targets": links,
            "unresolved_runtime_targets": runtime,
            "checks": checks,
            "review_status": "not_editorially_reviewed",
            "runtime_status": "not_verified_against_live_mediawiki",
        })
    objects = [row for row in rows if row["role"] == "knowledge_object"]
    summary = {
        "staged_pages": len(rows),
        "role_counts": dict(sorted(Counter(row["role"] for row in rows).items())),
        "canonical_objects": len(objects),
        "ontology_object_count": len(object_titles),
        "domain_counts": dict(sorted(Counter(d for row in objects for d in row["domain"]).items())),
        "objects_without_typed_edges": sum(not (r["typed_edges_incoming"] or r["typed_edges_outgoing"]) for r in objects),
        "objects_without_external_urls_or_inline_citation_markup": sum(not (r["external_url_count"] or r["inline_citation_markup_count"]) for r in objects),
        "objects_with_reference_heading": sum(r["source_ref_heading"] for r in objects),
        "objects_without_both_reader_depths": sum(not (r["simple_present"] and r["technical_present"]) for r in objects),
        "objects_under_500_approx_source_words": sum(r["source_words_approx"] < 500 for r in objects),
        "graph_layers": dict(sorted(graph_layer_counts.items())),
        "scope_source_catalogs": "External comparison/reference catalogs are separate Library research assets; not inferred from corpus titles or counted as articles",
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "source_sha": meta["source_sha"],
        "method": "static GitHub Pages projection (not live MediaWiki)",
        "summary": summary,
        "rows": rows,
        "limitations": [
            "Source word counts include wikitext markup and are rough sizing signals, not a quality score",
            "A References heading or URL is not proof of claim-level sourcing",
            "Missing external URLs do not mean missing named bibliographic references",
            "Parsed graph is not the live SMW database",
            "No editorial decision or publication authorization is inferred",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("build/staging/site/data"))
    parser.add_argument("--output", type=Path, default=Path("v2-staging-readiness.json"))
    args = parser.parse_args()
    report = audit_pages(args.data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "schema_version": report["schema_version"],
        "source_sha": report["source_sha"],
        "summary": report["summary"],
    }, indent=2))


if __name__ == "__main__":
    main()
