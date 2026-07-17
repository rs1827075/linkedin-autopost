"""
Reads state/new_items.json (written by fetch_sources.py) and asks Gemini
(free tier) to draft one LinkedIn post per item. Each draft is written to
drafts/ as a markdown file for a human to review, edit, and approve via PR
merge.

This script never posts to LinkedIn. It only drafts.

Required env var: GEMINI_API_KEY (free, no credit card - get one at
https://aistudio.google.com/app/apikey)
"""
import datetime
import json
import os
import pathlib
import re
import sys

from google import genai

ROOT = pathlib.Path(__file__).resolve().parent.parent
NEW_ITEMS_FILE = ROOT / "state" / "new_items.json"
DRAFTS_DIR = ROOT / "drafts"

MODEL = "gemini-flash-lite-latest"  # free-tier available; auto-tracks newest Flash-Lite

SYSTEM_PROMPT = """You draft LinkedIn posts for a Senior Software Engineer \
specializing in Salesforce (Financial Services Cloud, Apex, LWC, Agentforce, \
integrations). Voice: informative, first-person, practical - explains what \
changed, why it matters, and a concrete use case or two. Ends by inviting \
readers to share their own use cases or thoughts.

Hard rules:
- You only know what is in the "source material" the user gives you. \
Do not add facts, version numbers, dates, or claims that are not in that \
material. If the source material is thin, write a shorter, more cautious \
post rather than filling gaps from general knowledge.
- Never quote the source material directly for more than a few words at a \
time - paraphrase in your own words throughout.
- 150-300 words. Plain text, no markdown formatting, sentence case, no \
hashtag spam (3-5 relevant hashtags at the very end is fine).
- Do not fabricate a "verified" or "confirmed" tone - if something is \
uncertain, say so plainly instead of asserting it.

Respond with STRICT JSON only, no markdown fences, no preamble, with \
exactly two keys:
  "post": the full LinkedIn post text
  "image_brief": one sentence describing a simple, non-infringing visual \
that would suit this post (e.g. a code snippet card, a before/after \
diagram) - never a request to depict a real person, logo, or branded UI.
"""


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:60] or "untitled"


def main():
    if not NEW_ITEMS_FILE.exists():
        print("No new_items.json found - run fetch_sources.py first.", file=sys.stderr)
        sys.exit(1)

    items = json.loads(NEW_ITEMS_FILE.read_text())
    if not items:
        print("No new items to draft.")
        return

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    DRAFTS_DIR.mkdir(exist_ok=True)

    for item in items:
        source_material = (
            f"Title: {item['title']}\n"
            f"Source: {item['source']}\n"
            f"Link: {item['link']}\n"
            f"Summary/excerpt: {item['summary']}"
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=f"Source material:\n\n{source_material}",
            config={
                "system_instruction": SYSTEM_PROMPT,
                "response_mime_type": "application/json",
            },
        )
        raw_text = (response.text or "").strip()

        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError:
            print(f"[warn] could not parse model output for '{item['title']}', skipping", file=sys.stderr)
            continue

        date_str = datetime.date.today().isoformat()
        slug = slugify(item["title"])
        draft_path = DRAFTS_DIR / f"{date_str}-{slug}.md"

        draft_path.write_text(
            "---\n"
            f"source_title: {item['title']}\n"
            f"source_link: {item['link']}\n"
            f"status: pending-review\n"
            "---\n\n"
            "## Post text (edit freely, this is what gets published)\n\n"
            f"{data['post']}\n\n"
            "## Image brief (for your own reference / manual image creation)\n\n"
            f"{data['image_brief']}\n\n"
            "## Reviewer checklist before merging this PR\n\n"
            "- [ ] Every claim in the post text is actually true - check the source link\n"
            "- [ ] Tone sounds like you, not like a template\n"
            "- [ ] An image is attached or linked below (optional)\n\n"
            "## Image\n\n"
            "<!-- paste an image URL or leave blank -->\n"
        )
        print(f"Wrote draft: {draft_path}")


if __name__ == "__main__":
    main()
