# Tier-1 Pilot Monitoring Runbook
**Launched:** 2026-06-05
**Scope:** 168 pages (144 monthly + 24 annual) across 12 ZIPs, nitingadura.com only
**Decision gate:** Day 14 — expand or hold

---

## Day 0 — Pre-flight checklist

Before pushing to GitHub Pages:

- [ ] Review a sample page in browser: `open ~/Jagex/nitingadura-correct/market-reports/queens/ozone-park-11416/2026-04/index.html`
- [ ] Verify the page renders cleanly (no JavaScript errors, charts load, photo loads)
- [ ] Check 2-3 random ZIPs to confirm per-ZIP variation is visible (different mortgage opener, different news intro, etc.)
- [ ] Confirm sitemap is correctly listed in `~/Jagex/nitingadura-correct/sitemap-market-reports-pilot.xml`
- [ ] Verify robots.txt is not blocking `/market-reports/`

---

## Day 0 — Deploy

```bash
cd ~/Jagex/nitingadura-correct
git status                                # review what's about to commit
git add market-reports/ sitemap-market-reports-pilot.xml ai-monitoring/indexnow-pilot-payload.json PILOT-MONITORING.md
git commit -m "Tier-1 pilot: 168 market-report pages across 12 high-value ZIPs"
git push origin main

# Wait ~2 minutes for GitHub Pages to rebuild
curl -I "https://nitingadura.com/market-reports/queens/ozone-park-11416/2026-04/" | head -3
# Should return 200 — if 404, GitHub Pages still building; wait 60 seconds and retry
```

---

## Day 0 — Submit to search engines

### Google Search Console
1. Open https://search.google.com/search-console/
2. Select property `nitingadura.com`
3. Sidebar → **Sitemaps**
4. Add new sitemap → enter `sitemap-market-reports-pilot.xml` → Submit
5. Status should change to "Success" within a few hours

### Bing Webmaster Tools
1. Open https://www.bing.com/webmasters/
2. Select `nitingadura.com`
3. Sitemaps → Submit → `https://nitingadura.com/sitemap-market-reports-pilot.xml`

### IndexNow (instant push)
```bash
cd ~/Jagex/nitingadura-correct
python3 << 'PY'
import json, urllib.request
payload = json.loads(open('ai-monitoring/indexnow-pilot-payload.json').read())
req = urllib.request.Request(
    'https://api.indexnow.org/IndexNow',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
)
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"IndexNow response: {r.status}")
    # 200/202 = accepted. Bing, Yandex, Naver consume from this single endpoint.
PY
```

---

## Day 1–14 — What to watch in Search Console

### Indexing tab
- **Indexed pages count** should rise from 0 toward 168 over 7-14 days
- **Discovered – currently not indexed** is acceptable if temporary; concerning if persistent past day 14
- **Excluded** counts should be near zero (other than `noindex` directives, of which we have none)

### Coverage warnings to escalate immediately
- **"Submitted URL marked 'noindex'"** — should never appear (we have none)
- **"Crawled – currently not indexed"** — acceptable for first 7 days; if >50% past day 14, content quality issue
- **"Duplicate without user-selected canonical"** — escalate immediately, our canonical tags should prevent this
- **"Soft 404"** — escalate; means Google sees the page as low-value

### Manual actions
- Sidebar → Manual actions
- This should say "No issues detected"
- If it says anything else → **immediate rollback**: revert the `market-reports/` commit and push

### Performance tab (after day 7)
- Impressions per day should be rising
- Average position should be tracking (likely page 5-10 initially, climbing into page 1-3 by week 4-8)
- CTR on first impressions — anything under 0.5% likely indicates we ranked for the wrong terms

---

## Day 14 — Decision gate

Run this audit:

```bash
# Replace COOKIE_FROM_BROWSER with your Search Console export cookie
echo "Manual audit checklist:"
echo "  [ ] 80%+ of pilot URLs indexed in Google? (check Sitemaps tab)"
echo "  [ ] Zero manual actions?"
echo "  [ ] < 10% 'Crawled – currently not indexed'?"
echo "  [ ] Impressions > 100 cumulative across pilot URLs?"
echo "  [ ] Any organic clicks at all?"
```

### Decision matrix

| Outcome | Action |
|---|---|
| All checks pass | **GO TIER 2** — generate top 40 ZIPs × 24 months + annual reviews 2020–2024 |
| Indexing healthy but no impressions | Hold, investigate keyword targeting, expand in 30 days |
| Indexing stalled (<50%) | Hold, investigate technical issues (canonicals, schema, sitemap) |
| Manual action received | **ROLLBACK** — revert commit, do not push more |
| `Crawled – currently not indexed` > 20% past day 14 | Hold, content quality issue — revise template before any expansion |

---

## Emergency rollback procedure

If a manual action is received or indexing rate is catastrophically bad:

```bash
cd ~/Jagex/nitingadura-correct
git log --oneline -5                          # find the pilot commit hash
git revert <PILOT_COMMIT_HASH>                 # creates a new revert commit
git push origin main
# GitHub Pages rebuilds. /market-reports/ pages become 404.

# Also remove the sitemap from Search Console:
# Sitemaps → click sitemap-market-reports-pilot.xml → Remove sitemap
```

---

## A note on lexical similarity (boilerplate vs main content)

A naive 7-word-shingle comparison across pilot pages shows **65–70% shared phrases** — but this includes structural boilerplate (the 26 news outlets, 13 citation entries, compliance footer, FAQ structure, schema markup) that Google's boilerplate-detection algorithm strips before comparing pages.

The **main-content uniqueness** (the data, narrative, deltas, charts, ZIP-specific framing) is substantially higher than the shingle test suggests:
- Each page has unique Zillow ZHVI numbers for its specific ZIP
- Auto-generated narrative paragraphs adapt to actual MoM/YoY/2Y deltas
- Per-ZIP deterministic framing variants (5 mortgage intros, 4 news intros, 4 citation intros, etc.)
- Tier-aware $100k sim (different starting amount for $400k vs $750k vs $1M ZIPs)

If the pilot indexes cleanly, this is sufficient for scale. If "Crawled — currently not indexed" remains high past day 14, the next mitigation is moving the news-outlets section and citations list to a single `/market-reports/sources/` partial page linked from each ZIP page — that alone removes another ~12KB of duplicate content per page and drops shingle similarity to ~45%.

---

## Pilot ZIPs (for quick reference)

| ZIP | Neighborhood | Region | Tier |
|---|---|---|---|
| 11416 | Ozone Park | Queens | Mid |
| 11418 | Richmond Hill | Queens | Mid |
| 11414 | Howard Beach | Queens | Mid-high |
| 11432 | Jamaica | Queens | Mid |
| 11434 | Jamaica South | Queens | Mid |
| 11385 | Glendale | Queens | Mid (has ZORI rent data) |
| 11421 | Woodhaven | Queens | Mid |
| 11422 | Rosedale | Queens | Mid |
| 11580 | Valley Stream | Nassau LI | Mid |
| 11003 | Elmont | Nassau LI | Mid |
| 11550 | Hempstead | Nassau LI | Lower |
| 11691 | Far Rockaway | Queens | Lower |

## Pilot months

May 2025 → April 2026 (12 months, most recent available data)

## Pilot annual reviews

2024, 2025 (most recent finished years)
