#!/usr/bin/env python3
"""Audit non-deployable knowledge-request records, not a public wiki/Cargo queue.

Repository file visibility is public. This audit does not supply private storage,
prove live wiki retirement, validate research quality or publish a workflow UI.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUESTS = ROOT / "ops" / "knowledge-requests.json"
OUTPUT = ROOT / "v2-workflow-audit.json"
RUNTIME_SCHEMA = json.loads(
    (ROOT / "bitwiki-runtime-schema.json").read_text(encoding="utf-8")
)
ALLOWED_DOMAINS = set(RUNTIME_SCHEMA["domains"])
REQUIRED_FIELDS = ("request", "reason", "needed_depth", "status")
ALL_FIELDS = (
    "request", "reason", "candidate_domains", "source_leads",
    "needed_depth", "status", "canonical_page", "notes"
)
ACTIVE_STATUSES = {"requested", "researching", "drafting", "review"}
ALLOWED_STATUSES = ACTIVE_STATUSES | {"satisfied", "declined"}


def normalize(value: object) -> str:
    return re.sub(r"\s+", " ", value.strip()) if isinstance(value, str) else ""


def canonical_source(title: str) -> Path | None:
    title = normalize(title)
    if not title:
        return None
    if ":" not in title:
        return ROOT / "Main" / f"{title}.mediawiki"
    prefix, local = title.split(":", 1)
    roots = {
        "BITwiki": "BITwiki", "Project": "BITwiki", "Category": "Category",
        "Concept": "Concept", "Property": "Property", "Template": "Template",
        "Portal": "Portal", "Help": "Help"
    }
    root = roots.get(prefix)
    return ROOT / root / f"{local}.mediawiki" if root else None


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    if not REQUESTS.exists():
        errors.append("Non-deployable ops/knowledge-requests.json is missing.")
        data = {}
    else:
        try:
            data = json.loads(REQUESTS.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            errors.append(f"Operational request JSON is invalid: {exc}")
            data = {}

    calls = data.get("records", []) if isinstance(data, dict) else []
    if not isinstance(calls, list) or not calls:
        errors.append("Operational request queue must be a nonempty array.")
        calls = []

    # Detect incoming links to titles retired from the public wiki namespace.
    # This only inspects source-controlled wiki pages, not historical archives or
    # non-deployable repository documents.
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    retired = re.compile(
        r"\[\[\s*BITwiki\s*:\s*"
        r"(?:Computational scope|Requested knowledge|Deployment prerequisites)"
        r"\s*(?:[\]|#])|\[\[\s*Template\s*:\s*Knowledge request"
        r"\s*(?:[\]|#])|\{\{\s*Knowledge request\b",
        re.IGNORECASE,
    )
    for spec in manifest["mediawiki_substrate"]["source_control_mappings"].values():
        source_root = ROOT / spec["path"]
        for public_source in source_root.rglob("*.mediawiki"):
            if retired.search(public_source.read_text(encoding="utf-8")):
                errors.append(
                    "Public page still links or invokes a retired operational title: "
                    + public_source.relative_to(ROOT).as_posix()
                )

    # Prevent silent reintroduction into public MediaWiki source.
    for forbidden in (
        ROOT / "BITwiki" / "Requested knowledge.mediawiki",
        ROOT / "Template" / "Knowledge request.mediawiki",
    ):
        if forbidden.exists():
            errors.append(
                "Retired public-wiki request source still exists: "
                + forbidden.relative_to(ROOT).as_posix()
            )

    status_counts: Counter[str] = Counter()
    domain_counts: Counter[str] = Counter()
    seen: dict[str, int] = {}
    duplicates: list[str] = []
    conflicts: list[dict[str, str]] = []
    missing_canonical: list[str] = []
    invalid_domains: list[dict[str, str]] = []
    incomplete: list[dict[str, object]] = []
    records: list[dict[str, object]] = []

    for index, call in enumerate(calls, start=1):
        if not isinstance(call, dict):
            errors.append(f"Record {index} is not an object.")
            continue
        missing = [key for key in REQUIRED_FIELDS if not normalize(call.get(key))]
        if missing:
            incomplete.append({"record": index, "missing": missing})
            errors.append(f"Record {index} missing: {', '.join(missing)}.")
        extra = set(call) - set(ALL_FIELDS)
        if extra:
            errors.append(f"Record {index} has unknown fields: {sorted(extra)}.")

        request = normalize(call.get("request"))
        status = normalize(call.get("status")).casefold()
        canonical = normalize(call.get("canonical_page"))
        domains = [
            normalize(item) for item in normalize(call.get("candidate_domains")).split(",")
            if normalize(item)
        ]
        if request:
            key = request.casefold()
            if key in seen:
                duplicates.append(request)
                errors.append(f"Duplicate request {request!r} at records {seen[key]} and {index}.")
            else:
                seen[key] = index
        if status:
            status_counts[status] += 1
            if status not in ALLOWED_STATUSES:
                errors.append(f"Record {request!r} has invalid status {status!r}.")
        for domain in domains:
            domain_counts[domain] += 1
            if domain not in ALLOWED_DOMAINS:
                invalid_domains.append({"request": request, "domain": domain})
                errors.append(f"Uncontrolled candidate Domain {domain!r} in {request!r}.")
        if request and status in ACTIVE_STATUSES:
            source = ROOT / "Main" / f"{request}.mediawiki"
            if source.exists():
                rel = source.relative_to(ROOT).as_posix()
                conflicts.append({"request": request, "path": rel})
                errors.append(f"Active request {request!r} exists as Main source {rel}.")
        if status == "satisfied":
            if not canonical:
                missing_canonical.append(request)
                errors.append(f"Satisfied request {request!r} has no canonical_page.")
            else:
                source = canonical_source(canonical)
                if source is None or not source.exists():
                    errors.append(f"Satisfied request {request!r} references absent {canonical!r}.")
        elif canonical:
            warnings.append(f"Active/non-satisfied request {request!r} has canonical_page {canonical!r}.")
        records.append({
            "request": request, "status": status, "candidate_domains": domains,
            "needed_depth": normalize(call.get("needed_depth")),
            "canonical_page": canonical
        })

    report = {
        "status": "ok" if not errors else "error",
        "purpose": "Validate repository-only operational request data without publishing it to MediaWiki.",
        "source": REQUESTS.relative_to(ROOT).as_posix(),
        "repository_visibility": "public; not confidential",
        "published_wiki_queue": False,
        "request_count": len(calls),
        "status_counts": dict(sorted(status_counts.items())),
        "active_request_count": sum(status_counts[s] for s in ACTIVE_STATUSES),
        "candidate_domain_counts": dict(sorted(domain_counts.items())),
        "duplicate_requests": duplicates,
        "incomplete_records": incomplete,
        "invalid_candidate_domains": invalid_domains,
        "active_request_canonical_conflicts": conflicts,
        "satisfied_missing_canonical": missing_canonical,
        "records": records,
        "warnings": warnings,
        "errors": errors,
    }
    OUTPUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
