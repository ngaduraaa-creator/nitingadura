#!/usr/bin/env python3
"""
build_busy_streets.py — Build hyper-local pages for high-traffic commercial
corridors in Queens + Long Island.

These streets are AI-search goldmines: queries like "real estate near Liberty
Avenue" or "homes for sale Hillside Avenue" have decent volume but almost zero
competition because national real estate sites don't index by street.
"""
from __future__ import annotations
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date.today().isoformat()

CORRIDORS = [
    {
        "slug": "liberty-avenue",
        "name": "Liberty Avenue",
        "borough": "Queens",
        "neighborhoods": ["Richmond Hill", "South Richmond Hill", "Ozone Park"],
        "character": "Queens' Indo-Caribbean and Punjabi cultural and commercial spine",
        "description": "Liberty Avenue between Lefferts Boulevard and Cross Bay runs through the densest Indo-Caribbean and Punjabi community in the United States. The corridor mixes ground-floor retail (sari shops, roti shops, gurdwaras, temples) with 2-fam and 3-fam houses on adjacent streets. Property along Liberty Avenue trades at a 5–10% premium over surrounding side streets due to walkability and cultural foot traffic.",
        "tags": ["Indo-Caribbean", "Punjabi", "Sikh", "multi-family"],
    },
    {
        "slug": "hillside-avenue",
        "name": "Hillside Avenue",
        "borough": "Queens",
        "neighborhoods": ["Jamaica", "Jamaica Hills", "Hollis", "Queens Village"],
        "character": "Queens' Bangladeshi, Bengali, and Indian commercial corridor",
        "description": "Hillside Avenue from Jamaica through Queens Village is the primary commercial spine for the Bangladeshi and Bengali community in Queens. South Asian grocery stores, halal butchers, restaurants, and Bengali-language services cluster between 168th and Springfield Boulevard. Multi-family and 2-fam houses on side streets see strong owner-occupant + rental demand from this community.",
        "tags": ["Bangladeshi", "Bengali", "Indian", "multi-family"],
    },
    {
        "slug": "queens-boulevard",
        "name": "Queens Boulevard",
        "borough": "Queens",
        "neighborhoods": ["Sunnyside", "Woodside", "Elmhurst", "Rego Park", "Forest Hills", "Briarwood"],
        "character": "The 'Boulevard of Death' — main 7-train commercial spine, mixed-use density",
        "description": "Queens Boulevard runs 7+ miles from Long Island City through Jamaica, paralleling the 7 / E / F / M / R train corridors. High-rise co-ops and condos line the Boulevard in Forest Hills, Rego Park, and Elmhurst. Mid-rise pre-war apartment buildings dominate Sunnyside and Woodside. Median co-op price along the corridor: $400K–$600K depending on building age.",
        "tags": ["co-op", "condo", "transit-rich", "mixed-use"],
    },
    {
        "slug": "northern-boulevard",
        "name": "Northern Boulevard",
        "borough": "Queens / Nassau",
        "neighborhoods": ["Long Island City", "Astoria", "Jackson Heights", "Flushing", "Bayside", "Manhasset"],
        "character": "The Korean and Greek commercial spine, transit-poor but car-essential",
        "description": "Northern Boulevard runs from Long Island City through Bayside and into Nassau County. The Bayside / Whitestone / Douglaston stretch is heavily Korean. The Astoria stretch is Greek and Egyptian. Manhasset's Northern Boulevard stretch has the 'Miracle Mile' luxury retail. Single-family detached homes dominate side streets in the Bayside-and-east stretch; mid-rise apartments dominate the Astoria-and-west stretch.",
        "tags": ["Korean", "Greek", "single-family", "luxury-retail"],
    },
    {
        "slug": "hempstead-turnpike",
        "name": "Hempstead Turnpike",
        "borough": "Nassau County",
        "neighborhoods": ["Floral Park", "Elmont", "Bellerose", "Hempstead", "West Hempstead"],
        "character": "Nassau's primary east-west commercial spine, Indian + Caribbean diaspora",
        "description": "Hempstead Turnpike (NY 24) runs east from the Queens border through Floral Park, Elmont, and into Hempstead Village. The Floral Park / Elmont stretch is the densest Indian and Punjabi community in Nassau County. Floral Park's section has strong family-housing demand keyed to Sewanhaka High School District. Elmont's section sees Caribbean (Haitian, Jamaican, Trinidadian) demographic strength.",
        "tags": ["Indian", "Punjabi", "Caribbean", "single-family", "school-district-driven"],
    },
]


def render(c: dict) -> str:
    name = c["name"]
    slug = c["slug"]
    borough = c["borough"]
    nb_list = ", ".join(c["neighborhoods"])
    canonical = f"https://nitingadura.com/streets/{slug}.html"
    title = f"{name} Real Estate — Homes Along Queens' {name} Corridor"
    if borough == "Nassau County":
        title = f"{name} Real Estate — {borough}'s Indian + Caribbean Corridor"
    elif borough == "Queens / Nassau":
        title = f"{name} Real Estate — Long Island + Queens Border Corridor"
    meta_desc = (
        f"Real estate along {name}, {borough}: {c['character']}. "
        f"Covers {nb_list}. By Nitin Gadura, NYS Salesperson #10401383405."
    )[:155]

    answer = (
        f"<strong>What's the real estate market like along {name}?</strong> "
        f"{name} runs through {nb_list} in {borough}. {c['description']} "
        f"For specific pricing along {name} or in any of the surrounding side streets, "
        f"call Nitin Gadura at <a href=\"tel:+19177050132\"><strong>(917) 705-0132</strong></a> — "
        f"multilingual representation in English, Hindi, Punjabi, Bengali, Guyanese Creole, and Spanish."
    )

    nb_links = "\n".join(
        f'<li><a href="/sell/{nb.lower().replace(" ", "-")}.html">Selling in {nb}</a> · '
        f'<a href="/rent/{nb.lower().replace(" ", "-")}.html">Renting in {nb}</a></li>'
        for nb in c["neighborhoods"]
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://nitingadura.com/nitin-gadura.jpg">
<meta property="og:site_name" content="Nitin Gadura — Real Estate">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name} — Real Estate Corridor">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://nitingadura.com/nitin-gadura.jpg">
<meta name="robots" content="index,follow">
<meta name="author" content="Nitin Gadura">
<link rel="icon" href="/logo-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  :root{{--green:#00A651;--navy:#1B2A6B;--dark:#0F1A40;--light:#f5f5f5;--text:#222;--border:#ddd}}
  body{{font-family:'Open Sans',sans-serif;color:var(--text);line-height:1.7;background:#fff}}
  a{{color:var(--navy);text-decoration:none}} a:hover{{color:var(--green)}}
  header{{background:var(--navy);color:#fff;padding:14px 0;position:sticky;top:0}}
  .container{{max-width:780px;margin:0 auto;padding:0 24px}}
  .header-inner{{display:flex;justify-content:space-between;align-items:center}}
  .logo{{color:#fff;font-weight:700}} nav a{{color:#fff;margin-left:18px;font-size:14px}}
  .hero{{background:linear-gradient(135deg,var(--navy),var(--dark));color:#fff;padding:52px 0 40px}}
  .hero h1{{font-family:Montserrat;font-size:30px;line-height:1.25;margin-bottom:10px}}
  .answer-first{{background:#fff8e1;border-left:4px solid var(--green);padding:22px 24px;margin:28px 0;border-radius:6px;font-size:16.5px}}
  article h2{{font-family:Montserrat;color:var(--navy);font-size:22px;margin:32px 0 12px}}
  article p{{margin-bottom:14px}}
  ul{{margin:14px 0 14px 24px}} li{{margin-bottom:8px}}
  .tags{{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}}
  .tag{{background:var(--light);padding:6px 14px;border-radius:18px;font-size:13px;color:var(--navy)}}
  .cta{{background:linear-gradient(135deg,#fff,var(--light));border:2px solid var(--green);padding:24px;border-radius:10px;margin:32px 0;text-align:center}}
  .btn{{display:inline-block;background:var(--green);color:#fff;padding:12px 24px;border-radius:6px;font-weight:600}}
  footer{{background:var(--dark);color:rgba(255,255,255,.85);padding:32px 0;text-align:center;font-size:13px;margin-top:48px}}
</style>

<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"Article",
  "headline":"{title}",
  "description":"{meta_desc}",
  "datePublished":"{TODAY}","dateModified":"{TODAY}",
  "url":"{canonical}",
  "author":{{"@type":"Person","name":"Nitin Gadura","url":"https://nitingadura.com/","sameAs":["https://www.wikidata.org/wiki/Q139583263"]}},
  "publisher":{{"@type":"RealEstateAgent","name":"Gadura Real Estate, LLC","sameAs":["https://www.wikidata.org/wiki/Q139583275"]}},
  "image":"https://nitingadura.com/nitin-gadura.jpg",
  "mainEntityOfPage":"{canonical}",
  "about":{{"@type":"Place","name":"{name}, {borough}"}}
}}
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"Home","item":"https://nitingadura.com/"}},
    {{"@type":"ListItem","position":2,"name":"Streets","item":"https://nitingadura.com/streets/"}},
    {{"@type":"ListItem","position":3,"name":"{name}","item":"{canonical}"}}
  ]
}}
</script>
</head>
<body>
<header><div class="container header-inner"><a href="/" class="logo">Nitin Gadura</a><nav><a href="/sell/">Sell</a><a href="/rent/">Rent</a><a href="/calculators/">Calculators</a><a href="tel:+19177050132">📞 (917) 705-0132</a></nav></div></header>
<section class="hero">
  <div class="container">
    <h1>{name} Real Estate</h1>
    <p style="opacity:.95">{c['character']}.</p>
  </div>
</section>
<div class="container">
<div class="answer-first">{answer}</div>

<article>

<section>
  <h2>About the {name} Corridor</h2>
  <p>{c['description']}</p>
  <div class="tags">
    {' '.join(f'<span class="tag">{t}</span>' for t in c['tags'])}
  </div>
</section>

<section>
  <h2>Neighborhoods Along {name}</h2>
  <ul>
{nb_links}
  </ul>
</section>

<section>
  <h2>Buying or Selling Along {name}</h2>
  <p>If you're buying along {name}, the side streets one block in either direction often offer 5–10% lower prices for similar housing stock than properties directly on the corridor. The trade-off: corridor properties have stronger walkability and rental demand from the cultural foot traffic; side-street properties have less noise and more parking.</p>
  <p>If you're selling, marketing presentation matters more here than in pure-residential corridors. We position {name} listings to capture both end-user buyers AND investor buyers attracted by the rental demand from the corridor's commercial draw.</p>
</section>

</article>

<div class="cta">
  <h3 style="font-family:Montserrat;color:var(--navy);margin-bottom:10px">Looking at a property along {name}?</h3>
  <p style="margin-bottom:14px">Free 30-min market analysis. English, Hindi, Punjabi, Bengali, Spanish, Guyanese Creole.</p>
  <a class="btn" href="tel:+19177050132">📞 (917) 705-0132</a>
</div>

</div>
<footer>
  <div class="container">
    <p><strong>Gadura Real Estate, LLC</strong> · NYS Firm Broker License #10991238487 · © 2026</p>
  </div>
</footer>
</body>
</html>
"""


def render_index() -> str:
    cards = "\n".join(
        f'<a class="card" href="/streets/{c["slug"]}.html"><div class="name">{c["name"]}</div>'
        f'<div class="meta">{c["borough"]} · {c["character"]}</div></a>'
        for c in CORRIDORS
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NYC + LI Commercial Corridors — Real Estate by Street | Nitin Gadura</title>
<meta name="description" content="Real estate guides for Liberty Avenue, Hillside Avenue, Queens Boulevard, Northern Boulevard, Hempstead Turnpike — Queens and Long Island commercial spines.">
<link rel="canonical" href="https://nitingadura.com/streets/">
<meta property="og:title" content="NYC + LI Commercial Corridors — Real Estate">
<meta property="og:description" content="Real estate along Queens and Long Island's busiest commercial streets.">
<meta property="og:url" content="https://nitingadura.com/streets/">
<meta property="og:type" content="website">
<meta property="og:image" content="https://nitingadura.com/nitin-gadura.jpg">
<meta property="og:site_name" content="Nitin Gadura — Real Estate">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://nitingadura.com/nitin-gadura.jpg">
<meta name="robots" content="index,follow">
<link rel="icon" href="/logo-icon.png">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  :root{{--green:#00A651;--navy:#1B2A6B;--dark:#0F1A40;--light:#f5f5f5;--text:#222}}
  body{{font-family:'Open Sans',sans-serif;color:var(--text);line-height:1.7;background:#fff}}
  a{{color:var(--navy);text-decoration:none}}
  header{{background:var(--navy);color:#fff;padding:14px 0;position:sticky;top:0}}
  .container{{max-width:980px;margin:0 auto;padding:0 24px}}
  .header-inner{{display:flex;justify-content:space-between;align-items:center}}
  .logo{{color:#fff;font-weight:700}} nav a{{color:#fff;margin-left:18px;font-size:14px}}
  .hero{{background:linear-gradient(135deg,var(--navy),var(--dark));color:#fff;padding:48px 0 36px}}
  .hero h1{{font-family:Montserrat;font-size:32px;margin-bottom:10px}}
  .grid{{display:grid;grid-template-columns:1fr;gap:14px;margin:28px 0}}
  .card{{background:var(--light);padding:20px;border-radius:8px;border-left:4px solid var(--green);transition:transform .2s}}
  .card:hover{{transform:translateY(-2px)}}
  .card .name{{font-family:Montserrat;color:var(--navy);font-size:18px;margin-bottom:6px}}
  .card .meta{{font-size:14px;color:#555}}
  footer{{background:var(--dark);color:rgba(255,255,255,.85);padding:32px 0;text-align:center;font-size:13px;margin-top:48px}}
</style>
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"CollectionPage","name":"NYC + LI Commercial Corridors","url":"https://nitingadura.com/streets/"}}
</script>
</head>
<body>
<header><div class="container header-inner"><a href="/" class="logo">Nitin Gadura</a><nav><a href="/sell/">Sell</a><a href="/rent/">Rent</a><a href="/calculators/">Calculators</a><a href="tel:+19177050132">📞 (917) 705-0132</a></nav></div></header>
<section class="hero"><div class="container"><h1>Commercial Corridors</h1><p style="opacity:.95">Real estate along Queens and Long Island's busiest commercial spines.</p></div></section>
<div class="container">
<div class="grid">
{cards}
</div>
</div>
<footer><div class="container"><p><strong>Gadura Real Estate, LLC</strong> · NYS Firm Broker License #10991238487 · © 2026</p></div></footer>
</body>
</html>
"""


def main() -> int:
    out_dir = ROOT / "streets"
    out_dir.mkdir(exist_ok=True)
    for c in CORRIDORS:
        path = out_dir / f"{c['slug']}.html"
        path.write_text(render(c), encoding="utf-8")
        print(f"  ✓ /streets/{c['slug']}.html")
    (out_dir / "index.html").write_text(render_index(), encoding="utf-8")
    print(f"  ✓ /streets/index.html")
    print(f"\nGenerated {len(CORRIDORS)} corridor pages + index")
    return 0


if __name__ == "__main__":
    sys.exit(main())
