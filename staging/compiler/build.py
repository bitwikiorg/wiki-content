#!/usr/bin/env python3
"""Build a read-only, inspectable staging projection of BITwiki MediaWiki source."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
FRONTEND_ROOT = ROOT / "staging" / "frontend"
DEFAULT_OUT = ROOT / "build" / "staging"

HEADING_RE = re.compile(r"^(=+)\s*(.*?)\s*\1\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
TEMPLATE_RE = re.compile(r"\{\{\s*([^{}|\n]+)(.*?)\}\}", re.DOTALL)
INVOKE_RE = re.compile(r"\{\{\s*#invoke\s*:\s*([^|}\n]+)", re.IGNORECASE)
CATEGORY_RE = re.compile(r"\[\[Category:([^\]|]+)(?:\|[^\]]*)?\]\]", re.IGNORECASE)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
LITERAL_BLOCK_RE = re.compile(
    r"<(pre|nowiki|source|syntaxhighlight)\b[^>]*>.*?</\1\s*>",
    re.IGNORECASE | re.DOTALL,
)


@dataclass(frozen=True)
class NamespaceSpec:
    directory: str
    title_prefix: str
    content_model: str
    kind: str


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_id(title: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.casefold()).strip("-") or "page"
    digest = hashlib.sha1(title.encode("utf-8")).hexdigest()[:8]
    return f"{base}-{digest}"


def namespace_specs(manifest: dict[str, Any]) -> list[NamespaceSpec]:
    """Return each repository source surface exactly once."""
    specs: list[NamespaceSpec] = []
    seen_dirs: set[str] = set()

    for namespace, mapping in manifest["mediawiki_substrate"]["source_control_mappings"].items():
        directory = mapping["path"].rstrip("/")
        if directory in seen_dirs:
            continue
        seen_dirs.add(directory)
        specs.append(
            NamespaceSpec(
                directory=directory,
                title_prefix="" if namespace == "Main" else f"{namespace}:",
                content_model=mapping.get("content_model", "wikitext"),
                kind=mapping.get("kind", "namespace"),
            )
        )

    # Some projected title spaces (currently Portal/) are also represented in
    # source_control_mappings. Directory identity wins so transport metadata
    # cannot duplicate staged knowledge objects.
    for namespace, raw_directory in manifest.get("title_projection_paths", {}).items():
        directory = raw_directory.rstrip("/")
        if directory in seen_dirs:
            continue
        seen_dirs.add(directory)
        specs.append(NamespaceSpec(directory, f"{namespace}:", "wikitext", "title projection"))

    return specs


def title_from_path(spec: NamespaceSpec, path: Path) -> str:
    relative = path.relative_to(ROOT / spec.directory)
    local = urllib.parse.unquote(str(relative.with_suffix("")).replace("\\", "/"))
    return f"{spec.title_prefix}{local}"


def content_model_for(spec: NamespaceSpec, path: Path) -> str:
    suffix = path.suffix.casefold()
    if suffix == ".lua":
        return "Scribunto/Lua"
    if suffix == ".css":
        return "CSS"
    if suffix == ".js":
        return "JavaScript"
    if spec.content_model == "smw/schema":
        return "smw/schema"
    return "wikitext"


def split_template_params(raw: str) -> dict[str, str]:
    params: dict[str, str] = {}
    for piece in raw.split("|")[1:]:
        if "=" not in piece:
            continue
        key, value = piece.split("=", 1)
        params[key.strip()] = value.strip()
    return params


def parse_knowledge_object(source: str) -> dict[str, str]:
    match = re.search(r"\{\{\s*Knowledge object\b(.*?)\}\}", source, re.IGNORECASE | re.DOTALL)
    return split_template_params("|" + match.group(1)) if match else {}


def clean_target(target: str) -> str:
    return target.strip().replace("_", " ")


def classify_wikilink(raw: str) -> tuple[str, str | None, str | None]:
    target_part, *label_parts = raw.split("|", 1)
    label = label_parts[0].strip() if label_parts else None
    if "::" in target_part:
        prop, target = target_part.split("::", 1)
        return clean_target(target), prop.strip(), label
    return clean_target(target_part), None, label


def empty_parse() -> dict[str, Any]:
    return {
        "identity": {},
        "headings": [],
        "categories": [],
        "templates": [],
        "modules": [],
        "properties": [],
        "semantic": [],
        "wikilinks": [],
    }


def semantic_source(source: str) -> str:
    """Remove text MediaWiki treats as literal before semantic extraction.

    Examples inside <pre>, <nowiki>, <source>, or <syntaxhighlight> are source
    documentation, not executable template calls or semantic assertions.
    """
    text = COMMENT_RE.sub("", source)
    return LITERAL_BLOCK_RE.sub("", text)


def parse_page(source: str, relationship_names: set[str]) -> dict[str, Any]:
    text = semantic_source(source)
    identity = parse_knowledge_object(text)
    headings = [
        {"level": len(m.group(1)), "title": re.sub(r"''+", "", m.group(2)).strip()}
        for m in HEADING_RE.finditer(text)
    ]
    categories = sorted({clean_target(item) for item in CATEGORY_RE.findall(text)})

    templates: set[str] = set()
    for match in TEMPLATE_RE.finditer(text):
        name = match.group(1).strip()
        if name and not name.startswith(("#", "!")):
            templates.add(name if ":" in name else f"Template:{name}")

    modules = sorted({f"Module:{clean_target(name)}" for name in INVOKE_RE.findall(text)})
    semantic: list[dict[str, Any]] = []
    wikilinks: set[str] = set()
    properties: set[str] = set()

    for match in WIKILINK_RE.finditer(text):
        target, prop, _label = classify_wikilink(match.group(1).strip())
        if not target:
            continue
        if prop:
            properties.add(f"Property:{prop}")
            semantic.append(
                {
                    "property": prop,
                    "target": target,
                    "is_relationship": str(prop in relationship_names).lower(),
                }
            )
            continue
        lowered = target.casefold()
        if lowered.startswith(("category:", "file:", "image:")):
            continue
        wikilinks.add(target.lstrip(":"))

    return {
        "identity": identity,
        "headings": headings,
        "categories": categories,
        "templates": sorted(templates),
        "modules": modules,
        "properties": sorted(properties),
        "semantic": semantic,
        "wikilinks": sorted(wikilinks),
    }


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"'''''(.*?)'''''", r"<strong><em>\1</em></strong>", escaped)
    escaped = re.sub(r"'''(.*?)'''", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"''(.*?)''", r"<em>\1</em>", escaped)

    def wiki_link(match: re.Match[str]) -> str:
        target, _prop, label = classify_wikilink(html.unescape(match.group(1)))
        if target.casefold().startswith("category:"):
            return ""
        return f'<a href="#/page/{stable_id(target)}">{html.escape(label or target)}</a>'

    escaped = re.sub(r"\[\[([^\[\]]+)\]\]", wiki_link, escaped)

    def external_link(match: re.Match[str]) -> str:
        url = match.group(1)
        label = match.group(2) or url
        return f'<a href="{html.escape(url)}" target="_blank" rel="noreferrer">{html.escape(label)}</a>'

    return re.sub(r"\[(https?://[^\s\]]+)(?:\s+([^\]]+))?\]", external_link, escaped)


def render_preview(source: str, content_model: str) -> str:
    if content_model != "wikitext":
        return f'<pre class="source-code">{html.escape(source)}</pre>'

    text = COMMENT_RE.sub("", source)
    text = re.sub(r"\{\{\s*Source status\b.*?\}\}\s*", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"\{\{\s*Knowledge object\b.*?\}\}\s*", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<noinclude>.*?</noinclude>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = CATEGORY_RE.sub("", text)

    output: list[str] = []
    paragraph: list[str] = []
    in_list = False
    in_pre = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            joined = " ".join(part.strip() for part in paragraph if part.strip())
            if joined:
                output.append(f"<p>{inline_markup(joined)}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            output.append("</ul>")
            in_list = False

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.strip() == "<pre>":
            flush_paragraph()
            close_list()
            output.append('<pre class="source-code">')
            in_pre = True
            continue
        if line.strip() == "</pre>":
            output.append("</pre>")
            in_pre = False
            continue
        if in_pre:
            output.append(html.escape(line) + "\n")
            continue

        heading = re.match(r"^(=+)\s*(.*?)\s*\1\s*$", line)
        if heading:
            flush_paragraph()
            close_list()
            level = min(max(len(heading.group(1)), 2), 6)
            output.append(f"<h{level}>{inline_markup(heading.group(2))}</h{level}>")
            continue

        if re.match(r"^\*+\s+", line):
            flush_paragraph()
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append(f"<li>{inline_markup(re.sub(r'^\*+\s+', '', line))}</li>")
            continue

        if line.startswith(("{|", "|-", "|}", "!", "|")):
            flush_paragraph()
            close_list()
            output.append(f'<div class="wikitext-raw-line">{inline_markup(line)}</div>')
            continue

        if not line.strip():
            flush_paragraph()
            close_list()
            continue
        paragraph.append(line)

    flush_paragraph()
    close_list()
    return "\n".join(output)


def namespace_name(title: str) -> str:
    return title.split(":", 1)[0] if ":" in title else "Main"


def resolve_target(raw_target: str, known_titles: set[str]) -> str | None:
    target = clean_target(raw_target).lstrip(":")
    if target in known_titles:
        return target
    if target:
        candidate = target[0].upper() + target[1:]
        if candidate in known_titles:
            return candidate
    return None


def validate_identity(identity: dict[str, str], schema: dict[str, Any]) -> list[dict[str, str]]:
    if not identity:
        return []
    issues: list[dict[str, str]] = []
    for field in ("entity_type", "domain", "status", "provenance"):
        if not identity.get(field):
            issues.append({"severity": "error", "code": "missing_identity", "field": field})

    controlled = {
        "entity_type": set(schema.get("entity_types", [])),
        "domain": set(schema.get("domains", [])),
        "status": set(schema.get("epistemic_statuses", [])),
    }
    for field, allowed in controlled.items():
        value = identity.get(field)
        if value and value not in allowed:
            issues.append({"severity": "error", "code": "invalid_controlled_value", "field": field, "value": value})
    return issues


def collect_pages(manifest: dict[str, Any], schema: dict[str, Any]) -> list[dict[str, Any]]:
    relationships = set(schema.get("relationships", {}).keys())
    pages: list[dict[str, Any]] = []
    allowed_suffixes = {".mediawiki", ".lua", ".css", ".js"}

    for spec in namespace_specs(manifest):
        directory = ROOT / spec.directory
        if not directory.exists():
            continue
        for path in sorted(p for p in directory.rglob("*") if p.is_file() and p.suffix.casefold() in allowed_suffixes):
            title = title_from_path(spec, path)
            source = path.read_text(encoding="utf-8")
            model = content_model_for(spec, path)
            parsed = parse_page(source, relationships) if model == "wikitext" else empty_parse()
            issues = validate_identity(parsed["identity"], schema)
            pages.append(
                {
                    "id": stable_id(title),
                    "title": title,
                    "namespace": namespace_name(title),
                    "source_path": str(path.relative_to(ROOT)).replace("\\", "/"),
                    "content_model": model,
                    "projection_kind": spec.kind,
                    "source": source,
                    "preview_html": render_preview(source, model),
                    "parsed": parsed,
                    "validation": {
                        "status": "error" if any(issue["severity"] == "error" for issue in issues) else "pass",
                        "issues": issues,
                    },
                }
            )

    ids = [page["id"] for page in pages]
    titles = [page["title"] for page in pages]
    paths = [page["source_path"] for page in pages]
    if len(ids) != len(set(ids)) or len(titles) != len(set(titles)) or len(paths) != len(set(paths)):
        raise RuntimeError("staging projection produced duplicate page ids, titles, or source paths")
    return pages


def build_graph(pages: list[dict[str, Any]], relationships: set[str]) -> dict[str, Any]:
    known_titles = {page["title"] for page in pages}
    id_by_title = {page["title"]: page["id"] for page in pages}
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()

    def add(source: str, target_title: str, edge_type: str, layer: str, resolved: bool) -> None:
        key = (source, target_title, edge_type, layer)
        if key in seen:
            return
        seen.add(key)
        target_id = id_by_title.get(target_title)
        edges.append(
            {
                "source": source,
                "target": target_id,
                "target_title": target_title,
                "type": edge_type,
                "layer": layer,
                "resolved": bool(target_id) and resolved,
            }
        )

    for page in pages:
        source_id = page["id"]
        parsed = page["parsed"]
        for target in parsed["wikilinks"]:
            resolved = resolve_target(target, known_titles)
            add(source_id, resolved or target, "Wiki link", "structural", bool(resolved))
        for category in parsed["categories"]:
            target = f"Category:{category}"
            add(source_id, target, "Category", "structural", target in known_titles)
        for template in parsed["templates"]:
            add(source_id, template, "Template", "runtime", template in known_titles)
        for module in parsed["modules"]:
            add(source_id, module, "Invokes", "runtime", module in known_titles)
        for prop in parsed["properties"]:
            add(source_id, prop, "Uses property", "runtime", prop in known_titles)
        for semantic in parsed["semantic"]:
            if semantic["property"] in relationships:
                resolved = resolve_target(semantic["target"], known_titles)
                add(source_id, resolved or semantic["target"], semantic["property"], "semantic", bool(resolved))

    nodes = [
        {
            "id": page["id"],
            "title": page["title"],
            "namespace": page["namespace"],
            "entity_type": page["parsed"]["identity"].get("entity_type"),
            "domain": page["parsed"]["identity"].get("domain"),
        }
        for page in pages
    ]
    return {"nodes": nodes, "edges": edges}


def promotion_model(page: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    mapping = manifest["mediawiki_substrate"]["source_control_mappings"].get(page["namespace"])
    parsed = page["parsed"]
    return {
        "target_title": page["title"],
        "namespace": page["namespace"],
        "content_model": page["content_model"],
        "source_path": page["source_path"],
        "deployable": bool(mapping and mapping.get("kind") == "namespace"),
        "validation_status": page["validation"]["status"],
        "dependencies": sorted(set(parsed["templates"] + parsed["modules"] + parsed["properties"])),
        "deployment_executor": manifest["mediawiki_substrate"]["deployment_contract"]["executor"],
        "write_policy": manifest["mediawiki_substrate"]["deployment_contract"]["existing_page_policy"],
        "live_comparison": "not evaluated by static staging build",
    }


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build(out_dir: Path) -> dict[str, Any]:
    manifest = load_json(ROOT / "manifest.json")
    schema = load_json(ROOT / "bitwiki-runtime-schema.json")
    pages = collect_pages(manifest, schema)
    graph = build_graph(pages, set(schema.get("relationships", {}).keys()))

    site = out_dir / "site"
    data_dir = site / "data"
    if out_dir.exists():
        shutil.rmtree(out_dir)
    data_dir.mkdir(parents=True, exist_ok=True)

    page_index: list[dict[str, Any]] = []
    ontology: list[dict[str, Any]] = []
    for page in pages:
        write_json(data_dir / "page" / f"{page['id']}.json", {**page, "promotion": promotion_model(page, manifest)})
        page_index.append(
            {
                "id": page["id"],
                "title": page["title"],
                "namespace": page["namespace"],
                "source_path": page["source_path"],
                "content_model": page["content_model"],
                "entity_type": page["parsed"]["identity"].get("entity_type"),
                "domain": page["parsed"]["identity"].get("domain"),
                "status": page["parsed"]["identity"].get("status"),
                "validation_status": page["validation"]["status"],
            }
        )
        if page["parsed"]["identity"]:
            ontology.append(
                {
                    "id": page["id"],
                    "title": page["title"],
                    **page["parsed"]["identity"],
                    "semantic": page["parsed"]["semantic"],
                }
            )

    write_json(data_dir / "pages.json", page_index)
    write_json(data_dir / "ontology.json", {"schema": schema, "objects": ontology})
    write_json(data_dir / "graph.json", graph)
    write_json(
        data_dir / "search.json",
        [
            {
                "id": page["id"],
                "title": page["title"],
                "namespace": page["namespace"],
                "headings": [h["title"] for h in page["parsed"]["headings"]],
                "entity_type": page["parsed"]["identity"].get("entity_type"),
                "domain": page["parsed"]["identity"].get("domain"),
            }
            for page in pages
        ],
    )

    for name in ("index.html", "styles.css", "app.js"):
        shutil.copy2(FRONTEND_ROOT / name, site / name)
    common_css = ROOT / "MediaWiki" / "Common.css"
    if common_css.exists():
        shutil.copy2(common_css, site / "mediawiki-common.css")
    else:
        (site / "mediawiki-common.css").write_text("", encoding="utf-8")

    meta = {
        "project": "BITwiki staging workbench",
        "source_repository": manifest["repository"],
        "source_sha": os.environ.get("GITHUB_SHA", "local"),
        "page_count": len(pages),
        "ontology_object_count": len(ontology),
        "graph_node_count": len(graph["nodes"]),
        "graph_edge_count": len(graph["edges"]),
        "authority": "inspection projection only; MediaWiki source remains unchanged",
    }
    write_json(data_dir / "build-meta.json", meta)
    (site / ".nojekyll").write_text("", encoding="utf-8")
    return meta


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    meta = build(args.out.resolve())
    print(json.dumps(meta, indent=2))
    if meta["page_count"] == 0:
        raise SystemExit("staging compiler found no source pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
