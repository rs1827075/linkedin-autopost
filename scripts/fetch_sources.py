"""
Polls the RSS feeds listed in sources.json, compares against
state/seen_items.json, and writes any new items to state/new_items.json -
including the full extracted article text where it can be fetched, so the
drafting step has real material to work with instead of just a one-line
RSS summary.

Run this first in the pipeline. It never posts anywhere and never
calls an LLM - it just figures out "what's new" and grabs the article text.
"""
import json
import pathlib
import sys

import feedparser
import requests
import trafilatura

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCES_FILE = ROOT / "sources.json"
SEEN_FILE = ROOT / "state" / "seen_items.json"
NEW_ITEMS_FILE = ROOT / "state" / "new_items.json"

MAX_ARTICLE_CHARS = 6000  # keep prompt/cost reasonable, most detail is early in the article


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default


def fetch_article_text(url: str) -> str:
    """Best-effort full article text. Returns '' if it can't be fetched/parsed."""
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        text = trafilatura.extract(resp.text) or ""
        return text[:MAX_ARTICLE_CHARS]
    except Exception as exc:
        print(f"[warn] could not fetch full article for {url}: {exc}", file=sys.stderr)
        return ""


def main():
    sources = load_json(SOURCES_FILE, {"feeds": [], "max_items_per_run": 3})
    seen_ids = set(load_json(SEEN_FILE, []))

    new_items = []
    for feed in sources.get("feeds", []):
        parsed = feedparser.parse(feed["url"])
        if parsed.bozo and not parsed.entries:
            print(f"[warn] could not read feed '{feed['name']}' ({feed['url']}): "
                  f"{parsed.bozo_exception}", file=sys.stderr)
            continue

        for entry in parsed.entries:
            item_id = entry.get("id") or entry.get("link")
            if not item_id or item_id in seen_ids:
                continue
            new_items.append({
                "id": item_id,
                "source": feed["name"],
                "title": entry.get("title", "").strip(),
                "link": entry.get("link", ""),
                "summary": entry.get("summary", "").strip(),
                "published": entry.get("published", ""),
            })
            seen_ids.add(item_id)

    # Newest first, capped per run so we don't dump 20 drafts at once
    max_items = sources.get("max_items_per_run", 3)
    new_items = new_items[:max_items]

    # Now fetch full article text for the (small) set we're actually drafting
    for item in new_items:
        if item["link"]:
            item["content"] = fetch_article_text(item["link"])
        else:
            item["content"] = ""

    NEW_ITEMS_FILE.write_text(json.dumps(new_items, indent=2))
    SEEN_FILE.write_text(json.dumps(sorted(seen_ids), indent=2))

    print(f"Found {len(new_items)} new item(s). Wrote {NEW_ITEMS_FILE}")


if __name__ == "__main__":
    main()
