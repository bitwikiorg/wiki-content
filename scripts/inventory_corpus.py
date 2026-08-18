#!/usr/bin/env python3
"""Build empirical V2 corpus and V1 classification inventories.

This script is intentionally descriptive. It does not decide which schema values are
canonical and it does not mutate wiki content. Its job is to expose what the corpus
actually encodes so ontology changes can be justified from evidence rather than
intuition.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import unquote

ROOTS = ["Main", "BITwiki", "Portal", "Template", "Property", "Category"]
LITERAL_BLOCK_RE = re.compile(
    r"<!--.*?-->|<(pre|nowiki|syntaxhighlight|source)\b[^>]*>.*?</\1\s*>",
    re.I | re.S,
)
CATEGORY_RE = re.compile(r"\[\[\s*Category:([^\]|#]+)", re.I)
REDIRECT_RE = re.compile(r"^\s*#redirect\s*\[\[\s*([^\]|#]+)", re.I | re.M)
SEMANTIC_RE = re.compile(r"\[\[\s*([^\[\]|]+?)\s*::\s*([^\]|]+)", re.I)

V1_CLASSIFICATION_PROPERTIES = {
    "has entity type",
    "has extended type",
    "has page type",
    "has domain",
    "has field",
    "has category",
    "has parent",
    "has child",
    "has parent topic",
    "parent topic",
    "has subtopic",
    "subtopic of",
    "has related topic",
    "related topic",
    "has epistemic status",
    "has epistemic tier",
}

# These are API-recorded V1 category memberships that clearly carried an identity/type job.
V1_IDENTITY_CATEGORIES = {
    "Topics",
    "Ideas",
    "Implementations",
    "Projects",
    "Protocols",
    "Datasets",
    "People",
    "Organizations",
    "Events",
    "Publications",
    "Locations",
    "Technologies",
    "Concepts",
}


def normalized(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("_", " ").strip())


def executable_text(text: str) -> str:
    return LITERAL_BLOCK_RE.sub("", text)


def mediawiki_files(root: str) -> list[Path]:
    p = Path(root)
    return sorted(p.rglob("*.mediawiki")) if p.exists() else []


def mediawiki_title(path: Path) -> str:
    root = path.parts[0]
    rel = path.relative_to(root).as_posix()
    title = unquote(rel[: -len(".mediawiki")])
    prefix = {
        "Main": "",
        "BITwiki": "BITwiki:",
        "Portal": "Portal:",
        "Template": "Template:",
        "Property": "Property:",
        "Category": "Category:",
    }[root]
    return prefix + title


def template_params(text: str, name: str) -> dict[str, str]:
    """Parse the simple, line-oriented parameter style used by current V2 templates."""
    match = re.search(r"{{\s*" + re.escape(name) + r"\b(.*?)}}", text, re.I | re.S)
    if not match:
        return {}
    params: dict[str, str] = {}
    body = match.group(1)
    for part in body.split("|")[1:]:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = normalized(key).casefold().replace(" ", "_")
        value = normalized(value)
        if key:
            params[key] = value
    return params


def semantic_annotations(text: str) -> list[dict[str, str]]:
    """Recover source-syntax annotations; this is not an exported SMW semantic store."""
    annotations = []
    for raw_property, raw_value in SEMANTIC_RE.findall(executable_text(text)):
        prop = normalized(raw_property)
        value = normalized(raw_value)
        if not prop or not value or "{" in prop:
            continue
        annotations.append({"property": prop, "value": value})
    return annotations


def sorted_counter(counter: Counter) -> dict[str, int]:
    return dict(sorted(counter.items(), key=lambda kv: (-kv[1], kv[0].casefold())))


def build_v2_inventory() -> tuple[dict, dict]:
    records = []
    namespace_counts = Counter()
    nonredirect_namespace_counts = Counter()
    category_counts = Counter()
    semantic_property_counts = Counter()
    semantic_value_counts: dict[str, Counter] = defaultdict(Counter)
    entity_types = Counter()
    domains = Counter()
    statuses = Counter()
    main_roles = Counter()
    main_canonical_without_knowledge_object = []
    incomplete_knowledge_objects = []
    v1_term_reuse = []

    for root in ROOTS:
        for path in mediawiki_files(root):
            text = path.read_text(encoding="utf-8")
            parsed = executable_text(text)
            title = mediawiki_title(path)
            redirect_match = REDIRECT_RE.search(parsed)
            redirect_target = normalized(redirect_match.group(1)) if redirect_match else None
            categories = sorted({normalized(x) for x in CATEGORY_RE.findall(parsed)})
            knowledge = template_params(parsed, "Knowledge object")
            source_status = template_params(parsed, "Source status")
            annotations = semantic_annotations(parsed)

            for category in categories:
                category_counts[category] += 1
            # Source syntax is useful evidence, but template/property implementation markup is
            # not counted as instantiated page-level semantic data.
            if root not in {"Template", "Property"}:
                for ann in annotations:
                    semantic_property_counts[ann["property"]] += 1
                    semantic_value_counts[ann["property"]][ann["value"]] += 1

            entity_type = knowledge.get("entity_type")
            domain = knowledge.get("domain")
            status = knowledge.get("status")
            provenance = knowledge.get("provenance")
            if entity_type:
                entity_types[entity_type] += 1
            if domain:
                for value in [normalized(x) for x in domain.split(",") if normalized(x)]:
                    domains[value] += 1
            if status:
                statuses[status] += 1

            if knowledge:
                missing = [
                    field
                    for field, value in {
                        "entity_type": entity_type,
                        "domain": domain,
                        "status": status,
                        "provenance": provenance,
                    }.items()
                    if not value
                ]
                if missing:
                    incomplete_knowledge_objects.append({"path": str(path), "title": title, "missing": missing})

            if root == "Main":
                if redirect_target:
                    main_roles["compatibility_or_other_redirect"] += 1
                elif title == "Main Page":
                    main_roles["main_page"] += 1
                elif knowledge:
                    main_roles["explicit_knowledge_object"] += 1
                else:
                    main_roles["other_nonredirect"] += 1
                    main_canonical_without_knowledge_object.append(str(path))

            classification_values = []
            if entity_type:
                classification_values.append(("Knowledge object.entity_type", entity_type))
            for ann in annotations:
                if ann["property"].casefold() in {"entity type", "has entity type", "page type", "has page type"}:
                    classification_values.append((ann["property"], ann["value"]))
            historical_hits = [
                {"field": field, "value": value}
                for field, value in classification_values
                if value.casefold() in {"topic", "idea"}
            ]
            if historical_hits:
                v1_term_reuse.append({"path": str(path), "title": title, "uses": historical_hits})

            namespace_counts[root] += 1
            if not redirect_target:
                nonredirect_namespace_counts[root] += 1
            records.append(
                {
                    "path": str(path),
                    "title": title,
                    "namespace": root,
                    "redirect": bool(redirect_target),
                    "redirect_target": redirect_target,
                    "categories": categories,
                    "knowledge_object": knowledge or None,
                    "source_status": source_status or None,
                    "semantic_annotation_source_syntax": annotations,
                }
            )

    summary = {
        "deployable_pages": len(records),
        "namespace_counts": sorted_counter(namespace_counts),
        "nonredirect_namespace_counts": sorted_counter(nonredirect_namespace_counts),
        "redirect_pages": sum(1 for r in records if r["redirect"]),
        "nonredirect_pages": sum(1 for r in records if not r["redirect"]),
        "main_page_roles": sorted_counter(main_roles),
        "knowledge_object_pages": sum(1 for r in records if r["knowledge_object"]),
        "entity_type_distribution_explicit": sorted_counter(entity_types),
        "domain_distribution_explicit": sorted_counter(domains),
        "epistemic_status_distribution_explicit": sorted_counter(statuses),
        "category_usage": sorted_counter(category_counts),
        "semantic_annotation_source_syntax_usage": sorted_counter(semantic_property_counts),
        "semantic_annotation_source_values": {
            prop: sorted_counter(values)
            for prop, values in sorted(semantic_value_counts.items(), key=lambda kv: kv[0].casefold())
        },
        "main_nonredirect_without_knowledge_object": sorted(main_canonical_without_knowledge_object),
        "incomplete_knowledge_objects": incomplete_knowledge_objects,
        "v2_reuse_of_v1_topic_or_idea_classification": v1_term_reuse,
    }
    inventory = {
        "scope": ROOTS,
        "interpretation": (
            "Descriptive repository evidence only. Explicit Knowledge object parameters are "
            "reported separately from source-syntax semantic annotations; absence or frequency "
            "does not by itself authorize schema changes."
        ),
        "summary": summary,
        "pages": records,
    }
    return inventory, summary


def load_v1_index() -> dict[str, dict]:
    path = Path("archive-v1/index.json")
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get("records", data if isinstance(data, list) else [])
    return {record.get("current_source_path", ""): record for record in records if record.get("current_source_path")}


def build_v1_classification_inventory() -> dict:
    index = load_v1_index()
    property_counts = Counter()
    values_by_property: dict[str, Counter] = defaultdict(Counter)
    api_category_counts = Counter()
    identity_category_counts = Counter()
    infobox_type_counts = Counter()
    pages = []
    topic_function_counts = Counter()

    v1_root = Path("archive-v1/pages/Main")
    for path in sorted(v1_root.rglob("*.mediawiki")) if v1_root.exists() else []:
        repo_path = path.as_posix()
        meta = index.get(repo_path, {})
        text = path.read_text(encoding="utf-8")
        parsed = executable_text(text)
        annotations = semantic_annotations(parsed)
        relevant = []

        # API-recorded category memberships from the exhaustive archive are implementation
        # evidence. Do not infer them again from prose/examples in the page body.
        categories = sorted(
            normalized(c.split(":", 1)[1] if c.casefold().startswith("category:") else c)
            for c in meta.get("categories", [])
        )
        for category in categories:
            api_category_counts[category] += 1
            if category in V1_IDENTITY_CATEGORIES:
                identity_category_counts[category] += 1

        for ann in annotations:
            key = ann["property"].casefold()
            if key not in V1_CLASSIFICATION_PROPERTIES:
                continue
            property_counts[ann["property"]] += 1
            values_by_property[ann["property"]][ann["value"]] += 1
            relevant.append(ann)

            if ann["value"].casefold() == "topic" and key in {"has entity type", "has extended type", "has page type"}:
                topic_function_counts["entity_or_page_type_source_syntax"] += 1
            if "topic" in key:
                topic_function_counts["hierarchy_or_topic_relation_source_syntax"] += 1
            if key in {"has domain", "has field"}:
                topic_function_counts["domain_or_field_source_syntax"] += 1

        infobox = template_params(parsed, "Infobox")
        infobox_type = infobox.get("type")
        if infobox_type:
            infobox_type_counts[infobox_type] += 1

        topic_literal = bool(re.search(r"\bTopic\b", parsed, re.I))
        if relevant or infobox_type or topic_literal or any(c in V1_IDENTITY_CATEGORIES for c in categories):
            pages.append(
                {
                    "path": repo_path,
                    "title": meta.get("title") or unquote(path.stem),
                    "pageid": meta.get("pageid"),
                    "current_revid": meta.get("current_revid"),
                    "api_recorded_categories": categories,
                    "api_recorded_templates": meta.get("templates", []),
                    "infobox_type_source_parameter": infobox_type,
                    "classification_annotation_source_syntax": relevant,
                    "contains_topic_literal": topic_literal,
                }
            )

    topic_pages = [p for p in pages if p["contains_topic_literal"]]
    return {
        "scope": "archive-v1/pages/Main",
        "interpretation": (
            "Category memberships and template callers come from the exhaustive MediaWiki API "
            "archive and are implementation evidence. Semantic/property occurrences and Infobox "
            "parameters are recovered from source syntax and may include documentation/specification "
            "examples; they therefore require page-context review before being called deployed schema behavior."
        ),
        "summary": {
            "pages_with_classification_or_topic_signal": len(pages),
            "pages_containing_topic_literal": len(topic_pages),
            "api_recorded_category_usage": sorted_counter(api_category_counts),
            "api_recorded_identity_category_usage": sorted_counter(identity_category_counts),
            "classification_annotation_source_syntax_usage": sorted_counter(property_counts),
            "classification_annotation_source_values": {
                prop: sorted_counter(values)
                for prop, values in sorted(values_by_property.items(), key=lambda kv: kv[0].casefold())
            },
            "infobox_type_source_parameter_usage": sorted_counter(infobox_type_counts),
            "topic_function_source_signal": sorted_counter(topic_function_counts),
        },
        "pages": pages,
    }


def main() -> None:
    v2_inventory, v2_summary = build_v2_inventory()
    v1_inventory = build_v1_classification_inventory()

    Path("v2-corpus-inventory.json").write_text(
        json.dumps(v2_inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    Path("v1-classification-usage.json").write_text(
        json.dumps(v1_inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print("=== V2 corpus summary ===")
    print(json.dumps(v2_summary, indent=2, ensure_ascii=False))
    print("=== V1 classification summary ===")
    print(json.dumps(v1_inventory["summary"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
