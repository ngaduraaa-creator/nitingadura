# Gadura Mortgage — Research-Phase Deliverables

> 🛑 **DO NOT MERGE this repo's `claude/gadura-mortgage-operating-model-3zgdh7` branch to `main` without reading the warning at the top of `../GADURA-MORTGAGE-PROJECT-CELL-BRIEF.md` first.** `main` is nitingadura.com's live publish source. Added 2026-09-24 by a separate reviewing session.

Index of the Project CELL (Adjacent) research-only deliverables for Gadura Mortgage. See `../GADURA-MORTGAGE-PROJECT-CELL-BRIEF.md` for the governing brief (open verification items, AfBA/RESPA questions for Vineet, the 6-month workplan, and the explicit no-publishing scope limit that applies to everything in this directory).

**2026-09-24 correction:** an earlier pass of this research (before Nitin supplied `THE_GADURA_PLAYBOOK.md` and the `GADURA GROWTH MANIFESTO`, both dated 2026-09-24) incorrectly stated no live Gadura Mortgage web presence was found. **That was wrong** — gaduramortgage.com is live (WordPress/WP Engine + Cloudflare). Both supplied documents independently audited it read-only on 2026-09-24; see `regulatory-source-register.md` Item 0 for the resulting top-priority finding (NY DFS website-authorization status, separate from entity licensing) and the corrected facts below. **This session (a Claude Code cloud session with only the `nitingadura` GitHub repo attached) did not perform that live-site audit itself** — the facts below are drawn from the two supplied documents, which report they checked the live site directly; nothing here has been independently re-verified by this session against the live site or NMLS Consumer Access.

| Deliverable | File | Workplan month |
|---|---|---|
| Regulatory Source Register | [regulatory-source-register.md](./regulatory-source-register.md) | 1 / 5 |
| Fair-Lending & Advertising Risk Matrix + Rate-Sourcing Plan | [fair-lending-risk-matrix-and-rate-sourcing.md](./fair-lending-risk-matrix-and-rate-sourcing.md) | 2 / 5 |
| Keyword Master + Intent Clusters | [keyword-master-clusters.md](./keyword-master-clusters.md) | 3 |
| Competitor Matrix | [competitor-matrix.md](./competitor-matrix.md) | 4 |

## Still open (not started, or blocked)
- **NY DFS website-authorization status for gaduramortgage.com — now the top blocker.** Per both supplied documents, the live site's own footer currently states it is not authorized by NYDFS for NY solicitation/application activity. See `regulatory-source-register.md` Item 0. This gates web-facing work at a more basic level than content compliance. Not something this session can resolve — needs Vineet/company compliance to confirm directly with NYDFS.
- **Entity Truth Sheet** for Vineet/Gadura Mortgage — the two supplied documents report self-published figures from the live site (company NMLS #1859097, Vineet's individual MLO NMLS #1501434, address 106-09 101st Avenue 1F, Ozone Park NY 11416 — **the same building as Gadura Real Estate LLC**). **None of these have been independently verified against NMLS Consumer Access by this session or, per both supplied documents, by their sessions either** — NMLS Consumer Access is bot-protected and neither this nor the other sessions bypassed that protection. Treat every number above as "as self-published," not confirmed, until a manual NMLS Consumer Access lookup is done.
- **AfBA resolution with Vineet (and Nitin where it touches the real estate side)** — the questions in §(b) of the brief are unanswered, and now materially sharpened: the shared-building-address fact above is close to the textbook AfBA fact pattern. All cross-referral content stays blocked until resolved in writing.
- **Technical/GEO baseline audit** of gaduramortgage.com — partially done by the two supplied documents (homepage-only spot audit: no rate/APR content found on the homepage, no meta description, minimal structured data, a "Funded Loan Photos" section publishing ~10-11 closed transactions by address/price/loan amount with unverified consent, stale market statistics on the purchase FAQ page, an external "My1003" application portal of unconfirmed authorization). **A full sitewide crawl (every page, not just the homepage) has not been done by anyone yet** and remains open.
- **vineetgadura.com** — confirmed by both supplied documents not to exist (DNS does not resolve). A from-scratch build, gated on the same NY DFS website-authorization question (NY DFS treats private/unapproved domains as unacceptable for mortgage marketing).
- **Mortgage Search Battlefield report** and the **phased 90-day/12-month build plan** — Month 6 synthesis, depends on all of the above being resolved first.

## Standing rules that apply to everything in this directory
- No rate, payment amount, license number, or NMLS ID is published anywhere until independently verified against a primary source (NMLS Consumer Access, NY DFS licensee search) and dated.
- No content here has been reviewed by an attorney. Several entries in the Regulatory Source Register are explicitly flagged "NEEDS LEGAL REVIEW" — those flags are load-bearing.
- Nothing in this directory is live site content, an advertisement, or outreach. It is desk research only.
