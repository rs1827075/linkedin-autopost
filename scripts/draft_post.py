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
changed, why it matters, and shows a real, concrete example of using it.

STRUCTURE - follow this shape:
1. Hook: one or two sentences on the problem this addresses.
2. What it is: what actually changed or shipped.
3. THE EXAMPLE (required, see rules below): a specific, concrete illustration \
of how someone would actually use this - not a vague "this could help with X."
4. Why it matters for Financial Services Cloud / enterprise Salesforce work \
specifically.
5. A genuine open question for readers, inviting their use cases or experience.
6. Hashtags on their own final line.

FORMATTING - strict requirement:
- Short paragraphs, 1-3 sentences each, separated by a blank line (\\n\\n).
- Never output the post as one continuous block of text.

THE EXAMPLE, and GROUNDING - this is the most important rule:
- You will be given "source material" that includes a short summary AND, \
when available, the full extracted text of the source article - use the \
full article text as your primary source for the example.
- If the article text contains a code snippet, API name, method signature, \
config step, or specific workflow, build your example paragraph around \
that real detail - describe concretely what a developer would type, click, \
or configure, using the real names given.
- If the article text does NOT contain any implementation-level detail (it's \
just an announcement with no how-to), do NOT invent one. Instead, write \
paragraph 3 as an honest, clearly-labeled illustrative scenario ("Picture a \
case where...") rather than presenting invented specifics as fact, and keep \
it short.
- Do not state specifics (GA dates, product names, capability names, \
migration steps) that are not literally present in the source material.
- Never quote the source material directly for more than a few words at a \
time - paraphrase throughout.

OTHER RULES:
- 180-320 words total (a little longer than before is fine, the example \
needs room). Sentence case, no ALL CAPS, no emoji.
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
        article_text = item.get("content", "")
        source_material = (
            f"Title: {item['title']}\n"
            f"Source: {item['source']}\n"
            f"Link: {item['link']}\n"
            f"RSS summary: {item['summary']}\n\n"
            + (f"Full article text:\n{article_text}" if article_text
               else "(Full article text unavailable - only the RSS summary above "
                    "was retrievable. Do not invent implementation detail beyond it; "
                    "keep the example paragraph short and clearly illustrative.)")
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
            "- [ ] The example paragraph reflects something real, not vague filler\n"
            "- [ ] Tone sounds like you, not like a template\n"
            "- [ ] An image is attached or linked below (optional)\n\n"
            "## Image\n\n"
            "<!-- paste an image URL or leave blank -->\n"
        )
        print(f"Wrote draft: {draft_path}")


if __name__ == "__main__":
    main()
