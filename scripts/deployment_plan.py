#!/usr/bin/env python3
"""Build and validate the complete BITwiki MediaWiki deployment plan.

The plan is derived from manifest.json source-control mappings. Discovery is recursive:
nested Module paths are first-class deployable pages, not an optional convention.
Manual runtime checkpoints are encoded where repository page ordering alone cannot
complete deployment (for example Cargo table creation).
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
OUTPUT = ROOT / "v2-deployment-plan.json"

SOURCE_SUFFIXES = {".mediawiki", ".lua", ".css", ".js"}
PREFIXES = {
    "Main": "",
    "BITwiki": "BITwiki:",
    "Template": "Template:",
    "Property": "Property:",
    "Category": "Category:",
    "Concept": "Concept:",
    "Module": "Module:",
    "MediaWiki": "MediaWiki:",
    "Help": "Help:",
    "smw/schema": "smw/schema:",
    "Portal": "Portal:",
}
SURFACE_PRIORITY = {
    "smw/schema": 100,
    "Property": 200,
    "Concept": 250,
    "Module": 300,
    "Template": 400,
    "MediaWiki": 450,
    "Category": 500,
    "Help": 550,
    "BITwiki": 600,
    "Main": 700,
    "Portal": 800,
}
EXPLICIT_PRIORITY = {
    "Module:BITwiki/Data/Schema": 301,
    "Module:BITwiki/Core": 302,
    "Module:BITwiki/Compiler": 303,
    "Module:Structure": 304,
    "Template:Knowledge object": 401,
    "Template:Knowledge request": 402,
    "BITwiki:Requested knowledge": 601,
}
REQUIRED_RUNTIME_CHAIN = [
    "Module:BITwiki/Data/Schema",
    "Module:BITwiki/Core",
    "Module:BITwiki/Compiler",
    "Module:Structure",
    "Template:Knowledge object",
]
MANUAL_CHECKPOINTS = {
    "BITwiki:Requested knowledge": {
        "id": "cargo:Knowledge_requests",
        "after": "Template:Knowledge request",
        "reason": (
            "Create or recreate the Cargo Knowledge_requests table after deploying "
            "Template:Knowledge request and before deploying/querying its workflow consumer."
        ),
    }
}


def read_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def strip_source_suffix(name: str) -> str:
    for suffix in sorted(SOURCE_SUFFIXES, key=len, reverse=True):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    raise ValueError(f"Unsupported deployable source suffix: {name}")


def title_for(surface: str, root: Path, path: Path) -> str:
    if surface not in PREFIXES:
        raise ValueError(f"No title prefix mapping for manifest surface {surface!r}")
    rel = path.relative_to(root).as_posix()
    local_title = unquote(strip_source_suffix(rel))
    return PREFIXES[surface] + local_title


def content_model_for(path: Path, spec: dict) -> str:
    suffix = path.suffix.lower()
    if suffix == ".lua":
        return "Scribunto"
    if suffix == ".css":
        return "css"
    if suffix == ".js":
        return "javascript"

    declared = spec.get("content_model", "wikitext")
    if declared == "Scribunto/Lua":
        return "Scribunto"
    if declared.startswith("page-specific"):
        return "wikitext"
    return declared


def iter_deployable_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if path.name == "README.md":
            continue
        if path.suffix.lower() in SOURCE_SUFFIXES:
            yield path


def build_plan() -> dict:
    manifest = read_manifest()
    mappings = manifest["mediawiki_substrate"]["source_control_mappings"]
    records = []
    critical = []

    for surface, spec in mappings.items():
        rel_root = spec.get("path")
        if not rel_root:
            critical.append(f"Surface {surface} has no source path")
            continue

        source_root = ROOT / rel_root.rstrip("/")
        if not source_root.is_dir():
            critical.append(f"Mapped source root missing: {rel_root}")
            continue

        discovered = list(iter_deployable_files(source_root))
        if not discovered:
            critical.append(f"Mapped source root contains no deployable source: {rel_root}")
            continue

        for path in discovered:
            try:
                title = title_for(surface, source_root, path)
                model = content_model_for(path, spec)
            except ValueError as exc:
                critical.append(str(exc))
                continue

            priority = EXPLICIT_PRIORITY.get(title, SURFACE_PRIORITY.get(surface, 900))
            records.append(
                {
                    "priority": priority,
                    "surface": surface,
                    "source_path": path.relative_to(ROOT).as_posix(),
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "title": title,
                    "content_model": model,
                    "kind": spec.get("kind"),
                    "extension": spec.get("extension"),
                    "checkpoint_before": MANUAL_CHECKPOINTS.get(title),
                }
            )

    records.sort(key=lambda item: (item["priority"], item["title"].casefold()))
    by_title = {item["title"]: item for item in records}

    if len(by_title) != len(records):
        seen = set()
        duplicates = []
        for item in records:
            title = item["title"]
            if title in seen:
                duplicates.append(title)
            seen.add(title)
        critical.append("Duplicate deployment titles: " + ", ".join(sorted(set(duplicates))))

    missing_chain = [title for title in REQUIRED_RUNTIME_CHAIN if title not in by_title]
    if missing_chain:
        critical.append("Required Lua compiler chain missing: " + ", ".join(missing_chain))

    chain_priorities = [by_title[t]["priority"] for t in REQUIRED_RUNTIME_CHAIN if t in by_title]
    if chain_priorities != sorted(chain_priorities) or len(set(chain_priorities)) != len(chain_priorities):
        critical.append("Lua compiler dependency chain is not strictly ordered")

    module_records = [item for item in records if item["surface"] == "Module"]
    nested_modules = [item for item in module_records if item["source_path"].count("/") > 1]
    if module_records and not nested_modules:
        critical.append("Module mapping exists but no nested Module subpages were discovered")

    for title, checkpoint in MANUAL_CHECKPOINTS.items():
        consumer = by_title.get(title)
        producer = by_title.get(checkpoint["after"])
        if not consumer:
            critical.append(f"Checkpoint consumer missing from deployment plan: {title}")
            continue
        if not producer:
            critical.append(
                f'Checkpoint producer missing from deployment plan: {checkpoint["after"]}'
            )
            continue
        if producer["priority"] >= consumer["priority"]:
            critical.append(
                f'Checkpoint {checkpoint["id"]} is not ordered after {checkpoint["after"]} '
                f"and before {title}"
            )

    summary = {
        "status": "ok" if not critical else "error",
        "deployable_pages": len(records),
        "surfaces": sorted({item["surface"] for item in records}, key=str.casefold),
        "module_pages": len(module_records),
        "nested_module_pages": len(nested_modules),
        "manual_checkpoints": sorted(
            checkpoint["id"] for checkpoint in MANUAL_CHECKPOINTS.values()
        ),
        "content_models": sorted({item["content_model"] for item in records}),
        "critical": critical,
    }
    return {
        "purpose": (
            "Complete recursive deployment contract derived from manifest.json. "
            "This is the deployable page inventory; scripts/inventory_corpus.py is semantic corpus evidence."
        ),
        "manifest": MANIFEST.name,
        "dependency_rule": "lower priority deploys before higher priority",
        "required_runtime_chain": REQUIRED_RUNTIME_CHAIN,
        "manual_checkpoints": MANUAL_CHECKPOINTS,
        "summary": summary,
        "pages": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the generated plan and exit nonzero on contract errors.",
    )
    parser.add_argument(
        "--output",
        default=str(OUTPUT),
        help="Output JSON path (default: v2-deployment-plan.json).",
    )
    args = parser.parse_args()

    plan = build_plan()
    output = Path(args.output)
    output.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(plan["summary"], indent=2, ensure_ascii=False))
    return 1 if args.check and plan["summary"]["critical"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
