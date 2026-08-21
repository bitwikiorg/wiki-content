#!/usr/bin/env python3
"""Verify BITwiki compiler-facing schema projections stay synchronized.

bitwiki-runtime-schema.json is the reviewed repository authority. MediaWiki needs
an executable Lua projection and the existing Python validator consumes the same
controlled vocabularies. This audit makes duplication falsifiable instead of
allowing the three representations to drift silently.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "bitwiki-runtime-schema.json"
LUA_PATH = ROOT / "Module" / "BITwiki" / "Data" / "Schema.lua"
VALIDATOR_PATH = ROOT / "scripts" / "validate_v2.py"
OUTPUT = ROOT / "v2-runtime-schema-audit.json"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("bitwiki_validate_v2", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load scripts/validate_v2.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def lua_boolean_map(lua: str, section: str) -> set[str]:
    pattern = re.compile(
        rf"(?ms)^\s*{re.escape(section)}\s*=\s*\{{(.*?)^\s*\}},"
    )
    match = pattern.search(lua)
    if not match:
        return set()
    return set(re.findall(r'\["([^"]+)"\]\s*=\s*true', match.group(1)))


def lua_relationships(lua: str, names: set[str]) -> dict[str, dict[str, object]]:
    found: dict[str, dict[str, object]] = {}
    for name in names:
        block = re.search(
            rf'(?ms)\["{re.escape(name)}"\]\s*=\s*\{{(.*?)^\s*\}},',
            lua,
        )
        if not block:
            continue
        inverse = re.search(r'inverse_display\s*=\s*"([^"]+)"', block.group(1))
        derive = re.search(r'derive_inverse_assertion\s*=\s*(true|false)', block.group(1))
        found[name] = {
            "inverse_display": inverse.group(1) if inverse else None,
            "derive_inverse_assertion": (
                derive.group(1) == "true" if derive else None
            ),
        }
    return found


def compare_set(name: str, expected: set[str], actual: set[str], critical: list[str]):
    if expected == actual:
        return
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    critical.append(
        f"{name} drift: missing={missing or []}; extra={extra or []}"
    )


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    lua = LUA_PATH.read_text(encoding="utf-8")
    validator = load_validator_module()

    expected_entity_types = set(schema["entity_types"])
    expected_domains = set(schema["domains"])
    expected_statuses = set(schema["epistemic_statuses"])
    expected_relationships = schema.get("relationships", {})

    lua_entity_types = lua_boolean_map(lua, "entity_type")
    lua_domains = lua_boolean_map(lua, "domain")
    lua_statuses = lua_boolean_map(lua, "status")
    lua_relationship_meta = lua_relationships(lua, set(expected_relationships))

    critical: list[str] = []

    compare_set("Lua entity types", expected_entity_types, lua_entity_types, critical)
    compare_set("Lua domains", expected_domains, lua_domains, critical)
    compare_set("Lua epistemic statuses", expected_statuses, lua_statuses, critical)

    compare_set(
        "Python validator entity types",
        expected_entity_types,
        set(validator.ALLOWED_ENTITY_TYPES),
        critical,
    )
    compare_set(
        "Python validator domains",
        expected_domains,
        set(validator.ALLOWED_DOMAINS),
        critical,
    )
    compare_set(
        "Python validator epistemic statuses",
        expected_statuses,
        set(validator.ALLOWED_EPISTEMIC_STATUSES),
        critical,
    )

    for name, expected in expected_relationships.items():
        actual = lua_relationship_meta.get(name)
        if actual != expected:
            critical.append(
                f"Lua relationship metadata drift for {name!r}: "
                f"expected={expected!r}; actual={actual!r}"
            )

    version_match = re.search(r'schema_version\s*=\s*"([^"]+)"', lua)
    lua_version = version_match.group(1) if version_match else None
    if lua_version != schema.get("schema_version"):
        critical.append(
            "Lua schema version drift: "
            f"expected={schema.get('schema_version')!r}; actual={lua_version!r}"
        )

    report = {
        "status": "ok" if not critical else "error",
        "authority": str(SCHEMA_PATH.relative_to(ROOT)),
        "lua_projection": str(LUA_PATH.relative_to(ROOT)),
        "python_consumer": str(VALIDATOR_PATH.relative_to(ROOT)),
        "schema_version": schema.get("schema_version"),
        "entity_type_count": len(expected_entity_types),
        "domain_count": len(expected_domains),
        "epistemic_status_count": len(expected_statuses),
        "relationship_metadata_count": len(expected_relationships),
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
