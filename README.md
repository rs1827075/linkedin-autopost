# LinkedIn content bot

Watches a few Salesforce-dev RSS feeds, drafts a LinkedIn post with Claude
when something new shows up, opens a pull request so you can review and
edit it, and publishes to your profile only after you merge that PR.

Nothing posts automatically without you clicking "merge" first.

```
scheduled cron  ->  fetch_sources.py  ->  draft_post.py  ->  PR opened
                                                                |
                                                     you review, edit, merge
                                                                |
                                                          publish.yml
                                                                |
                                                     post_to_linkedin.py
                                                                |
                                                        your LinkedIn feed
```

## One-time setup

### 1. Create a LinkedIn developer app (free, no approval needed for this)

1. Go to https://www.linkedin.com/developers/apps -> Create app.
2. Link it to a LinkedIn Company Page (LinkedIn requires one to create an
   app - a placeholder page for yourself is fine).
3. Under the app's **Products** tab, add:
   - "Sign In with LinkedIn using OpenID Connect"
   - "Share on LinkedIn"
   Both are free and auto-approved, no waiting.
4. Under **Auth**, add this redirect URL exactly:
   `http://localhost:8080/callback`
5. Note your **Client ID** and **Client Secret** from the Auth tab.

### 2. Get your access token (run locally, once)

```
pip install -r requirements.txt
export LINKEDIN_CLIENT_ID=your_client_id
export LINKEDIN_CLIENT_SECRET=your_client_secret
python scripts/get_linkedin_token.py
```

This opens your browser, you approve, and it prints two values.

### 3. Push this repo to GitHub, then add repo secrets

Settings -> Secrets and variables -> Actions -> New repository secret:

| Secret name | Value |
|---|---|
| `ANTHROPIC_API_KEY` | your Anthropic API key |
| `LINKEDIN_ACCESS_TOKEN` | printed by step 2 |
| `LINKEDIN_PERSON_URN` | printed by step 2 |

### 4. Check the sources

Open `sources.json` and adjust the feed list to whatever you actually want
tracked. The two in there are a starting point - verify they resolve before
relying on them, blogs occasionally change their feed URLs.

### 5. Turn it on

Go to the **Actions** tab on GitHub and enable workflows if prompted. The
`draft.yml` workflow runs every Monday by default (edit the `cron` line in
`.github/workflows/draft.yml` to change that), or trigger it manually any
time from the Actions tab ("Run workflow").

## What happens each run

1. `fetch_sources.py` checks the feeds for anything not seen before.
2. `draft_post.py` asks Claude to draft a post + an image idea for each new
   item, and writes a markdown file under `drafts/`.
3. A pull request opens with those draft files.
4. **You review it.** The draft only saw the RSS summary, not the full
   article - the checklist in each draft file exists because of this.
   Open the source link and check the claims before you trust them.
5. Add an image if you want one (paste a URL under the `## Image` heading
   in the draft file - e.g. something built with Claude, or your own
   screenshot).
6. Merge the PR. That merge is what triggers `publish.yml`, which posts the
   text (and image, if you added one) to your LinkedIn profile.

## Things worth knowing

- **Your access token expires** (~60 days for this scope). When
  `publish.yml` starts failing with a 401, just re-run
  `get_linkedin_token.py` and update the GitHub secret.
- **This posts to your personal profile only** (`w_member_social` scope,
  the free tier). Company pages need LinkedIn's paid partner-gated
  Marketing API - not what this is built for.
- **Want a stronger approval gate than "merge = publish"?** Create a GitHub
  Environment called `linkedin-publish` under Settings > Environments, add
  yourself as a required reviewer, then uncomment the `environment:` line
  in `publish.yml`. That adds a second manual "approve" click in the
  Actions UI before anything actually posts.
- **Rate limits**: LinkedIn's free tier is generous enough for one post a
  week, this isn't built for high-volume posting.
