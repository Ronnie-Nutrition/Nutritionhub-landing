# Context Handoff — Nutrition Hub SEO Cluster + Reusable System (June 19, 2026, session 2)

## TL;DR
Completed the **4-page local landing cluster** for nutritionhub101.com, added a missing product to the order site, and **packaged the entire process as a reusable skill + PRD** for the upcoming **Broadway Nutrition** build. Everything live-verified, Meta Pixel untouched, committed to PR #1.

---

## What shipped this session
### Landing cluster — now COMPLETE (4 pages, all live + interlinked)
| Page | Intent | Accent | Pricing |
|---|---|---|---|
| `/energy-teas-pearland/` | energy/lit teas | cyan | $9.15 (prior session) |
| `/meal-replacement-shakes-pearland/` | weight loss | lime | $9.97 / $7.80 |
| `/b12-shots-pearland/` | B12 energy **drink** (not injection) | orange | $3 |
| `/protein-shakes-pearland/` | post-workout recovery | pink | $9.97 / $7.80 + BCAAs $3 / creatine $2 |

- Each homepage "Why" card now links to its page; pages cross-link to siblings.
- All carry Meta Pixel `915336731481586` additively; homepage pixel count verified `1` after every deploy.
- **B12 copy rule (Ronnie):** it's a $3 Liftoff energy DRINK — keep it non-medical, NO "no needles/clinic/injection" framing (even denials plant the medical frame). Describe positively.

### Order site change
- Added **Creatine Boost $2.00** (`boost-creatine`) to live `/opt/nutritionhub-menu/menu-data.js` (backed up, Python-patched in place, verified serving — 10 boosters now). It was sold in-store but missing online.

### Reusable system created (the big deliverable)
- **Skill:** `~/.claude/skills/local-seo-buildout/SKILL.md` (+ `assets/landing-page-template.html`). Invocable as `/local-seo-buildout`. Full playbook: site profile → technical foundation → landing cluster → menu audit → GBP NAP → content cluster, with all safety rules + deploy mechanics + per-deploy verification.
- **PRD:** `LOCAL-SEO-PRD.md` in this repo. Strategy, the 5 components, the Nutrition Hub reference implementation, hard constraints, and a **Broadway Nutrition application plan** with a site-profile table to fill in.

---

## 🚨 Critical rules (unchanged — read before touching anything)
1. **Meta Pixel `915336731481586` is sacred** — additive `<head>` metadata ONLY; verify count unchanged after every deploy. Live ad + CAPI depend on it.
2. **Never overwrite the order site wholesale** — patch `<head>`/menu-data.js in place via scp'd Python script (not heredoc). Live copy newer than repo.
3. **Back up live files first** (`.bak-<reason>-<timestamp>`).
4. **Homepage is NOT git-auto-deployed** — deploy = scp to VPS web root. No restart (static + Node reads disk per request).
5. **zsh does NOT word-split unquoted vars** — write ssh/scp flags inline, never store them in a `$VAR`.

## Infra / deploy cheat-sheet
- **VPS:** `ssh -o IdentitiesOnly=yes -i ~/.ssh/id_ed25519 root@64.23.156.59`
- **Homepage root:** `/var/www/nutritionhub-home/` (`index.html`; repo file `nutritionhub-neon-home.html`)
- **New pages:** `/var/www/nutritionhub-home/<slug>/index.html` → `/<slug>/`
- **Order site:** `/opt/nutritionhub-menu/` (Node app; `menu-data.js` served to client)
- **Repo:** `~/GTM-Workspace/nutritionhub-landing` → GitHub `Ronnie-Nutrition/Nutritionhub-landing`
- **PR #1:** branch `seo/phase1-local-optimization` — holds all homepage/sitemap/landing commits. Latest: `8bc9e22`.
- Geo for schema: lat `29.559174`, lng `-95.345263`

---

## 👉 Ronnie's manual actions (cannot be done from code)
**Request Indexing in Google Search Console** for the 3 new URLs (URL Inspection → paste → Request Indexing):
- `https://nutritionhub101.com/meal-replacement-shakes-pearland/`
- `https://nutritionhub101.com/b12-shots-pearland/`
- `https://nutritionhub101.com/protein-shakes-pearland/`

---

## Next session — pick up here (Ronnie wants ALL of these)
1. **Online menu audit** — full in-store vs. online `menu-data.js` comparison; add any other missing items (creatine already done).
2. **GBP NAP verification** — confirm Google Business Profile Name/Address/Phone match the site + schema char-for-char (#1 local ranking factor).
3. **Topical content cluster** — first blog posts per landing page (long-tail Q&A → link up to money pages). Write in-repo, add Article schema.
4. **Broadway Nutrition build** — Ysela's 2nd location, site ~30% done. Run `/local-seo-buildout`, capture the site profile first (own domain/pixel/GBP/prices — do NOT reuse Nutrition Hub's). See PRD §7.
5. Optional: merge PR #1 to sync `main` (production already live).

Memory updated: `project_nutrition_hub_seo.md`.
