#!/usr/bin/env python3
"""
freshen_pages.py — Stamp top pages with `data-last-reviewed="<today>"` and
update sitemap lastmod entries on the same set. This is the cheapest
freshness signal for Grok and supports Bing's IndexNow priority weighting.

Run weekly (Monday) via cron or GitHub Actions:
    0 9 * * MON  cd ~/Jagex/nitingadura-correct && python3 scripts/freshen_pages.py --apply && python3 scripts/indexnow_ping.py

Only pages that meaningfully change should be freshened. Don't run this on
pages whose content didn't change — that's a soft form of cloaking.
"""
from __future__ import annotations
import argparse
import datetime as dt
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WEEKLY_FRESH = [
    "index.html",
    "about.html",
    "press.html",
    "glossary.html",
    "sell/index.html",
    "rent/index.html",
    "calculators/index.html",
    "streets/index.html",
    "how-to-sell-a-house-in-nyc.html",
    "how-to-rent-out-an-apartment-in-ny.html",
    "how-to-screen-a-tenant-in-ny.html",
    "how-to-negotiate-a-real-estate-deal-in-ny.html",
]

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
ET.register_namespace("", NS)
URL_OF = lambda rel: f"https://nitingadura.com/{rel}".replace("/index.html", "/")
TODAY = dt.date.today().isoformat()


def stamp_html(p: Path) -> bool:
    if not p.exists():
        return False
    html = p.read_text(encoding="utf-8")
    new = re.sub(
        r'<body([^>]*?)\s*data-last-reviewed="[^"]*"',
        r'<body\1',
        html,
    )
    new = re.sub(
        r"<body([^>]*)>",
        rf'<body\1 data-last-reviewed="{TODAY}">',
        new,
        count=1,
    )
    if new != html:
        p.write_text(new, encoding="utf-8")
        return True
    return False


def stamp_sitemap(target_urls: set[str]) -> int:
    sm = ROOT / "sitemap.xml"
    if not sm.exists():
        return 0
    tree = ET.parse(sm)
    root = tree.getroot()
    updated = 0
    for url_node in root.findall(f"{{{NS}}}url"):
        loc = url_node.findtext(f"{{{NS}}}loc", default="").strip()
        if loc in target_urls or loc.rstrip("/") + "/" in target_urls:
            lm = url_node.find(f"{{{NS}}}lastmod")
            if lm is None:
                lm = ET.SubElement(url_node, f"{{{NS}}}lastmod")
            lm.text = TODAY
            updated += 1
    tree.write(sm, encoding="utf-8", xml_declaration=True)
    return updated


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    if not args.apply:
        print("DRY-RUN — would freshen:")
        for rel in WEEKLY_FRESH:
            print(f"  {rel}")
        return 0
    targets = {URL_OF(rel) for rel in WEEKLY_FRESH}
    sitemap_n = stamp_sitemap(targets)
    html_n = sum(1 for rel in WEEKLY_FRESH if stamp_html(ROOT / rel))
    print(f"  sitemap entries refreshed: {sitemap_n}")
    print(f"  body data-last-reviewed updated: {html_n}")
    print(f"\nNext: python3 scripts/indexnow_ping.py to push changes to Bing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
