# Gadura Mortgage — Fair-Lending & Advertising Risk Matrix + Rate-Data Sourcing Plan

**Status:** Research-phase deliverable (Month 2 / Month 5 of the Project CELL brief workplan). Informational synthesis of public enforcement and data-source research — not legal advice, and not a substitute for the legal review the brief requires before anything publishes. All URLs below were retrieved by a research pass in September 2026; re-verify before relying on them later, since enforcement postures and vendor offerings change.

---

## Part 1 — Redlining / Marketing-Footprint Risk: What Regulators Actually Use as Evidence

This is the single highest-priority compliance item flagged in the Project CELL brief. Four real, sourced examples of the evidentiary pattern regulators use, including one small-shop precedent so this isn't dismissed as "only applies to big lenders":

### Fairway Independent Mortgage Corp. — CFPB & DOJ, October 2024
Fairway operated all of its Birmingham, AL retail offices and loan-production desks in majority-white neighborhoods, and concentrated marketing/agent-referral relationships in the same areas. Only 3.7% of its 2018–2022 mortgage applications came from majority-Black tracts vs. 12.2% for peer lenders in the same market. Outcome: $1.9M civil penalty plus injunctive relief on office siting and marketing.
Source: [CFPB/DOJ action against Fairway](https://www.consumerfinance.gov/archive/newsroom/cfpb-and-justice-department-take-action-against-fairway-for-redlining-black-neighborhoods-in-birmingham-alabama/)

### Trident Mortgage Company (Berkshire Hathaway subsidiary) — DOJ & CFPB, July 2022
Alleged discriminatory marketing (imagery of "white-appearing models," an overwhelmingly white loan-officer roster relative to the Philadelphia metro) and office/loan-officer avoidance of majority-minority neighborhoods — >25% of area neighborhoods were majority-minority but only ~12% of applications came from them. Outcome: $24M+ total, including an $18.4M loan-subsidy fund and $2M earmarked specifically for minority-community outreach/advertising.
Source: [DOJ press release](https://www.justice.gov/archives/opa/pr/justice-department-and-consumer-financial-protection-bureau-secure-agreement-trident-mortgage)

### Townstone Financial, Inc. — CFPB, final judgment November 2024
**Directly relevant as a small-shop precedent** — Townstone is a small Chicago-based nonbank mortgage creditor/broker, not a national lender. The case centered on the owner's on-air/podcast statements alleged to discourage prospective Black applicants, combined with geographic application-share disparities — establishing that marketing *content* and targeting, not just office placement, can create liability under ECOA's anti-discouragement provisions. The case had a contested procedural history (dismissed, revived on appeal, a 2025 vacatur motion denied) — worth monitoring, but the underlying theory (marketing content itself is in scope) held.
Source: [CFPB enforcement action page](https://www.consumerfinance.gov/enforcement/actions/townstone-financial-inc-and-barry-sturner/)

### Digital ad targeting as an emerging vector (context)
HUD's 2022 Fair Housing Act settlement with Meta over its housing-ad delivery algorithm is widely cited by fair-lending compliance commentary as the reason DOJ/CFPB are now scrutinizing lenders' own paid social/digital ad targeting (geofencing, lookalike audiences, zip-code exclusions) as a redlining vector — digital targeting can reproduce the same exclusionary pattern as physical office placement.
Source: [Regulators' focus on digital redlining via social media marketing](https://www.activecomply.com/compliance-resources/dojs-settlement-with-meta-highlights-regulators-increased-focus-on-digital-redlining-via-social-media-marketing)

### The common evidentiary pattern across all of these
1. Map/geocode office locations, loan-officer locations, and referral-partner relationships against majority-minority vs. majority-white census tracts.
2. Compare the lender's share of applications/originations from majority-minority tracts against a peer-lender aggregate in the same market (HMDA-based).
3. Examine marketing content itself — imagery, media placement, on-air/podcast statements, digital ad targeting settings — for exclusionary patterns, independent of office location.

**Implication for Gadura Mortgage:** any future geographic or channel targeting decision (which towns/zips to mail, which social audiences to target, where to place a physical presence, which real-estate agents to build referral relationships with) needs to be checked against this pattern *before* it's proposed, not after a campaign is already running.

---

## Part 2 — Practical Self-Check Tools (Free / Accessible to a Small Shop)

A small operation doesn't need enterprise fair-lending software to do a basic footprint check. Real, free tools:

- **FFIEC HMDA Data Browser** (ffiec.cfpb.gov) — pull loan-level or aggregate HMDA data by state/county/MSA/census tract, build custom tables, map lending patterns. This is the same underlying dataset regulators use for peer comparisons.
- **FFIEC Geocoding / Census Report tool** — look up a census tract's income classification and minority-population percentage for a given address.
- **U.S. Census Bureau (ACS + TIGER geographies)** — tract-level racial/ethnic composition data and boundary shapefiles, for overlaying against a marketing footprint.
- **CFPB fair-lending geographic-analysis guidance** — HMDA data alone doesn't prove compliance, but is the standard starting point paired with the Interagency Fair Lending Examination Procedures.

**Practical workflow before any campaign is proposed:**
1. Pull Gadura Mortgage's own application geography (once originations exist) via HMDA LAR data.
2. Pull FFIEC/Census tract-level minority-population percentages for the Queens/Nassau/Suffolk service area.
3. Overlay the proposed marketing footprint (mail zones, digital geofences/zip targeting, office/loan-officer locations, referral-partner locations) against those tract classifications.
4. Compare majority-minority-tract application share against the market/peer aggregate from the HMDA Data Browser; flag material gaps for compliance review before spend is finalized.

This workflow needs actual origination history to be meaningful, so it's realistically a post-launch discipline — but the footprint-definition rule (draw the service area by objective geography — county, MSA, radius — never by demographic composition) applies from day one, including to this research phase's own keyword/cluster geography (Queens/Nassau/Suffolk, chosen as the existing verified real-estate service area, not drawn around any demographic pattern).

---

## Part 3 — Rate-Data Sourcing Plan

**Hard rule (carried from the Project CELL brief, restated here as the operative rule for this document):** no rate is ever hand-typed or estimated into any published content. If no compliant live-rate integration exists at publish time, no rate is published — a stale or approximate rate is not an acceptable fallback.

### Candidate general-market reference: Freddie Mac PMMS
- What it is: Freddie Mac's Primary Mortgage Market Survey, published weekly since 1971, reporting average rates/points for conventional conforming 30-year and 15-year fixed products.
- Cadence: lenders surveyed Monday–Wednesday, results released Thursdays at 10:00 a.m. ET.
- Methodology: as of November 17, 2022, PMMS rates are based on actual mortgage applications submitted through Freddie Mac's Loan Product Advisor system (not lender self-reported survey responses as before), for conforming conventional originations at or under the FHFA limit.
- Official source: [freddiemac.com/pmms](https://www.freddiemac.com/pmms) (current), [PMMS Archive](https://www.freddiemac.com/pmms/pmms_archives) (historical). Public mirror: [FRED MORTGAGE30US](https://fred.stlouisfed.org/series/MORTGAGE30US).
- **Limitation to flag for compliance review:** PMMS is a national conforming-conventional average — not lender-specific, not real-time, and not specific to NY/Queens-Nassau-Suffolk pricing. It is only suitable as a disclosed, clearly-labeled "general market reference" (e.g., "the national average this week was X, per Freddie Mac") — never presented as Gadura Mortgage's own quoted rate, which would need its own trigger-term disclosure treatment regardless of source.

### Landscape of live rate-quote engines (Product/Pricing/Eligibility vendors), named for reference only — no recommendation implied
- **Optimal Blue / Loansifter** — Optimal Blue is the largest PPE overall; Loansifter is its product built specifically for the independent-broker channel.
- **Polly** — newer, automation-focused PPE, generally positioned for mid-size shops.
- **Lender Price** — API-first PPE positioned for smaller shops wanting clean tech integration without enterprise cost/complexity.
- **Mortech** — another established PPE, more associated with the correspondent-lender segment.

### Decision this plan hands to Vineet (not decided here)
Does Gadura Mortgage already have, or plan to obtain, access to a compliant PPE/rate-quote engine? If yes, that becomes the only source ever quoted for a Gadura-specific rate, with the vendor's own compliance/disclosure requirements layered on top of Reg Z trigger-term review. If no, this project's default position holds: publish no rate at all, and treat PMMS as a labeled, disclosed general-market reference only, until a compliant engine exists.

---

## Part 4 — UDAAP Framing Constraints (Advertising Copy Guardrails)

Pending full compliance/legal review, the working default for any future copy:
- No "as low as [rate]" framing without the full trigger-term disclosure block required by that specific rate claim.
- No language implying guaranteed approval or pre-approval without qualifying language (subject to underwriting, credit approval, etc.).
- No urgency/scarcity claims ("rates won't be this low again," "limited time") unless factually and currently true and defensible.
- No geographic or channel targeting decision made without the Part 1/Part 2 footprint check above.

This section is a placeholder scaffold for the full Fair-Lending & Advertising Risk Matrix (a row-by-row matrix mapping each regulation to specific advertising/content decisions) — building the full matrix is a Month 2 task that also depends on the Regulatory Source Register being finalized first, so citations in the matrix are traceable to a primary source rather than restated from memory.
