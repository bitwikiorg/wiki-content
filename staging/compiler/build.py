#!/usr/bin/env python3
"""Build an inspectable static staging projection from BITwiki's MediaWiki source.

This compiler is deliberately read-only with respect to the canonical corpus. It
parses the existing namespace-native files, derives inspection artifacts, and
writes everything under build/staging/ for GitHub Pages or local inspection.
"""

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
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
STAGING_ROOT = ROOT / "staging"
FRONTEND_ROOT = STAGING_ROOT / "frontend"
DEFAULT_OUT = ROOT / "build" / "staging"

HEADING_RE = re.compile(r"^(=+)\s*(.*?)\s*\1\s*$", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\[\]]+)\]\]")
TEMPLATE_RE = re.compile(r"\{\{\s*([^{}|\n]+)(.*?)\}\}", re.DOTALL)
INVOKE_RE = re.compile(r"\{\{\s*#invoke\s*:\s*([^|}\n]+)", re.IGNORECASE)
CATEGORY_RE = re.compile(r"\[\[Category:([^\]|]+)(?:\|[^\]]*)?\]\]", re.IGNORECASE)
SEMANTIC_LINK_RE = re.compile(r"\[\[([^\[\]|:]+?)::([^\]|]+)(?:\|[^\]]*)?\]\]")
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)


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
    specs: list[NamespaceSpec] = []
    mappings = manifest["mediawiki_substrate"]["source_control_mappings"]
    for namespace, mapping in mappings.items():
        prefix = "" if namespace == "Main" else f"{namespace}:"
        specs.append(
            NamespaceSpec(
                directory=mapping["path"].rstrip("/"),
                title_prefix=prefix,
                content_model=mapping.get("content_model", "wikitext"),
                kind=mapping.get("kind", "namespace"),
            )
        )

    for namespace, directory in manifest.get("title_projection_paths", {}).items():
        specs.append(
            NamespaceSpec(
                directory=directory.rstrip("/"),
                title_prefix=f"{namespace}:",
                content_model="wikitext",
                kind="title projection",
            )
        )
    return specs


def title_from_path(spec: NamespaceSpec, path: Path) -> str:
    relative = path.relative_to(ROOT / spec.directory)
    local = str(relative.with_suffix("")).replace("\\", "/")
    local = urllib.parse.unquote(local).replace("/", "/")
    return f"{spec.title_prefix}{local}"


def content_model_for(spec: NamespaceSpec, path: Path) -> str:
    suffix = path.suffix.casefold()
    if suffix == ".lua":
        return "Scribunto/Lua"
    if suffix == ".css":
        return "CSS"
    if suffix == ".js":
        return "JavaScript"
    return spec.content_model


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
    if not match:
        return {}
    return split_template_params("|" + match.group(1))


def clean_target(target: str) -> str:
    return target.strip().replace("_", " ")


def classify_wikilink(raw: str) -> tuple[str, str | None, str | None]:
    # Returns target, relation/property, display label.
    target_part, *label_parts = raw.split("|", 1)
    label = label_parts[0].strip() if label_parts else None
    if "::" in target_part:
        prop, target = target_part.split("::", 1)
        return clean_target(target), prop.strip(), label
    return clean_target(target_part), None, label


def parse_page(source: str, relationship_names: set[str]) -> dict[str, Any]:
    source_no_comments = COMMENT_RE.sub("", source)
    identity = parse_knowledge_object(source_no_comments)

    headings = [
        {"level": len(match.group(1)), "title": re.sub(r"''+", "", match.group(2)).strip()}
        for match in HEADING_RE.finditer(source_no_comments)
    ]

    categories = sorted({clean_target(item) for item in CATEGORY_RE.findall(source_no_comments)})
    templates: set[str] = set()
    for match in TEMPLATE_RE.finditer(source_no_comments):
        name = match.group(1).strip()
        if not name or name.startswith("#") or name.startswith("!"):
            continue
        templates.add(name if ":" in name else f"Template:{name}")

    modules = sorted({f"Module:{clean_target(name)}" for name in INVOKE_RE.findall(source_no_comments)})

    semantic: list[dict[str, str]] = []
    wikilinks: set[str] = set()
    properties: set[str] = set()
    for match in WIKILINK_RE.finditer(source_no_comments):
        raw = match.group(1).strip()
        target, prop, _label = classify_wikilink(raw)
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
        if lowered.startswith("category:") or lowered.startswith("file:") or lowered.startswith("image:"):
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
        raw = html.unescape(match.group(1))
        target, _prop, label = classify_wikilink(raw)
        if target.casefold().startswith("category:"):
            return ""
        shown = html.escape(label or target)
        return f'<a href="#/page/{stable_id(target)}">{shown}</a>'

    escaped = re.sub(r"\[\[([^\[\]]+)\]\]", wiki_link, escaped)

    def ext_link(match: re.Match[str]) -> str:
        url = match.group(1)
        label = match.group(2) or url
        return f'<a href="{html.escape(url)}" target="_blank" rel="noreferrer">{html.escape(label)}</a>'

    escaped = re.sub(r"\[(https?://[^\s\]]+)(?:\s+([^\]]+))?\]", ext_link, escaped)
    return escaped


def render_preview(source: str, content_model: str) -> str:
    if content_model != "wikitext":
        return f'<pre class="source-code">{html.escape(source)}</pre>'

    text = COMMENT_RE.sub("", source)
    # The inspector renders the staging identity card separately; suppress metadata templates.
    text = re.sub(r"\{\{\s*Source status\b.*?\}\}\s*", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"\{\{\s*Knowledge object\b.*?\}\}\s*", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<noinclude>.*?</noinclude>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = CATEGORY_RE.sub("", text)

    output: list[str] = []
    in_list = False
    in_pre = False
    paragraph: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            joined = " ".join(part.strip() for part in paragraph if part.strip())
            if joined:
                output.append(f"<p>{inline_markup(joined)}</p>")
            paragraph = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if line.strip() == "<pre>":
            flush_paragraph()
            if in_list:
                output.append("</ul>")
                in_list = False
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
            if in_list:
                output.append("</ul>")
                in_list = False
            level = min(max(len(heading.group(1)), 2), 6)
            output.append(f"<h{level}>{inline_markup(heading.group(2))}</h{level}>")
            continue

        if re.match(r"^\*+\s+", line):
            flush_paragraph()
            if not in_list:
                output.append("<ul>")
                in_list = True
            item = re.sub(r"^\*+\s+", "", line)
            output.append(f"<li>{inline_markup(item)}</li>")
            continue

        if line.startswith("{|" ) or line.startswith("|-") or line.startswith("|}") or line.startswith("!") or line.startswith("|"):
            flush_paragraph()
            if in_list:
                output.append("</ul>")
                in_list = False
            output.append(f'<div class="wikitext-raw-line">{inline_markup(line)}</div>')
            continue

        if not line.strip():
            flush_paragraph()
            if in_list:
                output.append("</ul>")
                in_list = False
            continue

        paragraph.append(line)

    flush_paragraph()
    if in_list:
        output.append("</ul>")
    return "\n".join(output)


def namespace_name(title: str) -> str:
    return title.split(":", 1)[0] if ":" in title else "Main"


def resolve_target(raw_target: str, known_titles: set[str]) -> str | None:
    target = clean_target(raw_target).lstrip(":")
    if target in known_titles:
        return target
    # MediaWiki's first-letter behavior is approximated for staging lookup only.
    if target:
        candidate = target[0].upper() + target[1:]
        if candidate in known_titles:
            return candidate
    return None


def build_graph(pages: list[dict[str, Any]], relationships: set[str]) -> dict[str, Any]:
    known_titles = {page["title"] for page in pages}
    id_by_title = {page["title"]: page["id"] for page in pages}
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()

    def add_edge(source: str, target_title: str, edge_type: str, layer: str, resolved: bool = True) -> None:
        target_id = id_by_title.get(target_title)
        key = (source, target_title, edge_type, layer)
        if key in seen:
            return
        seen.add(key)
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
            resolved_title = resolve_target(target, known_titles)
            add_edge(source_id, resolved_title or target, "Wiki link", "structural", resolved=bool(resolved_title))
        for category in parsed["categories"]:
            target = f"Category:{category}"
            add_edge(source_id, target, "Category", "structural", resolved=target in known_titles)
        for template in parsed["templates"]:
            add_edge(source_id, template, "Template", "runtime", resolved=template in known_titles)
        for module in parsed["modules"]:
            add_edge(source_id, module, "Invokes", "runtime", resolved=module in known_titles)
        for prop in parsed["properties"]:
            add_edge(source_id, prop, "Uses property", "runtime", resolved=prop in known_titles)
        for semantic in parsed["semantic"]:
            if semantic["property"] not in relationships:
                continue
            target = semantic["target"]
            resolved_title = resolve_target(target, known_titles)
            add_edge(
                source_id,
                resolved_title or target,
                semantic["property"],
                "semantic",
                resolved=bool(resolved_title),
            )

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


def validate_identity(identity: dict[str, str], schema: dict[str, Any]) -> list[dict[str, str]]:
    if not identity:
        return []
    issues: list[dict[str, str]] = []
    required = ["entity_type", "domain", "status", "provenance"]
    for field in required:
        if not identity.get(field):
            issues.append({"severity": "error", "code": "missing_identity", "field": field})
    controls = {
        "entity_type": set(schema.get("entity_types", [])),
        "domain": set(schema.get("domains", [])),
        "status": set(schema.get("epistemic_statuses", [])),
    }
    for field, allowed in controls.items():
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
            if path.name.casefold() == "readme.md":
                continue
            title = title_from_path(spec, path)
            source = path.read_text(encoding="utf-8")
            parsed = parse_page(source, relationships) if path.suffix.casefold() == ".mediawiki" else {
                "identity": {}, "headings": [], "categories": [], "templates": [], "modules": [], "properties": [], "semantic": [], "wikilinks": []
            }
            model = content_model_for(spec, path)
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
    return pages


def promotion_model(page: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    mappings = manifest["mediawiki_substrate"]["source_control_mappings"]
    namespace = page["namespace"]
    mapping = mappings.get(namespace)
    if namespace == "BITwiki":
        mapping = mappings.get("BITwiki")
    deployable = bool(mapping and mapping.get("kind") == "namespace")
    parsed = page["parsed"]
    deps = sorted(set(parsed["templates"] + parsed["modules"] + parsed["properties"]))
    return {
        "target_title": page["title"],
        "namespace": namespace,
        "content_model": page["content_model"],
        "source_path": page["source_path"],
        "deployable": deployable,
        "validation_status": page["validation"]["status"],
        "dependencies": deps,
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
    site.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    page_index: list[dict[str, Any]] = []
    ontology: list[dict[str, Any]] = []
    for page in pages:
        promotion = promotion_model(page, manifest)
        page_doc = {**page, "promotion": promotion}
        write_json(data_dir / "page" / f"{page['id']}.json", page_doc)
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
                "headings": [heading["title"] for heading in page["parsed"]["headings"]],
                "entity_type": page["parsed"]["identity"].get("entity_type"),
                "domain": page["parsed"]["identity"].get("domain"),
            }
            for page in pages
        ],
    )

    shutil.copy2(FRONTEND_ROOT / "index.html", site / "index.html")
    shutil.copy2(FRONTEND_ROOT / "styles.css", site / "styles.css")
    shutil.copy2(FRONTEND_ROOT / "app.js", site / "app.js")
    common_css = ROOT / "MediaWiki" / "Common.css"
    if common_css.exists():
        shutil.copy2(common_css, site / "mediawiki-common.css")
    else:
        (site / "mediawiki-common.css").write_text("", encoding="utf-8")

    build_meta = {
        "project": "BITwiki staging workbench",
        "source_repository": manifest["repository"],
        "source_sha": os.environ.get("GITHUB_SHA", "local"),
        "page_count": len(pages),
        "ontology_object_count": len(ontology),
        "graph_node_count": len(graph["nodes"]),
        "graph_edge_count": len(graph["edges"]),
        "authority": "inspection projection only; MediaWiki source remains unchanged",
    }
    write_json(data_dir / "build-meta.json", build_meta)
    (site / ".nojekyll").write_text("", encoding="utf-8")
    return build_meta


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
