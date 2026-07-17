"""
ONE-TIME, run this on your own machine (not in GitHub Actions).

Walks you through LinkedIn's OAuth flow and prints the values you need to
paste into your GitHub repo's Actions secrets:
    LINKEDIN_ACCESS_TOKEN
    LINKEDIN_PERSON_URN

Before running:
    1. Create an app at https://www.linkedin.com/developers/apps
    2. Under "Products", add "Sign In with LinkedIn using OpenID Connect"
       and "Share on LinkedIn" (both free, auto-approved).
    3. Under "Auth", add this exact redirect URL:
           http://localhost:8080/callback
    4. Copy your app's Client ID and Client Secret and export them:
           export LINKEDIN_CLIENT_ID=...
           export LINKEDIN_CLIENT_SECRET=...

Then run:
    python scripts/get_linkedin_token.py

It opens your browser, you log in and approve, and this script catches the
redirect automatically and prints your token + person URN.

Note: LinkedIn access tokens for this scope last about 60 days and are not
reliably refreshable without extra partner access. Re-run this script when
publish.yml starts failing with a 401.
"""
import http.server
import os
import sys
import threading
import urllib.parse
import webbrowser

import requests

CLIENT_ID = os.environ.get("LINKEDIN_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LINKEDIN_CLIENT_SECRET")

print("CLIENT_ID:", repr(CLIENT_ID))
print("CLIENT_SECRET:", repr(CLIENT_SECRET))

REDIRECT_URI = "http://localhost:8080/callback"
SCOPES = "openid profile w_member_social"

auth_code = {}


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            auth_code["value"] = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Auth complete, you can close this tab and return to your terminal.")
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, *args):
        pass  # keep the terminal quiet


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Set LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET env vars first.", file=sys.stderr)
        sys.exit(1)

    server = http.server.HTTPServer(("localhost", 8080), CallbackHandler)
    threading.Thread(target=server.handle_request, daemon=True).start()

    auth_url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode({
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
    })
    print(f"Opening browser to log in and approve access:\n{auth_url}\n")
    webbrowser.open(auth_url)

    print("Waiting for you to approve in the browser...")
    while "value" not in auth_code:
        pass

    token_resp = requests.post("https://www.linkedin.com/oauth/v2/accessToken", data={
        "grant_type": "authorization_code",
        "code": auth_code["value"],
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    token_resp.raise_for_status()
    access_token = token_resp.json()["access_token"]

    userinfo_resp = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    userinfo_resp.raise_for_status()
    person_id = userinfo_resp.json()["sub"]
    person_urn = f"urn:li:person:{person_id}"

    print("\nSuccess. Add these as GitHub repo secrets (Settings > Secrets and variables > Actions):\n")
    print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
    print(f"LINKEDIN_PERSON_URN={person_urn}")


if __name__ == "__main__":
    main()