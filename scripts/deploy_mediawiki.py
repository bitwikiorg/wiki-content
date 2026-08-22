#!/usr/bin/env python3
"""Safely deploy reviewed BITwiki repository source through the MediaWiki API.

Dry-run is the default. Execution requires explicit --execute plus bot credentials.
Existing differing pages are refused unless --overwrite-existing is also supplied.
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

REQUIRED_EXTENSIONS = {"Scribunto", "Cargo"}


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
        content_model: str,
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
        if content_model:
            params["contentmodel"] = content_model
        return self.request(params, post=True)


def extension_names(siteinfo: dict) -> set[str]:
    return {
        item.get("name", "")
        for item in siteinfo.get("extensions", [])
        if item.get("name")
    }


def preflight(client: MediaWikiClient, plan: dict) -> list[str]:
    info = client.siteinfo()
    extensions = extension_names(info)
    errors = []

    for required in REQUIRED_EXTENSIONS:
        if required not in extensions:
            errors.append(f"Required extension not reported by target: {required}")

    if not any(name in extensions for name in {"Semantic MediaWiki", "SemanticMediaWiki"}):
        errors.append("Required extension not reported by target: Semantic MediaWiki")

    if any(page["surface"] == "Module" for page in plan["pages"]) and "Scribunto" not in extensions:
        errors.append("Deployment plan contains Module pages but target lacks Scribunto")

    return errors


def selected_pages(plan: dict, args: argparse.Namespace) -> list[dict]:
    pages = plan["pages"]
    if args.max_priority is not None:
        pages = [p for p in pages if p["priority"] <= args.max_priority]
    if args.title:
        wanted = set(args.title)
        pages = [p for p in pages if p["title"] in wanted]
    return pages


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
        help="Permit updating an existing page whose text differs from repository source.",
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
    print(
        json.dumps(
            {
                "mode": "execute" if args.execute else "dry-run",
                "api": args.api,
                "selected_pages": len(pages),
                "first_priority": pages[0]["priority"] if pages else None,
                "last_priority": pages[-1]["priority"] if pages else None,
            },
            indent=2,
        )
    )

    if not args.execute:
        for page in pages:
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

    errors = preflight(client, plan)
    if errors:
        for error in errors:
            print("PRECHECK ERROR:", error, file=sys.stderr)
        return 2

    token = client.csrf_token()
    changed = 0
    skipped = 0
    refused = 0

    for page in pages:
        source = (ROOT / page["source_path"]).read_text(encoding="utf-8")
        state = client.page_state(page["title"])

        if state["exists"] and state["content"] == source:
            print("UNCHANGED", page["title"])
            skipped += 1
            continue

        if state["exists"] and not args.overwrite_existing:
            print(
                "REFUSED existing differing page (use --overwrite-existing):",
                page["title"],
                file=sys.stderr,
            )
            refused += 1
            continue

        result = client.edit(
            title=page["title"],
            text=source,
            token=token,
            summary=args.summary,
            content_model=page["content_model"],
        )
        if result.get("edit", {}).get("result") != "Success":
            print("EDIT ERROR", page["title"], json.dumps(result), file=sys.stderr)
            refused += 1
            continue

        changed += 1
        print("DEPLOYED", page["title"])

    print(json.dumps({"deployed": changed, "unchanged": skipped, "refused": refused}, indent=2))
    return 1 if refused else 0


if __name__ == "__main__":
    raise SystemExit(main())
