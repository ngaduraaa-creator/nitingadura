#!/usr/bin/env python3
"""
build_howto_pages.py — Generate 4 HowTo schema pages targeting high-intent
voice/AI search queries that don't exist on nitingadura.com yet.

Each page has:
- HowTo + FAQPage + BreadcrumbList schema
- Step-by-step structured content (AI engines extract verbatim)
- Estimated cost / time per step
- Links to related pages
"""
from __future__ import annotations
import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date.today().isoformat()

GUIDES = [
    {
        "slug": "how-to-sell-a-house-in-nyc",
        "h1": "How to Sell a House in NYC — 9-Step 2026 Guide",
        "title": "How to Sell a House in NYC in 2026 — Step-by-Step Process | Nitin Gadura",
        "intent": "Sellers researching the NYC home-sale process",
        "intro": "Selling a house in NYC follows a different path than most US markets. NY uses attorneys (not title companies), the closing process runs 60–90 days, and seller-side closing costs run 8–10% of sale price. Here's the exact 9-step process.",
        "total_time": "P90D",
        "tool_needed": "NYS-licensed real estate broker, NY attorney, professional photographer",
        "steps": [
            ("Get a CMA (Comparative Market Analysis)", "Pull recent sold comps within 0.25 mi over the last 90 days, adjusted for sqft, lot size, and condition. Free CMA on request.", "PT45M", 0),
            ("Pick listing strategy", "Full-service (4–6% commission) vs flat-fee MLS-only ($500–$3,500 one-time). Math: full-service usually nets 5–10% higher final sale price.", "PT30M", 0),
            ("Pre-listing inspection", "Optional but recommended on $700K+ homes. Costs $500–$1,000. Saves $5K–$15K in negotiated reductions later.", "PT2H", 750),
            ("Professional photography + staging", "Pro photos: $300–$800. Staging: $1,500–$5,000 if vacant. Mandatory above $800K.", "PT3H", 2500),
            ("Write listing copy + price", "List Thursday morning for max weekend showing volume. Price within 2% of recent sold comps for first-14-day momentum.", "PT2H", 0),
            ("MLS + syndication exposure", "OneKey® MLS placement → auto-syndicates to Zillow, Realtor.com, Homes.com. Add StreetEasy for NYC listings.", "PT1H", 0),
            ("Showings + open house", "First-weekend open house drives 60% of total foot traffic. Pre-screen attendees by mortgage pre-approval.", "P14D", 0),
            ("Offer review + acceptance", "NY uses contracts of sale (not purchase agreements). Buyer's attorney negotiates riders before signature.", "PT1W", 0),
            ("Attorney coordination + closing", "60–90 days from contract to close. Attorney handles title cure, payoffs, escrows. Wire instructions disclosed in writing only.", "P75D", 2500),
        ],
        "faqs": [
            ("How long does it take to sell a house in NYC?",
             "Typically 60–90 days from listing date to closing. Pricing within 2% of comps + 14-day market exposure + 30–45 days under contract + 14 days closing prep. Outliers above and below."),
            ("What are typical NYC seller closing costs?",
             "8–10% of sale price including: real estate commission (negotiable), NY State transfer tax (0.4%), NYC RPTT (1–1.425%), seller attorney ($1,500–$3,500), title cure costs, and any co-op flip tax."),
            ("Do I need an attorney to sell a home in NY?",
             "Yes. NY is an attorney-driven state — every residential transaction requires the seller to have an attorney to negotiate the contract rider, manage closing, and handle the deed transfer."),
            ("Can I sell my NYC home FSBO without a broker?",
             "Legal but typically nets 12–18% LESS than agent-listed sales after pricing errors, missing buyer-broker exposure, and weaker negotiation. Flat-fee MLS ($500–$3,500) is a middle option."),
        ],
    },
    {
        "slug": "how-to-rent-out-an-apartment-in-ny",
        "h1": "How to Rent Out an Apartment in NY — 8-Step Landlord Guide",
        "title": "How to Rent Out an Apartment in NY in 2026 — Landlord Process | Nitin Gadura",
        "intent": "First-time and small landlords learning the NY rental process",
        "intro": "Renting out an apartment in NY in 2026 has changed dramatically since the 2019 Housing Stability and Tenant Protection Act and the 2024 NYC broker-fee rules. Here's the legal-compliant 8-step process.",
        "total_time": "P30D",
        "tool_needed": "NY-licensed broker (recommended), tenant screening service, lease forms",
        "steps": [
            ("Verify rent stabilization status", "Check at NYC Rent Guidelines Board or HCR registry. Pre-1974 buildings with 6+ units are typically stabilized. Stabilized units have annual increase caps.", "PT1H", 0),
            ("Set rent based on comps", "Pull comparable rentals in same ZIP, building tier, and bedroom count. Pricing 5–10% above market adds 30+ days vacancy.", "PT45M", 0),
            ("Photography + listing prep", "Professional photos (or high-quality phone shots in good light). Renters scan listings 3x faster than buyers — visuals matter most.", "PT2H", 200),
            ("List on MLS + StreetEasy + Zillow", "Cross-post for max exposure. NYC: StreetEasy is dominant. LI: Zillow + Realtor.com.", "PT1H", 0),
            ("Tenant screening (NY-compliant)", "Credit (650+ typical), employment + income verification (40x rent), 2 prior-landlord refs, ID. Application fee capped at $20 per applicant.", "PT3D", 50),
            ("Apply equally — source-of-income protection", "Section 8, CityFHEPS, SSDI, child support must be considered equally. Refusing voucher tenants is illegal in NY State + NYC.", "ongoing", 0),
            ("Lease execution", "1 or 2 year lease standard. Must include landlord disclosure (LL §235-f), security deposit terms, rent stabilization status if applicable.", "PT1H", 0),
            ("Move-in + collect deposits", "First month + security (capped at 1 month's rent). Document apartment condition with dated photos for security-deposit return later.", "PT1H", 0),
        ],
        "faqs": [
            ("Can I refuse a Section 8 voucher tenant in NY?",
             "No. Source-of-income discrimination is illegal in NY State + NYC. Section 8, CityFHEPS, SSDI, and child support must be considered equally with cash-paying applicants. Violations: up to $250K per case."),
            ("How much can I charge for a security deposit in NY?",
             "Capped at 1 month's rent (NY State Tenant Protection Act 2019). Must be returned within 14 days of move-out with itemized written deduction list."),
            ("How long does it take to rent an apartment in NY?",
             "Well-priced apartments typically lease within 14–21 days. Time to keys-in-hand: 30–45 days from listing through credit check, lease execution, and move-in."),
            ("Who pays the broker fee in NYC?",
             "As of 2024 NYC law, the party who hired the broker pays. Landlord-side brokers cannot bill tenants for the rental commission. Tenant-side brokers (renter-hired) can charge tenants."),
        ],
    },
    {
        "slug": "how-to-screen-a-tenant-in-ny",
        "h1": "How to Screen a Tenant in NY — Legal-Compliant 6-Step Process",
        "title": "How to Screen a Tenant in NY (2026 Compliance) | Nitin Gadura",
        "intent": "Landlords avoiding NY tenant-screening violations",
        "intro": "NY tenant screening has the strictest legal requirements in the country. Source-of-income protection, $20 application fee cap, written-denial-reason rule, and the 2024 NYC broker-fee disclosure all create traps for unwary landlords. Here's the 6-step compliant process.",
        "total_time": "P5D",
        "tool_needed": "Background check service (TransUnion SmartMove, RentSpree, etc.)",
        "steps": [
            ("Set written screening criteria BEFORE listing", "Required: minimum credit, income multiple, prior eviction status, criminal background limits. Apply identically to every applicant.", "PT2H", 0),
            ("Cap application fee at $20", "NY State law caps fees at $20 per applicant. No 'processing,' 'admin,' or 'background-check' fees beyond this. Fees above $20 = lawsuit-bait.", "PT0M", 0),
            ("Pull credit + verify income", "650+ typical for market-rate. Income: 40x monthly rent (single tenant) or 36x combined (multiple tenants). Verify last 30 days of income.", "PT24H", 35),
            ("Verify employment + landlord references", "Call current employer (verify position + tenure). Call 2 prior landlords (verify on-time payments + condition of unit at move-out).", "PT2H", 0),
            ("Apply criteria equally — no protected-class discrimination", "Federal + NY State + NYC anti-discrimination: race, color, national origin, religion, sex, familial status, disability, source of income, sexual orientation, gender identity, age, marital status, military status. Same criteria for everyone.", "ongoing", 0),
            ("Provide written denial reason within 30 days if rejecting", "NY law requires written reason. 'Insufficient income' is acceptable; 'too many kids in the household' is illegal (familial status protection).", "PT30M", 0),
        ],
        "faqs": [
            ("What's the $20 application fee cap in NY?",
             "NY State law caps tenant application fees at $20 per applicant. This includes credit-check costs. Landlords must absorb screening costs above $20. Fees above the cap can trigger fines up to $1,000 per violation."),
            ("Can I refuse a tenant with bad credit?",
             "Yes — IF you apply the same credit standard to every applicant AND provide written denial reason. You cannot use 'bad credit' selectively against protected classes."),
            ("Do I have to accept Section 8 vouchers in NY?",
             "Yes. Source-of-income protection is statewide. Section 8, CityFHEPS, SSDI, child support, alimony, veteran benefits all protected. Refusing a voucher tenant if other criteria are met is illegal."),
            ("How fast can I run NY tenant screening?",
             "Standard: 1–3 business days (credit pull + employment verification). Rush: same-day with services like SmartMove ($40 fee)."),
        ],
    },
    {
        "slug": "how-to-negotiate-a-real-estate-deal-in-ny",
        "h1": "How to Negotiate a NYC Real Estate Deal — 7 Levers",
        "title": "How to Negotiate a NYC Real Estate Deal in 2026 | Nitin Gadura",
        "intent": "Buyers and sellers preparing to negotiate",
        "intro": "Negotiating NYC real estate is different from most US markets. Multiple-offer dynamics, attorney-managed contracts, NY-specific contingencies, and 60–90 day closing windows give experienced negotiators 7 specific levers. Here's how to use them.",
        "total_time": "PT4H",
        "tool_needed": "NYS-licensed broker, NY real estate attorney, mortgage pre-approval",
        "steps": [
            ("Lock pre-approval BEFORE making offer", "Strong pre-approval letter (lender + amount + credit-pull date) signals seriousness. Verbal pre-qualifications are worthless in multi-offer.", "PT2D", 0),
            ("Read the listing agent's pricing strategy", "Has it been on market 30+ days? Price reduction yet? Comparable closings? These signal seller flexibility.", "PT1H", 0),
            ("Use contingencies as negotiation chips", "Mortgage contingency, inspection contingency, attorney-review contingency. Stronger offers waive some — but only when you can afford the risk.", "PT1H", 0),
            ("Earnest money level", "NY standard: 10% earnest money (much higher than national 1–3%). Higher earnest = stronger offer signal. Held in attorney's escrow.", "PT30M", 0),
            ("Closing timeline flexibility", "Sellers value certainty. Offering 45-day quick-close (when feasible) often beats higher price with 90-day timeline.", "PT30M", 0),
            ("Inspection findings — repair credits, not redo demands", "Most NY homes are 50–100+ years old. Asking for cosmetic redos kills deals. Asking for repair credits in cash at closing keeps deals alive.", "PT2H", 0),
            ("Final negotiation: walk-away price set in writing", "Decide your absolute max BEFORE the back-and-forth. Walk away if exceeded. Don't let emotional momentum push you 5–10% over.", "PT30M", 0),
        ],
        "faqs": [
            ("Are real estate commissions negotiable in NY?",
             "Yes. NY law explicitly states commissions are negotiable (19 NYCRR §175.7). After the 2024 NAR settlement, buyer-broker compensation is negotiated upfront in a written buyer-broker agreement."),
            ("How much earnest money is standard in NYC?",
             "10% of purchase price is the NYC norm — much higher than the national 1–3% standard. Held in seller-attorney escrow. Demonstrates buyer commitment."),
            ("Can I waive the inspection contingency in NYC?",
             "Legal but risky on 50+ year old NYC housing stock. Most homes have findings. Waiving contingency = you accept all unknown defects. Inspect anyway, even if not contingent."),
            ("What happens if my mortgage falls through after contract?",
             "If you have a mortgage contingency clause AND meet its conditions (denial letter from lender within timeframe), you get earnest money back. Without contingency: forfeit earnest money."),
        ],
    },
]


def render(g: dict) -> str:
    slug = g["slug"]
    canonical = f"https://nitingadura.com/{slug}.html"
    meta_desc = g["intro"][:155]

    steps_html = ""
    for i, (name, text, dur, cost) in enumerate(g["steps"], 1):
        cost_str = f" · ~${cost}" if cost else ""
        steps_html += f"""<div class="step">
<div class="step-num">{i}</div>
<div class="step-body">
<h3>{name}</h3>
<p>{text}</p>
<p class="step-meta">Estimated time: {dur} {cost_str}</p>
</div>
</div>"""

    faq_html = "\n".join(
        f'<div class="faq-item"><div class="q">{q}</div><p>{a}</p></div>' for q, a in g["faqs"]
    )

    howto_steps = []
    for i, (name, text, dur, cost) in enumerate(g["steps"], 1):
        howto_steps.append({
            "@type": "HowToStep",
            "position": i,
            "name": name,
            "text": text,
            "totalTime": dur,
        })
    howto_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": g["h1"],
        "description": g["intro"],
        "totalTime": g["total_time"],
        "tool": [{"@type": "HowToTool", "name": g["tool_needed"]}],
        "step": howto_steps,
        "author": {"@type": "Person", "name": "Nitin Gadura", "url": "https://nitingadura.com/about.html",
                   "sameAs": ["https://www.wikidata.org/wiki/Q139583263"]},
        "publisher": {"@type": "RealEstateAgent", "name": "Gadura Real Estate, LLC",
                      "sameAs": ["https://www.wikidata.org/wiki/Q139583275"]},
        "datePublished": TODAY,
        "dateModified": TODAY,
    }, indent=2, ensure_ascii=False)

    faq_jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in g["faqs"]
        ],
    }, indent=2, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{g['title']}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{g['h1']}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="article">
<meta property="og:image" content="https://nitingadura.com/nitin-gadura.jpg">
<meta property="og:site_name" content="Nitin Gadura — Real Estate">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{g['h1']}">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://nitingadura.com/nitin-gadura.jpg">
<meta name="robots" content="index,follow,max-snippet:-1">
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
  .answer-first{{background:#fff8e1;border-left:4px solid var(--green);padding:22px;margin:28px 0;border-radius:6px;font-size:16.5px}}
  article h2{{font-family:Montserrat;color:var(--navy);font-size:22px;margin:32px 0 14px}}
  .step{{display:grid;grid-template-columns:48px 1fr;gap:18px;background:var(--light);padding:22px;border-radius:8px;margin-bottom:14px}}
  .step-num{{width:42px;height:42px;border-radius:50%;background:var(--green);color:#fff;display:flex;align-items:center;justify-content:center;font-family:Montserrat;font-weight:700;font-size:18px}}
  .step-body h3{{font-family:Montserrat;color:var(--navy);font-size:17px;margin-bottom:6px}}
  .step-meta{{font-size:13px;color:#666;margin-top:8px;font-style:italic}}
  .faq-item{{background:var(--light);padding:18px 22px;border-radius:8px;margin-bottom:10px}}
  .faq-item .q{{font-weight:700;color:var(--navy);margin-bottom:8px;font-size:16px}}
  .cta{{background:linear-gradient(135deg,#fff,var(--light));border:2px solid var(--green);padding:24px;border-radius:10px;margin:32px 0;text-align:center}}
  .btn{{display:inline-block;background:var(--green);color:#fff;padding:12px 24px;border-radius:6px;font-weight:600}}
  footer{{background:var(--dark);color:rgba(255,255,255,.85);padding:32px 0;text-align:center;font-size:13px;margin-top:48px}}
</style>

<script type="application/ld+json">
{howto_jsonld}
</script>
<script type="application/ld+json">
{faq_jsonld}
</script>
<script type="application/ld+json">
{{
  "@context":"https://schema.org","@type":"BreadcrumbList",
  "itemListElement":[
    {{"@type":"ListItem","position":1,"name":"Home","item":"https://nitingadura.com/"}},
    {{"@type":"ListItem","position":2,"name":"How-To Guides","item":"{canonical}"}}
  ]
}}
</script>
</head>
<body>
<header><div class="container header-inner"><a href="/" class="logo">Nitin Gadura</a><nav><a href="/sell/">Sell</a><a href="/rent/">Rent</a><a href="/calculators/">Calculators</a><a href="tel:+19177050132">📞 (917) 705-0132</a></nav></div></header>
<section class="hero">
  <div class="container">
    <h1>{g['h1']}</h1>
    <p style="opacity:.95">For {g['intent']}. By Nitin Gadura, NYS Salesperson #10401383405. Last reviewed {TODAY}.</p>
  </div>
</section>
<div class="container">

<div class="answer-first">{g['intro']}</div>

<article>

<h2>The {len(g['steps'])}-Step Process</h2>
{steps_html}

<h2>Frequently Asked Questions</h2>
{faq_html}

</article>

<div class="cta">
  <h3 style="font-family:Montserrat;color:var(--navy);margin-bottom:10px">Want personalized guidance?</h3>
  <p style="margin-bottom:14px">Free 30-minute consultation. English, Hindi, Punjabi, Bengali, Spanish, Guyanese Creole.</p>
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


def main() -> int:
    for g in GUIDES:
        path = ROOT / f"{g['slug']}.html"
        path.write_text(render(g), encoding="utf-8")
        print(f"  ✓ /{g['slug']}.html")
    print(f"\n{len(GUIDES)} HowTo pages generated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
