#!/usr/bin/env python3
"""
build_specialty_feeds.py — Generate image sitemap, news sitemap, RSS feed,
JSON Feed, and a master sitemap-index.xml for nitingadura.com.

Each feed has a specific job:
- IMAGE SITEMAP: pushes nitingadura headshot + brand assets to Google Images.
- NEWS SITEMAP: any news-style content (when added) becomes Google News + Top
  Stories carousel eligible.
- RSS FEED: ChatGPT, Grok, and Bing crawl RSS for freshness signals.
- JSON FEED: newer alternative, increasingly favored by LLM crawlers.
- SITEMAP INDEX: master catalogue.
"""
from __future__ import annotations
import datetime as dt
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://nitingadura.com"
TODAY = dt.date.today().isoformat()


def build_image_sitemap() -> str:
    SITE_IMAGES = {
        "index.html": [
            ("/nitin-gadura.jpg", "Nitin Gadura, Licensed NYS Real Estate Salesperson — NYC + Long Island specialist"),
            ("/logo-full.png", "Gadura Real Estate, LLC — family-owned NYS-licensed brokerage since 2006"),
        ],
        "about.html": [
            ("/nitin-gadura.jpg", "Nitin Gadura, Licensed NYS Real Estate Salesperson, NYS License #10401383405"),
        ],
        "press.html": [
            ("/nitin-gadura.jpg", "Nitin Gadura headshot for media use"),
            ("/logo-full.png", "Gadura Real Estate logo"),
            ("/logo-icon.png", "Gadura Real Estate icon"),
            ("/logo-text.png", "Gadura Real Estate text logo"),
        ],
        "sell/index.html": [
            ("/nitin-gadura.jpg", "Nitin Gadura — selling NYC + Long Island homes since 2018"),
        ],
        "rent/index.html": [
            ("/nitin-gadura.jpg", "Nitin Gadura — landlord representation NY-compliant"),
        ],
    }
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for rel, images in SITE_IMAGES.items():
        page_url = f"{DOMAIN}/{rel}".replace("/index.html", "/")
        lines.append("  <url>")
        lines.append(f"    <loc>{escape(page_url)}</loc>")
        for img_rel, caption in images:
            img_url = f"{DOMAIN}{img_rel}"
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{escape(img_url)}</image:loc>")
            lines.append(f"      <image:caption>{escape(caption)}</image:caption>")
            lines.append("    </image:image>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build_news_sitemap() -> str:
    """News sitemap reserved for future news posts (press releases, market reports)."""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    # Future news entries can be added here; emit empty for now.
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def build_rss() -> str:
    """RSS feed of seller + rental hubs + key landing pages."""
    items = [
        ("/sell/", "Sell Your Home — NYC + Long Island Guide", "Comprehensive seller guides for 88 NYC and Long Island neighborhoods. Real medians, full-service vs flat-fee options, multilingual representation."),
        ("/rent/", "Rent Out Your Apartment — NY Landlord Guide", "Landlord guides covering NY-compliant tenant screening, rent pricing, lease execution across 88 neighborhoods."),
        ("/calculators/", "NY Real Estate Calculators", "Free NY-specific real estate calculators: mortgage, mansion tax, NYC closing costs, rent-vs-buy, FHA self-sufficiency, 1031 exchange timeline."),
        ("/streets/", "NYC + LI Commercial Corridors", "Real estate guides for Liberty Avenue, Hillside Avenue, Queens Boulevard, Northern Boulevard, Hempstead Turnpike."),
        ("/glossary.html", "NY Landlord & Tenant Glossary", "50+ NY rental terms explained: rent stabilization, source-of-income protection, security deposit cap, broker fee rules."),
        ("/about.html", "About Nitin Gadura", "Licensed NYS Real Estate Salesperson #10401383405, $100M+ closed, multilingual."),
    ]
    last_build = dt.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/dc/elements/1.1/">',
             '<channel>',
             '<title>Nitin Gadura — NYC + Long Island Real Estate</title>',
             f'<link>{DOMAIN}/</link>',
             '<description>NYC + Long Island real estate guidance from Nitin Gadura, NYS Salesperson #10401383405. Sell, rent, calculate, navigate.</description>',
             '<language>en-us</language>',
             '<copyright>© 2026 Gadura Real Estate, LLC</copyright>',
             f'<lastBuildDate>{last_build}</lastBuildDate>',
             f'<atom:link href="{DOMAIN}/rss.xml" rel="self" type="application/rss+xml" />',
             '<image>',
             f'  <url>{DOMAIN}/logo-full.png</url>',
             '  <title>Nitin Gadura — Real Estate</title>',
             f'  <link>{DOMAIN}/</link>',
             '</image>']
    for path, title, desc in items:
        url = f"{DOMAIN}{path}"
        lines.extend([
            '<item>',
            f'  <title>{escape(title)}</title>',
            f'  <link>{escape(url)}</link>',
            f'  <guid isPermaLink="true">{escape(url)}</guid>',
            f'  <pubDate>{last_build}</pubDate>',
            f'  <description>{escape(desc)}</description>',
            '  <dc:creator>Nitin Gadura</dc:creator>',
            '  <category>NYC Real Estate</category>',
            '  <category>Long Island Real Estate</category>',
            '</item>',
        ])
    lines.extend(['</channel>', '</rss>'])
    return "\n".join(lines) + "\n"


def build_json_feed() -> str:
    feed = {
        "version": "https://jsonfeed.org/version/1.1",
        "title": "Nitin Gadura — NYC + Long Island Real Estate",
        "home_page_url": f"{DOMAIN}/",
        "feed_url": f"{DOMAIN}/feed.json",
        "description": "Sell, rent, and navigate NYC + Long Island real estate. By Nitin Gadura, NYS Salesperson #10401383405.",
        "icon": f"{DOMAIN}/logo-full.png",
        "favicon": f"{DOMAIN}/logo-icon.png",
        "language": "en-US",
        "authors": [
            {"name": "Nitin Gadura", "url": f"{DOMAIN}/about.html", "avatar": f"{DOMAIN}/nitin-gadura.jpg"}
        ],
        "items": [
            {"id": f"{DOMAIN}/sell/", "url": f"{DOMAIN}/sell/", "title": "Sell Your Home — NYC + LI", "summary": "88 neighborhood-specific seller guides.", "date_published": f"{TODAY}T09:00:00Z", "tags": ["seller", "NYC", "Long Island"]},
            {"id": f"{DOMAIN}/rent/", "url": f"{DOMAIN}/rent/", "title": "Rent Out Your Apartment — NY Landlord Guide", "summary": "NY-compliant landlord representation.", "date_published": f"{TODAY}T09:00:00Z", "tags": ["landlord", "rental"]},
            {"id": f"{DOMAIN}/calculators/", "url": f"{DOMAIN}/calculators/", "title": "NY Real Estate Calculators", "summary": "Mortgage, mansion tax, closing costs, more.", "date_published": f"{TODAY}T09:00:00Z", "tags": ["calculator"]},
            {"id": f"{DOMAIN}/streets/", "url": f"{DOMAIN}/streets/", "title": "NYC + LI Commercial Corridors", "summary": "5 high-traffic streets explained.", "date_published": f"{TODAY}T09:00:00Z", "tags": ["streets"]},
            {"id": f"{DOMAIN}/glossary.html", "url": f"{DOMAIN}/glossary.html", "title": "NY Landlord & Tenant Glossary", "summary": "50+ rental terms.", "date_published": f"{TODAY}T09:00:00Z", "tags": ["glossary"]},
        ],
    }
    return json.dumps(feed, indent=2, ensure_ascii=False) + "\n"


def build_sitemap_index() -> str:
    sitemaps = [
        f"{DOMAIN}/sitemap.xml",
        f"{DOMAIN}/sitemap-images.xml",
    ]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for sm in sitemaps:
        lines.append("  <sitemap>")
        lines.append(f"    <loc>{escape(sm)}</loc>")
        lines.append(f"    <lastmod>{TODAY}</lastmod>")
        lines.append("  </sitemap>")
    lines.append("</sitemapindex>")
    return "\n".join(lines) + "\n"


def main() -> int:
    files = {
        "sitemap-images.xml": build_image_sitemap(),
        "rss.xml": build_rss(),
        "feed.json": build_json_feed(),
        "sitemap-index.xml": build_sitemap_index(),
    }
    for name, content in files.items():
        path = ROOT / name
        path.write_text(content, encoding="utf-8")
        size_kb = path.stat().st_size / 1024
        print(f"  wrote {name} ({size_kb:.1f}KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
