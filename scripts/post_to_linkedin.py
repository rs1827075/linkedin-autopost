"""
Publishes ONE approved draft markdown file to your LinkedIn profile using
the official Posts API (w_member_social scope - free tier, your own profile
only).

Usage:
    python post_to_linkedin.py drafts/2026-07-17-some-post.md

Required env vars:
    LINKEDIN_ACCESS_TOKEN   - from scripts/get_linkedin_token.py
    LINKEDIN_PERSON_URN     - from scripts/get_linkedin_token.py, looks like
                              "urn:li:person:AbCdEfGhIj"

This script is meant to run ONLY after a human has reviewed and merged the
draft's pull request - see .github/workflows/publish.yml. It does not decide
what to post; it just posts what you already approved.
"""
import os
import re
import sys

import requests

API_BASE = "https://api.linkedin.com/rest"
LINKEDIN_VERSION = "202601"  # LinkedIn requires a YYYYMM version header


def parse_draft(path: str):
    text = open(path, encoding="utf-8").read()

    post_match = re.search(
        r"## Post text.*?\n\n(.*?)\n\n## Image brief", text, re.S
    )
    image_match = re.search(r"## Image\n\n(.*)", text, re.S)

    if not post_match:
        raise ValueError("Could not find '## Post text' section in draft file")

    post_text = post_match.group(1).strip()
    image_url = ""
    if image_match:
        candidate = image_match.group(1).strip()
        if candidate and not candidate.startswith("<!--"):
            image_url = candidate

    return post_text, image_url


def upload_image(session: requests.Session, person_urn: str, image_url: str) -> str:
    """Registers an image upload with LinkedIn, uploads the bytes, returns the asset URN."""
    register_resp = session.post(
        f"{API_BASE}/images?action=initializeUpload",
        json={"initializeUploadRequest": {"owner": person_urn}},
    )
    register_resp.raise_for_status()
    upload_info = register_resp.json()["value"]
    upload_url = upload_info["uploadUrl"]
    asset_urn = upload_info["image"]

    image_bytes = requests.get(image_url, timeout=30).content
    put_resp = requests.put(upload_url, data=image_bytes, headers={
        "Authorization": session.headers["Authorization"],
    })
    put_resp.raise_for_status()
    return asset_urn


def main():
    if len(sys.argv) != 2:
        print("Usage: python post_to_linkedin.py <path-to-draft.md>", file=sys.stderr)
        sys.exit(1)

    access_token = os.environ["LINKEDIN_ACCESS_TOKEN"]
    person_urn = os.environ["LINKEDIN_PERSON_URN"]

    post_text, image_url = parse_draft(sys.argv[1])

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "LinkedIn-Version": LINKEDIN_VERSION,
        "X-Restli-Protocol-Version": "2.0.0",
    })

    body = {
        "author": person_urn,
        "commentary": post_text,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    if image_url:
        asset_urn = upload_image(session, person_urn, image_url)
        body["content"] = {"media": {"id": asset_urn}}

    resp = session.post(f"{API_BASE}/posts", json=body)
    if resp.status_code >= 300:
        print(f"LinkedIn API error {resp.status_code}: {resp.text}", file=sys.stderr)
        sys.exit(1)

    post_urn = resp.headers.get("x-restli-id", "unknown")
    print(f"Published. Post URN: {post_urn}")


if __name__ == "__main__":
    main()
