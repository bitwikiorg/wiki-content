#!/usr/bin/env python3
"""Safely deploy reviewed BITwiki repository source through the MediaWiki API.

Dry-run is the default. Execution requires explicit --execute plus bot credentials.
Before any write, the complete current deployment segment is read and preflighted.
Existing differing pages are refused unless --overwrite-existing is supplied.
Runtime checkpoints such as Cargo table creation must be explicitly acknowledged.
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import os
import sys
import urllib.parse
import urllib.request

from deployment_plan import ROOT, build_plan


class MediaWikiClient:
    def __init__(self, api_url: str):
        self.api_url = api_url
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies)
        )

    def request(self, params: dict, *, post: bool = False) -> dict:
        payload = {"format": "json", "formatversion": "2", **params}
        if post:
            data = urllib.parse.urlencode(payload).encode("utf-8")
            request = urllib.request.Request(self.api_url, data=data)
        else:
            request = urllib.request.Request(
                self.api_url + "?" + urllib.parse.urlencode(payload)
            )
        with self.opener.open(request, timeout=60) as response:
            data = json.load(response)
        if "error" in data:
            raise RuntimeError(json.dumps(data["error"], ensure_ascii=False))
        return data

    def login(self, username: str, password: str) -> None:
        token_data = self.request({"action": "query", "meta": "tokens", "type": "login"})
        token = token_data["query"]["tokens"]["logintoken"]
        result = self.request(
            {
                "action": "login",
                "lgname": username,
                "lgpassword": password,
                "lgtoken": token,
            },
            post=True,
        )
        if result.get("login", {}).get("result") != "Success":
            raise RuntimeError("MediaWiki login failed: " + json.dumps(result))

    def csrf_token(self) -> str:
        data = self.request({"action": "query", "meta": "tokens"})
        return data["query"]["tokens"]["csrftoken"]

    def siteinfo(self) -> dict:
        return self.request(
            {
                "action": "query",
                "meta": "siteinfo",
                "siprop": "general|extensions|namespaces",
            }
        )["query"]

    def page_state(self, title: str) -> dict:
        data = self.request(
            {
                "action": "query",
                "prop": "revisions",
                "titles": title,
                "rvprop": "content|contentmodel|ids",
                "rvslots": "main",
            }
        )
        page = data["query"]["pages"][0]
        if page.get("missing"):
            return {"exists": False, "title": page["title"]}
        revision = page["revisions"][0]
        slot = revision["slots"]["main"]
        return {
            "exists": True,
            "title": page["title"],
            "pageid": page["pageid"],
            "revid": revision["revid"],
            "content_model": slot.get("contentmodel"),
            "content": slot.get("content", ""),
        }

    def edit(
        self,
        *,
        title: str,
        text: str,
        token: str,
        summary: str,
        create: bool,
        content_model: str | None = None,
        base_revid: int | None = None,
    ) -> dict:
        params = {
            "action": "edit",
            "title": title,
            "text": text,
            "token": token,
            "summary": summary,
            "bot": "1",
            "assert": "user",
        }
        if create:
            params["createonly"] = "1"
            if content_model:
                params["contentmodel"] = content_model
        else:
            params["nocreate"] = "1"
            if base_revid is None:
                raise ValueError("Existing-page edit requires base_revid")
            params["baserevid"] = str(base_revid)
        return self.request(params, post=True)


def extension_names(siteinfo: dict) -> set[str]:
    return {
        item.get("name", "")
        for item in siteinfo.get("extensions", [])
        if item.get("name")
    }


def preflight_extensions(client: MediaWikiClient, pages: list[dict]) -> list[str]:
    info = client.siteinfo()
    extensions = extension_names(info)
    errors = []

    needs_scribunto = any(
        page["surface"] == "Module" or page["title"] == "Template:Knowledge object"
        for page in pages
    )
    needs_cargo = any(
        page["title"] in {"Template:Knowledge request", "BITwiki:Requested knowledge"}
        for page in pages
    )
    needs_smw = any(page["surface"] != "Module" for page in pages)

    if needs_scribunto and "Scribunto" not in extensions:
        errors.append("Selected deployment requires Scribunto but target does not report it")
    if needs_cargo and "Cargo" not in extensions:
        errors.append("Selected deployment requires Cargo but target does not report it")
    if needs_smw and not any(
        name in extensions for name in {"Semantic MediaWiki", "SemanticMediaWiki"}
    ):
        errors.append("Selected deployment requires Semantic MediaWiki but target does not report it")

    return errors


def selected_pages(plan: dict, args: argparse.Namespace) -> list[dict]:
    pages = plan["pages"]
    if args.max_priority is not None:
        pages = [p for p in pages if p["priority"] <= args.max_priority]
    if args.title:
        wanted = set(args.title)
        pages = [p for p in pages if p["title"] in wanted]
    return pages


def checkpoint_is_acknowledged(page: dict, acknowledgements: set[str]) -> bool:
    checkpoint = page.get("checkpoint_before")
    return not checkpoint or checkpoint["id"] in acknowledgements


def execution_segment(
    pages: list[dict], acknowledgements: set[str]
) -> tuple[list[dict], dict | None]:
    """Return pages safe to attempt before the first unacknowledged checkpoint."""
    segment = []
    for page in pages:
        checkpoint = page.get("checkpoint_before")
        if checkpoint and not checkpoint_is_acknowledged(page, acknowledgements):
            return segment, {"page": page, "checkpoint": checkpoint}
        segment.append(page)
    return segment, None


def read_segment_states(
    client: MediaWikiClient, pages: list[dict]
) -> dict[str, dict]:
    return {page["title"]: client.page_state(page["title"]) for page in pages}


def preflight_page_states(
    pages: list[dict], states: dict[str, dict], *, overwrite_existing: bool
) -> list[str]:
    errors = []
    for page in pages:
        state = states[page["title"]]
        source = (ROOT / page["source_path"]).read_text(encoding="utf-8")

        if state["exists"] and state["content_model"] != page["content_model"]:
            errors.append(
                f'{page["title"]}: content-model mismatch '
                f'target={state["content_model"]!r} plan={page["content_model"]!r}; '
                "change content model explicitly outside this deployer"
            )
            continue

        if (
            state["exists"]
            and state["content"] != source
            and not overwrite_existing
        ):
            errors.append(
                f'{page["title"]}: existing content differs; rerun only after review with '
                "--overwrite-existing"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api",
        default=os.environ.get("BITWIKI_API", "https://bitwiki.org/w/api.php"),
        help="MediaWiki api.php endpoint.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Perform API writes. Without this flag the command is a dry-run.",
    )
    parser.add_argument(
        "--overwrite-existing",
        action="store_true",
        help="Permit updating existing pages whose text differs from repository source.",
    )
    parser.add_argument(
        "--ack-checkpoint",
        action="append",
        default=[],
        help=(
            "Acknowledge a manual deployment checkpoint by exact ID; repeat as needed. "
            "Example: --ack-checkpoint cargo:Knowledge_requests"
        ),
    )
    parser.add_argument(
        "--max-priority",
        type=int,
        help="Deploy only records at or below this dependency priority.",
    )
    parser.add_argument(
        "--title",
        action="append",
        help="Deploy only an exact MediaWiki title; repeat for multiple titles.",
    )
    parser.add_argument(
        "--summary",
        default="Deploy reviewed BITwiki V2 source from bitwikiorg/wiki-content",
    )
    args = parser.parse_args()

    plan = build_plan()
    if plan["summary"]["critical"]:
        print(json.dumps(plan["summary"], indent=2), file=sys.stderr)
        return 2

    pages = selected_pages(plan, args)
    acknowledgements = set(args.ack_checkpoint)
    segment, blocked = execution_segment(pages, acknowledgements)
    print(
        json.dumps(
            {
                "mode": "execute" if args.execute else "dry-run",
                "api": args.api,
                "selected_pages": len(pages),
                "current_segment_pages": len(segment),
                "first_priority": pages[0]["priority"] if pages else None,
                "last_priority": pages[-1]["priority"] if pages else None,
                "acknowledged_checkpoints": sorted(acknowledgements),
                "stops_before": blocked["page"]["title"] if blocked else None,
                "required_checkpoint": blocked["checkpoint"]["id"] if blocked else None,
            },
            indent=2,
        )
    )

    if not args.execute:
        for page in pages:
            checkpoint = page.get("checkpoint_before")
            if checkpoint:
                state = (
                    "ACKNOWLEDGED"
                    if checkpoint_is_acknowledged(page, acknowledgements)
                    else "REQUIRED"
                )
                print(
                    f'CHECKPOINT {state}: {checkpoint["id"]} before {page["title"]} — '
                    f'{checkpoint["reason"]}'
                )
            print(
                f'{page["priority"]:03d} {page["content_model"]:<12} '
                f'{page["title"]} <- {page["source_path"]}'
            )
        return 0

    username = os.environ.get("BITWIKI_BOT_USER")
    password = os.environ.get("BITWIKI_BOT_PASSWORD")
    if not username or not password:
        print(
            "Execution requires BITWIKI_BOT_USER and BITWIKI_BOT_PASSWORD.",
            file=sys.stderr,
        )
        return 2

    client = MediaWikiClient(args.api)
    client.login(username, password)

    errors = preflight_extensions(client, segment)
    if errors:
        for error in errors:
            print("PRECHECK ERROR:", error, file=sys.stderr)
        return 2

    # Read the entire current segment before the first write. This prevents a known
    # differing page or content-model conflict from producing a predictable partial deploy.
    states = read_segment_states(client, segment)
    errors = preflight_page_states(
        segment,
        states,
        overwrite_existing=args.overwrite_existing,
    )
    if errors:
        for error in errors:
            print("PRECHECK ERROR:", error, file=sys.stderr)
        print("No writes were attempted.", file=sys.stderr)
        return 4

    token = client.csrf_token()
    changed = 0
    skipped = 0

    for page in segment:
        source = (ROOT / page["source_path"]).read_text(encoding="utf-8")
        state = states[page["title"]]

        if state["exists"] and state["content"] == source:
            print("UNCHANGED", page["title"])
            skipped += 1
            continue

        result = client.edit(
            title=page["title"],
            text=source,
            token=token,
            summary=args.summary,
            create=not state["exists"],
            content_model=page["content_model"] if not state["exists"] else None,
            base_revid=state.get("revid") if state["exists"] else None,
        )
        if result.get("edit", {}).get("result") != "Success":
            print("EDIT ERROR", page["title"], json.dumps(result), file=sys.stderr)
            print(
                "Deployment stopped immediately; earlier successful edits, if any, remain applied.",
                file=sys.stderr,
            )
            return 5

        changed += 1
        print("DEPLOYED", page["title"])

    print(json.dumps({"deployed": changed, "unchanged": skipped}, indent=2))

    if blocked:
        checkpoint = blocked["checkpoint"]
        page = blocked["page"]
        print(
            f'STOPPED at checkpoint {checkpoint["id"]} before {page["title"]}: '
            f'{checkpoint["reason"]}',
            file=sys.stderr,
        )
        print(
            "Complete and verify the runtime checkpoint, then rerun with "
            f'--ack-checkpoint {checkpoint["id"]}.',
            file=sys.stderr,
        )
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
