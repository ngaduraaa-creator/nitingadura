#!/usr/bin/env python3
"""
generate_market_reports_sitemap.py
Regenerates sitemap-market-reports-pilot.xml from the ACTUAL market-reports/
pages on disk, so it never lists renamed/removed slugs (404s) or omits real
pages. Applies a quality-tiered priority/changefreq instead of a flat value:

  annual  /YYYY/      → priority 0.70, monthly   (strong evergreen hub pages)
  recent  /YYYY-MM/   → priority 0.62, weekly    (fresh — last ~7 months)
  archive /YYYY-MM/   → priority 0.45, monthly   (older monthly snapshots)

lastmod is the file's real modification date (honest freshness signal).

Run from the repo root:
  python3 scripts/generate_market_reports_sitemap.py
"""
import os
import re
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MR_DIR = os.path.join(ROOT, 'market-reports')
OUT = os.path.join(ROOT, 'sitemap-market-reports-pilot.xml')
BASE = 'https://nitingadura.com/'

# "Recent" = this month and the ~7 months before it (kept fresh in the index).
RECENT_THRESHOLD = '2025-12'

ANNUAL_RE = re.compile(r'/(\d{4})/index\.html$')
MONTHLY_RE = re.compile(r'/(\d{4}-\d{2})/index\.html$')


def url_for(path: str) -> str:
    rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
    rel = re.sub(r'index\.html$', '', rel)   # dir pages → trailing slash
    return BASE + rel


def tier(path: str):
    """Return (priority, changefreq) for a market-report page."""
    if ANNUAL_RE.search(path):
        return '0.70', 'monthly'
    m = MONTHLY_RE.search(path)
    if m:
        ym = m.group(1)
        if ym >= RECENT_THRESHOLD:
            return '0.62', 'weekly'
        return '0.45', 'monthly'
    return '0.50', 'monthly'   # any non-dated hub page


def lastmod(path: str) -> str:
    ts = os.path.getmtime(path)
    return datetime.date.fromtimestamp(ts).isoformat()


def main():
    pages = []
    for dirpath, _dirs, files in os.walk(MR_DIR):
        for f in files:
            if f == 'index.html':
                pages.append(os.path.join(dirpath, f))
    pages.sort()

    rows = []
    counts = {'annual': 0, 'recent': 0, 'archive': 0}
    for p in pages:
        pr, cf = tier(p)
        if ANNUAL_RE.search(p):
            counts['annual'] += 1
        elif cf == 'weekly':
            counts['recent'] += 1
        else:
            counts['archive'] += 1
        rows.append(
            '  <url>\n'
            f'    <loc>{url_for(p)}</loc>\n'
            f'    <lastmod>{lastmod(p)}</lastmod>\n'
            f'    <changefreq>{cf}</changefreq>\n'
            f'    <priority>{pr}</priority>\n'
            '  </url>'
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + '\n'.join(rows) + '\n'
        + '</urlset>\n'
    )
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write(xml)

    print(f'Wrote {len(pages)} market-report URLs to {os.path.relpath(OUT, ROOT)}')
    print(f'  annual (0.70/monthly): {counts["annual"]}')
    print(f'  recent (0.62/weekly):  {counts["recent"]}')
    print(f'  archive (0.45/monthly):{counts["archive"]}')


if __name__ == '__main__':
    main()
