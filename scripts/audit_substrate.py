#!/usr/bin/env python3
"""Audit actual use of BITwiki's MediaWiki/SMW runtime substrate.

The report is intentionally descriptive. It counts executable primitives in
source-controlled surfaces and compares repository mappings with captured live
MediaWiki site information and the live-template inventory.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
SITEINFO = ROOT / "archive-v1" / "siteinfo.json"
LIVE_TEMPLATES = ROOT / "archive-v1" / "templates" / "index.json"
OUTPUT = ROOT / "v2-substrate-audit.json"

SOURCE_ROOTS = (
    "Main",
    "BITwiki",
    "Portal",
    "Template",
    "Property",
    "Category",
    "Concept",
    "Module",
    "SMWSchema",
    "MediaWiki",
    "Help",
)
SOURCE_SUFFIXES = {".mediawiki", ".lua", ".css", ".js", ".json"}

PATTERNS = {
    "smw_ask": re.compile(r"\{\{\s*#ask\s*:", re.I),
    "smw_concept": re.compile(r"\{\{\s*#concept\s*:", re.I),
    "smw_subobject": re.compile(r"\{\{\s*#subobject\s*:", re.I),
    "scribunto_invoke": re.compile(r"\{\{\s*#invoke\s*:", re.I),
    "cargo_declare": re.compile(r"\{\{\s*#cargo_declare\s*:", re.I),
    "cargo_store": re.compile(r"\{\{\s*#cargo_store\s*:", re.I),
    "cargo_query": re.compile(r"\{\{\s*#cargo_query\s*:", re.I),
    "includeonly": re.compile(r"<includeonly>", re.I),
    "onlyinclude": re.compile(r"<onlyinclude>", re.I),
    "noinclude": re.compile(r"<noinclude>", re.I),
    "main_namespace_transclusion": re.compile(r"\{\{\s*:[^{}|\n]+", re.I),
}
SEMANTIC_ANNOTATION = re.compile(r"\[\[([^\[\]|:]+)::", re.I)

INTENTIONALLY_NOT_DEPLOYED_NAMESPACES = {
    "Talk",
    "User",
    "User talk",
    "BITwiki talk",
    "File",
    "File talk",
    "MediaWiki talk",
    "Template talk",
    "Help talk",
    "Category talk",
    "Property talk",
    "Concept talk",
    "smw/schema talk",
    "Module talk",
}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_files() -> list[Path]:
    found = []
    for root_name in SOURCE_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES:
                found.append(path)
    return sorted(found)


def namespace_name(item: dict) -> str:
    if item.get("id") == 0:
        return "Main"
    return item.get("name", "")


def main() -> int:
    manifest = read_json(MANIFEST)
    siteinfo = read_json(SITEINFO)
    template_index = read_json(LIVE_TEMPLATES)

    files = source_files()
    primitive_counts = Counter()
    primitive_files: dict[str, list[str]] = {name: [] for name in PATTERNS}
    property_counts = Counter()
    surface_counts = Counter()

    for path in files:
        rel = relative(path)
        surface_counts[path.relative_to(ROOT).parts[0]] += 1
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for name, pattern in PATTERNS.items():
            matches = pattern.findall(text)
            if matches:
                primitive_counts[name] += len(matches)
                primitive_files[name].append(rel)

        for prop in SEMANTIC_ANNOTATION.findall(text):
            property_counts[prop.strip()] += 1

    namespace_records = [
        item
        for item in siteinfo["query"]["namespaces"].values()
        if item.get("id", -1) >= 0
    ]
    configured_namespaces = sorted(
        {namespace_name(item) for item in namespace_records if namespace_name(item)},
        key=str.casefold,
    )
    extensions = sorted(
        {
            item.get("name", "")
            for item in siteinfo["query"].get("extensions", [])
            if item.get("name")
        },
        key=str.casefold,
    )

    substrate = manifest.get("mediawiki_substrate", {})
    mappings = substrate.get("source_control_mappings", {})
    mapped_paths = {spec["path"] for spec in mappings.values() if spec.get("path")}
    missing_mapped_roots = sorted(
        path
        for path in mapped_paths
        if not (ROOT / path.rstrip("/")).exists()
    )
    configured_but_unmapped = sorted(
        namespace
        for namespace in configured_namespaces
        if namespace not in mappings
        and namespace not in INTENTIONALLY_NOT_DEPLOYED_NAMESPACES
    )

    title_projections = sorted(
        namespace
        for namespace, spec in mappings.items()
        if spec.get("kind") == "title projection"
    )
    projections_that_are_configured_namespaces = sorted(
        set(title_projections) & set(configured_namespaces)
    )

    live_template_records = template_index.get("records", [])
    declared_live_template_count = template_index.get("count")
    live_template_titles = sorted(item["title"] for item in live_template_records)
    live_template_usage = {
        item["title"]: item.get("transclusion_count", 0)
        for item in live_template_records
    }
    source_controlled_template_titles = sorted(
        f"Template:{path.stem}"
        for path in (ROOT / "Template").glob("*.mediawiki")
    )
    missing_live_templates = sorted(
        set(live_template_titles) - set(source_controlled_template_titles)
    )

    all_dirs = [
        path
        for path in ROOT.rglob("*")
        if path.is_dir()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
    ]
    missing_readmes = sorted(
        relative(path)
        for path in all_dirs
        if not (path / "README.md").exists()
    )

    warnings = []
    if primitive_counts["cargo_declare"] == 0:
        warnings.append(
            "Cargo is installed but no source-controlled Cargo table declaration was found; "
            "keep this at zero until a repeated-data workflow justifies a table."
        )
    if primitive_counts["cargo_store"] == 0:
        warnings.append("No source-controlled Cargo storage call was found.")
    if primitive_counts["smw_subobject"] == 0:
        warnings.append(
            "No SMW subobject usage was found; introduce subobjects only for qualified/nested facts."
        )

    critical = []
    if missing_mapped_roots:
        critical.append("Mapped source roots missing: " + ", ".join(missing_mapped_roots))
    if declared_live_template_count != len(live_template_records):
        critical.append(
            "Live template inventory count mismatch: index declares "
            f"{declared_live_template_count}, records contain {len(live_template_records)}."
        )
    if declared_live_template_count and not live_template_titles:
        critical.append(
            "Live template inventory declares templates but no template titles were parsed."
        )
    if missing_live_templates:
        critical.append(
            "Current live templates absent from Template/: "
            + ", ".join(missing_live_templates)
        )
    if missing_readmes:
        critical.append("Directories without README.md: " + ", ".join(missing_readmes))
    if configured_but_unmapped:
        critical.append(
            "Configured content/runtime namespaces without repository mapping: "
            + ", ".join(configured_but_unmapped)
        )

    report = {
        "status": "ok" if not critical else "error",
        "purpose": (
            "Measure actual use of MediaWiki, Semantic MediaWiki, Scribunto, Cargo "
            "and transclusion primitives instead of inferring architecture from prose."
        ),
        "siteinfo_snapshot": str(SITEINFO.relative_to(ROOT)),
        "configured_namespaces": configured_namespaces,
        "installed_extensions": extensions,
        "source_control_mappings": mappings,
        "configured_but_unmapped": configured_but_unmapped,
        "title_projections": title_projections,
        "title_projections_also_configured_as_namespaces": projections_that_are_configured_namespaces,
        "source_files_scanned": len(files),
        "source_surface_file_counts": dict(sorted(surface_counts.items())),
        "primitive_counts": {name: primitive_counts.get(name, 0) for name in PATTERNS},
        "primitive_files": {
            name: sorted(paths)
            for name, paths in primitive_files.items()
            if paths
        },
        "semantic_property_source_syntax_counts": dict(
            sorted(
                property_counts.items(),
                key=lambda item: (-item[1], item[0].casefold()),
            )
        ),
        "live_template_inventory_declared_count": declared_live_template_count,
        "live_template_records_count": len(live_template_records),
        "live_template_titles": live_template_titles,
        "live_template_transclusion_counts": dict(
            sorted(live_template_usage.items(), key=lambda item: item[0].casefold())
        ),
        "source_controlled_template_titles": source_controlled_template_titles,
        "missing_live_templates": missing_live_templates,
        "missing_mapped_roots": missing_mapped_roots,
        "missing_readmes": missing_readmes,
        "warnings": warnings,
        "critical": critical,
    }

    OUTPUT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not critical else 1


if __name__ == "__main__":
    raise SystemExit(main())
