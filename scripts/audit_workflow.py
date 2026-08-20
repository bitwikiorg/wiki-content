#!/usr/bin/env python3
"""Audit BITwiki's structured knowledge-request workflow.

The request queue is operational data, not canonical subject content. This audit
checks both the Cargo template contract and the governance boundary between an
active request and a canonical Main-namespace page.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "Template" / "Knowledge request.mediawiki"
REQUESTS = ROOT / "BITwiki" / "Requested knowledge.mediawiki"
OUTPUT = ROOT / "v2-workflow-audit.json"

TABLE = "Knowledge_requests"
EXPECTED_FIELDS = [
    "Request",
    "Reason",
    "Candidate_domains",
    "Source_leads",
    "Needed_depth",
    "Status",
    "Canonical_page",
    "Notes",
]
REQUIRED_PARAMS = ("request", "reason", "needed_depth", "status")
ACTIVE_STATUSES = {"requested", "researching", "drafting", "review"}
ALLOWED_STATUSES = ACTIVE_STATUSES | {"satisfied", "declined"}
ALLOWED_DOMAINS = {
    "Systems science",
    "Science",
    "Biology",
    "Computer science",
    "Mathematics",
    "Philosophy",
    "Technology",
    "Electronics",
    "Energy",
    "Engineering",
    "Chemistry",
    "Physics",
    "Medicine",
}

REQUEST_CALL_RE = re.compile(r"{{\s*Knowledge request\b(.*?)}}", re.I | re.S)


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def parser_function_calls(text: str, name: str) -> list[str]:
    """Extract deliberately line-oriented MediaWiki parser-function calls.

    A non-greedy ``{{...}}`` regex is unsafe for Cargo storage calls because
    their values contain nested template parameters such as ``{{{request|}}}``.
    The workflow contract keeps parser-function calls line-oriented, so consume
    from the opening ``{{#name:`` line through a closing line containing only
    ``}}``. This preserves nested braces inside values without pretending to be
    a general MediaWiki parser.
    """
    start = re.compile(
        r"^\s*\{\{\s*#" + re.escape(name) + r"\s*:\s*(.*)$",
        re.I,
    )
    end = re.compile(r"^\s*\}\}\s*$")
    calls: list[str] = []
    current: list[str] | None = None

    for line in text.splitlines():
        if current is None:
            match = start.match(line)
            if match:
                current = [match.group(1)]
            continue

        if end.match(line):
            calls.append("\n".join(current))
            current = None
        else:
            current.append(line)

    return calls


def parse_call(body: str) -> dict[str, str]:
    """Parse the deliberately line-oriented calls used by this workflow."""
    params: dict[str, str] = {}
    for part in body.split("|"):
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        key = normalize(key)
        value = normalize(value)
        if key:
            params[key] = value
    return params


def canonical_source(title: str) -> Path | None:
    """Resolve supported public titles to this repository's source projections."""
    title = normalize(title)
    if not title:
        return None
    if ":" not in title:
        return ROOT / "Main" / f"{title}.mediawiki"

    prefix, local = title.split(":", 1)
    roots = {
        "BITwiki": "BITwiki",
        "Project": "BITwiki",
        "Category": "Category",
        "Concept": "Concept",
        "Property": "Property",
        "Template": "Template",
        "Portal": "Portal",
        "Help": "Help",
    }
    root = roots.get(prefix)
    if root is None:
        return None
    return ROOT / root / f"{local}.mediawiki"


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not TEMPLATE.exists():
        errors.append("Template:Knowledge request source is missing.")
        template_text = ""
    else:
        template_text = TEMPLATE.read_text(encoding="utf-8")

    if not REQUESTS.exists():
        errors.append("BITwiki:Requested knowledge source is missing.")
        request_text = ""
    else:
        request_text = REQUESTS.read_text(encoding="utf-8")

    declares = parser_function_calls(template_text, "cargo_declare")
    stores = parser_function_calls(template_text, "cargo_store")
    if len(declares) != 1:
        errors.append(f"Expected exactly one #cargo_declare call; found {len(declares)}.")
    if len(stores) != 1:
        errors.append(f"Expected exactly one #cargo_store call; found {len(stores)}.")

    declare = parse_call(declares[0]) if len(declares) == 1 else {}
    store = parse_call(stores[0]) if len(stores) == 1 else {}

    if declare.get("_table") != TABLE:
        errors.append(
            f"#cargo_declare must target {TABLE}; found {declare.get('_table')!r}."
        )
    if store.get("_table") != TABLE:
        errors.append(
            f"#cargo_store must target {TABLE}; found {store.get('_table')!r}."
        )

    declared_fields = [field for field in declare if not field.startswith("_")]
    stored_fields = [field for field in store if not field.startswith("_")]
    if declared_fields != EXPECTED_FIELDS:
        errors.append(
            "Cargo declaration fields/order differ from workflow contract: "
            f"{declared_fields!r}."
        )
    if stored_fields != EXPECTED_FIELDS:
        errors.append(
            "Cargo storage fields/order differ from workflow contract: "
            f"{stored_fields!r}."
        )
    if set(declared_fields) != set(stored_fields):
        errors.append("Cargo declared and stored field sets do not match.")

    for field in ("Request", "Reason", "Needed_depth", "Status"):
        if "mandatory" not in declare.get(field, "").casefold():
            errors.append(f"Cargo field {field} must be declared mandatory.")
    if "unique" not in declare.get("Request", "").casefold():
        errors.append("Cargo Request field must be declared unique.")

    status_declaration = declare.get("Status", "").casefold()
    for status in sorted(ALLOWED_STATUSES):
        if status not in status_declaration:
            errors.append(
                f"Cargo Status declaration does not expose allowed value {status!r}."
            )

    calls = [parse_call(body) for body in REQUEST_CALL_RE.findall(request_text)]
    if not calls:
        errors.append("Requested knowledge contains no Knowledge request records.")

    status_counts: Counter[str] = Counter()
    candidate_domain_counts: Counter[str] = Counter()
    seen: dict[str, int] = {}
    duplicate_requests: list[str] = []
    active_canonical_conflicts: list[dict[str, str]] = []
    satisfied_missing_canonical: list[str] = []
    invalid_candidate_domains: list[dict[str, str]] = []
    incomplete_records: list[dict[str, object]] = []
    records: list[dict[str, object]] = []

    for index, call in enumerate(calls, start=1):
        missing = [field for field in REQUIRED_PARAMS if not call.get(field)]
        if missing:
            incomplete_records.append({"record": index, "missing": missing})
            errors.append(
                f"Knowledge request record {index} is missing: {', '.join(missing)}."
            )

        request = normalize(call.get("request", ""))
        status = normalize(call.get("status", "")).casefold()
        canonical_page = normalize(call.get("canonical_page", ""))
        domains = [
            normalize(value)
            for value in call.get("candidate_domains", "").split(",")
            if normalize(value)
        ]

        if request:
            key = request.casefold()
            if key in seen:
                duplicate_requests.append(request)
                errors.append(
                    f"Duplicate request title {request!r} in records {seen[key]} and {index}."
                )
            else:
                seen[key] = index

        if status:
            status_counts[status] += 1
            if status not in ALLOWED_STATUSES:
                errors.append(f"Request {request!r} uses invalid status {status!r}.")

        for domain in domains:
            candidate_domain_counts[domain] += 1
            if domain not in ALLOWED_DOMAINS:
                invalid_candidate_domains.append({"request": request, "domain": domain})
                errors.append(
                    f"Request {request!r} proposes uncontrolled Domain {domain!r}."
                )

        if request and status in ACTIVE_STATUSES:
            main_path = ROOT / "Main" / f"{request}.mediawiki"
            if main_path.exists():
                rel = main_path.relative_to(ROOT).as_posix()
                active_canonical_conflicts.append({"request": request, "path": rel})
                errors.append(
                    f"Active request {request!r} already exists as canonical Main source {rel}."
                )

        if status == "satisfied":
            if not canonical_page:
                satisfied_missing_canonical.append(request)
                errors.append(
                    f"Satisfied request {request!r} must provide canonical_page."
                )
            else:
                source = canonical_source(canonical_page)
                if source is None:
                    errors.append(
                        f"Satisfied request {request!r} uses unsupported canonical title {canonical_page!r}."
                    )
                elif not source.exists():
                    errors.append(
                        f"Satisfied request {request!r} points to missing source "
                        f"{source.relative_to(ROOT).as_posix()}."
                    )

        if status != "satisfied" and canonical_page:
            warnings.append(
                f"Request {request!r} has canonical_page while status is {status!r}; verify intent."
            )

        records.append(
            {
                "request": request,
                "status": status,
                "candidate_domains": domains,
                "needed_depth": normalize(call.get("needed_depth", "")),
                "canonical_page": canonical_page,
            }
        )

    queries = [
        parse_call(body)
        for body in parser_function_calls(request_text, "cargo_query")
    ]
    workflow_queries = [
        query for query in queries if normalize(query.get("tables", "")) == TABLE
    ]
    if not workflow_queries:
        errors.append(
            f"Requested knowledge must query Cargo table {TABLE} with #cargo_query."
        )

    report = {
        "status": "ok" if not errors else "error",
        "purpose": (
            "Validate the repeated knowledge-request workflow and enforce the boundary "
            "between operational requests and canonical Main-namespace knowledge."
        ),
        "cargo_table": TABLE,
        "declared_fields": declared_fields,
        "stored_fields": stored_fields,
        "request_count": len(calls),
        "status_counts": dict(sorted(status_counts.items())),
        "active_request_count": sum(
            count for status, count in status_counts.items() if status in ACTIVE_STATUSES
        ),
        "candidate_domain_counts": dict(
            sorted(candidate_domain_counts.items(), key=lambda item: item[0].casefold())
        ),
        "cargo_query_count": len(workflow_queries),
        "duplicate_requests": duplicate_requests,
        "incomplete_records": incomplete_records,
        "invalid_candidate_domains": invalid_candidate_domains,
        "active_request_canonical_conflicts": active_canonical_conflicts,
        "satisfied_missing_canonical": satisfied_missing_canonical,
        "records": records,
        "warnings": warnings,
        "errors": errors,
    }

    OUTPUT.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
