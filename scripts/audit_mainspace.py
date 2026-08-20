#!/usr/bin/env python3
"""Describe the deployable Main namespace without pretending every file is an article.

This audit is descriptive. It separates compatibility redirects, Book Matter/subpages,
knowledge objects, domain exemplars, and other content pages, and flags very short
non-redirect pages for human review. File length is never treated as quality by itself.
"""

import json
import re
from pathlib import Path

ROOT = Path("Main")
OUT = Path("v2-mainspace-audit.json")
REDIRECT_RE = re.compile(r"^\s*#redirect\s*\[\[([^\]]+)\]\]", re.I | re.M)
CATEGORY_RE = re.compile(r"\[\[\s*Category:([^\]|#]+)", re.I)
KNOWLEDGE_OBJECT_RE = re.compile(r"{{\s*Knowledge object\b", re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
TEMPLATE_RE = re.compile(r"{{.*?}}", re.S)
CATEGORY_LINK_RE = re.compile(r"\[\[\s*Category:[^\]]+\]\]", re.I)


def title_from_path(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return rel[:-10].replace("_", " ")  # strip .mediawiki


def visible_text_size(text: str) -> int:
    """Rough descriptive signal only; not a MediaWiki parser or quality score."""
    cleaned = COMMENT_RE.sub("", text)
    cleaned = TEMPLATE_RE.sub("", cleaned)
    cleaned = CATEGORY_LINK_RE.sub("", cleaned)
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    cleaned = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", cleaned)
    cleaned = re.sub(r"\[\[([^\]]+)\]\]", r"\1", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return len(cleaned)


def classify(path: Path, text: str, categories: list[str]) -> str:
    if REDIRECT_RE.search(text):
        return "compatibility_or_title_redirect"
    if path.name == "Main Page.mediawiki":
        return "main_page"
    if "Domain exemplars" in categories:
        return "domain_exemplar"
    if len(path.relative_to(ROOT).parts) > 1:
        return "book_matter_or_subpage"
    if KNOWLEDGE_OBJECT_RE.search(text):
        return "knowledge_object"
    return "other_main_content"


def main() -> None:
    files = sorted(ROOT.rglob("*.mediawiki"))
    rows = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        redirect = REDIRECT_RE.search(text)
        categories = sorted({c.strip() for c in CATEGORY_RE.findall(text)})
        kind = classify(path, text, categories)
        visible = visible_text_size(text)
        rows.append(
            {
                "path": path.as_posix(),
                "title": title_from_path(path),
                "bytes": path.stat().st_size,
                "visible_text_chars_approx": visible,
                "kind": kind,
                "redirect_target": redirect.group(1).strip() if redirect else None,
                "categories": categories,
                "knowledge_object": bool(KNOWLEDGE_OBJECT_RE.search(text)),
                "subpage": len(path.relative_to(ROOT).parts) > 1,
                "review_short_content": bool(
                    not redirect
                    and kind not in {"main_page", "domain_exemplar"}
                    and visible < 500
                ),
            }
        )

    kinds = {}
    for row in rows:
        kinds[row["kind"]] = kinds.get(row["kind"], 0) + 1

    short_review = [row["path"] for row in rows if row["review_short_content"]]
    report = {
        "scope": "deployable Main/**/*.mediawiki",
        "generated_by": "scripts/audit_mainspace.py",
        "interpretation": [
            "Main/ is a transport mirror of MediaWiki main namespace, not a curated reading list.",
            "Compatibility redirects are not article stubs.",
            "Byte/character counts are descriptive signals only and never quality scores.",
            "Short non-redirect pages are review candidates, not automatically bad content.",
        ],
        "total_main_mediawiki_files": len(rows),
        "kind_counts": dict(sorted(kinds.items())),
        "redirect_count": sum(row["redirect_target"] is not None for row in rows),
        "domain_exemplar_count": sum(row["kind"] == "domain_exemplar" for row in rows),
        "knowledge_object_count": sum(row["knowledge_object"] for row in rows),
        "subpage_count": sum(row["subpage"] for row in rows),
        "short_content_review_count": len(short_review),
        "short_content_review_paths": short_review,
        "pages": rows,
    }
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "pages"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
