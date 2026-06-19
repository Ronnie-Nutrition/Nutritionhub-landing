# PRD — Free Local SEO Program for Nutrition Businesses

**Owner:** Ronnie Craig · **Created:** 2026-06-19 · **Status:** Nutrition Hub Phase 1–2 live; reusable for Broadway Nutrition
**Companion skill:** `/local-seo-buildout` (`~/.claude/skills/local-seo-buildout/`) — the executable playbook. This PRD is the *why/what*; the skill is the *how*.

---

## 1. Problem & goal
Local nutrition clubs live or die on local search ("energy teas near me", "protein shake Pearland"). Paid SEO tools (SEMrush ~$100/mo, Harbor €29/mo) were declined. **Goal: rank organically using only Claude Code + Google Search Console — $0/mo.** Drive walk-ins and online orders from people searching local + high-intent product terms.

## 2. Strategy in one line
**Content fills the funnel → schema-rich local landing pages rank → internal links from indexed pages pass authority → Search Console accelerates crawl.** The website becomes the lead engine; DMs/ads close.

## 3. The 5 components (every location needs all 5)
| # | Component | What it delivers | Status @ Nutrition Hub |
|---|---|---|---|
| 1 | **Technical foundation** | JSON-LD LocalBusiness schema (+geo, hours), canonical, OG/Twitter, robots.txt, sitemap.xml, Search Console verified | ✅ Live |
| 2 | **Local landing cluster** | One schema-rich page per high-intent keyword, distinct intent + accent, FAQ rich-result schema, fully interlinked | ✅ 4 pages live |
| 3 | **Online menu audit** | Online order menu matches the real in-store menu (you can only sell what's listed) | ✅ Done (added creatine) |
| 4 | **Google Business Profile NAP** | Name/Address/Phone match site char-for-char — the #1 local ranking factor | ⏳ To verify |
| 5 | **Topical content cluster** | Blog posts answering long-tail questions, linking up to money pages → topical authority | ⏳ Not started |

## 4. Nutrition Hub — what shipped (reference implementation)
Live cluster on **nutritionhub101.com**, all interlinked with the homepage, all carrying Meta Pixel `915336731481586` additively:

| Page | Target intent | Accent | Real pricing used |
|---|---|---|---|
| `/energy-teas-pearland/` | energy / lit teas | cyan | $9.15 lit tea |
| `/meal-replacement-shakes-pearland/` | weight loss / meal swap | lime | $9.97 gourmet / $7.80 small |
| `/b12-shots-pearland/` | B12 energy shot (drink, not injection) | orange | $3 |
| `/protein-shakes-pearland/` | post-workout / recovery | pink | $9.97 / $7.80 + BCAAs $3 / creatine $2 |

Key product decisions baked into copy:
- **B12 "shot" = a $3 B-vitamin energy drink (Liftoff), NOT an injection.** Copy describes it positively as an energy drink — no needle/clinic framing (even denials plant the wrong frame). Keep non-medical.
- **Shakes split into two intents** (weight-loss vs post-workout) so the two pages don't cannibalize the same searches.
- Order site gained **Creatine Boost $2** during the audit (was sold in-store, missing online).

## 5. 🚨 Hard constraints (carry to every build)
1. **Meta Pixel/CAPI sacred** — SEO edits are additive `<head>` only; verify `init` count unchanged after every deploy. A live ad + server-side CAPI depend on it.
2. **Real data only** — pull prices/products from the menu source of truth; never invent. Ask if unknown.
3. **Preview → owner approval → deploy.** Owners catch positioning/claim issues.
4. **No medical/cure claims** for wellness products; benefit language only.
5. **Back up live files before every deploy;** patch live apps in place (Python script via scp, never heredoc); never overwrite a newer live app wholesale.

## 6. Success metrics (track in Search Console / GBP Insights)
- Pages indexed (target: 100% of cluster within 2 weeks of indexing request)
- Impressions + clicks per landing page (Search Console Performance)
- FAQ rich-result appearances
- GBP "Directions" + "Website" + "Call" actions
- New customers citing "found you on Google"

---

## 7. 🆕 Broadway Nutrition — application plan (next build)
Second location (Ysela's). Website ~30% complete. **Reuse this entire system via `/local-seo-buildout`.**

**Site profile to capture first (TBD — fill in next session):**
| Field | Value |
|---|---|
| Business name (exact, match GBP) | Broadway Nutrition (confirm) |
| Domain | _TBD_ |
| Address / NAP | _TBD_ (Ysela's location) |
| Geo lat/lng | _TBD_ |
| Hours | _TBD_ |
| Schema type | FoodEstablishment |
| Order/menu URL + price source | _TBD_ (own GHL? separate order site?) |
| Meta Pixel ID | _TBD_ (own pixel — do NOT reuse Nutrition Hub's) |
| Deploy target | _TBD_ (VPS web root? GitHub Pages?) |

**Build order for Broadway Nutrition:**
1. Capture the site profile above.
2. Finish the homepage to 100%, then Phase 1 technical foundation.
3. Build the landing cluster — same 4 intents adapted to Broadway's menu/market (+ any location-specific keywords).
4. Audit Broadway's online menu vs. in-store.
5. Verify Broadway's GBP NAP.
6. Start the content cluster.

> ⚠️ Broadway gets its **own** pixel, domain, GBP, and price data. Do not copy Nutrition Hub's IDs/prices — only the *method* and the page templates transfer.

---

## 8. Open items / next session (Nutrition Hub)
1. **Online menu audit** — full in-store vs. online comparison (creatine already fixed; check for other gaps).
2. **GBP NAP verification** — confirm exact match to site + schema.
3. **Content cluster** — first blog posts per landing page.
4. Consider merging PR #1 (`seo/phase1-local-optimization`) to keep `main` in sync (production already live).
