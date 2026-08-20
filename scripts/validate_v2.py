#!/usr/bin/env python3
"""Validate deployable BITwiki V2 wikitext by MediaWiki role.

Filesystem roots are transport/source-control projections, not the ontology.
Validation rules therefore differ for content, templates, semantic schema,
runtime configuration, and navigation title projections.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


WIKITEXT_ROOTS = [
    "Main",
    "BITwiki",
    "Portal",  # title projection; not a configured namespace in captured siteinfo
    "Template",
    "Property",
    "Category",
    "Concept",
    "SMWSchema",
    "MediaWiki",
    "Help",
]

# Runtime/schema payloads are deliberately excluded from category/template
# reference parsing because their content models can contain syntax that merely
# resembles wikitext.
REFERENCE_SCAN_ROOTS = {
    "Main",
    "BITwiki",
    "Portal",
    "Template",
    "Property",
    "Category",
    "Concept",
    "Help",
}
CATEGORY_REQUIRED_ROOTS = {"Main", "BITwiki", "Portal"}
IDENTITY_SCAN_ROOTS = {"Main", "BITwiki", "Portal", "Category", "Concept", "Help"}

CATEGORY_RE = re.compile(r"\[\[\s*Category:([^\]|#]+)", re.I)
TEMPLATE_RE = re.compile(r"(?<!\{)\{\{(?!\{)\s*([^{}|\n]+)")
REDIRECT_RE = re.compile(r"^\s*#redirect\s*\[\[", re.I | re.M)
LITERAL_BLOCK_RE = re.compile(
    r"<!--.*?-->|<(pre|nowiki|syntaxhighlight|source)\b[^>]*>.*?</\1\s*>",
    re.I | re.S,
)

MAGIC_WORDS = {
    "PAGENAME", "PAGENAMEE", "FULLPAGENAME", "FULLPAGENAMEE",
    "BASEPAGENAME", "BASEPAGENAMEE", "SUBPAGENAME", "SUBPAGENAMEE",
    "ROOTPAGENAME", "ROOTPAGENAMEE", "NAMESPACE", "NAMESPACEE",
    "NAMESPACENUMBER", "TALKSPACE", "TALKSPACEE", "SUBJECTSPACE",
    "SUBJECTSPACEE", "ARTICLESPACE", "ARTICLESPACEE", "TALKPAGENAME",
    "TALKPAGENAMEE", "SUBJECTPAGENAME", "SUBJECTPAGENAMEE",
    "ARTICLEPAGENAME", "ARTICLEPAGENAMEE", "REVISIONID", "REVISIONDAY",
    "REVISIONDAY2", "REVISIONMONTH", "REVISIONMONTH1", "REVISIONYEAR",
    "REVISIONTIMESTAMP", "REVISIONUSER", "CURRENTYEAR", "CURRENTMONTH",
    "CURRENTMONTH1", "CURRENTMONTHNAME", "CURRENTMONTHABBREV", "CURRENTDAY",
    "CURRENTDAY2", "CURRENTDOW", "CURRENTDAYNAME", "CURRENTTIME",
    "CURRENTHOUR", "CURRENTWEEK", "CURRENTTIMESTAMP", "LOCALYEAR",
    "LOCALMONTH", "LOCALMONTH1", "LOCALMONTHNAME", "LOCALMONTHABBREV",
    "LOCALDAY", "LOCALDAY2", "LOCALDOW", "LOCALDAYNAME", "LOCALTIME",
    "LOCALHOUR", "LOCALWEEK", "LOCALTIMESTAMP", "NUMBEROFPAGES",
    "NUMBEROFARTICLES", "NUMBEROFFILES", "NUMBEROFEDITS", "NUMBEROFVIEWS",
    "NUMBEROFUSERS", "NUMBEROFADMINS", "NUMBEROFACTIVEUSERS",
    "NUMBERINGROUP", "NUMBERINGROUPE", "CONTENTLANG", "CONTENTLANGUAGE",
    "DIRECTIONMARK", "DIRMARK", "SITENAME", "SERVER", "SERVERNAME",
    "SCRIPTPATH", "STYLEPATH", "CURRENTVERSION", "PROTECTIONLEVEL",
    "PROTECTIONEXPIRY", "DISPLAYTITLE", "DEFAULTSORT",
}

ALLOWED_ENTITY_TYPES = {
    "Concept", "Method", "Protocol", "Implementation", "Project", "Dataset",
    "Person", "Organization", "Event", "Publication", "Location", "Technology",
}
ALLOWED_DOMAINS = {
    "Systems science", "Science", "Biology", "Computer science", "Mathematics",
    "Philosophy", "Technology", "Electronics", "Energy", "Engineering",
    "Chemistry", "Physics", "Medicine",
}
ALLOWED_EPISTEMIC_STATUSES = {
    "Hypothetical", "Emerging", "Supported", "Well-supported", "Established",
    "Disputed",
}
REQUIRED_KNOWLEDGE_FIELDS = ("entity_type", "domain", "status", "provenance")


def title(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("_", " ").strip())


def files(root: str) -> list[Path]:
    path = Path(root)
    return sorted(path.rglob("*.mediawiki")) if path.exists() else []


def executable_text(text: str) -> str:
    return LITERAL_BLOCK_RE.sub("", text)


def template_params(text: str, name: str) -> dict[str, str] | None:
    """Parse current line-oriented V2 template calls for identity validation."""
    match = re.search(r"{{\s*" + re.escape(name) + r"\b(.*?)}}", text, re.I | re.S)
    if not match:
        return None

    params: dict[str, str] = {}
    for part in match.group(1).split("|")[1:]:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = title(key).casefold().replace(" ", "_")
        value = title(value)
        if key:
            params[key] = value
    return params


def split_domains(domain_text: str) -> list[str]:
    return [title(item) for item in domain_text.split(",") if title(item)]


def main() -> None:
    all_files = [path for root in WIKITEXT_ROOTS for path in files(root)]

    category_pages = {
        title(path.relative_to("Category").as_posix()[:-10])
        for path in files("Category")
    }
    template_pages = {
        title(path.relative_to("Template").as_posix()[:-10])
        for path in files("Template")
    }

    category_refs: dict[str, list[str]] = {}
    template_refs: dict[str, list[str]] = {}
    uncategorized: list[str] = []
    knowledge_objects: list[str] = []
    missing_knowledge_fields: list[dict[str, object]] = []
    invalid_entity_types: list[dict[str, str]] = []
    invalid_domains: list[dict[str, str]] = []
    invalid_epistemic_statuses: list[dict[str, str]] = []
    exemplar_domains: set[str] = set()

    for path in all_files:
        text = path.read_text(encoding="utf-8")
        parsed = executable_text(text)
        root = path.parts[0]

        categories: list[str] = []
        if root in REFERENCE_SCAN_ROOTS:
            categories = sorted(
                {title(item) for item in CATEGORY_RE.findall(parsed) if "{" not in item}
            )
            for category in categories:
                category_refs.setdefault(category, []).append(str(path))

            templates = []
            for raw in TEMPLATE_RE.findall(parsed):
                template = title(raw)
                lower = template.casefold()
                if (
                    not template
                    or template.startswith(("#", ":", "!"))
                    or "{" in template
                    or lower.startswith(("subst:", "safesubst:"))
                ):
                    continue
                if template.upper() in MAGIC_WORDS:
                    continue
                if ":" in template and template.split(":", 1)[0].casefold() in {
                    "int", "msg", "msgnw"
                }:
                    continue
                templates.append(template)

            for template in sorted(set(templates)):
                template_refs.setdefault(template, []).append(str(path))

        if root in CATEGORY_REQUIRED_ROOTS and not categories:
            uncategorized.append(str(path))

        if root in IDENTITY_SCAN_ROOTS and not REDIRECT_RE.search(parsed):
            ko = template_params(parsed, "Knowledge object")
            if ko is None:
                continue

            knowledge_objects.append(str(path))
            missing = [field for field in REQUIRED_KNOWLEDGE_FIELDS if not ko.get(field)]
            if missing:
                missing_knowledge_fields.append({"path": str(path), "missing": missing})

            entity_type = ko.get("entity_type")
            if entity_type and entity_type not in ALLOWED_ENTITY_TYPES:
                invalid_entity_types.append({"path": str(path), "value": entity_type})

            domain_text = ko.get("domain")
            if domain_text:
                domains = split_domains(domain_text)
                for domain in domains:
                    if domain not in ALLOWED_DOMAINS:
                        invalid_domains.append({"path": str(path), "value": domain})
                if "Domain exemplars" in categories:
                    exemplar_domains.update(domains)

            status = ko.get("status")
            if status and status not in ALLOWED_EPISTEMIC_STATUSES:
                invalid_epistemic_statuses.append({"path": str(path), "value": status})

    missing_categories = {
        key: value for key, value in category_refs.items() if key not in category_pages
    }
    missing_templates = {
        key: value for key, value in template_refs.items() if key not in template_pages
    }

    required_domains = sorted(ALLOWED_DOMAINS)
    missing_domain_categories = [d for d in required_domains if d not in category_pages]
    missing_domain_portals = [
        d for d in required_domains if not Path("Portal", d + ".mediawiki").exists()
    ]

    exemplars = [
        path for path in files("Main")
        if "[[Category:Domain exemplars]]" in path.read_text(encoding="utf-8")
    ]
    missing_domain_exemplar_domains = [
        d for d in required_domains if d not in exemplar_domains
    ]

    report = {
        "deployable_wikitext_files": len(all_files),
        "wikitext_roots": WIKITEXT_ROOTS,
        "reference_scan_roots": sorted(REFERENCE_SCAN_ROOTS),
        "category_required_roots": sorted(CATEGORY_REQUIRED_ROOTS),
        "category_pages": len(category_pages),
        "template_pages": len(template_pages),
        "distinct_category_references": len(category_refs),
        "distinct_template_references": len(template_refs),
        "missing_category_pages": missing_categories,
        "missing_template_pages": missing_templates,
        "uncategorized_content_or_navigation_pages": uncategorized,
        "required_domain_count": len(required_domains),
        "required_domain_categories_missing": missing_domain_categories,
        "required_domain_portal_title_projections_missing": missing_domain_portals,
        "domain_exemplar_count": len(exemplars),
        "domain_exemplar_domains": sorted(exemplar_domains),
        "domain_exemplar_domains_missing": missing_domain_exemplar_domains,
        "domain_exemplars": [str(path) for path in exemplars],
        "knowledge_object_count": len(knowledge_objects),
        "knowledge_object_pages": knowledge_objects,
        "knowledge_object_required_fields_missing": missing_knowledge_fields,
        "invalid_entity_type_values": invalid_entity_types,
        "invalid_domain_values": invalid_domains,
        "invalid_epistemic_status_values": invalid_epistemic_statuses,
        "controlled_vocabularies": {
            "entity_types": sorted(ALLOWED_ENTITY_TYPES),
            "domains": sorted(ALLOWED_DOMAINS),
            "epistemic_statuses": sorted(ALLOWED_EPISTEMIC_STATUSES),
        },
        "notes": [
            "Portal/ is validated as a title projection, not asserted to be a configured namespace.",
            "Compatibility/runtime Template pages are not required to join a category merely to satisfy CI.",
            "SMWSchema/ and MediaWiki/ payloads are counted but not parsed as ordinary wikitext references.",
            "Module/Lua is audited by scripts/audit_substrate.py rather than parsed as wikitext.",
        ],
    }

    report["valid"] = not any([
        missing_categories,
        missing_templates,
        uncategorized,
        missing_domain_categories,
        missing_domain_portals,
        missing_domain_exemplar_domains,
        missing_knowledge_fields,
        invalid_entity_types,
        invalid_domains,
        invalid_epistemic_statuses,
    ])

    Path("v2-validation.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["valid"] else 1)


if __name__ == "__main__":
    main()
