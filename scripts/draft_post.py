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

MODEL = "gemini-flash-lite-latest"  # free tier

SYSTEM_PROMPT = """You draft LinkedIn posts for a Senior Software Engineer \
specializing in Salesforce (Financial Services Cloud, Apex, LWC, Agentforce, \
integrations). Voice: informative, first-person, practical - explains what \
changed, why it matters, and a concrete use case or two. Ends by inviting \
readers to share their own use cases or thoughts.

FORMATTING - this is a strict requirement, not a suggestion:
- Write 4-7 SHORT paragraphs, each 1-3 sentences.
- Separate every paragraph with a blank line (two newline characters, \\n\\n).
- Never output the post as one continuous block of text. If you catch \
yourself writing a paragraph longer than 3 sentences, break it up.
- Put the hashtags on their own final line, not folded into the last paragraph.

GROUNDING - this is the most important rule:
- You only know what is in the "source material" the user gives you. That \
is usually just a short RSS summary, not the full article.
- Do NOT state specifics that are not literally present in the source \
material - no invented GA/release dates, no invented migration steps, no \
invented product or capability names beyond what's given. If the source \
material doesn't say a feature is "generally available," don't say that \
either.
- If the source material is thin, write a SHORTER, more hedged post ("early \
signals suggest...", "worth keeping an eye on...") rather than inventing \
specifics to sound more authoritative.
- Never quote the source material directly for more than a few words at a \
time - paraphrase in your own words throughout.

OTHER RULES:
- 150-300 words total. Sentence case, no ALL CAPS, no emoji.
- 3-5 relevant hashtags at the very end only.
- Do not fabricate a "verified" or "confirmed" tone - if something is \
uncertain, say so plainly instead of asserting it.

Respond with STRICT JSON only, no markdown fences, no preamble, with \
exactly two keys:
  "post": the full LinkedIn post text, WITH the \\n\\n paragraph breaks \
described above actually included as characters in the string
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
                "temperature": 0.5,
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
