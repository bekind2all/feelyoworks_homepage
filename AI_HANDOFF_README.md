# Feelyoworks AI Agent Handoff

This file is for AI agents and developers working on the Feelyoworks homepage.

Read this document before making any change.

## Non-Negotiable Rule

The live website is already receiving real lecture inquiries.

Do not change visible design, visible body copy, layout, contact/inquiry flow, images, navigation, forms, CSS, or user-facing content unless the owner explicitly asks for that specific visible change.

SEO/GEO work must stay behind the scenes:

- `<head>` metadata
- canonical URLs
- Open Graph/Twitter metadata
- JSON-LD structured data
- `robots.txt`
- `sitemap.xml`
- `llms.txt`
- `_headers`
- `_redirects`
- Cloudflare Pages middleware
- Search Console verification files
- documentation

## Important Paths

- Original source folder:
  `C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage`
- SEO/GEO working copy:
  `C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900`
- Deployment staging folder:
  `C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900_deploy_public`

The original folder should be treated as the preserved baseline. For future code changes, make a separate timestamped copy first.

## Current Production Deployment

- Domain: `https://feelyoworks.com/`
- Cloudflare Pages project: `feelyoworks-homepage`
- Connected domains:
  - `feelyoworks.com`
  - `www.feelyoworks.com`
  - `feelyoworks-homepage.pages.dev`
- Latest known deployment preview:
  `https://8bdd68d8.feelyoworks-homepage.pages.dev`

## SEO/GEO Work Already Applied

The SEO/GEO changes were applied in the working copy, then deployed to the existing Cloudflare Pages project.

Applied files:

- `index.html`: head metadata, canonical, Open Graph/Twitter, JSON-LD
- `profile.html`: head metadata for `조은이 강사`, ProfilePage/Person JSON-LD
- `insights.html`: head metadata for newsletter/AI insights, CollectionPage JSON-LD
- `robots.txt`: crawler policy and sitemap location
- `sitemap.xml`: canonical URL list
- `llms.txt`: AI-search/GEO summary for retrieval systems
- `_headers`: index/follow X-Robots-Tag and content types
- `_redirects`: legacy `.html` canonical redirects
- `functions/_middleware.js`: host/path canonical redirects
- `google9bc1d9b7c6206944.html`: Google Search Console ownership verification

## Google Search Console Status

Google Search Console was configured for:

- Property type: URL prefix
- Property URL: `https://feelyoworks.com/`
- Verification method: HTML file
- Verification file:
  `https://feelyoworks.com/google9bc1d9b7c6206944.html`
- Submitted sitemap:
  `https://feelyoworks.com/sitemap.xml`
- Sitemap status: Success
- Discovered pages: 3

Indexing was requested for:

- `https://feelyoworks.com/`
- `https://feelyoworks.com/profile`
- `https://feelyoworks.com/insights`

Do not delete `google9bc1d9b7c6206944.html`. If it is removed, Google Search Console ownership may fail later.

## Canonical URL Rules

Preferred canonical host:

- `https://feelyoworks.com`

Canonical pages:

- `https://feelyoworks.com/`
- `https://feelyoworks.com/profile`
- `https://feelyoworks.com/insights`

Required redirects:

- `https://www.feelyoworks.com/` -> `https://feelyoworks.com/`
- `https://feelyoworks.com/profile.html` -> `/profile`
- `https://feelyoworks.com/insights.html` -> `/insights`

Do not reintroduce `.html` URLs into the sitemap.

## Do Not Touch Without Explicit Approval

- Visible `<body>` content in `index.html`, `profile.html`, `insights.html`
- `styles.css` visual rules
- Site navigation labels and section structure
- Contact/lecture inquiry links and form flows
- Images/assets currently shown on the public site
- Google Search Console verification file
- `robots.txt`, unless adjusting crawler policy intentionally
- `sitemap.xml`, unless adding a real canonical page
- `llms.txt`, unless updating AI-search summary intentionally
- `_headers`, `_redirects`, and `functions/_middleware.js`, unless preserving canonical behavior

## Required Verification Before Any Deployment

Before deploying, verify that the visible body has not changed unless the task explicitly requires it.

PowerShell body comparison:

```powershell
$orig = 'C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage'
$copy = 'C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900'
$sha = [System.Security.Cryptography.SHA256]::Create()
foreach ($p in @('index.html','profile.html','insights.html')) {
  $a = Get-Content -LiteralPath (Join-Path $orig $p) -Raw -Encoding UTF8
  $b = Get-Content -LiteralPath (Join-Path $copy $p) -Raw -Encoding UTF8
  $bodyA = [regex]::Match($a, '<body[\s\S]*?</body>', 'IgnoreCase').Value
  $bodyB = [regex]::Match($b, '<body[\s\S]*?</body>', 'IgnoreCase').Value
  $hashA = [System.BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($bodyA))).Replace('-','')
  $hashB = [System.BitConverter]::ToString($sha.ComputeHash([Text.Encoding]::UTF8.GetBytes($bodyB))).Replace('-','')
  Write-Output "$p bodySha256Equal=$($hashA -eq $hashB)"
}
```

Expected result when doing SEO-only work:

```text
index.html bodySha256Equal=True
profile.html bodySha256Equal=True
insights.html bodySha256Equal=True
```

Live checks:

```powershell
curl.exe -I --location https://feelyoworks.com/sitemap.xml
curl.exe -L --silent --show-error https://feelyoworks.com/google9bc1d9b7c6206944.html
curl.exe -I https://www.feelyoworks.com/
curl.exe -I https://feelyoworks.com/profile.html
curl.exe -I https://feelyoworks.com/insights.html
```

Expected live behavior:

- `sitemap.xml`: `200 OK`
- Google verification file: contains `google-site-verification: google9bc1d9b7c6206944.html`
- `www.feelyoworks.com`: `301` to `https://feelyoworks.com/`
- `/profile.html`: redirect to `/profile`
- `/insights.html`: redirect to `/insights`

## Deployment Notes

Deploy only the public staging folder, not the full working copy with backups/docs:

```powershell
cd "C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900_deploy_public"
npx.cmd wrangler pages deploy . --project-name feelyoworks-homepage --branch main
```

Do not deploy `.seo-backup`, private notes, or unrelated source folders.

## Rollback

Rollback options:

1. Cloudflare Pages dashboard: roll back to the previous deployment.
2. Working copy: restore changed HTML files from `.seo-backup`.
3. Original folder: preserved baseline at `feelyoworks_homepage`.

## Handoff Summary

This project is currently optimized for:

- Google Search indexing
- Naver Search crawling readiness
- AI search/GEO retrieval via structured metadata and `llms.txt`
- Search query target: `조은이 강사`

Current known state:

- Naver shows `feelyoworks.com` for `조은이 강사`.
- Google Search Console is now verified and sitemap submitted.
- Google indexing requests were submitted, but public Google search result updates may take days.

## WordPress Insights Feed

The homepage and `insights.html` do not fetch WordPress posts directly in the browser.

They read:

`/data/insights.json`

That JSON is generated from:

`https://feelyoworks.wordpress.com/feed/`

Local sync command:

```powershell
cd "C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900"
python scripts\fetch-insights.py
Copy-Item -Path ".\data\insights.json" -Destination "C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900_deploy_public\data\insights.json" -Force
cd "C:\Users\hyjun\OneDrive\바탕 화면\claude_code\feelyoworks_homepage_seo_geo_20260626-112900_deploy_public"
npx.cmd wrangler pages deploy . --project-name feelyoworks-homepage --branch main
```

Verification:

```powershell
python -c "import json, urllib.request; req=urllib.request.Request('https://feelyoworks.com/data/insights.json', headers={'User-Agent':'Mozilla/5.0'}); data=json.load(urllib.request.urlopen(req)); print(data['updated']); print(data['items'][0]['title']); print(data['items'][0]['link'])"
```

If a newly published WordPress post does not appear immediately, first compare the RSS feed with live JSON. The most common cause is that `data/insights.json` was generated before the new WordPress post was published.

The repository includes `.github/workflows/sync-insights.yml`, which is designed to sync the RSS feed on a schedule. However, this local folder is not currently a Git repository, and Cloudflare Pages also has Git-connected deployments in its history. Be careful: a future Git-connected deployment may overwrite direct `wrangler pages deploy` changes if the connected repository does not contain the same SEO/GEO files.
