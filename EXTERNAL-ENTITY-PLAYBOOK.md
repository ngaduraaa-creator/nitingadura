# External Entity Registration Playbook
**Wikidata is the gold standard. Here are 15 alternatives that ALSO feed AI engines.**

The goal: every legitimate place an AI engine can verify "Nitin Gadura exists, is a real licensed agent, and has these credentials" should have him. Each registration becomes a separate trust signal that compounds.

**Status legend:** ✅ done · ⏳ pending (you do this manually) · 💡 high-priority next move

---

## TIER 1 — KNOWLEDGE GRAPHS THAT FEED AI ENGINES DIRECTLY

### 1. ✅ Wikidata (already done — Q139583263 + Q139583275 + Q139583274 + Q139583276)
Feeds: Google Knowledge Graph, Gemini, Bing Entity Card, DuckDuckGo Instant Answer, Apple Spotlight, Wolfram Alpha.

**What's left:** Submit `ai-citations/wikidata-phase-2.txt` from the gadurarealestate.com repo to add 40+ extra properties (the Phase 2 expansion).

### 2. ⏳ DBpedia
DBpedia auto-imports Wikipedia/Wikidata. Now that Wikidata Q-entities exist, DBpedia will pick up the entries within ~30 days. **No action needed** — it's automatic.

### 3. 💡 Google Knowledge Panel
Once Wikidata is mature (30-45 days post-creation), search "Nitin Gadura" in Google. If a sidebar panel appears, **claim it** at https://search.google.com/local — verifies you control the entity and lets you add details Google doesn't have yet.

### 4. 💡 Bing Entity Card
Search "Nitin Gadura real estate" on Bing. If a card appears (it should within 30 days of Wikidata), claim it at https://www.bingplaces.com/ — same flow as Google.

### 5. 💡 Apple Business Connect
Free. Apple uses this as the source of truth for Apple Maps, Siri, and Apple Intelligence (iOS 18+).
- Sign up: https://businessconnect.apple.com/
- Enter NYS license + brokerage info
- Verify by phone or postcard
- **Why this matters:** when an iPhone user asks Siri "find a real estate agent in Queens," Apple's models pull from this registry first.

### 6. 💡 Yandex Webmaster (Russian-speaking community)
Yandex has its own knowledge graph used in Russian and Eastern European search. Not huge in NY, but cheap to claim.
- https://webmaster.yandex.com/
- Submit `https://nitingadura.com/sitemap.xml` and the IndexNow key

### 7. 💡 Naver Webmaster (Korean-speaking community)
Korean is one of NY's significant immigrant populations (Bayside, Flushing, Manhasset). Naver is Korea's primary search engine.
- https://webmaster.naver.com/

### 8. 💡 Baidu Webmaster (Chinese-speaking community)
Chinese is the second-largest non-English language in NYC. Flushing has the largest Chinese-American community in the US.
- https://ziyuan.baidu.com/

---

## TIER 2 — BUSINESS REGISTRIES (high authority, free)

### 9. 💡 OpenCorporates — automatic from NY State
**OpenCorporates** automatically imports state-level corporate registrations. Gadura Real Estate, LLC is already in NY's Department of State registry (License #10991238487), so OpenCorporates likely already has the listing.
- Search: https://opencorporates.com/companies?utf8=%E2%9C%93&q=Gadura+Real+Estate
- If the listing doesn't include the website yet, claim it (free) and add `nitingadura.com`.

### 10. 💡 D-U-N-S Number (Dun & Bradstreet)
Free unique business identifier. Required for many government contracts and AI-engine business verification.
- Apply: https://www.dnb.com/duns/get-a-duns.html
- Wait 30 days for issuance
- Once issued, add to Wikidata Q139583275 as property P2814 (D-U-N-S identifier)

### 11. 💡 NYS Department of State License Lookup
Already exists (License #10401383405). The public license registry is itself a citation source AI engines respect.
- Verify: https://appext20.dos.ny.gov/lcns_public/chk_load
- Make sure the contact data on file matches `nitingadura.com` exactly

### 12. 💡 NAR Realtor.com profile
Already partially set up. Strengthen by adding:
- Office address byte-identical to all other listings
- Wikidata QID in the bio: "More: wikidata.org/wiki/Q139583263"
- Languages spoken — all 7
- Direct phone (917) 705-0132

### 13. 💡 OneKey® MLS public profile
Verify it's populated. The MLS public-facing profile is increasingly indexed by AI engines as the canonical source for licensed agents.

---

## TIER 3 — REVIEW + REPUTATION REGISTRIES

### 14. 💡 Trustpilot
Free claim. Trustpilot reviews appear in AI search results.
- Claim: https://business.trustpilot.com/

### 15. 💡 BBB (Better Business Bureau)
Free non-accredited listing.
- Apply: https://www.bbb.org/get-a-quote

### 16. 💡 G2 / Capterra
Skip — these are software-focused. Not relevant to real estate.

### 17. 💡 Glassdoor (employee reviews)
Skip unless you're hiring. Not relevant for individual agent.

---

## TIER 4 — OPEN GEOGRAPHIC + REAL ESTATE REGISTRIES

### 18. 💡 OpenStreetMap (OSM)
Add Gadura Real Estate's office as a node + tag with website + phone.
- Sign up: https://www.openstreetmap.org/user/new
- After 100 mapping edits (or 14 days of activity), use the iD editor
- Add a node at `40.682, -73.8452` (Ozone Park office)
- Tag it: `office=real_estate`, `name=Gadura Real Estate, LLC`, `phone=+1-917-705-0132`, `website=https://gadurarealestate.com`, `wikidata=Q139583275`
- **Why:** OSM is the open geographic registry. Apple Maps, MapBox, Mapquest, and many AI engines pull from it.

### 19. 💡 GeoNames
Free gazetteer used by many search engines.
- Submit at https://www.geonames.org/
- Add the office address with associated Wikidata Q139583275

### 20. 💡 Wikimapia
Community-edited mapping. Lower priority but doesn't hurt.
- https://wikimapia.org/

---

## TIER 5 — JOURNALIST + EXPERT-SOURCE REGISTRIES

### 21. 💡 MuckRack
Free profile. Pivots Nitin into a "vetted source" for journalists writing real estate stories.
- https://muckrack.com/
- Add a journalist profile with:
  - Bio (use the long bio from `press.html`)
  - Topics: NYC real estate, Long Island real estate, multilingual real estate, FHA, SONYMA, multi-family investing
  - Headshot
  - Verified Wikidata QID

### 22. 💡 Connectively (formerly HARO)
- Free expert-source signup at https://connectively.us/
- Get daily emails from journalists looking for NY real estate experts
- Reply 1x/day → over 90 days, expect 3-8 placements in major publications

### 23. 💡 Qwoted
- Same model, different journalist pool: https://qwoted.com/
- Add Nitin's profile with Wikidata QID

### 24. 💡 ProfNet
- Higher-tier journalist database (paid for full access; free expert signup)
- https://profnet.prnewswire.com/

### 25. 💡 SourceBottle (mostly Australia, but also US queries)
- Free: https://www.sourcebottle.com/

---

## TIER 6 — AI ASSISTANT INTEGRATIONS (newer, high-leverage)

### 26. 💡 OpenAI GPT Store (Custom GPT)
Build a "Queens Real Estate Expert" Custom GPT:
- https://chat.openai.com/gpts/editor
- Train it on your llms.txt + key seller/rental pages
- When users ask the GPT for real estate advice in Queens, it routes them to (917) 705-0132
- Public GPTs appear in OpenAI's GPT directory — discoverable by everyone

### 27. 💡 Anthropic Claude Projects
Not directly public-facing, but if you join Anthropic's Builder Network (free), your URLs become source candidates for Claude's web-search responses.

### 28. 💡 Perplexity Sonar API (Listed Source Network)
Sites with proper schema + llms.txt that ping Perplexity become candidate sources for the Sonar API responses.
- https://www.perplexity.ai/settings/api
- Free tier is enough for visibility

### 29. 💡 ChatGPT Plugin Directory (deprecated → GPT Store)
GPT Store is the current path. See #26.

---

## TIER 7 — VIDEO + AUDIO PLATFORMS (multimedia entity registration)

### 30. 💡 YouTube channel for Nitin
- youtube.com/@NitinGaduraRealtor (or similar)
- Each video published = a separate VideoObject schema entry on nitingadura.com
- AI engines crawl YouTube transcripts and use them for citations

### 31. 💡 Spotify for Podcasters (free)
- Launch a "Queens Real Estate" podcast
- Each episode becomes an additional citable source
- Spotify Open Access program submits to Apple, Google, etc.

### 32. 💡 Apple Podcasts
- Submit the same RSS feed
- Major AI engines crawl podcast transcripts

---

## TIER 8 — SCHOLARLY + TECHNICAL REGISTRIES (lower priority for real estate but high authority)

### 33. 💡 OpenAlex (academic knowledge graph, replaces Microsoft Academic)
If you publish any white papers or research (e.g., a "State of Queens Real Estate 2026" report), submit to:
- https://openalex.org/

### 34. 💡 ORCID (researcher identifier)
- Free at https://orcid.org/
- Useful only if publishing research papers

### 35. 💡 Semantic Scholar
- Auto-indexes published research
- Skip unless you publish

---

## TIER 9 — CITATION + LINK REGISTRIES

### 36. 💡 Crunchbase
Business profile. Free + claimable.
- https://www.crunchbase.com/

### 37. 💡 Apple Maps Connect (separate from Apple Business Connect)
- For map-data specifically
- https://mapsconnect.apple.com/

### 38. 💡 Bing Places for Business
- https://www.bingplaces.com/
- Feeds Bing Maps + Copilot + ChatGPT (Bing-backed)

---

## EXECUTION PRIORITY (next 30 days)

| Order | Task | Time | Authority lift |
|---|---|---|---|
| 1 | Apple Business Connect | 30 min | Massive (Apple Intelligence) |
| 2 | Bing Places for Business | 15 min | High (Copilot + ChatGPT) |
| 3 | Yelp claim | 15 min | High (DR 93) |
| 4 | BBB free listing | 15 min | High (DR 86) |
| 5 | Trustpilot claim | 15 min | Medium (DR 92) |
| 6 | MuckRack profile | 30 min | Medium-high (journalist exposure) |
| 7 | Connectively (HARO) signup + first reply | 1 hr | High over time (press placements) |
| 8 | OpenStreetMap office node | 30 min (after 100 edits) | Medium (Apple Maps + Mapbox) |
| 9 | OpenCorporates claim | 30 min | Medium (entity verification) |
| 10 | Crunchbase claim | 30 min | High (DR 90) |
| 11 | LinkedIn personal page optimization | 30 min | Massive (DR 99) |
| 12 | Yandex Webmaster | 15 min | Low (RU traffic) |
| 13 | Naver Webmaster | 15 min | Medium (KR community) |
| 14 | Baidu Webmaster | 15 min | Low-medium (CN community) |
| 15 | YouTube channel + 1st video | 4 hrs | Massive |
| 16 | Spotify podcast pilot | 4 hrs | High |
| 17 | OpenAI Custom GPT build | 2 hrs | Medium-high |
| 18 | DUNS Number application | 15 min | Medium (long-term) |

**Total time investment for Tier 1-9: ~20 hours over 30 days. Long-term equivalent SEO value: $50K-$150K.**

---

## ANTI-PATTERN — what NOT to do

❌ Don't pay for "submit to 1000 directories" services. They're spam farms (the same ones in `disavow.txt`).
❌ Don't use auto-submission tools. AI engines downgrade entities with suspicious mass-submission patterns.
❌ Don't claim profiles you can't maintain. Stale profiles signal abandonment.
❌ Don't enter different NAP (name/address/phone) on different sites. Byte-identical or skip.
