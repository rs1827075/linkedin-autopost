"""
Polls the RSS feeds listed in sources.json, compares against
state/seen_items.json, and writes any new items to state/new_items.json.

Run this first in the pipeline. It never posts anywhere and never
calls an LLM - it just figures out "what's new since last time".
"""
import json
import pathlib
import sys

import feedparser

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCES_FILE = ROOT / "sources.json"
SEEN_FILE = ROOT / "state" / "seen_items.json"
NEW_ITEMS_FILE = ROOT / "state" / "new_items.json"


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default


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

    NEW_ITEMS_FILE.write_text(json.dumps(new_items, indent=2))
    SEEN_FILE.write_text(json.dumps(sorted(seen_ids), indent=2))

    print(f"Found {len(new_items)} new item(s). Wrote {NEW_ITEMS_FILE}")


if __name__ == "__main__":
    main()
